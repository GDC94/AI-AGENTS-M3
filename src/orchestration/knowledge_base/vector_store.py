"""Chroma collections: one per Area, cosine distance, embedding model in the metadata."""

from collections.abc import Callable
from pathlib import Path

import chromadb
from chromadb.api import ClientAPI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from orchestration.area import Area
from orchestration.knowledge_base.chunker import TITLE_KEY
from orchestration.section import RetrievedSection

EMBEDDING_MODEL_KEY = "embedding_model"


def name_collection(area: Area) -> str:
    # Chroma requires at least three characters, so the bare Area value is not enough.
    return f"knowledge_base_{area.value}"


def open_client(persist_directory: Path | str | None) -> ClientAPI:
    """A persistent client for a directory, or the in-memory client when None."""
    if persist_directory is None:
        return chromadb.EphemeralClient()
    return chromadb.PersistentClient(path=str(persist_directory))


def collection_exists(client: ClientAPI, area: Area) -> bool:
    return name_collection(area) in {collection.name for collection in client.list_collections()}


def open_vector_store(client: ClientAPI, area: Area, embeddings: Embeddings, embedding_model: str) -> Chroma:
    """Open the Area's collection, creating it with cosine distance and the model name if missing."""
    return Chroma(
        client=client,
        collection_name=name_collection(area),
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine", EMBEDDING_MODEL_KEY: embedding_model},
    )


def build_retrieve(
    area: Area,
    top_k: int,
    embeddings: Embeddings,
    persist_directory: Path | str | None = None,
) -> Callable[[str], list[RetrievedSection]]:
    """Build the retrieval callable for one Area: Query text in, top-k RetrievedSections out.

    No threshold is applied here, so calibration can see raw Similarities.
    """
    client = open_client(persist_directory)
    # Opening a missing collection would silently create an empty one with Chroma's default L2 distance.
    if not collection_exists(client, area):
        raise ValueError(f"The {area.value} Knowledge Base has not been indexed; run index_all_areas first")
    store = Chroma(client=client, collection_name=name_collection(area), embedding_function=embeddings)

    def retrieve(query: str) -> list[RetrievedSection]:
        results = store.similarity_search_with_score(query, k=top_k)
        return [_to_retrieved_section(document, distance) for document, distance in results]

    return retrieve


def _to_retrieved_section(document: Document, cosine_distance: float) -> RetrievedSection:
    """The only place a LangChain Document becomes a RetrievedSection.

    Similarity is 1 - cosine distance (the same value LangChain calls relevance). It falls below 0
    for vectors pointing away from the Query, so it is clamped to [0, 1]; computing it here avoids
    LangChain's out-of-range warning on every such search.
    """
    return RetrievedSection(
        title=document.metadata[TITLE_KEY],
        text=document.page_content,
        similarity=min(1.0, max(0.0, 1.0 - cosine_distance)),
    )
