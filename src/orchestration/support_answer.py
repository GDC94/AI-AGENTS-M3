"""What the system returns for one Query."""

from pydantic import BaseModel

from orchestration.judging import QualityVerdict
from orchestration.routing import Route
from orchestration.section import RetrievedSection


class SupportAnswer(BaseModel):
    query: str
    route: Route
    answer: str
    sections: list[RetrievedSection]
    abstained: bool
    # None for Abstentions and Out of Scope replies, which are never judged.
    verdict: QualityVerdict | None = None
    trace_id: str
