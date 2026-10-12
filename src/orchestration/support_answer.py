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


def format_support_answer(answer: SupportAnswer, trace_url: str | None) -> str:
    """Plain text for one SupportAnswer: Route, Sections used, Answer, abstained flag, verdict if any, trace link."""
    lines = [
        f"Query: {answer.query}",
        f"Route: {answer.route.target}",
        f"Reasoning: {answer.route.reasoning}",
        "Sections used:",
        *(_format_sections(answer.sections)),
        f"Answer: {answer.answer}",
        f"abstained: {answer.abstained}",
    ]
    if answer.verdict is not None:
        ratings = ", ".join(f"{name}: {rating}" for name, rating in answer.verdict.ratings_by_name().items())
        lines += [f"Quality Verdict: {ratings}", f"Verdict reason: {answer.verdict.reason}"]
    lines.append(f"Trace: {trace_url if trace_url is not None else '(no trace link available)'}")
    return "\n".join(lines)


def _format_sections(sections: list[RetrievedSection]) -> list[str]:
    if not sections:
        return ["  (none)"]
    return [f"  - {section.title} (similarity {section.similarity:.3f})" for section in sections]
