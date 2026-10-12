# Atalaya Data support routing

A multi-agent support system for Atalaya Data, a fictional SaaS company for public administrations. A **Router** reads each Query and sends it to one **Area** (HR, Tech or Finance) or marks it Out of Scope. That Area's **Specialist** answers only from the Area's Knowledge Base. A **Judge** then rates each grounded Answer from 1 to 10. Langfuse traces the whole path, from Router to Judge, as one trace.

Built with LangChain (Runnables, structured output, retrievers), LangGraph (the routing graph), Chroma (one collection per Area, cosine similarity) and Langfuse (traces, scores, Datasets and Experiments).

The domain terms (Query, Route, Area, Section, Abstention, ...) are defined in [CONTEXT.md](CONTEXT.md). The decisions that are hard to reverse are recorded in [docs/adr/](docs/adr/).

## Assignment vocabulary

The assignment uses "agent" for three different things. This project gives each one its own name:

| Assignment | This project | Why |
|---|---|---|
| Orchestrator agent | **Router** (produces a **Route**) plus the graph that executes it (`build_router`, `build_graph`) | The Router is what classifies; "orchestrating" is what the whole graph does |
| RAG agent / `hr_agent.py`, `tech_agent.py`, `finance_agent.py` | **Specialist** (`specialists/specialist.py`, `build_specialist(Area.HR, ...)`) | They are deterministic chains, not tool-calling agents ([ADR 0002](docs/adr/0002-specialists-are-chains-not-agents.md)). One factory is built once per Area, so there is no file per Area |
| Evaluator agent | **Judge** (`judging/answer_judge.py`, `build_judge`) | Langfuse already uses "evaluator" for Experiment functions, which this project calls **Checks** |
| category / department / domain / intent | **Area** (`hr` \| `tech` \| `finance`) | One word, one concept |
| chunk | **Section** | By design, one `##` section of a Document is one chunk. "Chunk" only appears inside `chunker.py` |

Where each deliverable lives:

| Deliverable | Location |
|---|---|
| Main notebook | [multi_agent_system.ipynb](multi_agent_system.ipynb) (six sections, in the order the assignment asks for) |
| System wiring | `src/orchestration/multi_agent_system.py` (`build_support_system`) |
| Document collections | `data/hr_docs/`, `data/tech_docs/`, `data/finance_docs/` (more than 50 Sections each) |
| Test Queries | [test_queries.json](test_queries.json) (`calibration` and `validation` splits) |
| Evaluator (Judge) and Langfuse Score API | `src/orchestration/judging/` and `src/orchestration/observability/score_publisher.py` |
| Dependencies | [requirements.txt](requirements.txt) |
| Environment template | [.env.example](.env.example) |

## Installation

You need Python 3.14, an OpenAI API key and a Langfuse project.

With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv sync
```

Or with the requirements file, which is exported from `uv.lock`:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e . --no-deps
```

The last command installs the `orchestration` package from `src/` so the notebook can import it. `uv sync` already does this.

To regenerate the requirements file after changing dependencies:

```bash
uv export --format requirements-txt --no-hashes --no-emit-project -o requirements.txt
```

## Configuration

Copy the environment template and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Required | Default | Notes |
|---|---|---|---|
| `OPENAI_API_KEY` | yes | — | Chat models and embeddings |
| `LANGFUSE_PUBLIC_KEY` | yes | — | `build_support_system` raises `ValueError` without it |
| `LANGFUSE_SECRET_KEY` | yes | — | Same as above |
| `LANGFUSE_HOST` | no | Langfuse SDK default (`https://cloud.langfuse.com`, EU) | Set it to your project's region, e.g. `https://us.cloud.langfuse.com` (US) |
| `SIMILARITY_THRESHOLD` | no | `0.325` | Calibrated in the first real run ([ADR 0004](docs/adr/0004-threshold-cannot-catch-unanswerable-queries.md)) |
| `RETRIEVAL_TOP_K` | no | `4` | Sections retrieved per Query |
| `ROUTER_MODEL` | no | `gpt-4o-mini` | |
| `SPECIALIST_MODEL` | no | `gpt-4o-mini` | |
| `JUDGE_MODEL` | no | `gpt-4.1` | A different model from the one it rates |
| `EMBEDDING_MODEL` | no | `text-embedding-3-small` | Used both to index and to embed Queries |
| `LLM_TEMPERATURE` | no | `0.0` | |
| `CHUNK_MAX_TOKENS` / `CHUNK_OVERLAP_TOKENS` | no | `800` / `120` | Only long Sections are split |

`Settings` reads `.env` from the working directory, so run everything from the repository root.

## Running the notebook

From the repository root:

```bash
uv run jupyter notebook multi_agent_system.ipynb
```

(Or `jupyter notebook multi_agent_system.ipynb` inside the activated virtual environment.)

Run the cells **top to bottom** (Run All works). The first code cell of section 2 must run before anything else, because it builds the whole system:

1. **Setup and imports.** Imports only; the notebook never reads keys itself.
2. **Document loading and vector stores.** `build_support_system()` reads the settings, indexes the three Knowledge Bases into `.chroma/` and connects to Langfuse. The first run embeds all Documents once; later runs reuse the index. The next cell retrieves Sections for a sample Query.
3. **Agent definition (Specialists).** Shows the Area descriptions and the two fixed messages.
4. **Orchestrator and routing.** Answers one Query end to end and prints its Langfuse trace link.
5. **Tests and examples.** One grounded Answer per Area, a Frontier Query, an Out of Scope Query and an Abstention.
6. **Langfuse integration.** The calibration sweep (writes `outputs/threshold_sweep.json`), the validation Experiment over the `validation` split (uploads the Dataset and prints the run link), and a final `langfuse.flush()`.

The code cells of sections 2, 4, 5 and 6 call OpenAI, except the final flush; sections 1 and 3 make no network calls. The validation Experiment cell runs the full pipeline, Judge included, over 16 Test Queries, so it is the slowest and most expensive cell. Each execution creates a new Experiment run in Langfuse; the reference run is the one in [Measured results](#measured-results).

## Usage examples

To try a single Query, run sections 1 and 2, then any cell of section 4 or 5. The same calls work outside the notebook:

```python
from orchestration.multi_agent_system import build_support_system
from orchestration.support_answer import format_support_answer

system = build_support_system()
answer = system.answer_query("¿Cómo solicito una tarjeta corporativa para viajar?")
print(format_support_answer(answer, system.langfuse.get_trace_url(trace_id=answer.trace_id)))
system.langfuse.flush()
```

Each trace in Langfuse shows the Route with the Router's reasoning, the retrieved Sections with their Similarity, the Answer, and the scores: `quality`, `relevance`, `completeness` and `accuracy` from the Judge, plus `abstained`.

Tests:

```bash
uv run pytest                 # unit tests, no network
uv run pytest -m integration  # real OpenAI and Langfuse calls; skipped without keys
```

## Measured results

Validation Experiment, run once on 2026-10-12 over the 16 Test Queries of the `validation` split (Similarity Threshold 0.325, top-k 4, Router and Specialists `gpt-4o-mini`, Judge `gpt-4.1`): [run in Langfuse](https://us.cloud.langfuse.com/project/cmv48hrxk012mad0iu5ad20ir/datasets/cmv4i3rx1007jad0jplfx4dyb/runs/5f3204c8-6778-44ae-afe2-196774aef162). The project is private, so the link only opens for project members.

| Area | Test Queries | Routing correct | Retrieval hits | Abstentions (unanswerable) | Abstentions (answerable) | Judged | Mean quality |
|---|---|---|---|---|---|---|---|
| hr | 5 | 5/5 | 4/4 | 0/1 | 0/4 | 5 | 9.6 |
| tech | 6 | 6/6 | 5/5 | 0/1 | 0/5 | 6 | 9.0 |
| finance | 3 | 2/3 | 2/3 | — | 0/3 | 3 | 10.0 |
| out_of_scope | 2 | 2/2 | — | — | — | — | — |
| **Total** | **16** | **15/16 (93.8%)** | **11/12 (91.7%)** | **0/2** | **0/12** | 14 | 9.4 |

- All four Frontier Queries were routed correctly.
- One misroute: finance-07 went to HR. The Router read "plástico de la empresa" (the company card) as equipment. The HR Specialist answered and the Judge still rated it 10/10, because the Judge only sees the Sections it received and cannot tell that the Route was wrong.
- Neither unanswerable Test Query produced an Abstention. Both Specialists still declined in their text, so the `abstained` score undercounts declines.
- Nothing was tuned after this run, to keep the validation split clean.

## Known limitations

- **One Query, one Route.** A Query that asks about two Areas goes to the Area of its main request and gets a partial Answer ([ADR 0001](docs/adr/0001-one-knowledge-base-per-fact.md), PLAN.md §3.1).
- **The Judge runs synchronously.** It runs after the graph, inside the same trace, so it adds latency to every grounded Answer. This is a scope decision for this delivery (PLAN.md §3.1).
- **The fixed messages are in Spanish.** `OUT_OF_SCOPE_MESSAGE` and `NO_INFORMATION_MESSAGE` do not follow the Query's language, unlike generated Answers, which do (PLAN.md §7.2).
- **The calibration is tied to these Documents.** The Similarity Threshold (0.325) and top-k (4) come from a sweep over these Documents and Test Queries. The threshold cannot catch unanswerable Queries, which therefore depend on the Specialist declining in its text. New or edited Documents need a new sweep ([ADR 0004](docs/adr/0004-threshold-cannot-catch-unanswerable-queries.md), PLAN.md §3.5).

## Further reading

- [CONTEXT.md](CONTEXT.md): the glossary every name in the code follows.
- [docs/adr/](docs/adr/): architecture decision records.
- [PLAN.md](PLAN.md) (Spanish): the full plan, architecture and calibration notes.
