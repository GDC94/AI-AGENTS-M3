"""Composition: wire built Router, Specialists, Judge and ScorePublisher into answer_query.

This module holds wiring only; every prompt lives in its own package (ADR 0003).
"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, get_args

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_openai import OpenAIEmbeddings
from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from orchestration.area import Area
from orchestration.config import load_settings
from orchestration.judging import build_judge
from orchestration.knowledge_base import build_retrieve, index_all_areas
from orchestration.llm import build_chat_model
from orchestration.observability import LangfuseScorePublisher, ScorePublisher, init_langfuse
from orchestration.routing import Route, RouteTarget, build_router
from orchestration.section import RetrievedSection
from orchestration.specialists import OUT_OF_SCOPE_MESSAGE, Retrieve, Specialist, build_specialist
from orchestration.support_answer import SupportAnswer

ROUTE_NODE = "route"
OUT_OF_SCOPE_NODE = "out_of_scope"


class SupportState(TypedDict, total=False):
    query: str
    route: Route
    sections: list[RetrievedSection]
    answer: str
    abstained: bool


def build_graph(
    router: Runnable[str, Route],
    specialists: Mapping[Area, Specialist],
) -> CompiledStateGraph:
    """Route node, a conditional edge on Route.target, one node per Area and an out-of-scope node."""

    def route(state: SupportState) -> SupportState:
        return {"route": router.invoke(state["query"])}

    def reply_out_of_scope(state: SupportState) -> SupportState:
        return {"answer": OUT_OF_SCOPE_MESSAGE, "sections": [], "abstained": False}

    graph = StateGraph(SupportState)
    graph.add_node(ROUTE_NODE, route)
    for area in Area:
        graph.add_node(area.value, _specialist_node(specialists[area]))
        graph.add_edge(area.value, END)
    graph.add_node(OUT_OF_SCOPE_NODE, reply_out_of_scope)
    graph.add_edge(START, ROUTE_NODE)
    # Node names equal Route targets; the explicit map makes compile() check every target has a node.
    graph.add_conditional_edges(
        ROUTE_NODE,
        lambda state: state["route"].target,
        {target: target for target in get_args(RouteTarget)},
    )
    graph.add_edge(OUT_OF_SCOPE_NODE, END)
    return graph.compile()


def _specialist_node(specialist: Specialist) -> Callable[[SupportState], SupportState]:
    def run_specialist(state: SupportState) -> SupportState:
        reply = specialist(state["query"])
        return {"answer": reply.answer, "sections": reply.sections, "abstained": reply.abstained}

    return run_specialist


def build_specialists(
    retrieve_by_area: Mapping[Area, Retrieve],
    chat_model: BaseChatModel,
    threshold: float,
) -> dict[Area, Specialist]:
    """One Specialist per Area, all sharing the chat model and the Similarity Threshold."""
    return {area: build_specialist(area, retrieve_by_area[area], chat_model, threshold) for area in Area}


def build_answer_query(
    graph: CompiledStateGraph,
    judge: Runnable,
    publisher: ScorePublisher,
) -> Callable[[str], SupportAnswer]:
    """Return answer_query: run the graph inside one Langfuse trace, publish `abstained`, judge grounded Answers."""

    def answer_query(query: str) -> SupportAnswer:
        langfuse = get_client()
        with langfuse.start_as_current_observation(name="answer_query", as_type="span") as span:
            state = graph.invoke({"query": query}, config={"callbacks": [CallbackHandler()]})
            trace_id = span.trace_id
            publisher.publish_abstention(trace_id, state["abstained"])
            verdict = None
            if _is_grounded(state):
                verdict = judge.invoke(
                    {"query": query, "answer": state["answer"], "sections": state["sections"]}
                )
                publisher.publish_quality_scores(trace_id, verdict)
        return SupportAnswer(
            query=query,
            route=state["route"],
            answer=state["answer"],
            sections=state["sections"],
            abstained=state["abstained"],
            verdict=verdict,
            trace_id=trace_id,
        )

    return answer_query


def _is_grounded(state: SupportState) -> bool:
    """Only a Specialist's grounded reply is judged: it has Sections and is not an Abstention."""
    return not state["abstained"] and bool(state["sections"])


@dataclass(frozen=True)
class SupportSystem:
    answer_query: Callable[[str], SupportAnswer]
    retrieve_by_area: dict[Area, Retrieve]
    langfuse: Langfuse


def build_support_system(
    data_dir: Path = Path("data"),
    persist_directory: Path = Path(".chroma"),
) -> SupportSystem:
    """Read Settings once, index the Documents (idempotent) and wire the whole system."""
    settings = load_settings()
    if settings.langfuse_public_key is None or settings.langfuse_secret_key is None:
        raise ValueError("LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY are required to trace the system")
    api_key = settings.openai_api_key.get_secret_value()
    embeddings = OpenAIEmbeddings(model=settings.embedding_model, api_key=api_key)
    index_all_areas(
        data_dir,
        embeddings,
        settings.embedding_model,
        settings.chunk_max_tokens,
        settings.chunk_overlap_tokens,
        persist_directory=persist_directory,
    )
    retrieve_by_area = {
        area: build_retrieve(area, settings.retrieval_top_k, embeddings, persist_directory) for area in Area
    }

    def make_chat_model(model_name: str) -> BaseChatModel:
        return build_chat_model(model_name, api_key=api_key, temperature=settings.llm_temperature)

    langfuse = init_langfuse(
        settings.langfuse_public_key.get_secret_value(),
        settings.langfuse_secret_key.get_secret_value(),
        settings.langfuse_host,
    )
    graph = build_graph(
        build_router(make_chat_model(settings.router_model)),
        build_specialists(retrieve_by_area, make_chat_model(settings.specialist_model), settings.similarity_threshold),
    )
    judge = build_judge(make_chat_model(settings.judge_model))
    answer_query = build_answer_query(graph, judge, LangfuseScorePublisher(langfuse))
    return SupportSystem(answer_query=answer_query, retrieve_by_area=retrieve_by_area, langfuse=langfuse)
