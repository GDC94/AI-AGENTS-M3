# 07: Langfuse Experiment over the validation split

**What to build:** the engineer uploads a split of Test Queries as a Langfuse Dataset and runs an Experiment whose task is the answering function and whose evaluators are the three Checks, so that the Langfuse UI shows routing accuracy, retrieval hits and abstentions per run and lets two runs (prompt or model variants) be compared side by side, each item linked to its trace.

**Blocked by:** 05 (Judge), 06 (Checks and threshold sweep).

**Status:** ready-for-agent

Scope (PRD "Checks and calibration", "Observability"):

- `upload_test_queries` creates or reuses a Dataset and one item per Test Query (input: the Query text; expected output: Area, Section title and type).
- `run_validation_experiment` runs the Experiment with the answering function as task and the three Checks adapted to the Langfuse evaluator signature. The observability package only adapts; Check logic stays in the checks package.
- `flush` is called at the end of the run.

- [ ] Unit test: the adapters map a `TestQuery` to a Dataset item and back without loss, and wrap each Check so that the Check's boolean becomes a named Langfuse evaluation; the Checks themselves are called, not reimplemented.
- [ ] Integration test: three sample Test Queries are uploaded and one Experiment run completes, visible in Langfuse with the three evaluations per item and each item linked to its trace.
- [ ] Running the Experiment twice does not duplicate Dataset items.
