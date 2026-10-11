"""The Judge: a zero-shot prompt plus strict structured output (ADR 0003)."""

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda

from orchestration.judging.quality_verdict import QualityVerdict
from orchestration.section import RetrievedSection

JUDGE_SYSTEM_PROMPT = """You are the Judge of a support system for Atalaya Data, a SaaS company whose \
platform serves public administrations. A Specialist answered a Query using only the Sections below, \
taken from its Knowledge Base. Rate that Answer.

Give four whole-number Ratings from 1 (worst) to 10 (best):
- relevance: the Answer addresses what the Query asks.
- completeness: the Answer covers everything the Sections say that the Query needs.
- accuracy: every claim in the Answer is supported by the Sections; penalise anything invented or contradicted.
- quality: your overall Rating of the Answer.

Rules:
- Judge against the Sections, not against your own knowledge.
- Write the reason in Spanish, in one to three sentences, whatever the language of the Query.

Explain your reasoning in the reason first, then give the Ratings."""

JUDGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", JUDGE_SYSTEM_PROMPT),
        ("human", "Query:\n{query}\n\nAnswer:\n{answer}\n\nSections used:\n{sections}"),
    ]
)


def build_judge(chat_model: BaseChatModel) -> Runnable[dict, QualityVerdict]:
    """Build the Judge runnable: {"query", "answer", "sections"} in, QualityVerdict out."""
    format_input = RunnableLambda(_format_judge_input)
    return format_input | JUDGE_PROMPT | chat_model.with_structured_output(QualityVerdict, method="json_schema", strict=True)


def _format_judge_input(judge_input: dict) -> dict:
    return judge_input | {"sections": _format_sections(judge_input["sections"])}


def _format_sections(sections: list[RetrievedSection]) -> str:
    return "\n\n---\n\n".join(f"Section title: {section.title}\n{section.text}" for section in sections)
