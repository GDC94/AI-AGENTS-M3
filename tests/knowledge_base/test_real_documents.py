"""The real Documents in data/ split into enough Sections to make retrieval meaningful."""

from pathlib import Path

import pytest

from orchestration.area import Area
from orchestration.config import Settings
from orchestration.knowledge_base.chunker import split_into_sections
from orchestration.knowledge_base.document_loader import load_area_documents

DATA_DIR = Path("data")
MIN_SECTIONS_PER_KNOWLEDGE_BASE = 50


@pytest.mark.parametrize("area", list(Area))
def test_knowledge_base_has_more_than_fifty_sections(area):
    documents = load_area_documents(DATA_DIR / f"{area.value}_docs")

    sections = split_into_sections(
        documents,
        Settings.model_fields["chunk_max_tokens"].default,
        Settings.model_fields["chunk_overlap_tokens"].default,
    )

    assert len(sections) > MIN_SECTIONS_PER_KNOWLEDGE_BASE, f"{area.value}: {len(sections)} Sections"
