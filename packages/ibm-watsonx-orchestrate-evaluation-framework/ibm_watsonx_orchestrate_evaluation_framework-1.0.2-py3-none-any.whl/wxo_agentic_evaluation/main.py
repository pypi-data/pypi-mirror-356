from wxo_agentic_evaluation.watsonx_provider import WatsonXProvider
from wxo_agentic_evaluation.llm_user import LLMUser
from wxo_agentic_evaluation.prompt.template_render import LlamaUserTemplateRenderer
from wxo_agentic_evaluation.inference_backend import (
    EvaluationController,
    get_wxo_inference_backend,
)
from wxo_agentic_evaluation.evaluation_package import EvaluationPackage
from wxo_agentic_evaluation.type import EvaluationData

from wxo_agentic_evaluation.arg_configs import TestConfig
from wxo_agentic_evaluation.utils.utils import (
    create_table,
    create_average_row,
    SummaryPanel,
)
from wxo_agentic_evaluation.utils import json_dump
from wxo_agentic_evaluation.metrics.metrics import KnowledgeBaseMetricSummary
import os
import json

import yaml
import dataclasses
import glob
import rich
import csv
from rich.progress import Progress
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from jsonargparse import CLI


def process_test_case(task_n, test_case, config, inference_backend, llm_user):
    summary_results_for_path = []
    tc_name = os.path.basename(test_case).replace(".json", "")
    with open(test_case, "r") as f:
        test_case: EvaluationData = EvaluationData.model_validate(json.load(f))

    evaluation_controller = EvaluationController(
        wxo_inference_backend=inference_backend, llm_user=llm_user, config=config
    )
    rich.print(f"[bold magenta]Running test case: {tc_name}[/bold magenta]")
    history, call_tracker, conversational_search_data = evaluation_controller.run(
        task_n,
        test_case.story,
        agent_name=test_case.agent,
        starting_user_input=test_case.starting_sentence,
    )
    result = list()
    for message in history:
        result.append(message.model_dump())

    json_dump(
        os.path.join(config.output_dir, "messages", tc_name + ".messages.json"), result
    )

    if len(conversational_search_data) > 0:
        fn = tc_name + ".retrieval_context.json"
        out_folder = Path(config.output_dir) / "knowledge_base_metrics"
        out_folder.mkdir(exist_ok=True)
        rc = [context.model_dump() for context in conversational_search_data]
        json_dump(out_folder / fn, rc)

    # If data annotation run, skip summary generation
    if config.data_annotation_run:
        return summary_results_for_path  # empty result set, skip summary

    evaluation_package = EvaluationPackage(
        test_case_name=tc_name,
        messages=history,
        ground_truth=test_case,
        conversational_search_data=conversational_search_data,
    )
    (
        tool_call_metrics,
        keyword_semantic_matches,
        knowledge_base_metrics,
        messages_with_reason,
        metrics,
    ) = evaluation_package.generate_summary()
    temp = []
    for message in messages_with_reason:
        temp.append(message.model_dump())
    json_dump(
        os.path.join(config.output_dir, "messages", tc_name + ".messages.analyze.json"),
        temp,
    )

    json_dump(
        os.path.join(config.output_dir, "messages", tc_name + ".metrics.json"),
        metrics.model_dump(),
    )

    tool_call_metrics["Avg Resp Time (Secs)"] = (
        sum(call_tracker.generic) + sum(call_tracker.tool_call)
    ) / (len(call_tracker.generic) + len(call_tracker.tool_call))
    tool_call_metrics["Avg Resp Time (Secs)"] = round(
        tool_call_metrics["Avg Resp Time (Secs)"], 2
    )

    summary_results_for_path.append((tool_call_metrics, knowledge_base_metrics))

    return summary_results_for_path


def main(config: TestConfig):
    executor = ThreadPoolExecutor(max_workers=config.num_workers)
    wai_client = WatsonXProvider(model_id=config.llm_user_config.model_id)
    inference_backend = get_wxo_inference_backend(
        config.auth_config.url, config.auth_config.tenant_name, config.auth_config.token
    )

    llm_user = LLMUser(
        wai_client=wai_client,
        template=LlamaUserTemplateRenderer(config.llm_user_config.prompt_config),
        user_response_style=config.llm_user_config.user_response_style,
    )

    print(f"Running evaluation with tenant {config.auth_config.tenant_name}")

    results_list = []

    knowledge_base_output_folder = Path(config.output_dir) / "knowledge_base_metrics"
    knowledge_base_output_folder.mkdir(exist_ok=True, parents=True)
    detailed_rag_output_file = (
        knowledge_base_output_folder / "knowledge_base_detailed_metrics.json"
    )
    summary_rag_output_file = (
        Path(config.output_dir) / "knowledge_base_summary_metrics.json"
    )

    os.makedirs(os.path.join(config.output_dir, "messages"), exist_ok=True)
    available_res = set()
    if config.skip_available_results:
        available_res = set(
            [
                os.path.basename(f).replace(".messages", "")
                for f in glob.glob(
                    os.path.join(config.output_dir, "messages", "*.messages.json")
                )
            ]
        )

    test_cases = []
    for test_path in config.test_paths:
        if os.path.isdir(test_path):
            test_path = os.path.join(test_path, "*.json")
        test_cases.extend(sorted(glob.glob(test_path)))
    
    futures = []
    task_n = 0
    for test_case in test_cases:
        if not test_case.endswith(".json") or test_case.endswith("agent.json"):
            continue
        if config.skip_available_results:
            if test_case in available_res:
                print(f"Skipping test case {test_case} as results already exist.")
                continue

        future = executor.submit(
            process_test_case,
            task_n,
            test_case,
            config,
            inference_backend,
            llm_user,
        )

        futures.append((test_case, future))
        task_n += 1

    if futures:
        with Progress() as progress:
            task1 = progress.add_task(
                f"[purple]Evaluating {len(futures)} tasks...", total=len(futures)
            )
            for test_case, future in futures:
                try:
                    results_list.extend(future.result())
                except Exception as e:
                    rich.print(f"test case {test_case} fails with {e}")
                finally:
                    progress.update(task1, advance=1)

    tool_call_metrics = [metric[0] for metric in results_list]
    knowledge_base_metrics = [metric[1] for metric in results_list]

    rag_metric_summary = KnowledgeBaseMetricSummary(
        knowledge_base_metrics=knowledge_base_metrics
    )
    SummaryPanel(rag_metric_summary).print()

    with open(detailed_rag_output_file, "w+", encoding="utf-8") as f:
        json.dump(rag_metric_summary.model_dump(by_alias=True)["detailed"], f, indent=4)

    with open(summary_rag_output_file, "w+", encoding="utf-8") as f:
        json.dump(rag_metric_summary.model_dump(by_alias=True)["summary"], f, indent=4)

    if len(tool_call_metrics) > 0:
        # remove the average row if exist
        tool_call_metrics = [
            row for row in tool_call_metrics if row["Dataset"] != "Summary (Average)"
        ]
        avg_row = create_average_row(tool_call_metrics)
        tool_call_metrics.append(avg_row)
    
    tool_call_table = create_table(tool_call_metrics)
    
    if tool_call_table:
        tool_call_table.print()

    if len(tool_call_metrics) > 0:
        output_file = os.path.join(config.output_dir, "summary_metrics.csv")
        header = list(tool_call_metrics[0].keys())

        with open(output_file, "w") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(header)
            for entry in tool_call_metrics:
                csv_writer.writerow([entry[name] for name in header])

    with open(
        os.path.join(config.output_dir, "config.yml"), "w", encoding="utf-8"
    ) as f:
        yaml.safe_dump(dataclasses.asdict(config), f)

    print(f"Results saved to {config.output_dir}")


if __name__ == "__main__":
    main(CLI(TestConfig, as_positional=False))
