"""Test doubles shared by the unit tests."""


class RecordingScorePublisher:
    """In-memory ScorePublisher that records every published score."""

    def __init__(self) -> None:
        self.abstentions: list[tuple[str, bool]] = []

    def publish_abstention(self, trace_id: str, abstained: bool) -> None:
        self.abstentions.append((trace_id, abstained))
