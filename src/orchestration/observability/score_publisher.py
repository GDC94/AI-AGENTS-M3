"""Port for publishing scores on a trace, so answering never imports Langfuse."""

from typing import Protocol

from langfuse import Langfuse

from orchestration.judging import QualityVerdict


class ScorePublisher(Protocol):
    def publish_abstention(self, trace_id: str, abstained: bool) -> None: ...

    def publish_quality_scores(self, trace_id: str, verdict: QualityVerdict) -> None: ...


class LangfuseScorePublisher:
    """Production adapter: writes scores to Langfuse."""

    def __init__(self, client: Langfuse) -> None:
        self._client = client

    def publish_abstention(self, trace_id: str, abstained: bool) -> None:
        self._client.create_score(
            trace_id=trace_id, name="abstained", value=1 if abstained else 0, data_type="BOOLEAN"
        )

    def publish_quality_scores(self, trace_id: str, verdict: QualityVerdict) -> None:
        for name in ("quality", "relevance", "completeness", "accuracy"):
            self._client.create_score(
                trace_id=trace_id,
                name=name,
                value=getattr(verdict, name),
                data_type="NUMERIC",
                comment=verdict.reason,
            )
