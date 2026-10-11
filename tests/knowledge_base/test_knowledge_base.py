"""Seam 2: the knowledge base public interface, with in-memory Chroma and fake embeddings."""

import chromadb
import pytest
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_openai import OpenAIEmbeddings

from orchestration.area import Area
from orchestration.config import load_settings
from orchestration.knowledge_base import build_retrieve, index_all_areas
from orchestration.section import RetrievedSection
from tests.keys import requires_keys

# Test fixture written for these tests, not an Atalaya Document.
SAMPLE_DOCUMENTS = {
    Area.HR: ("Annual leave", "Parental leave", "Performance reviews"),
    Area.TECH: ("VPN access", "Password reset", "Dashboard exports"),
    Area.FINANCE: ("Payslips", "Corporate cards", "Travel allowances"),
}


def write_sample_documents(data_dir):
    for area, titles in SAMPLE_DOCUMENTS.items():
        area_dir = data_dir / f"{area.value}_docs"
        area_dir.mkdir(parents=True)
        sections = "\n\n".join(f"## {title}\n\nEverything about {title.lower()}." for title in titles)
        (area_dir / "sample.md").write_text(f"# Sample {area.value} handbook\n\nVersion 1.0.\n\n{sections}\n")


def stored_ids(area: Area) -> list[str]:
    # Reads Chroma directly: stored ids are not part of the public interface.
    return chromadb.EphemeralClient().get_collection(f"knowledge_base_{area.value}").get()["ids"]


@pytest.fixture(autouse=True)
def empty_in_memory_chroma():
    """In-memory Chroma is shared within the process, so every test starts and ends empty."""
    client = chromadb.EphemeralClient()

    def clear():
        for collection in client.list_collections():
            client.delete_collection(collection.name)

    clear()
    yield
    clear()


@pytest.fixture
def data_dir(tmp_path):
    write_sample_documents(tmp_path)
    return tmp_path


def index(data_dir, embedding_model="fake-model", force=False):
    return index_all_areas(
        data_dir,
        embeddings=DeterministicFakeEmbedding(size=32),
        embedding_model=embedding_model,
        chunk_max_tokens=800,
        chunk_overlap_tokens=120,
        persist_directory=None,
        force=force,
    )


def test_indexing_stores_one_section_per_heading_under_deterministic_ids(data_dir):
    index(data_dir)

    assert sorted(stored_ids(Area.HR)) == sorted(f"hr:{title}" for title in SAMPLE_DOCUMENTS[Area.HR])


def test_a_split_section_stores_each_part_under_its_own_id(data_dir):
    long_body = " ".join(f"word{index}" for index in range(300))
    (data_dir / "hr_docs" / "sample.md").write_text(f"## Long topic\n\n{long_body}\n")

    index_all_areas(
        data_dir,
        embeddings=DeterministicFakeEmbedding(size=32),
        embedding_model="fake-model",
        chunk_max_tokens=60,
        chunk_overlap_tokens=15,
    )

    ids = stored_ids(Area.HR)
    assert len(ids) > 1
    assert sorted(ids) == sorted(f"hr:Long topic:{part}" for part in range(1, len(ids) + 1))


def test_first_run_indexes_every_area(data_dir):
    assert index(data_dir) == {area: "indexed" for area in Area}


def test_second_run_with_the_same_model_skips_every_area(data_dir):
    index(data_dir)

    assert index(data_dir) == {area: "skipped" for area in Area}
    assert len(stored_ids(Area.HR)) == 3


def test_indexing_with_a_different_embedding_model_is_refused(data_dir):
    index(data_dir, embedding_model="fake-model")

    with pytest.raises(ValueError, match="fake-model.*other-model"):
        index(data_dir, embedding_model="other-model")


def test_force_rebuilds_without_duplicates(data_dir):
    index(data_dir)

    assert index(data_dir, force=True) == {area: "indexed" for area in Area}
    assert len(stored_ids(Area.HR)) == 3


def test_force_rebuilds_with_a_new_embedding_model(data_dir):
    index(data_dir, embedding_model="fake-model")

    index(data_dir, embedding_model="other-model", force=True)

    assert index(data_dir, embedding_model="other-model") == {area: "skipped" for area in Area}


def build(area, top_k):
    return build_retrieve(area, top_k=top_k, embeddings=DeterministicFakeEmbedding(size=32), persist_directory=None)


def test_retrieve_returns_at_most_top_k_sections_titled_by_their_headings(data_dir):
    index(data_dir)
    retrieve = build(Area.FINANCE, top_k=2)

    sections = retrieve("When are payslips published?")

    assert len(sections) == 2
    assert all(isinstance(section, RetrievedSection) for section in sections)
    assert {section.title for section in sections} <= set(SAMPLE_DOCUMENTS[Area.FINANCE])
    assert all(section.text.lstrip().startswith(f"## {section.title}") for section in sections)


def test_retrieved_similarities_are_between_zero_and_one(data_dir):
    # Random fake vectors give some negative cosine similarities; they must come back clamped to 0.
    index(data_dir)
    retrieve = build(Area.TECH, top_k=3)

    for query in ("vpn", "password", "export", "unrelated words"):
        assert all(0.0 <= section.similarity <= 1.0 for section in retrieve(query))


# Test fixture with distinct topics, so a real embedding model has a clear best match.
REALISTIC_TECH_DOCUMENT = """# Sample tech handbook

Version 1.0.

## VPN access

Staff connect to the internal network from home through the corporate VPN client.
Install the client, sign in with your corporate account and approve the two-factor prompt.

## Password reset

Clients who forget their platform password use the "Forgot password" link on the login page.
A reset email arrives within five minutes and the link expires after one hour.

## Dashboard exports

Dashboards can be exported to CSV or PDF from the share menu.
Exports are limited to one hundred thousand rows.
"""


@pytest.mark.integration
@requires_keys("OPENAI_API_KEY")
def test_real_embeddings_retrieve_the_expected_section_first(tmp_path):
    settings = load_settings()
    data_dir = tmp_path / "data"
    for area in Area:
        (data_dir / f"{area.value}_docs").mkdir(parents=True)
        (data_dir / f"{area.value}_docs" / "sample.md").write_text(REALISTIC_TECH_DOCUMENT)
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model, api_key=settings.openai_api_key.get_secret_value()
    )
    persist_directory = tmp_path / ".chroma"

    index_all_areas(
        data_dir,
        embeddings=embeddings,
        embedding_model=settings.embedding_model,
        chunk_max_tokens=settings.chunk_max_tokens,
        chunk_overlap_tokens=settings.chunk_overlap_tokens,
        persist_directory=persist_directory,
    )
    retrieve = build_retrieve(
        Area.TECH, top_k=settings.retrieval_top_k, embeddings=embeddings, persist_directory=persist_directory
    )

    sections = retrieve("How do I connect to the internal network from home?")

    assert sections[0].title == "VPN access"
    assert sections[0].similarity > sections[-1].similarity


def test_retrieving_from_an_area_that_was_never_indexed_is_refused():
    with pytest.raises(ValueError, match="hr Knowledge Base"):
        build(Area.HR, top_k=3)


def test_force_keeps_the_old_knowledge_base_when_the_documents_cannot_be_read(data_dir):
    index(data_dir)
    for document in (data_dir / "hr_docs").glob("*.md"):
        document.unlink()

    with pytest.raises(ValueError, match="No Markdown Documents"):
        index(data_dir, force=True)

    assert len(stored_ids(Area.HR)) == 3
