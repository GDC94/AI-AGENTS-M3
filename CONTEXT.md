# Support Routing

Routes support queries from Atalaya Data's clients and staff to the area that can resolve them, answers from that area's documentation, and rates each answer. One context: routing, answering and judging share the same language.

## Language

### Who asks

**Query**:
A single question sent to the system by an Asker.
_Avoid_: ticket, consulta, question, request

**Asker**:
The person who sends a Query: either a Client or Staff.

**Client**:
A user from a customer organisation (a public administration) that uses the Atalaya platform.
_Avoid_: customer, user, organismo

**Staff**:
An Atalaya employee or consultant.
_Avoid_: employee, personal, internal user

### Routing

**Area**:
One of the three departments that can resolve a Query: HR, Tech or Finance.
_Avoid_: category, domain, department, intent

**Router**:
The component that reads a Query and produces a Route.
_Avoid_: orchestrator, intent classifier, dispatcher

**Route**:
The Router's decision for a Query: the single Area that resolves its main request, or Out of Scope. A Query never has more than one Route.
_Avoid_: classification, intent, category

**Out of Scope**:
A Route meaning the Query is not about Atalaya at all, so no Area can resolve it.
_Avoid_: unknown, unrelated, other

**Frontier Query**:
A Query whose topic touches two Areas. It is routed to the Area whose staff act to resolve it, not to the Area the topic sounds like.
_Avoid_: ambiguous query, edge case

### Answering

**Specialist**:
The component that answers Queries of one Area, grounded only in that Area's Knowledge Base.
_Avoid_: agent, RAG agent, node, expert

**Answer**:
The text returned to the Asker for a Query: a Specialist's grounded reply, an Abstention, or the Out of Scope reply.
_Avoid_: response, output, completion

**Abstention**:
A Specialist's Answer stating that its Knowledge Base does not cover the Query. Differs from Out of Scope: the Query belongs to the Area, but is undocumented.
_Avoid_: no information, fallback, refusal

### Knowledge

**Knowledge Base**:
The set of Documents owned by one Area. Each fact lives in exactly one Knowledge Base.
_Avoid_: collection, vector store, library, docs

**Document**:
One source file inside a Knowledge Base.
_Avoid_: manual, policy file

**Section**:
A single-topic unit of a Document, and the unit that is retrieved to ground an Answer.
_Avoid_: chunk, passage, fragment, paragraph

**Similarity**:
How closely a Section matches a Query, from 0 to 1. Sections below the Similarity Threshold are not used.
_Avoid_: score, distance, relevance score

**Similarity Threshold**:
The minimum Similarity a Section needs to be used in an Answer.
_Avoid_: cutoff, min score

### Judging

**Judge**:
The component that rates a grounded Answer against its Query and the Sections used to produce it. Abstentions and Out of Scope replies are counted, never judged.
_Avoid_: evaluator, evaluator agent, grader, critic

**Quality Verdict**:
The Judge's result for one Answer: an overall Rating, one Rating per Dimension, and a Reason.
_Avoid_: score, evaluation, grade

**Rating**:
A whole number from 1 to 10 given by the Judge.
_Avoid_: score, points, grade

**Dimension**:
One aspect the Judge rates separately: Relevance, Completeness or Accuracy.
_Avoid_: metric, criterion, axis

**Check**:
A deterministic pass/fail comparison of a system result against a Test Query's expectation, such as whether the Route matched.
_Avoid_: evaluator, assertion, metric

### Testing

**Test Query**:
A Query with a known expected Route and, when applicable, expected Section, used to measure the Router, the Similarity Threshold and Abstention.
_Avoid_: sample, example, fixture
