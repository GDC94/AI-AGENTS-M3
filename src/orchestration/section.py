"""The only shape of Section seen outside the knowledge base package."""

from pydantic import BaseModel, Field


class RetrievedSection(BaseModel):
    """A Section returned by retrieval, with its Similarity to the Query."""

    title: str = Field(min_length=1)
    text: str = Field(min_length=1)
    similarity: float = Field(ge=0.0, le=1.0)
