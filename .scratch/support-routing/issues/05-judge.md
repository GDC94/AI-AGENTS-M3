# 05: Judge

**What to build:** every grounded Answer leaves the system with a Quality Verdict (four whole-number Ratings from 1 to 10: overall quality, relevance, completeness, accuracy; and a Reason in Spanish), and its trace in Langfuse shows the four scores. Abstentions and Out of Scope replies are never judged and keep an empty verdict.

**Blocked by:** 04 (Grounded Answer and Abstention end to end).

**Status:** ready-for-agent

Scope (PRD "Judge", "Observability"; ADR 0003):

- `QualityVerdict` with the four Ratings and the Reason.
- The judging package owns the prompt and exposes a builder taking a plain chat model, returning a runnable that receives the Query, the Answer and the Retrieved Sections used, and produces the verdict in one structured-output call. Section formatting for the prompt happens inside the judging package.
- The answering function calls the Judge only when the Answer is grounded, then publishes the four quality scores through the `ScorePublisher` on the same trace, after the `abstained` score.
- The Judge model is the one configured for the Judge role (default gpt-4.1).

- [x] Seam 1 test with a `RunnableLambda` Judge returning a fixed verdict: on a grounded Answer the Judge double is called exactly once with the Query, the Answer and the Sections used; the `SupportAnswer` carries the verdict; the recorder holds four quality scores plus `abstained` 0 for that trace id.
- [x] Seam 1 test: on an Abstention and on an Out of Scope reply the Judge double is never called and the verdict is empty.
- [x] `QualityVerdict` rejects Ratings outside 1 to 10 and non-integer values.
- [x] Integration test: the real Judge rates one grounded Answer from the sample Document; the Reason is in Spanish; the four scores are visible on the trace in Langfuse.
- [x] Unit tests make no network calls.

## Comments

**Implementer choices for the author to confirm:**

- `QualityVerdict` lives in `judging/quality_verdict.py` (as in PLAN), not at the package root: like `Route` in `routing/`, it is owned by the package that produces it. `SupportAnswer` imports it from `orchestration.judging`.
- Field order is `reason`, `quality`, `relevance`, `completeness`, `accuracy` (reason first so the model explains before rating, mirroring `Route`). Ratings use strict integers: `7.0`, `"7"` and `True` are rejected.
- The Judge input is a dict `{"query", "answer", "sections"}`; Sections are formatted inside `judging/answer_judge.py`. `build_judge` uses `method="json_schema", strict=True`, like the Router, and has no unit test (ADR 0003).
- A reply is judged when it is not an Abstention and has Sections (`_is_grounded` in `multi_agent_system.py`); Out of Scope has no Sections, so it is excluded too.
- Langfuse scores are named `quality`, `relevance`, `completeness`, `accuracy` (NUMERIC), each carrying the Reason as the score comment. Order on the trace: `abstained`, then the four.
- The `abstained` score is published before the Judge runs; if the Judge call fails, the trace keeps `abstained` and the exception propagates.
- Existing tests that reached a grounded Answer now inject a fixed-verdict Judge instead of a failing one.
- The Spanish check in the integration test is a crude stopword heuristic (no language-detection dependency added).

**Test runs:** 85 unit tests passed; 9 integration tests passed with real keys (one earlier integration run had one unidentified failure that did not reproduce in three later runs).
