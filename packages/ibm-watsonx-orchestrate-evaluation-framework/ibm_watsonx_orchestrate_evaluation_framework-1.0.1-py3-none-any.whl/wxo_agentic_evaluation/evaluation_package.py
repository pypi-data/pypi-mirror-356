from typing import List
import json
import os 
import rich

from wxo_agentic_evaluation.data_annotator import ERROR_KEYWORDS

from wxo_agentic_evaluation.type import (
    ContentType,
    Message,
    EvaluationData,
    ToolCallAndRoutingMetrics,
    EventTypes,
    ConversationalSearch,
    ExtendedMessage,
)
from wxo_agentic_evaluation.watsonx_provider import WatsonXProvider
from wxo_agentic_evaluation.metrics.metrics import (
    KnowledgeBaseMetrics,
    KeywordSemanticSearchMetric,
)
from wxo_agentic_evaluation.prompt.template_render import (
    KeywordMatchingTemplateRenderer,
    SemanticMatchingTemplateRenderer,
    FaithfulnessTemplateRenderer,
    AnswerRelevancyTemplateRenderer,
)
from wxo_agentic_evaluation.llm_matching import LLMMatcher
from wxo_agentic_evaluation.llm_rag_eval import LLMJudge
from wxo_agentic_evaluation import __file__

root_dir = os.path.dirname(__file__)
KEYWORD_MATCHING_PROMPT_PATH = os.path.join(root_dir, "prompt", "keyword_matching_prompt.jinja2")
SEMANTIC_MATCHING_PROMPT_PATH = os.path.join(root_dir, "prompt", "semantic_matching_prompt.jinja2")
FAITHFULNESS_PROMPT_PATH = os.path.join(root_dir, "prompt", "faithfulness_prompt.jinja2")
ANSWER_RELEVANCY_PROMPT_PATH = os.path.join(root_dir, "prompt", "answer_relevancy_prompt.jinja2")


class EvaluationPackage:
    def __init__(
        self,
        test_case_name,
        ground_truth,
        messages,
        conversational_search_data: List[ConversationalSearch] = None,
        is_analyze_run=False,
    ):
        self.tool_dictionary = {
            goal_detail.name: goal_detail
            for goal_detail in ground_truth.goal_details
            if goal_detail.type == ContentType.tool_call
        }
        self.text_list = [
            goal_detail
            for goal_detail in ground_truth.goal_details
            if goal_detail.type == ContentType.text
        ]
        self.messages = messages
        self.conversational_search_data = conversational_search_data
        self.validate_ground_truth(ground_truth, test_case_name)
        self.ground_truth = ground_truth
        self.test_case_name = test_case_name
        self.is_analyze_run = is_analyze_run

        self.matcher = LLMMatcher(
            llm_client=WatsonXProvider(
                model_id="meta-llama/llama-3-405b-instruct",
                llm_decode_parameter={
                    "min_new_tokens": 0,
                    "decoding_method": "greedy",
                    "max_new_tokens": 10,
                },
            ),
            keyword_template=KeywordMatchingTemplateRenderer(
                KEYWORD_MATCHING_PROMPT_PATH
            ),
            semantic_template=SemanticMatchingTemplateRenderer(
                SEMANTIC_MATCHING_PROMPT_PATH
            ),
        )
        self.rag_llm_as_a_judge = LLMJudge(
            llm_client=WatsonXProvider(
                model_id="meta-llama/llama-3-405b-instruct",
                llm_decode_parameter={
                    "min_new_tokens": 0,
                    "decoding_method": "greedy",
                    "max_new_tokens": 4096,
                },
            ),
            faithfulness=FaithfulnessTemplateRenderer(FAITHFULNESS_PROMPT_PATH),
            answer_relevancy=AnswerRelevancyTemplateRenderer(
                ANSWER_RELEVANCY_PROMPT_PATH
            ),
        )

    @staticmethod
    def is_topological_sort(graph, ordering):
        position = {node: i for i, node in enumerate(ordering)}
        for u in graph:
            for v in graph[u]:
                if u not in position or v not in position:
                    return False
                if position[u] >= position[v]:
                    return False
        return True

    @staticmethod
    def validate_ground_truth(ground_truth, test_case_name):
        if len(ground_truth.agent) == 0:
            raise ValueError(
                f"No agent provided in the ground truth. test_case_name: {test_case_name}"
            )

        if len(ground_truth.goals) == 0:
            raise ValueError(
                f"No goals provided in the ground truth. test_case_name: {test_case_name}"
            )

        if len(ground_truth.goal_details) == 0:
            raise ValueError(
                f"No goal details provided in the ground truth. test_case_name: {test_case_name}"
            )

        if len(ground_truth.story) == 0:
            raise ValueError(
                f"No story provided in the ground truth. test_case_name: {test_case_name}"
            )

        goals = set()

        for key, value in ground_truth.goals.items():
            goals.add(key)
            if isinstance(value, list):
                goals.update(value)
            else:
                raise ValueError(
                    f"The goal '{key}' is not mapping to a list: {value}. test_case_name: {test_case_name}"
                )

        for goal_detail in ground_truth.goal_details:
            if goal_detail.name not in goals:
                raise ValueError(
                    f"Goal detail '{goal_detail.name}' does not match any goals: {goals}. test_case_name: {test_case_name}"
                )
            if goal_detail.name == "summarize":
                if len(goal_detail.keywords) == 0 and len(goal_detail.response) == 0:
                    rich.print(
                        f"Summarize goal should have keywords or final response. test_case_name: {test_case_name}"
                    )
                elif len(goal_detail.response) == 0:
                    rich.print(
                        f"⚠️‼️ [bold][yellow] WARNING:[/yellow][/bold] Summarize goal has no final response. test_case_name: {test_case_name}"
                    )
        if len(ground_truth.goal_details) != len(goals):
            raise ValueError(
                f"Goal details count does not match the goals count: {len(ground_truth.goal_details)} != {len(goals)}. test_case_name: {test_case_name}"
            )

    def _print_kw_sm(
        self, keyword_semantic_match_list: List[KeywordSemanticSearchMetric]
    ):
        """Prints the keyword match/mismatch, and semantic match/mismatch results
        Right now only successful matches are printed
        """

        for keyword_semantic_match in keyword_semantic_match_list:
            if (
                keyword_semantic_match.semantic_match
                and keyword_semantic_match.keyword_match
            ):
                rich.print(
                    f"[green][SUCCESS] Text message matched: Summary - {keyword_semantic_match.message}[/green]"
                )

    def traverse(self):
        labelled_messages = []
        message_outcomes = []
        labelled_messages_without_text_step = []
        # Counters for tool-calling related metrics
        tool_call_and_routing_metrics = ToolCallAndRoutingMetrics(
            total_tool_calls=0,
            expected_tool_calls=0,
            relevant_tool_calls=0,
            correct_tool_calls=0,
            total_routing_calls=0,
            expected_routing_calls=0,
        )
        tool_call_and_routing_metrics.expected_tool_calls = len(self.tool_dictionary)

        for message in self.messages:
            if message.type == ContentType.tool_call:
                tool_call_and_routing_metrics.total_tool_calls += 1
                msg_tool_call = json.loads(message.content)

                # Check for transfer_* calls
                if msg_tool_call["name"].startswith("transfer_to_"):
                    tool_call_and_routing_metrics.total_routing_calls += 1

                # evaluating more than once is fine
                # agent could make repeated calls with the same function signature
                # in our is_topological_sort algorithm, the most recent occurrence is evaluated
                matching_goal_details = [
                    goal_detail
                    for goal_detail in self.tool_dictionary.values()
                    if goal_detail.tool_name == msg_tool_call["name"]
                ]
                if len(matching_goal_details) > 0:
                    tool_call_and_routing_metrics.relevant_tool_calls += 1  # tool name matches one of the expected tool names, as defined in the ground truth
                    found = False
                    possible_ground_truth = []
                    for goal_detail in matching_goal_details:
                        if (
                            is_transfer := msg_tool_call["name"].startswith(
                                "transfer_to_"
                            )
                        ) or msg_tool_call["args"] == goal_detail.args:
                            labelled_messages.append(goal_detail.name)
                            labelled_messages_without_text_step.append(goal_detail.name)
                            if is_transfer:
                                tool_call_and_routing_metrics.expected_routing_calls += (
                                    1
                                )
                            else:
                                tool_call_and_routing_metrics.correct_tool_calls += 1  # correct tool call (no erroneous response) + expected arguments, as defined in the ground truth
                            found = True
                            message_outcome = ExtendedMessage(message=message)
                            message_outcomes.append(message_outcome)
                            break
                        else:
                            possible_ground_truth.append(goal_detail.args)

                    if not found:
                        message_outcome = ExtendedMessage(message=message)
                        message_outcome.reason = {
                            "reason": "incorrect parameter",
                            "actual": msg_tool_call["args"],
                            "expected": possible_ground_truth,
                        }
                        message_outcomes.append(message_outcome)
                        rich.print(
                            f"[red][ERROR] Wrong parameters for function: {msg_tool_call['name']}. "
                            f"Expected one of {[g.args for g in matching_goal_details]}, Received={msg_tool_call['args']}[/red]"
                        )
                        labelled_messages.append(
                            msg_tool_call["name"] + "_WRONG_PARAMETERS"
                        )
                else:
                    # TO-DO: we need a way to backtrack agent/tool pairs.
                    # if we route to an agent without the right toolset, that makes it a routing error.
                    # this will remove the need to label routing calls explicitly
                    if not msg_tool_call["name"].startswith("transfer_to_"):
                        rich.print(
                            f"[red][ERROR] Wrong function call: {msg_tool_call['name']}[/red]"
                        )
                        labelled_messages.append(
                            msg_tool_call["name"] + "_WRONG_FUNCTION_CALL"
                        )
                        message_outcome = ExtendedMessage(message=message)
                        message_outcome.reason = {"reason": "irrelevant tool call"}
                        message_outcomes.append(message_outcome)

            elif message.type == ContentType.tool_response:
                found = False
                for keyword in ERROR_KEYWORDS:
                    if keyword in message.content.lower():
                        message_outcome = ExtendedMessage(message=message)
                        message_outcome.reason = {"reason": "runtime error"}
                        message_outcomes.append(message_outcome)
                        found = True
                        break
                if not found:
                    message_outcome = ExtendedMessage(message=message)
                    message_outcomes.append(message_outcome)
            else:

                message_outcome = ExtendedMessage(message=message)
                message_outcomes.append(message_outcome)
        assistant_responses = [
            message
            for message in self.messages
            if message.event == EventTypes.message_created
            and message.role == "assistant"
        ]
        keyword_semantic_list = []
        for message in assistant_responses:
            for goal_detail in self.text_list:
                if goal_detail.name not in labelled_messages:
                    keyword_match: bool = self.matcher.keywords_match(
                        message.content, goal_detail.keywords
                    )
                    semantic_match: bool = self.matcher.semantic_match(
                        message.content, goal_detail.response
                    )
                    keyword_semantic_match = KeywordSemanticSearchMetric(
                        keyword_match=keyword_match,
                        semantic_match=semantic_match,
                        message=message.content,
                        goal_detail=goal_detail.name,
                    )
                    if keyword_match and semantic_match:
                        labelled_messages.append(goal_detail.name)
                        keyword_semantic_list.append(keyword_semantic_match)
                        break

        # only prints when the semantic and keyword matched
        self._print_kw_sm(keyword_semantic_list)

        return (
            labelled_messages,
            labelled_messages_without_text_step,
            keyword_semantic_list,
            tool_call_and_routing_metrics,
            message_outcomes,
        )

    def _is_text_match(
        self, keyword_semantic_match_list: List[KeywordSemanticSearchMetric]
    ):

        if len(self.text_list) == 0:
            return "NA"
        elif len(self.text_list) == len(keyword_semantic_match_list):
            return "Summary Matched"
        else:
            return "Summary MisMatched"

    def generate_summary(self):
        llm_steps = 0
        total_step = 0
        (
            labelled_messages,
            labelled_messages_without_text_step,
            matches,
            metrics,
            message_with_reasons,
        ) = self.traverse()
        if self.is_analyze_run:
            print(labelled_messages)
        wrong_call_count = sum(
            1 for msg in labelled_messages if "_WRONG_FUNCTION_CALL" in msg
        )
        is_success = self.is_topological_sort(
            self.ground_truth.goals, labelled_messages
        )
        match = self._is_text_match(matches)

        for message in self.messages:
            if message.role == "assistant" and (
                message.type
                in (
                    ContentType.text,
                    ContentType.conversational_search,
                    ContentType.tool_call,
                )
            ):
                llm_steps += 1
            total_step += 1

        knowledge_base_metric_summary = self.generate_knowledge_base_metric_summary()
        # TO-DO: the table is not printing properly anymore with the new columns introduced
        # we need to introduce a separate table for these.
        data = {
            "Dataset": self.test_case_name,
            "Total Step": total_step,
            "Agent Step": llm_steps,
            "Ground Truth Calls": len(self.tool_dictionary),
            "Wrong Function Calls": wrong_call_count,
            # "Bad Calls": 0,
            "Wrong Parameters": sum(
                1 for msg in labelled_messages if "_WRONG_PARAMETERS" in msg
            ),
            "Wrong Routing Calls": sum(
                1 for msg in labelled_messages if "_WRONG_ROUTING_CALL" in msg
            ),
            "Text Match": match,
            "Journey Success": is_success,
            # "Tool Call Accuracy": metrics.tool_call_accuracy,
            # "Tool Call Relevancy": metrics.tool_call_relevancy,
            # "Agent Routing Accuracy": metrics.agent_routing_accuracy
        }

        return (
            data,
            matches,
            knowledge_base_metric_summary,
            message_with_reasons,
            metrics,
        )

    def _get_messages_by_role_before_cs(
        self, idx_conversational_search: int, role: str, type: str = "text"
    ):
        """Utility method to filter `self.messages` for messages with a given role
        that occur before the conversational search message index
        """

        filtered_messages = [
            message
            for idx, message in enumerate(self.messages)
            if idx < idx_conversational_search
            and message.role == role
            and message.type == type
        ]

        return filtered_messages

    def _weave_user_assistant_messages(self, user_messages, assistant_messages):
        weave = []
        for user, assistant in zip(user_messages, assistant_messages):
            msg = f"User: {user.content}\nAssistant: {assistant.content}\n\n"
            weave.append(msg)

        return " ".join(weave)

    def _find_tool_call_name(self, tool_call_id):
        for message in self.messages:
            if message.type == ContentType.tool_call:
                content = json.loads(message.content)
                id = content.get("tool_call_id", "")
                if id == tool_call_id:
                    return content.get("name")

        raise Exception(f"'{tool_call_id}' not found in messages")

    def generate_knowledge_base_metric_summary(self) -> KnowledgeBaseMetrics:
        idx_conv_search = [
            idx
            for idx, message in enumerate(self.messages)
            if message.type == ContentType.conversational_search
        ]
        metrics = []

        for search_index in idx_conv_search:
            user_messages = self._get_messages_by_role_before_cs(
                role="user", idx_conversational_search=search_index
            )
            assistant_messages = self._get_messages_by_role_before_cs(
                role="assistant",
                idx_conversational_search=search_index,
                type=ContentType.text,
            )

            context = self._weave_user_assistant_messages(
                user_messages, assistant_messages
            )
            most_recent_user_message = user_messages[-1]
            search_message = self.messages[search_index]

            # find the conversational search metadata associated with this message
            conversational_search_data = None
            if self.conversational_search_data:
                for cs_metadata in self.conversational_search_data:
                    if (
                        search_message.conversational_search_metadata.tool_call_id
                        == cs_metadata.metadata.tool_call_id
                    ):
                        conversational_search_data = cs_metadata

            tool_name = self._find_tool_call_name(
                conversational_search_data.metadata.tool_call_id
            )  # name of knowledge base

            search_results = [
                result.body for result in conversational_search_data.search_results
            ]
            faithfulness = self.rag_llm_as_a_judge.faithfulness(
                conversational_search_data.text, search_results
            )
            answer_relevancy = self.rag_llm_as_a_judge.answer_relevancy(
                question=most_recent_user_message.content,
                context=context,
                answer=search_message.content,
            )
            knowledge_base_metrics = KnowledgeBaseMetrics(
                dataset_name=self.test_case_name,
                knowledge_base_name=tool_name,
                tool_call_id=search_message.conversational_search_metadata.tool_call_id,
                faithfulness=faithfulness,
                answer_relevancy=answer_relevancy,
                confidence_scores=conversational_search_data.confidence_scores,
            )

            metrics.append(knowledge_base_metrics)

        return metrics


if __name__ == "__main__":

    messages = []

    with open(
        "./benchmarks/workday_tools/concise/result/llama/messages/data18.messages.json",
        "r",
        encoding="utf-8",
    ) as f:

        temp = json.load(f)

        for message in temp:
            messages.append(Message.model_validate(message))

    for message in messages:
        if message.role == "user":
            rich.print("[yellow]GENERATED_USER_MESSAGE:[/yellow]", message.content)
        else:
            rich.print("[orange3]WXO:[/orange3]", message.content)

    with open("./benchmarks/workday_tools/data/data18.json", "r") as f:
        ground_truth = EvaluationData.model_validate(json.load(f))

    evaluate_package = EvaluationPackage(
        test_case_name="data1.messages.json",
        ground_truth=ground_truth,
        messages=messages,
    )
    print(evaluate_package.generate_summary())
    # print(evaluate_package.traverse())
