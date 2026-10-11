import pytest
from pydantic import ValidationError

from orchestration.section import RetrievedSection


def test_holds_title_text_and_similarity():
    section = RetrievedSection(title="Payslips", text="## Payslips\nWhere to find them.", similarity=0.8)

    assert section.title == "Payslips"
    assert section.text == "## Payslips\nWhere to find them."
    assert section.similarity == 0.8


@pytest.mark.parametrize("similarity", [0.0, 1.0])
def test_accepts_similarity_bounds(similarity):
    assert RetrievedSection(title="Payslips", text="Where to find them.", similarity=similarity).similarity == similarity


@pytest.mark.parametrize("similarity", [-0.01, 1.01])
def test_rejects_similarity_outside_zero_to_one(similarity):
    with pytest.raises(ValidationError):
        RetrievedSection(title="Payslips", text="Where to find them.", similarity=similarity)


@pytest.mark.parametrize("field", ["title", "text"])
def test_rejects_empty_title_or_text(field):
    values = {"title": "Payslips", "text": "Where to find them.", "similarity": 0.5} | {field: ""}

    with pytest.raises(ValidationError):
        RetrievedSection(**values)
