"""Split Documents into Sections. "Chunk" is the splitter's word and stays in this module."""

import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

TITLE_KEY = "title"
PART_KEY = "part"
_ENCODING = "cl100k_base"


def split_into_sections(documents: list[Document], max_tokens: int, overlap_tokens: int) -> list[Document]:
    """One Section per second-level heading, with the heading kept inside the text.

    Text before the first second-level heading (document title, version line, introduction)
    is not a Section and is dropped. A Section above max_tokens is split into parts with
    overlap; every part repeats the heading so it stays findable on its own and carries its
    1-based part number in the metadata.
    """
    heading_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", TITLE_KEY)], strip_headers=False)
    sections: list[Document] = []
    for document in documents:
        for part in heading_splitter.split_text(document.page_content):
            if TITLE_KEY not in part.metadata:
                continue
            metadata = {**document.metadata, **part.metadata}
            sections.extend(_split_oversize(part.page_content, metadata, max_tokens, overlap_tokens))
    return sections


def _split_oversize(text: str, metadata: dict, max_tokens: int, overlap_tokens: int) -> list[Document]:
    if _count_tokens(text) <= max_tokens:
        return [Document(page_content=text, metadata=metadata)]
    heading, _, body = text.partition("\n")
    prefix = f"{heading.rstrip()}\n\n"
    body_budget = max_tokens - _count_tokens(prefix)
    chunk_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name=_ENCODING, chunk_size=body_budget, chunk_overlap=min(overlap_tokens, body_budget - 1)
    )
    return [
        Document(page_content=prefix + chunk, metadata={**metadata, PART_KEY: part})
        for part, chunk in enumerate(chunk_splitter.split_text(body.strip()), start=1)
    ]


def _count_tokens(text: str) -> int:
    return len(tiktoken.get_encoding(_ENCODING).encode(text))
