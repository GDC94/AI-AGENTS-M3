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
    answerable = [test_query for test_query in test_queries if test_query.is_answerable]
    unanswerable = [test_query for test_query in test_queries if test_query.is_unanswerable]
    retrieved = {
        test_query.id: retrieve_by_area[Area(test_query.expected_area)](test_query.query)
        for test_query in [*answerable, *unanswerable]
    }

    def list_surviving_titles(test_query: TestQuery, threshold: float) -> list[str]:
        return [section.title for section in retrieved[test_query.id] if section.similarity >= threshold]

    return [
        SweepPoint(
            threshold=threshold,
            retrieval_hits=sum(test_query.expected_section in list_surviving_titles(test_query, threshold) for test_query in answerable),
            answerable=len(answerable),
            correct_abstentions=sum(not list_surviving_titles(test_query, threshold) for test_query in unanswerable),
            unanswerable=len(unanswerable),
        )
        for threshold in thresholds
    ]
