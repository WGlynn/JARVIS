---
name: "Generalize Solutions — Solve Classes, Not Instances"
description: When creating protocols, primitives, or fixes, always generalize beyond the triggering incident so they address the full class of problem, not just the specific case.
type: feedback
---

Always generalize solutions so they tackle larger groups of issues in the future, not just the specific incident that triggered them.

**Why:** A fix scoped to one incident protects against that exact scenario repeating. A fix scoped to the failure class protects against every variant. The marginal cost of generalizing at write-time is near zero. The cost of discovering the same class of failure again in a different domain is a full credibility hit each time.

**How to apply:** When writing any protocol, primitive, or gate:
1. Identify the specific failure that triggered it
2. Abstract to the failure *class* — what's the general pattern?
3. Write the solution against the class, using the incident as one example
4. Test mentally: "Does this gate catch the same failure in a completely different domain?" If not, it's too narrow.

Origin: Citation Hygiene Gate (2026-04-04). First draft was model-assessment-specific. Will flagged it — generalized to any claim grounded in external evidence across all domains.
