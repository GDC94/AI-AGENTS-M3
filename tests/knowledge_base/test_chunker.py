import tiktoken
from langchain_core.documents import Document

from orchestration.knowledge_base.chunker import split_into_sections

SAMPLE = """# Sample handbook

Version 1.0. A short introduction that is not a Section.

## Payslips

Payslips are published on the first working day of each month.

## Corporate cards

Corporate cards have a monthly limit.

## Travel allowances

Travel allowances are reimbursed within ten days.
"""


def token_count(text: str) -> int:
    return len(tiktoken.get_encoding("cl100k_base").encode(text))


def test_one_section_per_second_level_heading():
    sections = split_into_sections([Document(page_content=SAMPLE)], max_tokens=800, overlap_tokens=120)

    assert [section.metadata["title"] for section in sections] == [
        "Payslips",
        "Corporate cards",
        "Travel allowances",
    ]


def test_heading_is_kept_inside_the_section_text():
    sections = split_into_sections([Document(page_content=SAMPLE)], max_tokens=800, overlap_tokens=120)

    assert sections[0].page_content.startswith("## Payslips")
    assert "first working day" in sections[0].page_content


def test_section_above_the_token_maximum_is_split_with_overlap():
    words = " ".join(f"word{index}" for index in range(300))
    document = Document(page_content=f"## Long topic\n\n{words}\n")

    parts = split_into_sections([document], max_tokens=60, overlap_tokens=15)

    assert len(parts) > 1
    assert all(part.metadata["title"] == "Long topic" for part in parts)
    assert all(part.page_content.startswith("## Long topic\n") for part in parts)
    assert all(token_count(part.page_content) <= 60 for part in parts)
    for previous, following in zip(parts, parts[1:]):
        last_word = previous.page_content.split()[-1]
        assert last_word in following.page_content.split()
