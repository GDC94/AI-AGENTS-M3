import pytest
from pydantic import ValidationError

from orchestration.judging import QualityVerdict


def verdict(**overrides) -> dict:
    return {"quality": 8, "relevance": 9, "completeness": 7, "accuracy": 10, "reason": "Respuesta correcta."} | overrides


def test_a_verdict_keeps_its_four_ratings_and_reason():
    result = QualityVerdict(**verdict())

    assert (result.quality, result.relevance, result.completeness, result.accuracy) == (8, 9, 7, 10)
    assert result.reason == "Respuesta correcta."


@pytest.mark.parametrize("rating", [1, 10])
def test_the_boundary_ratings_are_accepted(rating):
    assert QualityVerdict(**verdict(quality=rating)).quality == rating


@pytest.mark.parametrize("field", ["quality", "relevance", "completeness", "accuracy"])
@pytest.mark.parametrize("rating", [0, 11, -3])
def test_a_rating_outside_1_to_10_is_rejected(field, rating):
    with pytest.raises(ValidationError):
        QualityVerdict(**verdict(**{field: rating}))


@pytest.mark.parametrize("field", ["quality", "relevance", "completeness", "accuracy"])
@pytest.mark.parametrize("rating", [7.5, 7.0, "7", True])
def test_a_non_integer_rating_is_rejected(field, rating):
    with pytest.raises(ValidationError):
        QualityVerdict(**verdict(**{field: rating}))
