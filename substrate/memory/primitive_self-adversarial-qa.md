---
name: SelfAdversarialQA
description: ∀ substantive code-write or design-decision ⇒ run N rounds of self-Q&A asking hypothetical critical questions BEFORE declaring complete. Find weak spots by interrogating own work as if hostile reviewer arrived next. Origin Rick TG 2026-06-10 — his "how does this work? who is doing the default prompt assessment?" exposed regex-only first-match-wins weakness in coordination-mechanism-gate that I hadn't asked myself. Sibling of [P·adoption-roleplay] (outside-vantage critique on partner artifacts); this is SELF-vantage critique on internal code.
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Self-Adversarial Q&A

## Glyph

```
∀ substantive-code-write ⇒ self-Q&A BEFORE ship-claim
mechanism:
  pick N critical-question categories
  for each: ask one hostile-reviewer question
  attempt honest answer
  surface uncertainty / hidden assumption / edge-case
  fix or annotate, then ship
N ≥ 3 (one per category-tier)
exit: ∀ N rounds returned "no new weakness found" ⇒ discovery-ceiling per [P·discovery-ceiling]
```

> *"Q&A rounds where you ask yourself hypothetically critical questions to find weak spots in our own code"* — Will, 2026-06-10

## ∃ Why

- 2026-06-10 Rick TG question "how does this work? who is doing the default prompt assessment?" exposed regex-only weakness in coordination-mechanism-gate
- Three reply-drafts collapsed when actual research returned opposite answer
- Critical question Rick asked ≡ the question I should have asked MYSELF before shipping the hook
- Pattern: hostile-reviewer-Q&A surfaces weak spots the implementer misses
- Sibling of [P·adoption-roleplay] (outside-vantage on partner artifacts); this is SELF-vantage on internal code

## ⇒ Rule

- ∀ shipped code (hook, skill, script, primitive, contract) ⇒ run ≥3 self-Q&A rounds
- ≥3 ≡ cover ≥3 of the 8 categories below
- if any round surfaces uncertainty/hidden-assumption/edge-case ⇒ fix or annotate
- ∀ N consecutive rounds with no new finding ⇒ discovery-ceiling reached, ship

## ↦ Question categories (8 tiers, pick ≥3)

1. **Mechanism transparency** — "Who/what is actually doing X? What's the literal answer?"
2. **Edge cases** — "What about empty input? Massive input? Adversarial input? Concurrent?"
3. **Confidence exposure** — "How confident is the output? Does the consumer know?"
4. **Failure modes** — "What happens when X fails? Are failures visible or silent?"
5. **Counterfactual** — "What if I'm wrong about the central assumption? Would I notice?"
6. **Adversarial** — "If someone wanted to break this, how would they?"
7. **Composition** — "How does this interact with existing system? What's the integration surface?"
8. **Honesty** — "Is this fact-grounded or am I extrapolating? Did I verify or assume?"

## ⇒ Skill invocation

- `/critical-qa <code-area>` ⇒ runs the pattern explicitly
- skill body: takes the artifact under review, generates 3+ hostile-reviewer questions across distinct categories, attempts honest answers, surfaces weak spots
- output: structured findings + fix recommendations

## ↦ Apply To

- ∀ hook write (PreToolUse / PostToolUse / Stop / etc.)
- ∀ Solidity contract function
- ∀ CKB cell-script
- ∀ Python script that handles partner-facing data
- ∀ memory primitive at promotion-time (does the rule survive its own counter-example?)
- ⊥ trivial fixes (typo, formatting) — exempt
- ⊥ already passed adoption-roleplay AND severity-calibration — diminishing returns

## ⊥ Anti-pattern

- ✗ asking softball questions (charitable-reader fail)
- ✗ stopping at first weak spot found (one round ¬ enough)
- ✗ answering "no, that's fine" without verifying
- ✗ skipping when code is "obvious" (Rick-exposed regex was "obvious" until it wasn't)
- ✗ confusing with [P·adoption-roleplay] — different vantage (self vs outside)

## ↦ Compose with

- [F·no-bullshit-do-the-research] (AA#4) — research IS the answer-honest move
- [P·adoption-roleplay] — outside-vantage sibling; both axes load-bearing
- [P·recursive-self-audit-via-wwwd] (RSAW) — multi-agent parallel form of this same impulse
- [P·discovery-ceiling] — stop condition when N rounds find nothing new
- [P·apply-the-rule-you-just-wrote] — apply this primitive to itself before shipping

## ⇒ Self-Apply (this primitive, right now)

R1 Mechanism transparency: "Who runs the Q&A?" A: Me, manually, OR via `/critical-qa` skill invocation. No automated trigger. → weak spot: relies on discipline.

R2 Edge cases: "What if I run Q&A on something trivial?" A: anti-pattern list says trivial fixes exempt. → covered.

R3 Honesty: "Did I just invent the 8 categories?" A: yes, from the Rick-exposed pattern + general critical-thinking taxonomy. Not citation-grounded; could be refined with hostile-reviewer literature. → annotated.

R4 Adversarial: "Can someone game this by asking 3 trivial questions and shipping?" A: yes, if they choose 3 softball categories. → mitigation: "anti-pattern softball questions" listed, but not enforced.

R5 Composition: "How does this interact with AdoptionRoleplay?" A: AdoptionRoleplay = outside-vantage on partner artifacts; SelfAdversarialQA = self-vantage on internal code. Different domain. Both load-bearing per the new primitive.

→ ship with discipline-dependence noted as known weakness; gate hook could enforce later but not in v1.
