# 10: README and requirements file

**What to build:** a new person installs the project, configures keys and runs the notebook following only the README, and a reviewer finds each assignment deliverable through the mapping table from the assignment's words (orchestrator, RAG agent, evaluator, category, chunk) to this project's vocabulary (Router, Specialist, Judge, Area, Section).

**Blocked by:** 08 (First real run). Can run in parallel with 09.

**Status:** done

Scope (PRD user stories 26 and 27; plan sections 1 and 6):

- README: project description; installation with uv and the requirements file; key configuration from the environment template; how to run the notebook and in which cell order; usage examples; the mapping table; the measured results of the validation run with the Experiment link; known limitations (one Query one Route, synchronous Judge, Spanish fixed messages, calibration tied to these Documents); pointers to CONTEXT.md and the ADRs.
- Requirements file exported from the uv lock, containing at least the nine packages the assignment lists.

- [x] The mapping table matches the one in the plan and uses CONTEXT.md terms.
- [x] The requirements file lists langchain, langchain-openai, langfuse, openai, a vector store library, tiktoken, python-dotenv, jupyter and ipykernel.
- [x] Known limitations are stated as such, with the ADR or plan section that explains each.

## Comments

**Implementation (commits 0830708, plus the closing commit):**

- `README.md` is in English (author's decision). Its mapping table translates the one in `PLAN.md` §1 and adds "intent" to the Area row and the three `*_agent.py` names to the Specialist row; `PLAN.md` §1 now says the README carries the table translated into English. A second table locates each deliverable.
- Sections: description, installation (uv, or pip with `requirements.txt` plus `pip install -e . --no-deps`), configuration (every `Settings` variable with its default), running the notebook (section order and which cells call OpenAI), usage examples, measured results (ticket 08's validation run, its link and both findings: the `abstained` score undercounts declines, and a high Judge rating does not prove the Route was right), the four known limitations with their ADR or plan section, and further reading.
- `requirements.txt` is exported with `uv export --format requirements-txt --no-hashes --no-emit-project` (the command is in its header); it includes the dev group, so `jupyter` and `ipykernel` are pinned, and `chromadb` is the vector store library.
- Tests: `tests/test_readme.py` (each assignment word shares a table row with its bolded CONTEXT.md term; each known limitation cites an ADR or `PLAN.md`; every linked repository file exists) and `tests/test_requirements.py` (the nine assignment packages are pinned). Unit suite: 157 passed.
- Review fixes before approval: `LANGFUSE_HOST` is optional (a `None` host uses the SDK default, `https://cloud.langfuse.com`); the claim that every cell from section 2 calls OpenAI was wrong (sections 1 and 3 make no network calls). The README now also states that each notebook execution creates a new Experiment run (ticket 09 decision).
- Integration tests were not run for this ticket. The clean-machine criterion ("Following the README alone on a clean machine reaches a running notebook") was removed at the author's request on 2026-10-12, before any clean-machine check was made; the pip path in the README is untested.
- The import reordering in `tests/test_layering.py` and `tests/test_multi_agent_system.py` (noted in ticket 09) was the author's own edit; committed in 7e199f7. The environment template's threshold and top-k were committed in 7d6c866.

**Approval (2026-10-12):** the author approved ticket 10, including the English README and the two review fixes.
