---
status: accepted
---

# Specialists are deterministic chains, not tool-calling agents

The assignment calls them "RAG agents" and LangChain offers `create_agent` with the retriever as a tool, which would be the obvious path. We implement each Specialist as a fixed sequence instead: retrieve Sections, drop those below the Similarity Threshold, abstain without calling the model when none remain, otherwise call the model once with the surviving Sections. A tool-calling agent would run the model before retrieval (so abstention could not skip it), could rewrite the Query before searching (so the threshold could not be calibrated against the exact Test Queries), and would produce traces of varying shape (so misroutes and failed retrievals would be harder to compare in Langfuse). One Query needs one search and one Answer; an agent loop adds latency, cost and non-determinism without adding capability.

## Considered options

- `create_agent` with the retriever as a tool: rejected for the reasons above.
- A deterministic chain per Area, composed as nodes of a LangGraph `StateGraph`: chosen. The graph owns routing; each node owns one Area.
