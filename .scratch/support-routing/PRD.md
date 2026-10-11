# Support Routing

Status: ready-for-agent
Date: 2026-10-11
Sources: PLAN.md (approved), CONTEXT.md, ADR 0001–0003. Vocabulary follows CONTEXT.md.

## Problem Statement

Atalaya Data, a mid-sized SaaS company serving public administrations, receives support Queries from two kinds of Asker: Clients (users at customer organisations) and Staff (Atalaya employees and consultants). Queries belong to one of three Areas: HR, Tech or Finance. Today tickets are routed by hand and often land in the wrong Area, so answers are slow and sometimes wrong. The support team cannot see why a Query was misrouted, cannot tell a failed retrieval from a bad answer, and has no measure of answer quality before the Asker reads it.

The author of this project also needs to show engineering judgment: why each LangChain component, each routing strategy and each RAG configuration was chosen, with evidence from measured runs.

## Solution

A support routing system built with LangChain and LangGraph, traced in Langfuse:

- A **Router** reads each Query and produces exactly one **Route**: the Area that resolves the main request, or Out of Scope.
- One **Specialist** per Area answers from that Area's **Knowledge Base** only. It retrieves the most similar **Sections**, discards those under the **Similarity Threshold**, and either answers grounded in the surviving Sections or returns an **Abstention** without calling the model.
- Out of Scope Queries get a fixed reply without any Specialist.
- A **Judge** rates every grounded **Answer** (not an Abstention, with Sections) with four **Ratings** (overall quality, relevance, completeness, accuracy) and a Reason, using the Query, the Answer and the Sections used. Abstentions and Out of Scope replies are counted with a boolean `abstained` score, never judged.
- Every Query is one Langfuse trace holding the Route, the retrieval, the Answer and the Judge's scores, so the team can filter misroutes, failed retrievals and low-accuracy Answers.
- **Checks** (deterministic comparisons against **Test Queries**) measure routing accuracy, retrieval hits and abstention behaviour; the Similarity Threshold is calibrated locally and the final run is a Langfuse Experiment.

## User Stories

1. As a Client, I want to ask a question about platform access, data sources, dashboards or incidents, so that I get an answer grounded in Atalaya's Tech documentation.
2. As a Client, I want to ask about invoices, purchase orders, contracts, prices or payments, so that I get an answer grounded in the Finance documentation.
3. As a Client, I want to ask who my assigned consultant is or how to request a replacement, so that HR documentation answers it.
4. As Staff, I want to ask about onboarding, security clearances, leave, work modality, reviews or leaving the company, so that HR documentation answers it.
5. As Staff, I want to ask about VPN, phishing, equipment or internal security, so that Tech documentation answers it.
6. As Staff, I want to ask about expenses, corporate cards, salary payment dates or payslips, so that Finance documentation answers it.
7. As an Asker, I want my Query answered in the language I wrote it in, so that I do not have to translate.
8. As an Asker, I want to receive a clear fixed message when my Query is not about Atalaya at all, so that I know the system cannot help with it.
9. As an Asker, I want to receive a clear fixed message when my Query belongs to an Area but is not documented, so that I am not given an invented answer.
10. As an Asker, I want a Query that touches two Areas to be answered by the Area that resolves the main request, so that I at least get the part that can be acted on.
11. As an Asker, I want the Answer to cite the Sections it used, so that I can verify it against the documentation.
12. As a support team lead, I want every Query to appear as one trace in Langfuse with its Route and reasoning, so that I can see why a Query was routed where it was.
13. As a support team lead, I want each trace to show which Sections were retrieved and their Similarity, so that I can tell a failed retrieval from a bad Answer.
14. As a support team lead, I want four quality scores on every grounded Answer, so that I can filter Answers with low accuracy and review them.
15. As a support team lead, I want every trace to carry an `abstained` score, so that I can list abstentions per Area and review whether they were justified.
16. As a support team lead, I want the Judge's Reason in Spanish, attached once as the comment of the overall `quality` score, so that the support team can read it in Langfuse next to the overall Rating.
17. As an AI engineer, I want the Router, the Specialists and the Judge to each use a model chosen for its role and configured by environment variable, so that I can trade cost against quality per role.
18. As an AI engineer, I want the Similarity Threshold, top-k and chunking sizes in configuration, so that I can calibrate without editing code.
19. As an AI engineer, I want the Knowledge Bases indexed once and skipped on later runs unless forced, so that I do not pay for embeddings on every start.
20. As an AI engineer, I want indexing to refuse a collection built with a different embedding model, so that Similarities stay comparable.
21. As an AI engineer, I want a local threshold sweep over the calibration Test Queries with no model calls, so that I can pick the threshold cheaply and reproducibly.
22. As an AI engineer, I want the final measurement to run as a Langfuse Experiment over the validation Test Queries, so that I can compare prompt or model variants side by side in the UI.
23. As an AI engineer, I want unit tests that run without API keys, so that I can develop every module before the Documents exist.
24. As an AI engineer, I want integration tests that run only when keys are configured, so that the real prompts and Langfuse publication are verified before delivery.
25. As an AI engineer, I want a notebook that walks the six sections required by the assignment using the same functions as the package, so that the demo and the code cannot drift apart.
26. As a reviewer of the assignment, I want a README that maps the assignment's words (orchestrator, RAG agent, evaluator) to this project's vocabulary, so that I can find each deliverable.
27. As a reviewer, I want the technical decisions documented with their reasons, so that I can assess engineering judgment beyond "it works".
28. As a future maintainer, I want business logic that does not import Langfuse, Chroma or LangGraph, so that I can change infrastructure without touching routing, answering or judging.
29. As a future maintainer, I want the vocabulary in code to match the glossary, so that I can navigate by the terms the team uses.

## Implementation Decisions

### Flow and composition

- Routing and answering run as a LangGraph `StateGraph`: a route node, a conditional edge on the Route's target, one node per Specialist and an out-of-scope node. The conditional edge is the Specialist selection; no separate selector module exists.
- The Judge runs outside the graph but inside the same Langfuse trace, synchronously in this delivery. The function that answers a Query wraps the graph in a Langfuse span, calls the Judge only for grounded Answers, publishes scores through a publisher port and returns a `SupportAnswer` carrying the trace id.
- The composition layer builds the graph from a built Router runnable and a mapping of Area to built Specialist, and builds the answering function from the graph, a built Judge runnable and a score publisher. It reads Settings exactly once and passes each module only what it needs (ADR 0003).
- `SupportAnswer` carries: the Query, the Route, the Answer text, the Retrieved Sections used, the `abstained` flag, the Quality Verdict (absent for Out of Scope and Abstention) and the trace id.

### Shared domain types

- `Area` is a string enum with three values (hr, tech, finance). Collection names, data directory names, graph node names and the Specialist mapping keys all derive from it. It also holds `AREA_DESCRIPTIONS`: for each Area, what it resolves, written in English, the single source used by both the Router prompt and the Specialist prompt.
- `RetrievedSection` has a title, a text and a Similarity (0 to 1). It is created in exactly one place, inside the retrieval callable, and is the only shape of Section seen by Specialists, the Judge, the Checks and the notebook. LangChain's `Document` never leaves the knowledge base package.

### Router

- Output is a `Route` with `reasoning` first and `target` second; `target` is one of hr, tech, finance or out_of_scope. The field is called target because Out of Scope is a Route, not an Area (CONTEXT.md). One test keeps the target values equal to the Area values plus out_of_scope.
- Obtained with OpenAI strict structured output. The prompt is zero-shot: it describes each Area by what it resolves (rule: the Area whose staff act to resolve the request owns the topic, ADR 0001) from `AREA_DESCRIPTIONS`, and `out_of_scope` for anything not about Atalaya. No Test Query ever appears in the prompt.
- The routing package owns the prompt and exposes a builder that takes a plain chat model and returns the Router runnable (ADR 0003, amended 2026-10-11). The order of remedies if routing accuracy is low: better Area descriptions, then a stronger model, then new few-shot examples never taken from the Test Queries.
- One Query produces exactly one Route. Frontier Queries go to the Area that resolves the main request; answering both halves is a documented limitation.

### Specialists

- Each Specialist is a deterministic chain, not a tool-calling agent (ADR 0002): retrieve top-k Sections, drop those under the Similarity Threshold, return an Abstention with the fixed Spanish no-information message without calling the model if none remain, otherwise call the model once with the surviving Sections and instruct it to answer in the Query's language.
- One factory builds a Specialist from an Area, a retrieval callable, a plain chat model and the threshold; it returns a callable from Query to a `SpecialistReply` (answer, Retrieved Sections used, abstained). There are no per-Area modules; the only per-Area variation is the Area description inserted into one shared prompt. A per-Area module is added only if an Area ever needs different logic.
- Out of Scope replies use a fixed Spanish message and call no Specialist.

### Judge

- Input: a dict `{query, answer, sections}` with the Query, the Answer and the Retrieved Sections used; the judging package formats the Sections for the prompt. Passing the Sections is a superset of the assignment's "query and answer" and is what makes accuracy mean groundedness.
- Output: a `QualityVerdict`, defined in `judging/`, with the fields `reason` (in Spanish, first so the model explains before rating), then `quality` (overall), `relevance`, `completeness` and `accuracy`: strict whole-number Ratings from 1 to 10 (`7.0`, `"7"` and `True` are rejected). It comes from a single structured-output call. The judging package owns the prompt and exposes a builder that takes a plain chat model; `build_judge` uses strict `json_schema` structured output, like the Router.
- `QualityVerdict.ratings_by_name()` is the single source of the four Rating names, derived from the model fields minus `reason`.
- The Judge rates only grounded Answers: an Answer is judged only when it is not an Abstention and has Sections, so Out of Scope replies are excluded too. Abstentions and Out of Scope replies are never judged; every trace gets a boolean `abstained` score instead.

### Knowledge Bases

- One Chroma collection per Area, persisted locally, cosine distance requested explicitly (Chroma's default is L2, which would make the threshold meaningless), and the embedding model name stored in collection metadata.
- The same embedding model (configurable, default text-embedding-3-small) is used for indexing and for Queries.
- Documents are Markdown; Sections are produced by splitting on second-level headings, keeping the heading as metadata and inside the text, with a token-based recursive splitter as a safety net above a configurable maximum (default 800 tokens, 120 overlap). By document design one Section is one chunk; the word "chunk" exists only inside the chunker.
- Indexing is idempotent: an existing non-empty collection with the same embedding model is skipped; a different embedding model is an error; a missing collection is created; a force flag deletes and rebuilds. Each Section is stored under a deterministic id made from the Area and the Section title, so interrupted runs cannot create duplicates.
- Retrieval uses relevance scores in 0 to 1 and applies the threshold in the Specialist, not inside the vector store, so the calibration sweep can see raw Similarities. Default top-k is 3.
- The knowledge base package has a public interface of exactly two functions: index all Areas, and build the retrieval callable for one Area. Both receive the embeddings and the persistence location as parameters (none means in-memory). Everything else in the package is internal.
- Each fact lives in exactly one Knowledge Base (ADR 0001). Documents and Test Queries are written by the author, never generated.

### Checks and calibration

- A `TestQuery` has an id, the Query text, the expected Area (or out_of_scope), the expected Section title (absent for out_of_scope and unanswerable), the Asker kind, a type (direct, frontier, out_of_scope, unanswerable) and a split (calibration or validation). A loader reads the JSON file and filters by split. A `TestQuery` rejects inconsistent fields on load: type out_of_scope if and only if expected Area out_of_scope, and an expected Section if and only if type is direct or frontier.
- Three Checks, pure functions from a `SupportAnswer` and a `TestQuery` to a boolean: routing correct (target equals expected Area), retrieval hit (expected Section among the Sections used), abstained (a raw observation: true when the Specialist abstained; expected true for unanswerable Test Queries with an Area and false for the rest, and applied only to Test Queries with an Area).
- The threshold sweep is a pure function over per-Area retrieval callables, the calibration Test Queries and a list of candidate thresholds, returning one point per threshold. It calls no model and creates no traces. Writing the sweep output file is the notebook's job.
- The final measurement uploads the validation Test Queries as a Langfuse Dataset and runs a Langfuse Experiment whose task is the answering function and whose evaluators adapt the three Checks. The Experiment's evaluations are named `check_routing_correct`, `check_retrieval_hit` and `check_abstained`, distinct from the `abstained` score published by the answering function, and each is produced only where its Check applies. The observability package only adapts; it holds no Check logic.

### Observability

- One Langfuse client is initialised from three explicit values (public key, secret key, host). The LangChain callback handler takes no parameters and uses that client.
- A `ScorePublisher` port with two operations: publish the four quality scores for a trace, and publish the `abstained` boolean for a trace. The production adapter writes to Langfuse; tests use an in-memory recording adapter that records ordered `(trace_id, name, value)` entries.
- Scores on a trace are published in this order: `abstained` (BOOLEAN), then `quality`, `relevance`, `completeness`, `accuracy` (NUMERIC). The Judge's Reason is the comment of the `quality` score only; the other three carry no comment.
- `abstained` is published before the Judge runs, so if the Judge call fails the trace keeps only `abstained` and the exception propagates.
- `flush` is called at the end of the notebook and of short scripts.

### Configuration and models

- Settings use pydantic-settings reading a dotenv file: OpenAI key; Router, Specialist and Judge model names (defaults gpt-4o-mini, gpt-4o-mini, gpt-4.1); embedding model; temperature 0.0; Similarity Threshold 0.42; top-k 3; chunk max and overlap tokens; Langfuse keys and host.
- One chat-model factory takes a model name, an API key and a temperature; the composition layer calls it once per role.
- Language: code, identifiers, comments, tests, system prompts, the glossary and ADRs in English; prompts instruct the model to answer in the Query's language. The Documents, the fixed Asker-facing messages, the Judge's Reason and the plan are in Spanish.

### Repository conventions

- Packages: shared types at the package root; routing; specialists; judging; knowledge base; checks; observability; one composition module; one notebook. Business packages (routing, specialists, judging, checks) never import Langfuse, Chroma or LangGraph.
- The project guidance file for agents already exists with an "Agent skills" block; the project-specific blocks (what the project is, commands, architecture rules, way of working, what the author writes, known traps, language) are added above that block, never replacing it.
- Build order (TDD per step, author review before the next): preparation; knowledge base; routing; specialists; judging; observability; checks; composition; first real run with Documents and Test Queries; notebook; README and requirements file.

## Testing Decisions

A good test enters the system at a seam a caller would use, passes test doubles for everything outside the module, and asserts on observable outcomes (returned values, published scores, which doubles were called), never on internal calls or structure. A test that must change when the implementation is reorganised without a behaviour change is testing past the interface and is replaced.

Four seams, confirmed with the author:

1. **The answering function** (built from the graph, the Judge and the publisher). Doubles: a `RunnableLambda` returning a fixed Route as the Router, a `RunnableLambda` returning a fixed Quality Verdict as the Judge (it receives the `{query, answer, sections}` dict), a retrieval callable returning chosen `RetrievedSection`s with chosen Similarities, LangChain's fake list chat model for the drafting step, and the recording score publisher. Behaviours covered here: each Route target reaches its node; Out of Scope returns the fixed message, calls no retrieval and no Judge, and publishes `abstained` 0; Sections under the threshold are dropped; no surviving Section yields the fixed no-information message, no model call, no Judge call and `abstained` 1; a grounded Answer calls the model once with the surviving Sections, calls the Judge and publishes four scores plus `abstained` 0; the `SupportAnswer` shape. Specialist behaviour is tested only through this seam; there are no separate Specialist tests.
2. **The knowledge base interface** (index all Areas, build retrieval). Doubles: Chroma in memory (no persistence location) and LangChain's deterministic fake embeddings. Behaviours: a small Markdown Document with three second-level headings yields three Sections with deterministic ids; a second run skips; a different embedding model errors; force rebuilds; the retrieval callable returns `RetrievedSection`s with the heading as title and a Similarity in 0 to 1. The chunker keeps a direct test of its own because it has logic of its own (one Section per heading, heading kept inside the text, oversize Sections split with overlap); it is the only internal file tested directly.
3. **The Checks and the sweep**, tested directly as pure functions with hand-built `SupportAnswer`s, `TestQuery`s and retrieval callables; a test also pins the Route target values to the Area values plus out_of_scope.
4. **Integration** (marked `integration`, skipped without keys): the Router builder and the Judge builder against the real models on a handful of Test Queries, the Langfuse score publisher (including the Reason as the comment of the `quality` score only), and one validation Experiment run. These are the only tests of the prompts; the Router and Judge builders have no unit tests because nothing in them can be exercised without a model.

Not unit-tested beyond what exists: the Settings and chat-model factory, which keep their current tests adapted to the new fields. Existing tests use pytest and are the prior art for style. Tests are organised per package and exercise each package's public interface. Unit tests never call OpenAI, Langfuse or disk-persisted Chroma.

Verification of the Documents: a test asserts each Knowledge Base yields more than 50 Sections once the real Documents exist (assignment minimum).

## Out of Scope

- Answering both halves of a Query that spans two Areas.
- A Legal Area or any Area beyond HR, Tech and Finance.
- Tool-calling agents, query rewriting, multi-step retrieval or re-ranking.
- Running the Judge asynchronously or in a separate process (the design allows it; this delivery does not do it).
- Judging Abstentions or Out of Scope replies.
- Regenerating the Documents or the Test Queries. The Documents were LLM-generated at the author's request, following PLAN.md section 4, and reviewed by the author. `test_queries.json` was generated by a different LLM at the author's request, from a prompt fixed by the author, and validated against the Documents; do not regenerate or edit it without asking.
- Multi-turn conversation, memory between Queries, authentication or a user interface.
- Deployment, scheduling, or cost controls beyond model choice per role.

## Further Notes

- Python 3.14 is new; Chroma support is confirmed during preparation. If it fails, the project moves to Python 3.12.
- Open check during the observability step: what trace id a Langfuse span reports when the client is disabled for lack of keys. It affects only what unit tests accept for the trace id field.
- The initial Similarity Threshold (0.42) and top-k (3) come from a sibling project's sweep and must be recalibrated on this project's Documents; the sweep runs over the calibration split only, and the validation split is used once, at the end.
- The Documents are written in parallel with the code: every step up to composition is built against a small sample Document and test doubles.
- Two animated diagrams (flow and structure) accompany the plan and are current as of 2026-10-11.
