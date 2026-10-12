---
status: accepted
---

# The Similarity Threshold is calibrated for recall and does not catch unanswerable Queries

The plan expected a "good zone" of Similarity Thresholds that keeps every answerable Test Query's expected Section and still blocks the unanswerable ones, as in the sibling project. The calibration sweep in ticket 08 (`outputs/threshold_sweep.json`, top-k 4, 29 calibration Test Queries with an Area) found no such zone on these Documents. The lowest expected Section of an answerable Query has Similarity 0.408 (hr-05). The best Section of an unanswerable Query reaches 0.620 (hr-13, marriage leave, which is close to sick leave and vacations). The first threshold that blocks any unanswerable Query (0.50) already loses three answerable ones. Similarity measures topic, not whether the requested fact exists, and the unanswerable Test Queries share topics with real Sections.

We set the Similarity Threshold to 0.325, the middle of the zone with maximum retrieval hits (0.25 to 0.40), and accept that Abstentions for unanswerable Queries will mostly not happen. The Specialist's prompt still tells the model to say what the Sections do not cover, and the validation Experiment reports the `check_abstained` result as it is. A reader who sees unanswerable Queries answered should not raise the threshold: it trades answerable Queries for blocked ones, one for one or worse.

## Considered options

- A higher threshold (0.50 to 0.625): rejected; it blocks 1 to 5 of 5 unanswerable Queries at the cost of 3 to 18 of 24 answerable ones.
- Let the model decide the Abstention (a structured "covered / not covered" output in the Specialist): not taken in this project; it changes ADR 0002's rule that an Abstention never calls the model and needs its own calibration.
- Threshold for recall, Abstention by threshold only: chosen.
