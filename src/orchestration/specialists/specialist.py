"""The Specialist: a deterministic chain per Area (ADR 0002), built from one shared prompt."""

from collections.abc import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from orchestration.area import AREA_DESCRIPTIONS, Area
from orchestration.section import RetrievedSection, format_sections_for_prompt

Retrieve = Callable[[str], list[RetrievedSection]]
Specialist = Callable[[str], "SpecialistReply"]

NO_INFORMATION_MESSAGE = (
    "Lo siento, la documentación disponible no cubre tu consulta. "
    "Te recomendamos contactar directamente al equipo correspondiente."
)

SPECIALIST_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are the {area} Specialist of Atalaya Data's support team.
The {area} Area: {area_description}

Answer the Query using only the Sections below, taken from the {area} Knowledge Base.
- Do not add facts that are not in the Sections. If they only answer part of the Query, \
answer that part and say what is not covered.
- Cite the title of every Section you use in square brackets, exactly as written, for example [Annual leave].
- Answer in the same language as the Query.

Sections:
{sections}""",
        ),
        ("human", "{query}"),
    ]
)


class SpecialistReply(BaseModel):
    answer: str
    sections: list[RetrievedSection]
    abstained: bool


def build_specialist(
    area: Area,
    retrieve: Retrieve,
    chat_model: BaseChatModel,
    threshold: float,
) -> Specialist:
    """Retrieve, drop Sections under the threshold, then abstain or answer from the survivors.

    An Abstention never calls the model; a grounded Answer calls it exactly once.
    """
    prompt = SPECIALIST_PROMPT.partial(area=area.value, area_description=AREA_DESCRIPTIONS[area])
    draft = prompt | chat_model | StrOutputParser()

    def reply_to_query(query: str) -> SpecialistReply:
        surviving = [section for section in retrieve(query) if section.similarity >= threshold]
        if not surviving:
            return SpecialistReply(answer=NO_INFORMATION_MESSAGE, sections=[], abstained=True)
        text = draft.invoke({"query": query, "sections": format_sections_for_prompt(surviving)})
        return SpecialistReply(answer=text, sections=surviving, abstained=False)

    return reply_to_query
