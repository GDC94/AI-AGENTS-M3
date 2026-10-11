# 06: Checks and threshold sweep

**What to build:** the engineer can load Test Queries from the JSON file by split, run the three Checks (routing correct, retrieval hit, abstained) over any `SupportAnswer`, and run a threshold sweep over the calibration split that reports, per candidate threshold, how retrieval and abstention behave, all without calling any model or creating any trace.

**Blocked by:** 02 (Out of Scope end to end), for the `SupportAnswer` shape. Can run in parallel with 03, 04 and 05.

**Status:** ready-for-agent

Scope (PRD "Checks and calibration"; CONTEXT.md "Check", "Test Query"):

- `TestQuery` with id, Query text, expected Area or out_of_scope, expected Section title (absent for out_of_scope and unanswerable), Asker kind, type (direct, frontier, out_of_scope, unanswerable) and split (calibration, validation). A loader reads the file and filters by split, rejecting unknown values.
- Three Checks as pure functions from `SupportAnswer` and `TestQuery` to a boolean: routing correct (target equals expected), retrieval hit (expected Section title among the Sections used), abstained (true exactly for unanswerable Test Queries with an Area, false otherwise).
- `sweep_threshold` as a pure function over per-Area retrieval callables, Test Queries and candidate thresholds, returning one point per threshold with the counts needed to pick the threshold (retrieval hits on answerable Queries, correct abstentions on unanswerable ones). Writing the sweep output file is not part of this package.

- [ ] Seam 3 tests: each Check returns the right boolean on hand-built pairs, including expected Section absent, a Route to the wrong Area, and an unanswerable Query that was answered.
- [ ] The loader returns only the requested split and raises on an invalid type, split or Area value.
- [ ] The sweep over fake retrieval callables with chosen Similarities returns one point per threshold, calls no model and creates no trace; the point values follow the Similarities exactly.
- [ ] The checks package imports no Langfuse, Chroma or LangGraph symbols.
