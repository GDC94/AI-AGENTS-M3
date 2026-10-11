# 06: Checks and threshold sweep

**What to build:** the engineer can load Test Queries from the JSON file by split, run the three Checks (routing correct, retrieval hit, abstained) over any `SupportAnswer`, and run a threshold sweep over the calibration split that reports, per candidate threshold, how retrieval and abstention behave, all without calling any model or creating any trace.

**Blocked by:** 02 (Out of Scope end to end), for the `SupportAnswer` shape. Can run in parallel with 03, 04 and 05.

**Status:** ready-for-agent

Scope (PRD "Checks and calibration"; CONTEXT.md "Check", "Test Query"):

- `TestQuery` with id, Query text, expected Area or out_of_scope, expected Section title (absent for out_of_scope and unanswerable), Asker kind, type (direct, frontier, out_of_scope, unanswerable) and split (calibration, validation). A loader reads the file and filters by split, rejecting unknown values.
- Three Checks as pure functions from `SupportAnswer` and `TestQuery` to a boolean: routing correct (target equals expected), retrieval hit (expected Section title among the Sections used), abstained (true exactly for unanswerable Test Queries with an Area, false otherwise).
- `sweep_threshold` as a pure function over per-Area retrieval callables, Test Queries and candidate thresholds, returning one point per threshold with the counts needed to pick the threshold (retrieval hits on answerable Queries, correct abstentions on unanswerable ones). Writing the sweep output file is not part of this package.

- [x] Seam 3 tests: each Check returns the right boolean on hand-built pairs, including expected Section absent, a Route to the wrong Area, and an unanswerable Query that was answered.
- [x] The loader returns only the requested split and raises on an invalid type, split or Area value.
- [x] The sweep over fake retrieval callables with chosen Similarities returns one point per threshold, calls no model and creates no trace; the point values follow the Similarities exactly.
- [x] The checks package imports no Langfuse, Chroma or LangGraph symbols.

## Comments

**Implementer choices for the author to confirm:**

- `abstained` Check passes when `answer.abstained` equals "the Test Query is unanswerable". So it also passes for an answerable or out_of_scope Query that was not an Abstention (Out of Scope replies have `abstained` false). It is not limited to Test Queries with an Area; the experiment can choose to report it only for those.
- `retrieval_hit` returns False when the Test Query has no expected Section (out_of_scope, unanswerable), instead of a vacuous True. Callers should apply it only to direct and frontier Queries.
- `test_queries.json` is a top-level JSON list of objects with the PLAN 5.4 field names. `expected_area` reuses `RouteTarget`; `expected_section` defaults to null. Every item is validated whatever the requested split (a typo in validation is caught while calibrating); an unknown requested split raises `ValueError`, a bad item raises pydantic `ValidationError`.
- `sweep_threshold(retrieve_by_area: Mapping[Area, Retrieve], test_queries, thresholds) -> list[SweepPoint]`. A `SweepPoint` has `threshold`, `retrieval_hits`, `answerable`, `correct_abstentions`, `unanswerable` (counts, not rates). Answerable means direct or frontier; unanswerable means unanswerable; out_of_scope Queries are ignored.
- The sweep retrieves each Query once, from its expected Area (it assumes correct routing, so it measures only the threshold), and reuses the result for every threshold. A Section with Similarity equal to the threshold is kept, as in the Specialist.
- `Retrieve` is imported from `orchestration.specialists` (no Langfuse/Chroma there); `TestQuery` has `__test__ = False` so pytest does not try to collect it.

**Test runs:** 109 unit tests passed (23 new in `tests/checks/`); 9 integration tests passed with real keys.
