import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"

# Assignment word -> CONTEXT.md term (PLAN.md section 1, mapping table).
ASSIGNMENT_TO_PROJECT_TERMS = [
    ("Orchestrator", "Router"),
    ("RAG agent", "Specialist"),
    ("Evaluator", "Judge"),
    ("category", "Area"),
    ("chunk", "Section"),
]


def read_readme() -> str:
    return README_PATH.read_text()


def read_section(heading: str) -> str:
    match = re.search(rf"^## {heading}\n(.*?)(?=^## |\Z)", read_readme(), flags=re.MULTILINE | re.DOTALL)
    assert match, f"README has no '## {heading}' section"
    return match.group(1)


@pytest.mark.parametrize(("assignment_word", "project_term"), ASSIGNMENT_TO_PROJECT_TERMS)
def test_mapping_table_pairs_each_assignment_word_with_its_project_term(assignment_word, project_term):
    table_rows = [line for line in read_section("Assignment vocabulary").splitlines() if line.startswith("|")]

    assert any(assignment_word.lower() in row.lower() and f"**{project_term}**" in row for row in table_rows)


def test_each_known_limitation_points_to_the_adr_or_plan_section_that_explains_it():
    limitations = [line for line in read_section("Known limitations").splitlines() if line.startswith("- ")]

    assert len(limitations) >= 4
    for limitation in limitations:
        assert re.search(r"docs/adr/\d{4}-|PLAN\.md", limitation), limitation


def test_every_linked_repository_file_exists():
    linked_paths = re.findall(r"\]\((?!https?://)([^)#]+)", read_readme())

    assert "CONTEXT.md" in linked_paths
    for path in linked_paths:
        assert (REPO_ROOT / path).exists(), path
