"""Sample Document and indexing helper shared by the integration tests."""

from langchain_openai import OpenAIEmbeddings

from orchestration.area import Area
from orchestration.knowledge_base import build_retrieve, index_all_areas

# Test fixture with distinct HR topics, not an Atalaya Document.
HR_SAMPLE_DOCUMENT = """# Sample HR handbook

Version 1.0.

## Annual leave

Staff get 22 working days of annual leave per calendar year.
Leave is requested in the HR portal at least two weeks in advance and approved by the line manager.

## Parental leave

Parents get 16 weeks of paid parental leave, which can start up to two weeks before the birth.

## Performance reviews

Performance reviews take place every March and September with the line manager.
"""


def index_sample_document_for_every_area(settings, api_key, tmp_path):
    """Index HR_SAMPLE_DOCUMENT under every Area in a temporary Chroma and return the retrieve function per Area."""
    data_dir = tmp_path / "data"
    for area in Area:
        (data_dir / f"{area.value}_docs").mkdir(parents=True)
        (data_dir / f"{area.value}_docs" / "sample.md").write_text(HR_SAMPLE_DOCUMENT)
    embeddings = OpenAIEmbeddings(model=settings.embedding_model, api_key=api_key)
    persist_directory = tmp_path / ".chroma"
    index_all_areas(
        data_dir,
        embeddings=embeddings,
        embedding_model=settings.embedding_model,
        chunk_max_tokens=settings.chunk_max_tokens,
        chunk_overlap_tokens=settings.chunk_overlap_tokens,
        persist_directory=persist_directory,
    )
    return {area: build_retrieve(area, settings.retrieval_top_k, embeddings, persist_directory) for area in Area}
