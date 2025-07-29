import json
import ast
import csv
from pathlib import Path
import importlib.util
import re
from jsonargparse import CLI
import os

from wxo_agentic_evaluation.watsonx_provider import WatsonXProvider
from wxo_agentic_evaluation.arg_configs import BatchAnnotateConfig
from wxo_agentic_evaluation.prompt.template_render import ToolPlannerTemplateRenderer, ToolChainAgentTemplateRenderer
from wxo_agentic_evaluation import __file__

root_dir = os.path.dirname(__file__)
TOOL_PLANNER_PROMPT_PATH = os.path.join(root_dir, "prompt", "tool_planner.jinja2")


def extract_first_json_list(raw: str) -> list:
    matches = re.findall(r"\[\s*{.*?}\s*]", raw, re.DOTALL)
    for match in matches:
        try:
            parsed = json.loads(match)
            if isinstance(parsed, list) and all("tool_name" in step for step in parsed):
                return parsed
        except Exception:
            continue
    print("⚠️ Could not parse tool call plan. Raw output:")
    print(raw)
    return []


def load_tools_module(tools_path: Path) -> dict:
    tools_dict = {}
    files_to_parse = []

    if tools_path.is_file():
        files_to_parse.append(tools_path)
    elif tools_path.is_dir():
        files_to_parse.extend(tools_path.glob("**/*.py"))
    else:
        raise ValueError(f"Tools path {tools_path} is neither a file nor directory")

    for file_path in files_to_parse:
        try:
            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Add all module's non-private functions to tools_dict
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and not attr_name.startswith('_'):
                    tools_dict[attr_name] = attr
        except Exception as e:
            print(f"Warning: Failed to load {file_path}: {str(e)}")

    return tools_dict


def extract_tool_signatures(tools_path: Path) -> list:
    tool_data = []
    files_to_parse = []

    # Handle both single file and directory cases
    if tools_path.is_file():
        files_to_parse.append(tools_path)
    elif tools_path.is_dir():
        files_to_parse.extend(tools_path.glob("**/*.py"))
    else:
        raise ValueError(f"Tools path {tools_path} is neither a file nor directory")

    for file_path in files_to_parse:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                code = f.read()
            parsed_code = ast.parse(code)

            for node in parsed_code.body:
                if isinstance(node, ast.FunctionDef):
                    name = node.name
                    args = [arg.arg for arg in node.args.args if arg.arg != "self"]
                    docstring = ast.get_docstring(node)
                    tool_data.append({
                        "Function Name": name,
                        "Arguments": args,
                        "Docstring": docstring or "No description available"
                    })
        except Exception as e:
            print(f"Warning: Failed to parse {file_path}: {str(e)}")
            continue

    return tool_data


def ensure_data_available(tool_name: str, inputs: dict, snapshot: dict, tools_module: dict) -> dict:
    cache = snapshot.setdefault("input_output_examples", {}).setdefault(tool_name, [])
    for entry in cache:
        if entry["inputs"] == inputs:
            return entry["output"]

    if tool_name not in tools_module:
        raise ValueError(f"Tool '{tool_name}' not found")

    output = tools_module[tool_name](**inputs)
    cache.append({"inputs": inputs, "output": output})
    if not isinstance(output, dict):
        print(f" Tool {tool_name} returned non-dict output: {output}")
    return output

def plan_tool_calls_with_llm(story: str, agent_name: str, tool_signatures_str: str, provider) -> list:

    renderer = ToolPlannerTemplateRenderer(TOOL_PLANNER_PROMPT_PATH)

    prompt = renderer.render(
        user_story=story,
        agent_name=agent_name,
        available_tools=tool_signatures_str,
    )
    response = provider.query(prompt)
    raw = response.get("generated_text", "")
    parsed = extract_first_json_list(raw)
    print("\n LLM Tool Plan:")
    print(json.dumps(parsed, indent=2))
    return parsed


# --- Tool Execution Logic ---
def run_tool_chain(tool_plan: list, snapshot: dict, tools_module) -> None:
    memory = {}

    for step in tool_plan:
        name = step["tool_name"]
        raw_inputs = step["inputs"]
        print(f"\n🔧 Tool: {name}")
        print(f" Raw inputs: {raw_inputs}")

        resolved_inputs = {}
        list_keys = []

        for k, v in raw_inputs.items():
            if isinstance(v, str) and v.startswith("$"):
                expr = v[1:]
                try:
                    resolved_value = eval(expr, {}, memory)
                    resolved_inputs[k] = resolved_value
                    if isinstance(resolved_value, list):
                        list_keys.append(k)
                except Exception as e:
                    print(f" ❌ Failed to resolve {v} in memory: {memory}")
                    raise ValueError(f"Failed to resolve placeholder {v}: {e}")
            else:
                resolved_inputs[k] = v

        print(f" Resolved inputs: {resolved_inputs}")

        if list_keys:
            if len(list_keys) > 1:
                raise ValueError(f"Tool '{name}' received multiple list inputs. Only one supported for now.")
            list_key = list_keys[0]
            value_list = resolved_inputs[list_key]

            results = []
            for idx, val in enumerate(value_list):
                item_inputs = resolved_inputs.copy()
                item_inputs[list_key] = val
                print(f" ⚙️ Running {name} with {list_key} = {val}")
                output = ensure_data_available(name, item_inputs, snapshot, tools_module)
                results.append(output)
                memory[f"{name}_{idx}"] = output

            memory[name] = results
            print(f"Stored {len(results)} outputs under '{name}' and indexed as '{name}_i'")
        else:
            output = ensure_data_available(name, resolved_inputs, snapshot, tools_module)
            memory[name] = output
            print(f"Stored output under tool name: {name} = {output}")


# --- Main Snapshot Builder ---
def build_snapshot(agent_name: str, tools_path: Path, stories: list, output_path: Path):
    agent = {"name": agent_name}
    tools_module = load_tools_module(tools_path)
    tool_signatures = extract_tool_signatures(tools_path)

    provider = WatsonXProvider(
        model_id="meta-llama/llama-3-405b-instruct",
        llm_decode_parameter={
            "min_new_tokens": 50,
            "decoding_method": "greedy",
            "max_new_tokens": 200
        }
    )

    snapshot = {
        "agent": agent,
        "tools": tool_signatures,
        "input_output_examples": {}
    }

    for story in stories:
        print(f"\n📘 Planning tool calls for story: {story}")
        tool_plan = plan_tool_calls_with_llm(story, agent["name"], tool_signatures, provider)
        run_tool_chain(tool_plan, snapshot, tools_module)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    print(f"\n✅ Snapshot saved to {output_path}")


if __name__ == "__main__":
    config = CLI(BatchAnnotateConfig, as_positional=False)
    tools_path = Path(config.tools_path)
    stories_path = Path(config.stories_path)

    stories = []
    agent_name = None
    with stories_path.open("r", encoding="utf-8", newline='') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            stories.append(row["story"])
            if agent_name is None:
                agent_name = row["agent"]

    snapshot_path = stories_path.parent / f"{agent_name}_snapshot_llm.json"

    build_snapshot(agent_name, tools_path, stories, snapshot_path)