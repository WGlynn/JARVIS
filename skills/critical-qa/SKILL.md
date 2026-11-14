---
name: critical-qa
description: Self-adversarial Q&A on a code artifact. Run hostile-reviewer questions across ≥3 distinct categories (mechanism / edge / confidence / failure / counterfactual / adversarial / composition / honesty), attempt honest answers, surface weak spots. Per [P·self-adversarial-qa] (a partner chat) origin). Use BEFORE declaring code complete; sibling of /classify but on the quality axis not the cost axis.
---

# /critical-qa — self-adversarial Q&A

You are the implementer of a code artifact. A hostile reviewer is about to arrive. Pre-empt them by asking the questions YOU would ask if you were the reviewer.

Input: `$ARG` = code area / file / function / hook to interrogate.

## Question categories (pick ≥3 distinct)

1. **Mechanism transparency** — Who/what is literally doing X? Name the answer.
2. **Edge cases** — Empty / massive / adversarial / concurrent input?
3. **Confidence exposure** — Does output convey its own confidence? Silent failures?
4. **Failure modes** — What fails? Loud or quiet?
5. **Counterfactual** — If my central assumption is wrong, would I notice?
6. **Adversarial** — How would someone break this?
7. **Composition** — Integration surface with existing system?
8. **Honesty** — Verified or extrapolated?

## Output shape

```
## /critical-qa on <$ARG>

### R1 [category]
Q: <hostile question>
A: <honest answer; if uncertain, say so>
→ <weak spot found OR confirmed-ok>

### R2 [different category]
...

### R3 [different category]
...

## Findings
- <fixable now>
- <annotate as known weakness>
- <surface to operator for decision>

## Verdict
[ship | revise | research-needed | escalate]
```

## Rules

- ≥3 rounds across ≥3 distinct categories
- no softball questions (anti-pattern: "is this code clean? yes")
- if answer is "I don't know" — surface as research-needed
- if N consecutive rounds find nothing new → ship per [P·discovery-ceiling]
- compose with /classify (cost-axis) for spawn decisions

## Sibling

- Code-side companion to [P·adoption-roleplay] which is partner-artifact-side.
- Use this on YOUR OWN code; use AdoptionRoleplay on artifacts going to partners.
