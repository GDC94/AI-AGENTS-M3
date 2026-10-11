import time
from types import SimpleNamespace
from datetime import UTC, datetime, timedelta

import pytest
from langchain_core.runnables import RunnableLambda

from orchestration.config import load_settings
from orchestration.judging import QualityVerdict
from orchestration.llm import build_chat_model
from orchestration.multi_agent_system import build_answer_query, build_graph, build_specialists
from orchestration.checks import TestQuery
from orchestration.observability import LangfuseScorePublisher, init_langfuse
from orchestration.observability.experiments import (
    adapt_check,
    build_check_evaluators,
    build_dataset_item,
    build_experiment_task,
    rebuild_test_query,
    run_validation_experiment,
    upload_test_queries,
)
from orchestration.routing import Route, build_router
from orchestration.section import RetrievedSection
from orchestration.support_answer import SupportAnswer
from tests.doubles import RecordingLangfuse
from tests.keys import requires_keys
from tests.samples import index_sample_document_for_every_area

def make_test_query(**overrides) -> TestQuery:
    fields = {
        "id": "q01", "query": "How many days of annual leave do I get?", "expected_area": "hr",
        "expected_section": "Annual leave", "asker": "staff", "type": "direct", "split": "validation",
    }
    return TestQuery(**(fields | overrides))


DIRECT = make_test_query()
FRONTIER = make_test_query(
    id="q02", query="When is my raise paid?", expected_area="finance",
    expected_section="Payroll dates", asker="client", type="frontier",
)
UNANSWERABLE = make_test_query(
    id="q03", query="Can I bring my dog to the office?", expected_section=None, type="unanswerable",
)
OUT_OF_SCOPE = make_test_query(
    id="q04", query="Who won the match yesterday?", expected_area="out_of_scope", expected_section=None,
    asker="client", type="out_of_scope",
)
# Sample Test Queries for the integration test; they match the sample HR Document, not the real data.
TEST_DATASET_NAME = "support-routing-validation-test"
VERDICT = QualityVerdict(quality=8, relevance=9, completeness=7, accuracy=10, reason="Respuesta fiel a la sección.")
DIRECT_SAMPLE = make_test_query(id="sample-direct", query="How many days of annual leave do I get per year?")
UNANSWERABLE_SAMPLE = make_test_query(
    id="sample-unanswerable", query="Can I bring my dog to the office?", expected_section=None, type="unanswerable",
)
OUT_OF_SCOPE_SAMPLE = make_test_query(
    id="sample-out-of-scope", query="Who won the football match yesterday?", expected_area="out_of_scope",
    expected_section=None, asker="client", type="out_of_scope",
)
ALL_TEST_QUERIES = [DIRECT, FRONTIER, UNANSWERABLE, OUT_OF_SCOPE]


def test_dataset_item_carries_the_query_as_input_and_the_expectation_as_expected_output():
    item = build_dataset_item(DIRECT)

    assert item["input"] == "How many days of annual leave do I get?"
    assert item["expected_output"] == {"area": "hr", "section": "Annual leave", "type": "direct"}


@pytest.mark.parametrize("test_query", ALL_TEST_QUERIES, ids=lambda test_query: test_query.type)
def test_a_dataset_item_rebuilds_the_test_query_without_loss(test_query):
    item = build_dataset_item(test_query)

    rebuilt = rebuild_test_query(
        input=item["input"], expected_output=item["expected_output"], metadata=item["metadata"]
    )

    assert rebuilt == test_query


def make_support_answer(abstained: bool = False) -> SupportAnswer:
    return SupportAnswer(
        query="irrelevant", route=Route(reasoning="fixed", target="hr"), answer="An answer.",
        sections=[], abstained=abstained, trace_id="trace-1",
    )


def evaluate(evaluator, test_query: TestQuery, answer: SupportAnswer):
    item = build_dataset_item(test_query)
    return evaluator(
        input=item["input"], output=answer, expected_output=item["expected_output"], metadata=item["metadata"]
    )


@pytest.mark.parametrize("verdict", [True, False])
def test_an_adapted_check_calls_the_check_and_names_its_boolean_as_an_evaluation(verdict):
    calls = []

    def recording_check(answer, test_query):
        calls.append((answer, test_query))
        return verdict

    answer = make_support_answer()
    evaluator = adapt_check("my_check", recording_check)

    evaluations = evaluate(evaluator, DIRECT, answer)

    assert calls == [(answer, DIRECT)]
    assert [(e.name, e.value, e.data_type) for e in evaluations] == [("my_check", verdict, "BOOLEAN")]


def test_an_adapted_check_gives_no_evaluation_where_the_check_does_not_apply():
    def failing_check(answer, test_query):
        raise AssertionError("the Check must not run")

    evaluator = adapt_check("my_check", failing_check, applies_to=lambda test_query: test_query.is_answerable)

    assert evaluate(evaluator, OUT_OF_SCOPE, make_support_answer()) == []


def names_evaluated(test_query: TestQuery) -> dict[str, bool]:
    answer = SupportAnswer(
        query=test_query.query, route=Route(reasoning="fixed", target="hr"), answer="An answer.",
        sections=[RetrievedSection(title="Annual leave", text="Body.", similarity=0.9)],
        abstained=False, trace_id="trace-1",
    )
    evaluations = [
        evaluation
        for evaluator in build_check_evaluators()
        for evaluation in evaluate(evaluator, test_query, answer)
    ]
    return {evaluation.name: evaluation.value for evaluation in evaluations}


def test_the_three_checks_apply_where_the_ticket_06_decision_says_they_do():
    assert names_evaluated(DIRECT) == {"check_routing_correct": True, "check_retrieval_hit": True, "check_abstained": False}
    assert names_evaluated(FRONTIER) == {"check_routing_correct": False, "check_retrieval_hit": False, "check_abstained": False}
    assert names_evaluated(UNANSWERABLE) == {"check_routing_correct": True, "check_abstained": False}
    assert names_evaluated(OUT_OF_SCOPE) == {"check_routing_correct": False}


def test_uploading_creates_the_dataset_and_one_item_per_test_query():
    langfuse = RecordingLangfuse()

    upload_test_queries(langfuse, "validation-set", ALL_TEST_QUERIES)

    assert langfuse.datasets == {"validation-set"}
    assert len(langfuse.items) == len(ALL_TEST_QUERIES)
    stored = {item["metadata"]["id"]: item for item in langfuse.items.values()}
    for test_query in ALL_TEST_QUERIES:
        expected = build_dataset_item(test_query)
        assert {key: stored[test_query.id][key] for key in expected} == expected
        assert stored[test_query.id]["dataset_name"] == "validation-set"


def test_uploading_twice_does_not_duplicate_items():
    langfuse = RecordingLangfuse()

    upload_test_queries(langfuse, "validation-set", ALL_TEST_QUERIES)
    upload_test_queries(langfuse, "validation-set", ALL_TEST_QUERIES)

    assert len(langfuse.items) == len(ALL_TEST_QUERIES)


def run_experiment_with(langfuse, answer_query):
    return run_validation_experiment(langfuse, "validation-set", "prompt v1", answer_query)


def test_the_experiment_runs_on_the_dataset_with_the_three_checks_and_flushes_at_the_end():
    langfuse = RecordingLangfuse()
    upload_test_queries(langfuse, "validation-set", [DIRECT])
    langfuse.calls.clear()

    result = run_experiment_with(langfuse, lambda query: make_support_answer())

    assert result is langfuse.experiment_result
    (experiment,) = langfuse.last_dataset.experiments
    assert experiment["name"] == "prompt v1"
    assert [evaluator.__name__ for evaluator in experiment["evaluators"]] == [
        "check_routing_correct",
        "check_retrieval_hit",
        "check_abstained",
    ]
    assert langfuse.calls == ["get_dataset", "flush"]


def test_the_experiment_task_answers_the_query_of_the_dataset_item():
    langfuse = RecordingLangfuse()
    upload_test_queries(langfuse, "validation-set", [DIRECT])
    answered = []

    def answer_query(query):
        answered.append(query)
        return make_support_answer()

    run_experiment_with(langfuse, answer_query)
    (experiment,) = langfuse.last_dataset.experiments
    (item,) = langfuse.last_dataset.items
    output = experiment["task"](item=item)

    assert answered == [DIRECT.query]
    assert output == make_support_answer()


def test_the_experiment_task_needs_only_the_input_of_the_dataset_item():
    task = build_experiment_task(lambda query: make_support_answer())

    assert task(item=SimpleNamespace(input=DIRECT.query)) == make_support_answer()


def fetch_experiment_items(langfuse, run_name, ready, attempts=15, delay_seconds=2.0):
    """Poll the v4 experiments endpoint (the legacy dataset-run API answers 410) until `ready(items)`."""
    since = datetime.now(UTC) - timedelta(hours=1)
    for _ in range(attempts):
        items = langfuse.api.experiments.list_items(
            from_start_time=since, experiment_name=run_name, fields="core,dataset,scores"
        ).data
        if ready(items):
            return items
        time.sleep(delay_seconds)
    pytest.fail(f"experiment {run_name!r} never became readable in Langfuse")


@pytest.mark.integration
@requires_keys("OPENAI_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY")
def test_an_experiment_over_three_test_queries_is_linked_to_traces_and_never_duplicates_items(tmp_path):
    settings = load_settings()
    api_key = settings.openai_api_key.get_secret_value()
    langfuse = init_langfuse(
        settings.langfuse_public_key.get_secret_value(),
        settings.langfuse_secret_key.get_secret_value(),
        settings.langfuse_host,
    )
    chat_model = lambda model: build_chat_model(model, api_key=api_key, temperature=settings.llm_temperature)
    specialists = build_specialists(
        index_sample_document_for_every_area(settings, api_key, tmp_path),
        chat_model(settings.specialist_model),
        settings.similarity_threshold,
    )
    answer_query = build_answer_query(
        build_graph(build_router(chat_model(settings.router_model)), specialists),
        RunnableLambda(lambda judge_input: VERDICT),
        LangfuseScorePublisher(langfuse),
    )
    test_queries = [DIRECT_SAMPLE, UNANSWERABLE_SAMPLE, OUT_OF_SCOPE_SAMPLE]

    upload_test_queries(langfuse, TEST_DATASET_NAME, test_queries)
    upload_test_queries(langfuse, TEST_DATASET_NAME, test_queries)
    result = run_validation_experiment(langfuse, TEST_DATASET_NAME, "integration-test", answer_query)

    assert len(langfuse.get_dataset(TEST_DATASET_NAME).items) == 3
    evaluated = {
        item_result.output.query: {evaluation.name for evaluation in item_result.evaluations}
        for item_result in result.item_results
    }
    assert evaluated == {
        DIRECT_SAMPLE.query: {"check_routing_correct", "check_retrieval_hit", "check_abstained"},
        UNANSWERABLE_SAMPLE.query: {"check_routing_correct", "check_abstained"},
        OUT_OF_SCOPE_SAMPLE.query: {"check_routing_correct"},
    }
    assert all(item_result.trace_id == item_result.output.trace_id for item_result in result.item_results)
    expected_trace_ids = {item_result.trace_id for item_result in result.item_results}
    stored = fetch_experiment_items(
        langfuse,
        result.run_name,
        ready=lambda items: (
            {item.trace_id for item in items} == expected_trace_ids
            and sum(1 for item in items for score in item.scores or [] if score.name.startswith("check_")) >= 6
        ),
    )
    assert {item.trace_id for item in stored} == expected_trace_ids
    assert {item.experiment_item_id for item in stored} == {f"{TEST_DATASET_NAME}:{tq.id}" for tq in test_queries}
    # Traces also carry the scores that answer_query publishes (`abstained`, quality), so compare with <=, not ==.
    stored_names = {item.experiment_item_id: {score.name for score in item.scores} for item in stored}
    for test_query in test_queries:
        assert evaluated[test_query.query] <= stored_names[f"{TEST_DATASET_NAME}:{test_query.id}"]
    assert "check_abstained" in stored_names[f"{TEST_DATASET_NAME}:{UNANSWERABLE_SAMPLE.id}"]
    assert "check_abstained" not in stored_names[f"{TEST_DATASET_NAME}:{OUT_OF_SCOPE_SAMPLE.id}"]
    assert "check_retrieval_hit" not in stored_names[f"{TEST_DATASET_NAME}:{UNANSWERABLE_SAMPLE.id}"]
