"""The three Checks: pure, deterministic comparisons of a SupportAnswer with a Test Query."""

from orchestration.checks.test_query import TestQuery
from orchestration.support_answer import SupportAnswer


def routing_correct(answer: SupportAnswer, test_query: TestQuery) -> bool:
    """The Route's target equals the expected Area (or out_of_scope)."""
    return answer.route.target == test_query.expected_area


def retrieval_hit(answer: SupportAnswer, test_query: TestQuery) -> bool:
    """The expected Section is among the Sections used. False when no Section is expected."""
    if test_query.expected_section is None:
        return False
    return any(section.title == test_query.expected_section for section in answer.sections)


def abstained(answer: SupportAnswer, test_query: TestQuery) -> bool:
    """Whether the Specialist abstained. A raw observation: it ignores the Test Query's expectation.

    Expected true for unanswerable Test Queries with an Area and false for the rest. Like
    `retrieval_hit`, it applies only where it makes sense (Test Queries with an Area); the
    caller decides, because an out_of_scope Query never reaches a Specialist.
    """
    return answer.abstained
