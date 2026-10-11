"""The Router: a zero-shot prompt plus strict structured output (ADR 0003)."""

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from orchestration.area import AREA_DESCRIPTIONS
from orchestration.routing.route import Route

_AREA_LINES = "\n".join(f"- {area.value}: {description}" for area, description in AREA_DESCRIPTIONS.items())

ROUTER_SYSTEM_PROMPT = f"""You route support Queries for Atalaya Data, a SaaS company whose platform \
integrates, analyses and displays data for public administrations. Queries come from Clients \
(users at customer organisations) and from Staff (Atalaya employees and consultants).

Choose exactly one target:
{_AREA_LINES}
- out_of_scope: the Query is not about Atalaya at all, so no Area can resolve it.

Rules:
- A topic belongs to the Area whose staff act to resolve the request, not the Area the topic sounds like.
- If the Query asks for two things, choose the Area that resolves the main request: the first \
concrete action someone would have to take.
- Choose an Area even when you doubt its documentation covers the Query; out_of_scope is only \
for Queries unrelated to Atalaya.
- Queries may be written in any language.

Explain your reasoning in one or two sentences, then give the target."""

ROUTER_PROMPT = ChatPromptTemplate.from_messages(
    [("system", ROUTER_SYSTEM_PROMPT.replace("{", "{{").replace("}", "}}")), ("human", "{query}")]
)


def build_router(chat_model: BaseChatModel) -> Runnable[str, Route]:
    """Build the Router runnable: Query text in, Route out."""
    return ROUTER_PROMPT | chat_model.with_structured_output(Route, method="json_schema", strict=True)
