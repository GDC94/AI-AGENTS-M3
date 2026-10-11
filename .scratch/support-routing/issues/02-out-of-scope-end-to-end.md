# 02: Out of Scope end to end

**What to build:** an Asker sends a Query that is not about Atalaya ("who won the match?") and receives the fixed Out of Scope message. The Query runs through the real Router and the LangGraph graph, produces one Langfuse trace with the Router's reasoning visible and an `abstained` score of 0, and returns a `SupportAnswer` carrying the trace id. This is the first tracer bullet: Router, graph, answering function and observability all exist after it, even though the Specialist nodes are still placeholders.

**Blocked by:** 01 (Preparation and shared domain types).

**Status:** ready-for-agent

Scope (PRD "Router", "Flow and composition", "Observability"; ADR 0003 as amended):

- `Route` with `reasoning` first and `target` in {hr, tech, finance, out_of_scope}.
- The routing package owns the zero-shot prompt built from `AREA_DESCRIPTIONS` and exposes a builder that takes a plain chat model and returns the Router runnable using strict structured output. No Test Query appears in the prompt.
- The out-of-scope reply: a fixed Spanish message, no Specialist, no model call.
- `build_graph` from a Router runnable and an Area-to-Specialist mapping: route node, conditional edge on `target`, one node per Area, out-of-scope node. For this ticket the Area nodes may be placeholders that raise a clear "not implemented" error.
- `build_answer_query` from the graph, a Judge runnable and a `ScorePublisher`: wraps the graph in a Langfuse span with the LangChain callback handler, publishes the `abstained` boolean on every trace, and returns `SupportAnswer` (Query, Route, Answer, sections, abstained, verdict, trace id). The Judge is not called in this ticket (no grounded Answer can exist yet); the parameter is accepted so the interface is final.
- Langfuse client initialised from three explicit values; `ScorePublisher` port with the Langfuse adapter; a recording adapter for tests.

Open decision to confirm with the author (do not invent): the handful of real Queries used by the integration test live inside the test module as samples and never enter the official Test Queries file.

- [x] Seam 1 test: with a `RunnableLambda` Router returning target out_of_scope and a recording publisher, the Answer is the fixed message, no retrieval, model or Judge double is called, and exactly one `abstained` score with value 0 is recorded for the trace id in the `SupportAnswer`.
- [x] A test pins the `Route.target` values to the `Area` values plus out_of_scope.
- [x] Seam 1 test: the conditional edge sends each of the three Area targets to its own node (placeholders are acceptable; the test asserts which node ran).
- [x] Integration test: three sample Queries (one per Area) and one off-topic Query are routed by the real model to the expected target, and the off-topic one produces a trace in Langfuse with the `abstained` score visible.
- [x] Unit tests make no network calls.

## Comments

**2026-10-11, author:** approved. Open decision confirmed: the sample Queries used by the integration tests live inside the test modules and never enter the official Test Queries file.

Implementer choices approved by the author:

- `SupportAnswer` lives at the package root (`support_answer.py`), so the checks package can use it without importing LangGraph through the composition module.
- `SupportAnswer.verdict` accepts only `None` and `ScorePublisher` has only `publish_abstention` until ticket 05 adds `QualityVerdict` and `publish_quality_scores`.
- The recording score publisher lives in `tests/doubles.py`.

Findings:

- With no Langfuse keys the client is disabled and a span reports trace id `00000000000000000000000000000000`; unit tests accept it.
- Langfuse organizations created on or after 2026-09-16 get HTTP 410 from the legacy read APIs (traces, scores). The integration test reads through the v2 observations and v3 scores endpoints.
- Integration run with real keys: 6 passed.
