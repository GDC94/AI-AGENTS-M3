# 05: Judge

**What to build:** every grounded Answer leaves the system with a Quality Verdict (four whole-number Ratings from 1 to 10: overall quality, relevance, completeness, accuracy; and a Reason in Spanish), and its trace in Langfuse shows the four scores. Abstentions and Out of Scope replies are never judged and keep an empty verdict.

**Blocked by:** 04 (Grounded Answer and Abstention end to end).

**Status:** ready-for-agent

Scope (PRD "Judge", "Observability"; ADR 0003):

- `QualityVerdict` with the four Ratings and the Reason.
- The judging package owns the prompt and exposes a builder taking a plain chat model, returning a runnable that receives the Query, the Answer and the Retrieved Sections used, and produces the verdict in one structured-output call. Section formatting for the prompt happens inside the judging package.
- The answering function calls the Judge only when the Answer is grounded, then publishes the four quality scores through the `ScorePublisher` on the same trace, after the `abstained` score.
- The Judge model is the one configured for the Judge role (default gpt-4.1).

- [ ] Seam 1 test with a `RunnableLambda` Judge returning a fixed verdict: on a grounded Answer the Judge double is called exactly once with the Query, the Answer and the Sections used; the `SupportAnswer` carries the verdict; the recorder holds four quality scores plus `abstained` 0 for that trace id.
- [ ] Seam 1 test: on an Abstention and on an Out of Scope reply the Judge double is never called and the verdict is empty.
- [ ] `QualityVerdict` rejects Ratings outside 1 to 10 and non-integer values.
- [ ] Integration test: the real Judge rates one grounded Answer from the sample Document; the Reason is in Spanish; the four scores are visible on the trace in Langfuse.
- [ ] Unit tests make no network calls.
