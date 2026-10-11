"""Langfuse Datasets and Experiments: adapt Test Queries and Checks to Langfuse. Holds no Check logic."""

from collections.abc import Callable, Sequence
from typing import Any

from langfuse import Evaluation, Langfuse

from orchestration.checks import TestQuery, abstained, retrieval_hit, routing_correct
from orchestration.support_answer import SupportAnswer

Check = Callable[[SupportAnswer, TestQuery], bool]


def build_dataset_item(test_query: TestQuery) -> dict[str, Any]:
    """The Query is the input, the expectation is the expected output, the rest travels as metadata."""
    return {
        "input": test_query.query,
        "expected_output": {
            "area": test_query.expected_area,
            "section": test_query.expected_section,
            "type": test_query.type,
        },
        "metadata": {"id": test_query.id, "asker": test_query.asker, "split": test_query.split},
    }


def rebuild_test_query(*, input: Any, expected_output: Any, metadata: Any) -> TestQuery:
    """Inverse of `build_dataset_item`."""
    return TestQuery(
        id=metadata["id"],
        query=input,
        expected_area=expected_output["area"],
        expected_section=expected_output["section"],
        asker=metadata["asker"],
        type=expected_output["type"],
        split=metadata["split"],
    )


def adapt_check(
    name: str,
    check: Check,
    applies_to: Callable[[TestQuery], bool] = lambda test_query: True,
):
    """Wrap a Check as a Langfuse evaluator: its boolean becomes a BOOLEAN Evaluation called `name`.

    Where the Check does not apply to the Test Query, the evaluator returns no Evaluation.
    """

    def evaluator(*, input: Any, output: SupportAnswer, expected_output: Any, metadata: Any, **kwargs: Any):
        test_query = rebuild_test_query(input=input, expected_output=expected_output, metadata=metadata)
        if not applies_to(test_query):
            return []
        return [Evaluation(name=name, value=check(output, test_query), data_type="BOOLEAN")]

    evaluator.__name__ = name
    return evaluator


def build_check_evaluators() -> list:
    """The three Checks as evaluators, each applied only where it makes sense (ticket 06).

    routing_correct: every Test Query. retrieval_hit: direct and frontier (an expected Section exists).
    abstained: Test Queries with an Area (an out_of_scope Query never reaches a Specialist).
    """
    return [
        adapt_check("routing_correct", routing_correct),
        adapt_check("retrieval_hit", retrieval_hit, applies_to=lambda test_query: test_query.is_answerable),
        adapt_check("abstained", abstained, applies_to=lambda test_query: test_query.expected_area != "out_of_scope"),
    ]


def upload_test_queries(langfuse: Langfuse, dataset_name: str, test_queries: Sequence[TestQuery]) -> None:
    """Create (or reuse) the Dataset and upsert one item per Test Query.

    The item id is derived from the Dataset name and the Test Query id, so uploading again
    updates the same items. Langfuse item ids are global across Datasets, hence the prefix.
    """
    langfuse.create_dataset(name=dataset_name)
    for test_query in test_queries:
        langfuse.create_dataset_item(
            dataset_name=dataset_name, id=f"{dataset_name}:{test_query.id}", **build_dataset_item(test_query)
        )


def build_experiment_task(answer_query: Callable[[str], SupportAnswer]):
    """The Experiment task: rebuild the Test Query from the Dataset item and answer its Query."""

    def task(*, item: Any, **kwargs: Any) -> SupportAnswer:
        test_query = rebuild_test_query(
            input=item.input, expected_output=item.expected_output, metadata=item.metadata
        )
        return answer_query(test_query.query)

    return task


def run_validation_experiment(
    langfuse: Langfuse,
    dataset_name: str,
    experiment_name: str,
    answer_query: Callable[[str], SupportAnswer],
):
    """Run one Experiment over the Dataset: `answer_query` is the task, the three Checks are the evaluators.

    Flushes the client at the end, so short scripts do not lose traces or scores.
    """
    dataset = langfuse.get_dataset(dataset_name)
    try:
        return dataset.run_experiment(
            name=experiment_name,
            task=build_experiment_task(answer_query),
            evaluators=build_check_evaluators(),
        )
    finally:
        langfuse.flush()
