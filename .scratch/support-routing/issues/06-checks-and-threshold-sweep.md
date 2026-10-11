# 06: Checks and threshold sweep

**What to build:** the engineer can load Test Queries from the JSON file by split, run the three Checks (routing correct, retrieval hit, abstained) over any `SupportAnswer`, and run a threshold sweep over the calibration split that reports, per candidate threshold, how retrieval and abstention behave, all without calling any model or creating any trace.

**Blocked by:** 02 (Out of Scope end to end), for the `SupportAnswer` shape. Can run in parallel with 03, 04 and 05.

**Status:** ready-for-agent

Scope (PRD "Checks and calibration"; CONTEXT.md "Check", "Test Query"):

- `TestQuery` with id, Query text, expected Area or out_of_scope, expected Section title (absent for out_of_scope and unanswerable), Asker kind, type (direct, frontier, out_of_scope, unanswerable) and split (calibration, validation). A loader reads the file and filters by split, rejecting unknown values. `TestQuery` also rejects inconsistent fields: type out_of_scope iff expected Area out_of_scope, and expected Section present iff type is direct or frontier.
- Three Checks as pure functions from `SupportAnswer` and `TestQuery` to a boolean: routing correct (target equals expected), retrieval hit (expected Section title among the Sections used), abstained (a raw observation: true when the Specialist abstained; expected true for unanswerable Test Queries with an Area and false for the rest; applied only to Test Queries with an Area, which is the caller's concern).
- `sweep_threshold` as a pure function over per-Area retrieval callables, Test Queries and candidate thresholds, returning one point per threshold with the counts needed to pick the threshold (retrieval hits on answerable Queries, correct abstentions on unanswerable ones). Writing the sweep output file is not part of this package.

- [x] Seam 3 tests: each Check returns the right boolean on hand-built pairs, including expected Section absent, a Route to the wrong Area, and an unanswerable Query that was answered (the abstained Check reports `answer.abstained` whatever the type).
- [x] The loader returns only the requested split and raises on an invalid type, split or Area value, or on inconsistent type, Area and Section combinations.
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

**Review fixes (author decision: reading A, raw observation).** This supersedes decision 1 above.

- `abstained(answer, test_query)` now returns `answer.abstained`, as PLAN 5.1 says. It does not compare with the expectation; the expectation (true for unanswerable Test Queries with an Area, false for the rest) is checked by whoever reads the Check, and applying it only to Test Queries with an Area is the caller's concern, like `retrieval_hit` for direct and frontier.
- `TestQuery` validates on load: type out_of_scope iff expected Area out_of_scope; expected Section present iff type is direct or frontier.
- `TestQuery.is_answerable` and `is_unanswerable` replace the raw type strings in the sweep.
- Single-letter names in the sweep renamed; new tests for `routing_correct` on out_of_scope Queries, and for the sweep with out_of_scope Queries (retrieval never called), only a frontier Query, and no thresholds.
- Tickets 07 and 08 checked: no statement contradicted.
