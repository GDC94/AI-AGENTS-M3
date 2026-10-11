# 07: Langfuse Experiment over the validation split

**What to build:** the engineer uploads a split of Test Queries as a Langfuse Dataset and runs an Experiment whose task is the answering function and whose evaluators are the three Checks, so that the Langfuse UI shows routing accuracy, retrieval hits and abstentions per run and lets two runs (prompt or model variants) be compared side by side, each item linked to its trace.

**Blocked by:** 05 (Judge), 06 (Checks and threshold sweep).

**Status:** done

Scope (PRD "Checks and calibration", "Observability"):

- `upload_test_queries` creates or reuses a Dataset and one item per Test Query (input: the Query text; expected output: Area, Section title and type).
- `run_validation_experiment` runs the Experiment with the answering function as task and the three Checks adapted to the Langfuse evaluator signature, each producing an evaluation named `check_routing_correct`, `check_retrieval_hit` or `check_abstained`. The observability package only adapts; Check logic stays in the checks package.
- `flush` is called at the end of the run.

- [x] Unit test: the adapters map a `TestQuery` to a Dataset item and back without loss, and wrap each Check so that the Check's boolean becomes a Langfuse evaluation named with the `check_` prefix; the Checks themselves are called, not reimplemented.
- [x] Integration test: three sample Test Queries are uploaded and one Experiment run completes, visible in Langfuse with the `check_` evaluations that apply to each item (stored next to, and distinct from, the `abstained` score of `answer_query`) and each item linked to its trace.
- [x] Running the Experiment twice does not duplicate Dataset items.

## Comments

**Implementer choices for the author to confirm:**

- Signatures: `upload_test_queries(langfuse, dataset_name, test_queries)` and `run_validation_experiment(langfuse, dataset_name, experiment_name, answer_query)`; both live in `observability/experiments.py` with the adapters `build_dataset_item`, `rebuild_test_query`, `adapt_check`, `build_check_evaluators`, `build_experiment_task`.
- Dataset item: `input` is the Query text, `expected_output` is `{area, section, type}`, and `metadata` is `{id, asker, split}` so the Test Query rebuilds without loss. Item id is `"<dataset_name>:<test_query.id>"`: deterministic, so `create_dataset_item` upserts (documented SDK behaviour) and ids stay unique across Datasets, as Langfuse requires.
- Applicability (ticket 06): `routing_correct` for all Test Queries; `retrieval_hit` only for direct and frontier; `abstained` only for Test Queries with an Area. Where a Check does not apply, the evaluator returns no Evaluation (an empty list).
- Evaluations are BOOLEAN and named after the Check (`routing_correct`, `retrieval_hit`, `abstained`). **Superseded by the author's decision below: they are now prefixed `check_`.**
- `flush` runs in a `finally`, so traces are flushed even if the Experiment fails. The Experiment name is a parameter; the Langfuse run name is the name plus a timestamp, so repeated runs are separate runs over the same items.
- Finding: for Test Queries with an Area, the trace now holds two scores named `abstained`: the one `answer_query` publishes (ticket 04) and the Experiment evaluation. Both have the same value. I kept the Check name as the ticket says; renaming the evaluation (for example `abstained_check`) is a one-line change if you prefer. **Resolved by the author's decision below.**
- Legacy read endpoints return 410 for this organisation: the integration test reads results with `api.experiments.list_items(...)` (v4) instead of `datasets.get_run`.
- The integration test uses the dataset `support-routing-validation-test`, three sample Test Queries built in code against the sample HR Document, and a fixed-verdict Judge. Re-running it reuses the same items (never duplicates).

**Test runs:** 131 unit tests passed; 10 integration tests passed.

**Author decision and review fixes:**

- Experiment evaluations are prefixed `check_`: `check_routing_correct`, `check_retrieval_hit`, `check_abstained`. The `abstained` score published by `answer_query` (tickets 02/04) is unchanged. Reason: two scores named `abstained` on one trace doubled the counts and mixed Out of Scope traces into the Check's aggregate (the Check applies only to Test Queries with an Area). Each evaluation is produced only where its Check applies. The integration test now asserts `check_abstained` is stored for the unanswerable item and absent for the Out of Scope one.
- Review fixes: the shared integration helper `index_sample_document_for_every_area` and `HR_SAMPLE_DOCUMENT` moved to `tests/samples.py` (no test module imports another); `build_experiment_task` uses the item's input directly; `observability/__init__.py` exports only `upload_test_queries`, `run_validation_experiment`, `init_langfuse`, `LangfuseScorePublisher`, `ScorePublisher` (adapters are imported from `observability.experiments`); the `Check` alias lives in `checks/`; return types added to `adapt_check` and `build_check_evaluators`; a `make_test_query` factory replaces the repeated `TestQuery(...)` constants in the tests.

**Test runs after the fixes:** 132 unit tests passed; 10 integration tests passed.

**Approval (2026-10-11):** the author approved ticket 07 with the `check_` prefix for the Experiment evaluations and the implementer choices as they stand (item id `<dataset>:<test_query.id>`, item input/expected output/metadata shape, applicability per ticket 06, `flush` in `finally` and timestamped run names, results read through `api.experiments.list_items`). PLAN.md 5.1 names the Checks only, not the `check_` evaluation names; left unchanged.
