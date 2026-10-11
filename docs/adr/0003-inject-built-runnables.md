---
status: accepted
---

# Business modules receive pre-built Runnables, not raw chat models

`routing/`, `specialists/` and `judging/` must be unit-testable without network access, and the graph and `answer_query` must be testable without a model at all. LangChain's fake chat models cannot help with structured output: `with_structured_output` raises `NotImplementedError` on any model that does not implement `bind_tools`, and none of the fakes do. So we place the seam at the composition layer. Each business package builds its own Runnable from a plain chat model and owns its prompt: `routing/` exposes `build_router(chat_model) -> Runnable[str, Route]` (`ROUTER_PROMPT | chat_model.with_structured_output(Route)`), `judging/` exposes `build_judge(chat_model) -> Runnable[..., QualityVerdict]`, and `specialists/` exposes `build_specialist(area, retrieve, chat_model, threshold) -> Callable[[str], SpecialistReply]`. The composition layer (`build_graph(router, specialists)` and `build_answer_query(graph, judge, publisher)` in `multi_agent_system.py`) receives those built Runnables and callables and never builds them itself. Tests of the graph and of `answer_query` therefore inject `RunnableLambda` stubs returning fixed `Route`s and `QualityVerdict`s, a fake `retrieve` returning `RetrievedSection`s with chosen Similarities, and a `RecordingScorePublisher`. `build_router` and `build_judge` have no unit test: without a model there is nothing to test, and their proof is the `routing_correct` Check and the integration run.

**Amended 2026-10-11.** The first version of this decision built the prompts and Runnables in the composition layer and had `routing/` and `judging/` receive them through `route_query(query, router)` and `judge_answer(..., judge)`. That made both packages pass-throughs: deleting them left one line in the graph, and the Router's real logic (its prompt) lived in the most crowded file of the project. Moving `build_*` into each package keeps the testability seam while letting each package contain its whole behaviour.

## Consequences

- Business packages may use `langchain_core` structured output and prompt templates; they still never import Langfuse, Chroma or LangGraph.
- The Specialist's drafting step receives a plain chat model, since `invoke` works on fakes; its retrieval step receives a `retrieve` callable built by `knowledge_base/`.
- `multi_agent_system.py` contains wiring only: it reads `Settings` once, builds the real chat models, `retrieve` callables, Langfuse client and `ScorePublisher`, and passes them to the `build_*` functions.

## Considered options

- Build Runnables in composition and pass them into `route_query` / `judge_answer`: rejected after the deletion test (pass-through modules, prompts outside their package).
- Pass raw chat models into business functions and call `with_structured_output` inside: rejected, cannot be unit-tested with fakes.
