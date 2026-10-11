import time
from datetime import UTC, datetime, timedelta

import pytest
from langchain_core.runnables import RunnableLambda

from orchestration.area import Area
from orchestration.config import load_settings
from orchestration.llm import build_chat_model
from orchestration.multi_agent_system import build_answer_query, build_graph
from orchestration.observability import LangfuseScorePublisher, init_langfuse
from orchestration.routing import Route, build_router
from orchestration.specialists import OUT_OF_SCOPE_MESSAGE
from tests.doubles import RecordingScorePublisher
from tests.keys import requires_keys


@pytest.fixture(autouse=True)
def langfuse_disabled(monkeypatch):
    """Unit tests never reach Langfuse: without keys the client is disabled."""
    for var in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_HOST"):
        monkeypatch.delenv(var, raising=False)


def router_returning(target: str) -> RunnableLambda:
    return RunnableLambda(lambda query: Route(reasoning=f"fixed route to {target}", target=target))


def failing_double(name: str):
    def call(*args, **kwargs):
        raise AssertionError(f"{name} must not be called")

    return call


def build_answer_query_with(router, publisher):
    specialists = {area: failing_double(f"{area} Specialist") for area in Area}
    judge = RunnableLambda(failing_double("Judge"))
    return build_answer_query(build_graph(router, specialists), judge, publisher)


def test_out_of_scope_query_gets_the_fixed_message_without_specialist_or_judge():
    publisher = RecordingScorePublisher()
    answer_query = build_answer_query_with(router_returning("out_of_scope"), publisher)

    result = answer_query("Who won the match yesterday?")

    assert result.query == "Who won the match yesterday?"
    assert result.route.target == "out_of_scope"
    assert result.answer == OUT_OF_SCOPE_MESSAGE
    assert result.sections == []
    assert result.abstained is False
    assert result.verdict is None
    assert publisher.abstentions == [(result.trace_id, False)]


@pytest.mark.parametrize("area", list(Area))
def test_each_area_route_reaches_its_own_node(area):
    publisher = RecordingScorePublisher()
    answer_query = build_answer_query_with(router_returning(area.value), publisher)

    with pytest.raises(NotImplementedError, match=f"'{area.value}' Specialist node"):
        answer_query("Any question for this Area")


@pytest.mark.integration
@requires_keys("OPENAI_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY")
def test_off_topic_query_produces_a_langfuse_trace_with_abstained_score():
    settings = load_settings()
    langfuse = init_langfuse(
        settings.langfuse_public_key.get_secret_value(),
        settings.langfuse_secret_key.get_secret_value(),
        settings.langfuse_host,
    )
    router = build_router(
        build_chat_model(
            settings.router_model,
            api_key=settings.openai_api_key.get_secret_value(),
            temperature=settings.llm_temperature,
        )
    )
    specialists = {area: failing_double(f"{area} Specialist") for area in Area}
    answer_query = build_answer_query(
        build_graph(router, specialists),
        RunnableLambda(failing_double("Judge")),
        LangfuseScorePublisher(langfuse),
    )

    result = answer_query("¿Quién ganó el partido de fútbol de ayer?")
    langfuse.flush()

    assert result.route.target == "out_of_scope"
    assert result.answer == OUT_OF_SCOPE_MESSAGE
    observations, scores = fetch_observations_and_scores(langfuse, result.trace_id)
    abstained = [score for score in scores if score.name == "abstained"]
    assert len(abstained) == 1
    assert abstained[0].value is False
    assert result.route.reasoning in " ".join(str(observation.output) for observation in observations)


def fetch_observations_and_scores(langfuse, trace_id, attempts=15, delay_seconds=2.0):
    """Poll Langfuse until the trace's observations and scores are readable.

    Organizations created after 2026-09-16 cannot use the legacy traces API, so this
    reads through the v2 observations and v3 scores endpoints.
    """
    since = datetime.now(UTC) - timedelta(hours=1)
    for _ in range(attempts):
        observations = langfuse.api.observations.get_many(
            trace_id=trace_id, from_start_time=since, fields="core,basic,io"
        ).data
        scores = langfuse.api.scores_v3.get_many_v3(trace_id=trace_id).data
        if observations and scores:
            return observations, scores
        time.sleep(delay_seconds)
    pytest.fail(f"observations and scores of trace {trace_id} not readable from Langfuse")
