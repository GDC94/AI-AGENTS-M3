# 04: Grounded Answer and Abstention end to end

**What to build:** an Asker sends an HR Query that the sample Document covers and receives an Answer grounded in the retrieved Sections, listed in the `SupportAnswer`. An Asker sends an HR Query the Document does not cover and receives the fixed no-information message (an Abstention) without any model call, with an `abstained` score of 1 on the trace. The same works for Tech and Finance. The Judge is not yet involved: the verdict stays empty.

**Blocked by:** 02 (Out of Scope end to end), 03 (Knowledge Base: index and retrieve).

**Status:** ready-for-agent

Scope (PRD "Specialists", "Flow and composition"; ADR 0002, ADR 0003):

- One Specialist factory taking an Area, a retrieval callable, a plain chat model and the Similarity Threshold; returns a callable from Query to `SpecialistReply` (answer, Retrieved Sections used, abstained). One shared prompt that inserts `AREA_DESCRIPTIONS[area]` and instructs the model to answer in the Query's language. No per-Area modules.
- Chain: retrieve top-k, drop Sections under the threshold, abstain with the fixed Spanish message and no model call when none remain, otherwise one model call with the surviving Sections.
- The three Area nodes of the graph call their Specialist; the placeholders from ticket 02 are replaced. The composition layer builds the three Specialists from the enum and the real retrieval callables and chat model.
- `SupportAnswer` carries the Sections used and the `abstained` flag; the answering function publishes `abstained` 1 on Abstention and 0 on a grounded Answer.

- [ ] Seam 1 test with a fake retrieval callable and a fake list chat model: Sections under the threshold are dropped before drafting.
- [ ] Seam 1 test: when no Section survives, the Answer is the fixed no-information message, the chat model is never called, and one `abstained` score with value 1 is recorded.
- [ ] Seam 1 test: when Sections survive, the chat model is called exactly once with those Sections in its input, the Answer is the model's text, the `SupportAnswer` lists those Sections, and `abstained` 0 is recorded.
- [ ] Seam 1 test: the same behaviour holds when routed to each of the three Areas.
- [ ] Integration test: against the persisted index from ticket 03 and the real Specialist model, a covered Query returns a grounded Answer citing the expected Section and an uncovered Query returns the Abstention.
- [ ] Business packages still import no Langfuse, Chroma or LangGraph symbols.
