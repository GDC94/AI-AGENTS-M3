## Project

Multi-agent support routing for Atalaya Data (fictional SaaS for public administrations): a Router sends each Query to one Area, a Specialist answers from that Area's Knowledge Base, a Judge rates the Answer, all traced in Langfuse.

- Before implementing a step, read `PLAN.md` and the ticket in `.scratch/support-routing/issues/` (the ticket wins if they differ).
- Name everything with the vocabulary in `CONTEXT.md`.
- Before "fixing" something that looks odd, read `docs/adr/`.

## Commands

- `uv run pytest` runs unit tests; integration tests are excluded by default.
- `uv run pytest -m integration` runs integration tests; they skip when the API keys are absent.
- `uv add <pkg>` (or `uv add --dev <pkg>`), never `pip`.

## Architecture rules

- Business packages (`routing/`, `specialists/`, `judging/`, `checks/`) never import Langfuse, Chroma or LangGraph.
- Each business package builds its own Runnable (`build_router`, `build_judge`, `build_specialist`); `build_graph` and `build_answer_query` receive them already built (ADR 0003).
- `Settings` is read once, in `multi_agent_system.py`; every other module receives only the values it needs.
- Functions are named verb + object.
- Tests mirror the `src/` packages and exercise each package's public interface.

## Way of working

- One plan step at a time, strict TDD (failing test, minimal code, refactor).
- The author reviews each step before the next one starts.
- Keep explanations simple: the author is learning.
- Discuss changes to `PLAN.md` in chat before writing them.

## What the author writes

The Documents in `data/` were LLM-generated at the author's request and reviewed by the author; do not regenerate or edit them without asking. `test_queries.json` is written by the author; never generate it.

## Known traps

- Use the same embedding model for indexing and for Queries.
- Chroma defaults to L2 distance: request cosine explicitly.
- LangChain's fake chat models do not support `with_structured_output`.
- `.chroma/` is never committed.
- Unit tests never call OpenAI, Langfuse or disk-persisted Chroma.
- Call `langfuse.flush()` at the end of the notebook and of short scripts.

## Language

- English: code, identifiers, comments, tests, system prompts, `CONTEXT.md` and ADRs. Prompts tell the model to answer in the Query's language.
- Spanish: the Documents in `data/`, `PLAN.md`, fixed Asker-facing messages (`OUT_OF_SCOPE_MESSAGE`, `NO_INFORMATION_MESSAGE`), the Judge's `reason`, and explanations to the author.

## Agent skills

### Issue tracker

Issues live as local markdown files under `.scratch/<feature-slug>/`. There is no git remote, so external PRs are not a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use their default strings (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), recorded as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
