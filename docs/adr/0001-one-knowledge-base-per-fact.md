---
status: accepted
---

# Each fact lives in exactly one Knowledge Base

The Router is measured by comparing its Route against the expected Area of each Test Query. If the same fact were documented in two Knowledge Bases (for example, payroll dates in both HR and Finance), two Routes would be equally correct and routing accuracy would be unmeasurable. We therefore place every topic in the Knowledge Base of the Area whose staff act to resolve it, never in two, even when the topic sounds like it belongs elsewhere. Frontier topics are split by that rule: when a salary is paid is Finance, when it is reviewed is HR.

## Consequences

- Writing the Documents requires deciding an owner for every topic before writing it; `CONTEXT.md` defines Frontier Query for this.
- A Query spanning two Areas gets one Route and a partial Answer. This is a documented limitation, not a bug.
