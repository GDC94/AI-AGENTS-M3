# 10: README and requirements file

**What to build:** a new person installs the project, configures keys and runs the notebook following only the README, and a reviewer finds each assignment deliverable through the mapping table from the assignment's words (orchestrator, RAG agent, evaluator, category, chunk) to this project's vocabulary (Router, Specialist, Judge, Area, Section).

**Blocked by:** 08 (First real run). Can run in parallel with 09.

**Status:** ready-for-agent

Scope (PRD user stories 26 and 27; plan sections 1 and 6):

- README: project description; installation with uv and the requirements file; key configuration from the environment template; how to run the notebook and in which cell order; usage examples; the mapping table; the measured results of the validation run with the Experiment link; known limitations (one Query one Route, synchronous Judge, Spanish fixed messages, calibration tied to these Documents); pointers to CONTEXT.md and the ADRs.
- Requirements file exported from the uv lock, containing at least the nine packages the assignment lists.

- [ ] Following the README alone on a clean machine reaches a running notebook.
- [ ] The mapping table matches the one in the plan and uses CONTEXT.md terms.
- [ ] The requirements file lists langchain, langchain-openai, langfuse, openai, a vector store library, tiktoken, python-dotenv, jupyter and ipykernel.
- [ ] Known limitations are stated as such, with the ADR or plan section that explains each.
