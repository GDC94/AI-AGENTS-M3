# 05: Judge

**What to build:** every grounded Answer leaves the system with a Quality Verdict (four whole-number Ratings from 1 to 10: overall quality, relevance, completeness, accuracy; and a Reason in Spanish), and its trace in Langfuse shows the four scores. Abstentions and Out of Scope replies are never judged and keep an empty verdict.

**Blocked by:** 04 (Grounded Answer and Abstention end to end).

**Status:** done

Scope (PRD "Judge", "Observability"; ADR 0003):

- `QualityVerdict` (in `judging/`) with the Reason and the four Ratings, strict whole numbers from 1 to 10.
- The judging package owns the prompt and exposes a builder taking a plain chat model, returning a runnable that receives the Query, the Answer and the Retrieved Sections used, and produces the verdict in one structured-output call. Section formatting for the prompt happens inside the judging package.
- The answering function calls the Judge only when the Answer is grounded, then publishes the four quality scores through the `ScorePublisher` on the same trace, after the `abstained` score. The Judge's Reason is the comment of the `quality` score only.
- The Judge model is the one configured for the Judge role (default gpt-4.1).

- [x] Seam 1 test with a `RunnableLambda` Judge returning a fixed verdict: on a grounded Answer the Judge double is called exactly once with the Query, the Answer and the Sections used; the `SupportAnswer` carries the verdict; the recorder holds four quality scores plus `abstained` 0 for that trace id.
- [x] Seam 1 test: on an Abstention and on an Out of Scope reply the Judge double is never called and the verdict is empty.
- [x] `QualityVerdict` rejects Ratings outside 1 to 10 and non-integer values.
- [x] Integration test: the real Judge rates one grounded Answer from the sample Document; the Reason is in Spanish; the four scores are visible on the trace in Langfuse, with the Reason as the comment of the `quality` score and no comment on the other three.
- [x] Unit tests make no network calls.

## Comments

**Implementer choices for the author to confirm:**

- `QualityVerdict` lives in `judging/quality_verdict.py` (as in PLAN), not at the package root: like `Route` in `routing/`, it is owned by the package that produces it. `SupportAnswer` imports it from `orchestration.judging`.
- Field order is `reason`, `quality`, `relevance`, `completeness`, `accuracy` (reason first so the model explains before rating, mirroring `Route`). Ratings use strict integers: `7.0`, `"7"` and `True` are rejected.
- The Judge input is a dict `{"query", "answer", "sections"}`; Sections are formatted inside `judging/answer_judge.py`. `build_judge` uses `method="json_schema", strict=True`, like the Router, and has no unit test (ADR 0003).
- A reply is judged when it is not an Abstention and has Sections (`_is_grounded` in `multi_agent_system.py`); Out of Scope has no Sections, so it is excluded too.
- Langfuse scores are named `quality`, `relevance`, `completeness`, `accuracy` (NUMERIC). The Reason is the comment of the `quality` score only (changed at approval, see below). Order on the trace: `abstained`, then the four.
- The `abstained` score is published before the Judge runs; if the Judge call fails, the trace keeps `abstained` and the exception propagates.
- Existing tests that reached a grounded Answer now inject a fixed-verdict Judge instead of a failing one.
- The Spanish check in the integration test is a crude stopword heuristic (no language-detection dependency added).

**Test runs:** 85 unit tests passed; 9 integration tests passed with real keys (one earlier integration run had one unidentified failure that did not reproduce in three later runs).

**Review fixes:**

- `QualityVerdict.ratings_by_name()` is now the single source of the four Rating names (derived from the model fields, minus `reason`). `LangfuseScorePublisher` iterates it. Named after Ratings, not Dimensions, because `quality` is the overall Rating, not a Dimension (CONTEXT.md). The `publish_quality_scores(trace_id, verdict)` port is unchanged.
- `RecordingScorePublisher` now records ordered `(trace_id, name, value)` entries, so the seam-1 test asserts `abstained` 0 followed by the four named scores with their values.
- The grounded-answer test reuses `answer_query_for_area`; the two real-model integration tests share `index_sample_document_for_every_area`.

**2026-10-11, author:** approved.

Implementer choices approved by the author, all six:

- `QualityVerdict` lives in `judging/`, not at the package root.
- Field order `reason`, `quality`, `relevance`, `completeness`, `accuracy`; strict integer Ratings (`7.0`, `"7"` and `True` rejected).
- The Judge input is a dict `{query, answer, sections}`; `build_judge` uses strict `json_schema` structured output and has no unit test (ADR 0003).
- A reply is judged only when it is not an Abstention and has Sections (Out of Scope excluded).
- Scores are `abstained` then `quality`, `relevance`, `completeness`, `accuracy` (NUMERIC) on the same trace.
- `abstained` is published before the Judge runs; a Judge failure leaves only `abstained` and the exception propagates.

Change requested by the author: the Reason is attached as the comment of the `quality` score only (the overall Rating), not of all four, so the support team reads it once next to the overall Rating. The integration test now asserts this against Langfuse (reading scores with `fields="core,details"`, since comments are not in the default `core` group).

Test runs after the change: 86 unit tests passed; 9 integration tests passed with real keys.
