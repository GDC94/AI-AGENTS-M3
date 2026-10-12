"""The only shape of Section seen outside the knowledge base package."""

from pydantic import BaseModel, Field


class RetrievedSection(BaseModel):
    """A Section returned by retrieval, with its Similarity to the Query."""

    title: str = Field(min_length=1)
    text: str = Field(min_length=1)
    similarity: float = Field(ge=0.0, le=1.0)


def format_sections_for_prompt(sections: list[RetrievedSection]) -> str:
    """Each Section with its title stated explicitly, so citations never depend on the text format.

    Shared by the Specialist and the Judge, so the Judge reads the Sections exactly as the Specialist saw them.
    """
    return "\n\n---\n\n".join(f"Section title: {section.title}\n{section.text}" for section in sections)
