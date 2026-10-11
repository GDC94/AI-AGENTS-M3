"""What the system returns for one Query."""

from pydantic import BaseModel

from orchestration.routing import Route
from orchestration.section import RetrievedSection


class SupportAnswer(BaseModel):
    query: str
    route: Route
    answer: str
    sections: list[RetrievedSection]
    abstained: bool
    # Only None until the Judge exists (ticket 05 widens it to QualityVerdict | None).
    verdict: None = None
    trace_id: str
