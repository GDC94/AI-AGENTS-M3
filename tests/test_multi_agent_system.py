import time
from datetime import UTC, datetime, timedelta

import pytest
from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAIEmbeddings

from orchestration.area import AREA_DESCRIPTIONS, Area
from orchestration.config import load_settings
from orchestration.knowledge_base import build_retrieve, index_all_areas
from orchestration.llm import build_chat_model
from orchestration.multi_agent_system import build_answer_query, build_graph, build_specialists
from orchestration.observability import LangfuseScorePublisher, init_langfuse
from orchestration.routing import Route, build_router
from orchestration.section import RetrievedSection
from orchestration.specialists import NO_INFORMATION_MESSAGE, OUT_OF_SCOPE_MESSAGE
from tests.doubles import RecordingFakeChatModel, RecordingScorePublisher
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


THRESHOLD = 0.42


def section(title: str, similarity: float) -> RetrievedSection:
    # The text deliberately omits the title, so tests can tell whether the title reaches the model.
    return RetrievedSection(title=title, text=f"Section body with similarity {similarity}.", similarity=similarity)


def retrieve_returning(*sections: RetrievedSection):
    return lambda query: list(sections)


def answer_query_for_area(area: Area, retrieve, chat_model, publisher):
    retrieve_by_area = {other: failing_double(f"{other} retrieval") for other in Area} | {area: retrieve}
    specialists = build_specialists(retrieve_by_area, chat_model, THRESHOLD)
    judge = RunnableLambda(failing_double("Judge"))
    return build_answer_query(build_graph(router_returning(area.value), specialists), judge, publisher)


@pytest.mark.parametrize("area", list(Area))
def test_no_section_above_the_threshold_gives_an_abstention_without_calling_the_model(area):
    chat_model = RecordingFakeChatModel(responses=["must not be used"])
    publisher = RecordingScorePublisher()
    retrieve = retrieve_returning(section("Annual leave", 0.30), section("Parental leave", 0.41))
    answer_query = answer_query_for_area(area, retrieve, chat_model, publisher)

    result = answer_query("How do I request a sabbatical?")

    assert result.answer == NO_INFORMATION_MESSAGE
    assert result.sections == []
    assert result.abstained is True
    assert result.verdict is None
    assert chat_model.received == []
    assert publisher.abstentions == [(result.trace_id, True)]


@pytest.mark.parametrize("area", list(Area))
def test_surviving_sections_ground_one_model_call_and_weaker_ones_are_dropped(area):
    chat_model = RecordingFakeChatModel(responses=["You get 22 days of annual leave [Holiday entitlement]."])
    publisher = RecordingScorePublisher()
    covered, weak = section("Holiday entitlement", 0.80), section("Parental leave", 0.30)
    answer_query = answer_query_for_area(area, retrieve_returning(covered, weak), chat_model, publisher)

    result = answer_query("How many days of annual leave do I get?")

    assert result.answer == "You get 22 days of annual leave [Holiday entitlement]."
    assert result.sections == [covered]
    assert result.abstained is False
    assert len(chat_model.received) == 1
    model_input = " ".join(message.content for message in chat_model.received[0])
    assert covered.title in model_input
    assert covered.text in model_input
    assert weak.text not in model_input
    assert "How many days of annual leave do I get?" in model_input
    assert AREA_DESCRIPTIONS[area] in model_input
    assert publisher.abstentions == [(result.trace_id, False)]


def test_a_section_exactly_at_the_threshold_is_kept():
    chat_model = RecordingFakeChatModel(responses=["Grounded answer."])
    at_threshold = section("Annual leave", THRESHOLD)
    answer_query = answer_query_for_area(
        Area.HR, retrieve_returning(at_threshold), chat_model, RecordingScorePublisher()
    )

    result = answer_query("How many days of annual leave do I get?")

    assert result.sections == [at_threshold]
    assert result.abstained is False


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


# Test fixture with distinct HR topics, not an Atalaya Document.
HR_SAMPLE_DOCUMENT = """# Sample HR handbook

Version 1.0.

## Annual leave

Staff get 22 working days of annual leave per calendar year.
Leave is requested in the HR portal at least two weeks in advance and approved by the line manager.

## Parental leave

Parents get 16 weeks of paid parental leave, which can start up to two weeks before the birth.

## Performance reviews

Performance reviews take place every March and September with the line manager.
"""


@pytest.mark.integration
@requires_keys("OPENAI_API_KEY")
def test_real_specialist_answers_a_covered_query_and_abstains_on_an_uncovered_one(tmp_path):
    settings = load_settings()
    api_key = settings.openai_api_key.get_secret_value()
    data_dir = tmp_path / "data"
    for area in Area:
        (data_dir / f"{area.value}_docs").mkdir(parents=True)
        (data_dir / f"{area.value}_docs" / "sample.md").write_text(HR_SAMPLE_DOCUMENT)
    embeddings = OpenAIEmbeddings(model=settings.embedding_model, api_key=api_key)
    persist_directory = tmp_path / ".chroma"
    index_all_areas(
        data_dir,
        embeddings=embeddings,
        embedding_model=settings.embedding_model,
        chunk_max_tokens=settings.chunk_max_tokens,
        chunk_overlap_tokens=settings.chunk_overlap_tokens,
        persist_directory=persist_directory,
    )
    retrieve_by_area = {
        area: build_retrieve(area, settings.retrieval_top_k, embeddings, persist_directory) for area in Area
    }
    chat_model = build_chat_model(settings.specialist_model, api_key=api_key, temperature=settings.llm_temperature)
    specialists = build_specialists(retrieve_by_area, chat_model, settings.similarity_threshold)
    answer_query = build_answer_query(
        build_graph(router_returning("hr"), specialists),
        RunnableLambda(failing_double("Judge")),
        RecordingScorePublisher(),
    )

    covered = answer_query("How many days of annual leave do I get per year?")
    uncovered = answer_query("Can I bring my dog to the office?")

    assert covered.abstained is False
    assert covered.sections[0].title == "Annual leave"
    assert "22" in covered.answer
    assert "[Annual leave]" in covered.answer
    assert uncovered.abstained is True
    assert uncovered.answer == NO_INFORMATION_MESSAGE
