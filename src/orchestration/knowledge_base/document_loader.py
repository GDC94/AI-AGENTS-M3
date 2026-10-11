"""Read the Markdown Documents of one Area."""

from pathlib import Path

from langchain_core.documents import Document


def load_area_documents(area_dir: Path) -> list[Document]:
    """Load every .md file in area_dir, in name order, with its file name as source."""
    paths = sorted(area_dir.glob("*.md"))
    if not paths:
        raise ValueError(f"No Markdown Documents found in {area_dir}")
    return [Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.name}) for path in paths]
