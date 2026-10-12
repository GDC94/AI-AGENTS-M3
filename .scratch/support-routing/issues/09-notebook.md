# 09: Notebook with the six assignment sections

**What to build:** a reviewer opens the notebook, runs it top to bottom with keys configured, and sees the whole system work: setup, Knowledge Base loading, Specialist definition, Router and routing, example Queries with their Answers and trace links, and the Langfuse integration with the Judge's scores and the validation Experiment. The notebook calls only functions from the package, so it cannot drift from the code.

**Blocked by:** 08 (First real run).

**Status:** done

Scope (PRD "Solution", user stories 25 and 26; assignment table in the plan):

- Six sections with Markdown headings, in the assignment's order: setup and imports; document loading and vector stores; agent definition (Specialists); orchestrator and routing (Router and graph); tests and examples; Langfuse integration (Judge, scores, Experiment).
- Example Queries cover one grounded Answer per Area, one Frontier Query, one Out of Scope Query and one Abstention, each with its trace link and, where applicable, its Quality Verdict.
- `flush` is called in the last cell.

- [x] The notebook runs top to bottom without errors with keys configured.
- [x] Every section has a Markdown heading and a short explanation of what the cells do and why.
- [x] Example outputs show the Route with its reasoning, the Sections used, the Answer, the `abstained` flag and the verdict when present.
- [x] No logic is defined in the notebook that also exists in the package.

## Comments

**Implementation (commits 7a9d32d, 6e42b7e, 0e0246c, 02c2787):**

- `multi_agent_system.ipynb` at the repo root: a title cell and six `##` sections in the assignment's order, each with a short what-and-why explanation (English). Committed with outputs. No `def` or `class` in any code cell.
- New package code, so the notebook defines no logic: `format_support_answer(answer, trace_url)` in `support_answer.py` (Route and reasoning, Sections with Similarity, Answer, `abstained`, Quality Verdict when present, trace link from `langfuse.get_trace_url`), and `format_experiment_summary(result)` in `observability/experiments.py` (per-Area routing and retrieval as passed/applicable; abstentions as a raw count, "N (of M with an Area)", because the `abstained` Check is an observation, not a pass rate).
- Example Queries written for the notebook, not taken from `test_queries.json`: one grounded Answer per Area, one Frontier Query (routed to hr, quality 6), one Out of Scope Query, one Abstention ("¿Cuándo vencen mis stock options?"). The Abstention example is borderline: it sits just under the 0.325 threshold, and about 30 candidate Queries were tried before one abstained (ADR 0004).
- §6 runs the calibration sweep (rewrites `outputs/threshold_sweep.json`; unchanged so far) and a new validation Experiment run on every execution (author's decision), printing its link and per-Area summary. Ticket 08's run stays the reference; its figures appear in §6 as labelled static text. Committed run: https://us.cloud.langfuse.com/project/cmv48hrxk012mad0iu5ad20ir/datasets/cmv4i3rx1007jad0jplfx4dyb/runs/442683c6-7644-401b-bf95-296c99be37c7 (routing 15/16, retrieval 11/12, abstentions 0 of 14 with an Area).
- Tests: `tests/test_support_answer.py`; `tests/test_notebook.py` (six headings in order, no `def`/`class`, last code cell flushes; integration test runs the notebook with `nbclient`, so each integration run also creates an Experiment run); summary tests in `tests/observability/test_experiments.py`. Unit suite: 149 passed.
- Known: the first `format_support_answer` cycle wrote seven tests at once; one passed against the stub without a prior red. An unidentified tool keeps reordering imports in `tests/test_layering.py` and `tests/test_multi_agent_system.py`; those edits were reverted, not committed.

**Approval (2026-10-12):** the author approved ticket 09, including the notebook running the Experiment on every execution, the two review fixes (per-Area summary in §6, stronger Route assertion) and the abstentions label.
