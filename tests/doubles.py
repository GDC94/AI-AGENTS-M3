"""Test doubles shared by the unit tests."""

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import BaseMessage
from pydantic import Field


class RecordingScorePublisher:
    """In-memory ScorePublisher that records every published score."""

    def __init__(self) -> None:
        self.abstentions: list[tuple[str, bool]] = []

    def publish_abstention(self, trace_id: str, abstained: bool) -> None:
        self.abstentions.append((trace_id, abstained))


class RecordingFakeChatModel(FakeListChatModel):
    """Fake chat model that answers from a list and records the messages of every call."""

    received: list[list[BaseMessage]] = Field(default_factory=list)

    def _call(self, messages: list[BaseMessage], *args, **kwargs) -> str:
        self.received.append(messages)
        return super()._call(messages, *args, **kwargs)
