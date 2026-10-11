# 09: Notebook with the six assignment sections

**What to build:** a reviewer opens the notebook, runs it top to bottom with keys configured, and sees the whole system work: setup, Knowledge Base loading, Specialist definition, Router and routing, example Queries with their Answers and trace links, and the Langfuse integration with the Judge's scores and the validation Experiment. The notebook calls only functions from the package, so it cannot drift from the code.

**Blocked by:** 08 (First real run).

**Status:** ready-for-agent

Scope (PRD "Solution", user stories 25 and 26; assignment table in the plan):

- Six sections with Markdown headings, in the assignment's order: setup and imports; document loading and vector stores; agent definition (Specialists); orchestrator and routing (Router and graph); tests and examples; Langfuse integration (Judge, scores, Experiment).
- Example Queries cover one grounded Answer per Area, one Frontier Query, one Out of Scope Query and one Abstention, each with its trace link and, where applicable, its Quality Verdict.
- `flush` is called in the last cell.

- [ ] The notebook runs top to bottom without errors with keys configured.
- [ ] Every section has a Markdown heading and a short explanation of what the cells do and why.
- [ ] Example outputs show the Route with its reasoning, the Sections used, the Answer, the `abstained` flag and the verdict when present.
- [ ] No logic is defined in the notebook that also exists in the package.
