"""Threshold sweep: how retrieval and Abstention would behave at each candidate Similarity Threshold.

Pure: it only compares Similarities. No model is called and no trace is created.
"""

from collections.abc import Mapping, Sequence

from pydantic import BaseModel

from orchestration.area import Area
from orchestration.checks.test_query import TestQuery
from orchestration.specialists import Retrieve


class SweepPoint(BaseModel):
    threshold: float
    # Answerable Test Queries (direct, frontier) whose expected Section survives the threshold.
    retrieval_hits: int
    answerable: int
    # Unanswerable Test Queries for which no Section survives the threshold.
    correct_abstentions: int
    unanswerable: int


def sweep_threshold(
    retrieve_by_area: Mapping[Area, Retrieve],
    test_queries: Sequence[TestQuery],
    thresholds: Sequence[float],
) -> list[SweepPoint]:
    """One point per threshold. Each Query is retrieved once, from its expected Area.

    Uses the Specialist's rule: a Section is kept when its Similarity is >= the threshold.
    Out of Scope Test Queries never reach a Specialist, so they are ignored.
    """
    answerable = [q for q in test_queries if q.type in ("direct", "frontier")]
    unanswerable = [q for q in test_queries if q.type == "unanswerable"]
    retrieved = {q.id: retrieve_by_area[Area(q.expected_area)](q.query) for q in [*answerable, *unanswerable]}

    def survivors(test_query: TestQuery, threshold: float) -> list[str]:
        return [s.title for s in retrieved[test_query.id] if s.similarity >= threshold]

    return [
        SweepPoint(
            threshold=threshold,
            retrieval_hits=sum(q.expected_section in survivors(q, threshold) for q in answerable),
            answerable=len(answerable),
            correct_abstentions=sum(not survivors(q, threshold) for q in unanswerable),
            unanswerable=len(unanswerable),
        )
        for threshold in thresholds
    ]
