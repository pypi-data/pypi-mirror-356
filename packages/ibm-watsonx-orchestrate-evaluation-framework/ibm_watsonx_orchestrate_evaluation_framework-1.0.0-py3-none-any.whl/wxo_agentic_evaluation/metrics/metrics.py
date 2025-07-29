from typing import List, Mapping, Any

import numpy as np
from pydantic import BaseModel, computed_field

from wxo_agentic_evaluation.metrics.llm_as_judge import Faithfulness, AnswerRelevancy
from wxo_agentic_evaluation.type import ConversationalConfidenceThresholdScore


class KnowledgeBaseMetrics(BaseModel):
    dataset_name: str = None
    knowledge_base_name: str = (
        None  # in the message response body it is represented as "tool_name"
    )
    tool_call_id: str = None
    faithfulness: Faithfulness = None
    answer_relevancy: AnswerRelevancy = None
    confidence_scores: ConversationalConfidenceThresholdScore = None


class KnowledgeBaseMetricSummary(BaseModel):
    knowledge_base_metrics: List[List[KnowledgeBaseMetrics]]

    @computed_field(alias="detailed")
    @property
    def groupby_dataset(self) -> Mapping[str, Any]:
        groupby = {}
        for metric in self.knowledge_base_metrics:
            for row in metric:
                name = row.dataset_name
                tool_call_id = row.tool_call_id
                knowledge_base_name = row.knowledge_base_name
                faithfulness = row.faithfulness
                confidence_scores = row.confidence_scores
                answer_relevancy = row.answer_relevancy

                if name not in groupby:
                    groupby[name] = {
                        "knowledge_base_name": [knowledge_base_name],
                        "faithfulness": [faithfulness],
                        "confidence_scores": [confidence_scores],
                        "tool_call_id": [tool_call_id],
                        "answer_relevancy": [answer_relevancy],
                        "number_of_calls": 1,
                    }
                else:
                    values = groupby[name]
                    values.get("knowledge_base_name").append(knowledge_base_name)
                    values.get("faithfulness").append(faithfulness)
                    values.get("answer_relevancy").append(answer_relevancy)
                    values.get("confidence_scores").append(confidence_scores)
                    values.get("tool_call_id").append(tool_call_id)
                    values["number_of_calls"] += 1
                    groupby[name] = values

        return groupby

    @computed_field(alias="summary")
    @property
    def average(self) -> Mapping[str, Any]:
        summary = {}
        for dataset, metric in self.groupby_dataset.items():
            average_metric = {}
            average_metric["average_faithfulness"] = np.average(
                [
                    float(faithfulness.faithfulness_score)
                    for faithfulness in metric["faithfulness"]
                ]
            )
            average_metric["average_response_confidence"] = np.average(
                [
                    float(confidence_score.response_confidence)
                    for confidence_score in metric["confidence_scores"]
                ]
            )
            average_metric["average_retrieval_confidence"] = np.average(
                [
                    float(confidence_score.retrieval_confidence)
                    for confidence_score in metric["confidence_scores"]
                ]
            )
            average_metric["average_answer_relevancy"] = np.average(
                [
                    float(answer_relevancy.answer_relevancy_score)
                    for answer_relevancy in metric["answer_relevancy"]
                ]
            )
            average_metric["number_of_calls"] = metric["number_of_calls"]
            average_metric["knowledge_bases_called"] = ", ".join(
                set(metric["knowledge_base_name"])
            )
            summary[dataset] = average_metric

        return summary


class KeywordSemanticSearchMetric(BaseModel):
    keyword_match: bool
    semantic_match: bool
    message: str
    goal_detail: str
