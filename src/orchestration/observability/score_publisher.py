"""Port for publishing scores on a trace, so answering never imports Langfuse."""

from typing import Protocol

from langfuse import Langfuse


class ScorePublisher(Protocol):
    def publish_abstention(self, trace_id: str, abstained: bool) -> None: ...


class LangfuseScorePublisher:
    """Production adapter: writes scores to Langfuse."""

    def __init__(self, client: Langfuse) -> None:
        self._client = client

    def publish_abstention(self, trace_id: str, abstained: bool) -> None:
        self._client.create_score(
            trace_id=trace_id, name="abstained", value=1 if abstained else 0, data_type="BOOLEAN"
        )
