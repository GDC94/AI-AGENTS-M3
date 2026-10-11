"""Knowledge Bases: index Documents and retrieve Sections. Public interface: two functions."""

from orchestration.knowledge_base.indexer import index_all_areas
from orchestration.knowledge_base.vector_store import build_retrieve

__all__ = ["build_retrieve", "index_all_areas"]
