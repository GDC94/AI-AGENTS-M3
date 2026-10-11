# 01: Preparation and shared domain types

**What to build:** the repository is ready for test-driven work on every later ticket: dependencies installed, configuration read once through typed Settings, one chat-model factory per role, the two shared domain types in place, the agent guidance file completed, and a test suite that runs green without any API key while integration tests exist and are skipped.

**Blocked by:** None (can start immediately).

**Status:** done

Scope (from the PRD, "Configuration and models", "Shared domain types", "Repository conventions"):

- Install pydantic-settings, langfuse, langchain-chroma, langchain-text-splitters, jupyter and ipykernel. Confirm Chroma imports and creates an in-memory collection on Python 3.14; if it does not, record the fallback to Python 3.12 before continuing.
- Settings via pydantic-settings reading the dotenv file: OpenAI key; Router, Specialist and Judge model names (defaults gpt-4o-mini, gpt-4o-mini, gpt-4.1); embedding model (default text-embedding-3-small); temperature 0.0; Similarity Threshold 0.42; top-k 3; chunk max tokens 800 and overlap 120; Langfuse public key, secret key and host.
- One chat-model factory taking a model name, an API key and a temperature. Remove the empty legacy LLM module outside the package.
- `Area` string enum (hr, tech, finance) with `AREA_DESCRIPTIONS` (English, what each Area resolves, following ADR 0001's ownership rule and the frontier examples in the plan). `RetrievedSection` with title, text and Similarity.
- Environment template with the four keys the assignment lists; the persisted Chroma directory ignored by git.
- Agent guidance file: add the seven project blocks from the plan (what the project is, commands, architecture rules, way of working, what the author writes, known traps, language) ABOVE the existing "Agent skills" block. Never replace that block.
- Register an `integration` pytest marker; integration tests are skipped when the required keys are absent and excluded from the default run.

Open decisions to confirm with the author before closing (do not invent):

- Mechanism for skipping integration tests: proposed `skipif` on the key environment variables plus `-m "not integration"` in the default pytest options.
- Whether the sweep output directory is versioned (affects the git ignore list; the directory is used by ticket 08).

- [x] `uv run pytest` passes with no `.env` and no API keys.
- [x] Settings tests cover every variable above, its default, and the error on a missing OpenAI key.
- [x] The chat-model factory test builds a model for each role name without network access.
- [x] `Area` has exactly three values; `AREA_DESCRIPTIONS` has one non-empty English entry per Area.
- [x] `RetrievedSection` validates title, text and a Similarity between 0 and 1.
- [x] `uv run pytest -m integration` is recognised and reports skipped tests when keys are absent.
- [x] The agent guidance file still contains the original "Agent skills" block unchanged, below the new blocks.
- [x] Chroma works on the project's Python version, or the version change is recorded in the plan.

## Comments

**2026-10-11, author:** approved. Open decisions confirmed:

- Integration tests are skipped with `skipif` when the required keys are absent from the environment and from `.env` (`tests/keys.py`), and excluded from the default run with `-m 'not integration'` in the pytest options.
- The sweep output directory (`outputs/`) is versioned, so it is not in `.gitignore`.

Chroma 1.5.9 creates an in-memory collection on Python 3.14.7; no version change.
