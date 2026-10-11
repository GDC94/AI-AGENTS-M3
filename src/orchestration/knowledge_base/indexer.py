"""Index every Area's Documents into its Knowledge Base."""

from pathlib import Path
from typing import Literal

from chromadb.api import ClientAPI
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from orchestration.area import Area
from orchestration.knowledge_base.chunker import PART_KEY, TITLE_KEY, split_into_sections
from orchestration.knowledge_base.document_loader import load_area_documents
from orchestration.knowledge_base.vector_store import (
    EMBEDDING_MODEL_KEY,
    collection_exists,
    collection_name,
    open_client,
    open_vector_store,
)

IndexOutcome = Literal["indexed", "skipped"]


def index_all_areas(
    data_dir: Path,
    embeddings: Embeddings,
    embedding_model: str,
    chunk_max_tokens: int,
    chunk_overlap_tokens: int,
    persist_directory: Path | str | None = None,
    force: bool = False,
) -> dict[Area, IndexOutcome]:
    """Index the Documents in data_dir/<area>_docs into one collection per Area.

    Returns what happened to each Area. An existing non-empty collection built with the same
    embedding model is skipped; one built with another model is an error; force deletes and
    rebuilds every collection.
    """
    client = open_client(persist_directory)
    outcomes: dict[Area, IndexOutcome] = {}
    for area in Area:
        if not _needs_indexing(client, area, embedding_model, force):
            outcomes[area] = "skipped"
            continue
        # Read and split before deleting anything, so a failure keeps the old Knowledge Base.
        documents = load_area_documents(data_dir / f"{area.value}_docs")
        sections = split_into_sections(documents, chunk_max_tokens, chunk_overlap_tokens)
        if force and collection_exists(client, area):
            client.delete_collection(collection_name(area))
        ids = [_section_id(area, section) for section in sections]
        open_vector_store(client, area, embeddings, embedding_model).add_documents(sections, ids=ids)
        outcomes[area] = "indexed"
    return outcomes


def _needs_indexing(client: ClientAPI, area: Area, embedding_model: str, force: bool) -> bool:
    """False when the collection already holds Sections from the same embedding model."""
    if force or not collection_exists(client, area):
        return True
    collection = client.get_collection(collection_name(area))
    stored_model = (collection.metadata or {}).get(EMBEDDING_MODEL_KEY)
    if stored_model != embedding_model:
        raise ValueError(
            f"The {area.value} Knowledge Base was built with embedding model {stored_model!r}, "
            f"not {embedding_model!r}; rebuild it with force=True"
        )
    return collection.count() == 0


def _section_id(area: Area, section: Document) -> str:
    """Deterministic id from the Area and the Section title, plus the part number of a split Section."""
    section_id = f"{area.value}:{section.metadata[TITLE_KEY]}"
    if PART_KEY in section.metadata:
        section_id += f":{section.metadata[PART_KEY]}"
    return section_id
