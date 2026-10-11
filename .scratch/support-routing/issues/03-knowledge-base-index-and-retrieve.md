# 03: Knowledge Base: index and retrieve

**What to build:** a Markdown Document can be indexed into an Area's Knowledge Base once, and a Query against that Knowledge Base returns the most similar Sections as `RetrievedSection`s with a Similarity between 0 and 1. Re-running the indexing is free, a mismatched embedding model is refused, and a forced rebuild is possible.

**Blocked by:** 01 (Preparation and shared domain types). Can run in parallel with 02.

**Status:** done

Scope (PRD "Knowledge Bases"; ADR 0001):

- Public interface of the knowledge base package is exactly two functions: index all Areas, and build the retrieval callable for one Area. Both take the embeddings and the persistence location (none means in-memory). Everything else in the package is internal.
- Sections come from splitting on second-level headings, keeping the heading as metadata and inside the text, with a token-based recursive splitter above the configured maximum (800 tokens, 120 overlap). "Chunk" is a word that appears only inside the chunker.
- One Chroma collection per Area, cosine distance requested explicitly, embedding model name stored in the collection metadata.
- Indexing is idempotent: existing non-empty collection with the same model is skipped and reported; different model is an error; missing collection is created; `force` deletes and rebuilds. Each Section is stored under a deterministic id derived from the Area and the Section title.
- Retrieval returns relevance scores in 0 to 1, top-k from configuration, and converts to `RetrievedSection` in exactly one place. No threshold is applied here.

Open decision to confirm with the author (do not invent): the small sample Document used by the tests is a test fixture written by the implementer, not an Atalaya Document; the author keeps writing the real Documents under the data directory.

- [x] Seam 2 test, in-memory Chroma with deterministic fake embeddings: a sample Document with three second-level headings yields three stored Sections with the deterministic ids.
- [x] A second indexing run with the same model skips the Area and reports it; indexing with a different embedding model name raises an error; `force` rebuilds without duplicates.
- [x] The retrieval callable returns `RetrievedSection`s whose titles are the headings and whose Similarities are between 0 and 1, at most top-k of them.
- [x] Chunker test: one Section per heading, heading text present inside the Section text, a Section above the token maximum is split with the configured overlap.
- [x] Integration test: indexing the sample Document with the real embedding model into the persisted directory and retrieving a Query returns the expected Section first.
- [x] LangChain's `Document` type is not referenced outside the knowledge base package.

## Comments

**2026-10-11, author:** approved. Open decision confirmed: the sample Document used by the tests is a test fixture written by the implementer, not an Atalaya Document. Also confirmed: negative cosine Similarities are clamped to 0 where `RetrievedSection` is created.

Implementer choices approved by the author:

- Text before the first second-level heading (title, version line, introduction) is not a Section and is dropped.
- A Section above the token maximum is split into parts that each repeat the heading; part ids are `<area>:<title>:<part>`.
- Similarity is computed as 1 minus the cosine distance (`similarity_search_with_score`), the same value as LangChain's relevance score, without its out-of-range warning. PLAN.md section 3.6 still names `similarity_search_with_relevance_scores`.
- Errors are `ValueError` with a clear message, so the public interface stays at two functions. A missing or empty `<area>_docs` directory is an error.
- `index_all_areas` returns `"indexed"` or `"skipped"` for each Area.
- Collections are named `knowledge_base_<area>` because Chroma requires names of at least three characters.

Findings:

- Retrieving from an Area that was never indexed raises an error instead of silently creating an empty L2 collection.
- `force` reads and splits the Documents before deleting a collection, so a failed rebuild keeps the old Knowledge Base.
- Two Sections with the same title in one Area make indexing fail with Chroma's `DuplicateIDError`.
- Test runs: 45 unit tests passed; 7 integration tests passed with real keys.
