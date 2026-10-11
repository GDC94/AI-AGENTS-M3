# 08: First real run: index, calibrate, validate

**What to build:** with the author's real Documents and Test Queries in place, the three Knowledge Bases are indexed, the Similarity Threshold is chosen from a sweep over the calibration split, and the validation split is measured once as a Langfuse Experiment, producing the numbers the notebook and the README will report.

**Blocked by:** 07 (Langfuse Experiment). External dependency: the Documents for the three Areas (LLM-generated at the author's request and reviewed by the author) and the Test Queries file, written by the author, not generated (PRD "Out of Scope").

**Status:** ready-for-agent

Scope (PRD "Knowledge Bases", "Checks and calibration", "Further Notes"; ADR 0001):

- Wire the real system in `multi_agent_system.py`: read `Settings` once with `load_settings()`, build the real chat models, the persisted-Chroma `retrieve` callables and the Langfuse client with `init_langfuse()`, and pass them already built to `build_router`, `build_specialists`, `build_graph` and `build_answer_query` (ADR 0003). No other module reads `Settings`.
- Index the three real Knowledge Bases into the persisted directory with the configured embedding model.
- Run the sweep over the calibration split and save the output file; pick the middle of the good zone and set the Similarity Threshold in the environment template and the Settings default.
- Run the validation Experiment once and record the run link and the resulting routing accuracy, retrieval hit rate and abstention counts per Area.
- Any Frontier Query misrouted is examined against ADR 0001's ownership rule; the remedy order is better Area descriptions, then a stronger Router model, then new few-shot examples never taken from the Test Queries.

- [ ] `multi_agent_system.py` is the only module in `src/` that calls `load_settings()`; an integration test answers one Query through the real wired system (skipped without API keys).
- [ ] A test asserts each Knowledge Base yields more than 50 Sections from the real Documents.
- [ ] The sweep output file exists and lists one point per candidate threshold; the chosen threshold is recorded in the plan and in configuration.
- [ ] The validation Experiment ran once; its link and per-Area results are recorded for tickets 09 and 10.
- [ ] No Test Query text was added to any prompt.
