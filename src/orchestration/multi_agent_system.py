"""Composition: wire built Router, Specialists, Judge and ScorePublisher into answer_query.

This module holds wiring only; every prompt lives in its own package (ADR 0003).
"""

from collections.abc import Callable, Mapping
from typing import Any, TypedDict, get_args

from langchain_core.runnables import Runnable
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from orchestration.area import Area
from orchestration.observability import ScorePublisher
from orchestration.routing import Route, RouteTarget
from orchestration.section import RetrievedSection
from orchestration.specialists import OUT_OF_SCOPE_MESSAGE
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
    specialists: Mapping[Area, Callable[[str], Any]],
) -> CompiledStateGraph:
    """Route node, a conditional edge on Route.target, one node per Area and an out-of-scope node."""

    def route(state: SupportState) -> SupportState:
        return {"route": router.invoke(state["query"])}

    def reply_out_of_scope(state: SupportState) -> SupportState:
        return {"answer": OUT_OF_SCOPE_MESSAGE, "sections": [], "abstained": False}

    graph = StateGraph(SupportState)
    graph.add_node(ROUTE_NODE, route)
    for area in Area:
        graph.add_node(area.value, _placeholder_specialist_node(area))
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


def _placeholder_specialist_node(area: Area) -> Callable[[SupportState], SupportState]:
    # Replaced by the real Specialist node in ticket 04.
    def specialist_node(state: SupportState) -> SupportState:
        raise NotImplementedError(f"The '{area.value}' Specialist node is not implemented yet")

    return specialist_node


def build_answer_query(
    graph: CompiledStateGraph,
    judge: Runnable,
    publisher: ScorePublisher,
) -> Callable[[str], SupportAnswer]:
    """Return answer_query: run the graph inside one Langfuse trace and publish the abstained score."""

    def answer_query(query: str) -> SupportAnswer:
        langfuse = get_client()
        with langfuse.start_as_current_observation(name="answer_query", as_type="span") as span:
            state = graph.invoke({"query": query}, config={"callbacks": [CallbackHandler()]})
            trace_id = span.trace_id
        publisher.publish_abstention(trace_id, state["abstained"])
        return SupportAnswer(
            query=query,
            route=state["route"],
            answer=state["answer"],
            sections=state["sections"],
            abstained=state["abstained"],
            trace_id=trace_id,
        )

    return answer_query
