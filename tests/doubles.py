"""Test doubles shared by the unit tests."""

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import BaseMessage
from pydantic import Field

from orchestration.judging import QualityVerdict


class RecordingScorePublisher:
    """In-memory ScorePublisher that records every published score as (trace_id, name, value), in order."""

    def __init__(self) -> None:
        self.scores: list[tuple[str, str, int]] = []

    def publish_abstention(self, trace_id: str, abstained: bool) -> None:
        self.scores.append((trace_id, "abstained", 1 if abstained else 0))

    def publish_quality_scores(self, trace_id: str, verdict: QualityVerdict) -> None:
        for name, rating in verdict.ratings_by_name().items():
            self.scores.append((trace_id, name, rating))


class RecordingFakeChatModel(FakeListChatModel):
    """Fake chat model that answers from a list and records the messages of every call."""

    received: list[list[BaseMessage]] = Field(default_factory=list)

    def _call(self, messages: list[BaseMessage], *args, **kwargs) -> str:
        self.received.append(messages)
        return super()._call(messages, *args, **kwargs)
