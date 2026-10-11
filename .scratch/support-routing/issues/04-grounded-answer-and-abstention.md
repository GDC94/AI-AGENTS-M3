# 04: Grounded Answer and Abstention end to end

**What to build:** an Asker sends an HR Query that the sample Document covers and receives an Answer grounded in the retrieved Sections, listed in the `SupportAnswer`. An Asker sends an HR Query the Document does not cover and receives the fixed no-information message (an Abstention) without any model call, with an `abstained` score of 1 on the trace. The same works for Tech and Finance. The Judge is not yet involved: the verdict stays empty.

**Blocked by:** 02 (Out of Scope end to end), 03 (Knowledge Base: index and retrieve).

**Status:** done

Scope (PRD "Specialists", "Flow and composition"; ADR 0002, ADR 0003):

- One Specialist factory taking an Area, a retrieval callable, a plain chat model and the Similarity Threshold; returns a callable from Query to `SpecialistReply` (answer, Retrieved Sections used, abstained). One shared prompt that inserts `AREA_DESCRIPTIONS[area]` and instructs the model to answer in the Query's language. No per-Area modules.
- Chain: retrieve top-k, drop Sections under the threshold, abstain with the fixed Spanish message and no model call when none remain, otherwise one model call with the surviving Sections.
- The three Area nodes of the graph call their Specialist; the placeholders from ticket 02 are replaced. The composition layer builds the three Specialists from the enum and the real retrieval callables and chat model.
- `SupportAnswer` carries the Sections used and the `abstained` flag; the answering function publishes `abstained` 1 on Abstention and 0 on a grounded Answer.

- [x] Seam 1 test with a fake retrieval callable and a fake list chat model: Sections under the threshold are dropped before drafting.
- [x] Seam 1 test: when no Section survives, the Answer is the fixed no-information message, the chat model is never called, and one `abstained` score with value 1 is recorded.
- [x] Seam 1 test: when Sections survive, the chat model is called exactly once with those Sections in its input, the Answer is the model's text, the `SupportAnswer` lists those Sections, and `abstained` 0 is recorded.
- [x] Seam 1 test: the same behaviour holds when routed to each of the three Areas.
- [x] Integration test: against the persisted index from ticket 03 and the real Specialist model, a covered Query returns a grounded Answer citing the expected Section and an uncovered Query returns the Abstention.
- [x] Business packages still import no Langfuse, Chroma or LangGraph symbols.

## Comments

**2026-10-11, author:** approved.

Implementer choices approved by the author:

- No permanent index exists after ticket 03, so the integration test builds one the same way: an HR sample fixture, the real embedding model and Chroma persisted in a temporary directory.
- The integration test uses a fixed Router that always returns hr, so a failure points at the Specialist; the real Router has its own integration test (ticket 02).
- A Section whose Similarity equals the Similarity Threshold is kept; only Sections below it are dropped.
- The Specialist prompt asks the model to cite each Section title in square brackets, for example `[Annual leave]`; titles are passed to the prompt explicitly.
- `NO_INFORMATION_MESSAGE`: "Lo siento, la documentación disponible no cubre tu consulta. Te recomendamos contactar directamente al equipo correspondiente."
- The composition layer exposes `build_specialists(retrieve_by_area, chat_model, threshold)`.
- `tests/test_layering.py` guards that business packages import no Langfuse, Chroma or LangGraph.

Findings:

- Measured Similarities in the integration fixture against the 0.42 threshold: covered Query 0.654, uncovered Query 0.252.
- Specialists are tested only through `answer_query`, as the PRD requires; a reviewer request for a separate `tests/specialists/` package was declined for that reason.
- Test runs: 53 unit tests passed; 8 integration tests passed with real keys.
