---
name: NoBullshitDoTheResearch
description: ∀ factual answer ⇒ verify before asserting. ✗ speculate-then-frame-as-known. ✗ "I think X / probably Y / likely Z" laundered as fact. When uncertainty exists, WebSearch / gh / Read first, answer second. Standing rule per Will 2026-06-10. Elevated to **AA#4 anti-hallucination gate candidate** — 4-draft → research → opposite-answer demonstrated structural inadequacy of speculation. Hook design sketched below.
type: feedback
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# No Bullshit — Do the Research

## ⇒ Rule

- ∀ factual claim ⇒ verify before assert
- ✗ speculation laundered as fact
- ✗ "probably / likely / I think" wrapped as confident answer
- ✓ WebSearch / gh / Read / WebFetch ⇒ answer-grounded
- if uncertainty remains AFTER research ⇒ state explicitly

> *"no bullshit answers do the proper research"* — Will, 2026-06-10
> *"is a rule now ... because it works"* — Will, 2026-06-10 (same turn, promotion)

## ∃ Why

- 2026-06-10 incident: 3 successive drafts on Rick-OpenAI question
  - draft 1 (no research) ⇒ "not yet, anthropic-only, hermes does it" ⇒ wrong frame
  - draft 2 (still no research) ⇒ "llm-agnostic by design, TG bot does it" ⇒ off-target (Rick asked about overlay, not bot)
  - draft 3 (still no research) ⇒ "overlay substrate-agnostic, harness needs adapting" ⇒ vague
  - draft 4 (research done: Codex CLI ships hook system w/ CLAUDE_PLUGIN_ROOT compat) ⇒ specific, accurate, actionable
- 4 rounds of correction collapsed to 1 round when research came FIRST
- "because it works" ≡ structural validation of the rule

## ↦ Apply To

- ∀ partner-facing claim about technical product capability
- ∀ feature comparison ("does X support Y")
- ∀ ecosystem statement ("Z does W today")
- ∀ "I believe" / "I think" / "probably" — flag as unverified OR research
- ⊥ purely-internal reasoning ⇒ exempt (chain-of-thought is OK uncertain)
- ⊥ Will-emulation projections (WWWD) ⇒ that's by design speculative

## ⊥ Anti-pattern catalog

- ✗ asserting product capability from memory of marketing posts
- ✗ extrapolating from "this is the kind of thing X usually supports"
- ✗ confident-sounding wrappers on uncertain content
- ✗ partner-reply drafts that read clean but aren't grounded in current state
- ✗ skipping verify when the cost is one WebSearch

## ↦ Compose with

- [F·sound-human-no-ai-tells] — sister-rule, voice axis
- [F·respond-with-solution-not-problem] — both halve round-trips
- [P·anti-stale-feed] — verify-current-state-before-asserting (parent pattern)
- [F·apply-the-rule-you-just-wrote] — apply this to next reply
- [P·proactive-nash-equilibrium-no-harm-fixes] — research IS the no-harm move

## ⇒ AA#4 promotion (Will 2026-06-10)

> *"look how just a little research literally gave you the opposite of your original answer, this is an anti-hallucination gate worthy finding"* — Will, 2026-06-10

**Credit: Rick Beato (usd8.fi / OpenZeppelin), TG 2026-06-10.** Rick's question — *"how does this work? who is doing the default prompt assessment?"* — exposed the regex-only first-match-wins weakness in coordination-mechanism-gate.py. Three speculative reply-drafts collapsed when actual research (WebSearch) returned the opposite answer (Codex CLI ships claude-compatible hook system w/ CLAUDE_PLUGIN_ROOT env var). The AA#4 anti-hallucination gate exists because Rick poked at it. Attribution holds in the contribution graph: [P·shapley-5-axiom-set] applied to substrate-improvement contributions.

Joins the Audit Arsenal:
- AA#1 [P·audit-fork-loses-hardness]
- AA#2 [F·claim-needs-structural-enforcer]
- AA#3 [F·entity-context-cross-reference]
- **AA#4 [F·no-bullshit-do-the-research]** — research-before-asserting-product-capability

Sibling-of and shares-shape-with the existing anti-hallucination gates already firing:
- `time-logic-gate.py` — temporal-claims without anchor
- `entity-attribution-gate.py` — @-handle verification
- `conflict-detector.py` — entity-negation in memory
- `partner-facing-substance-gate.py` — claim-handshake

Gap covered: the existing gates catch TIME / ENTITY / CONFLICT / SUBSTANCE. None catch PRODUCT-CAPABILITY-ASSERTION-WITHOUT-RESEARCH. AA#4 fills that.

## ↦ Hook design sketch (Will-approval gated, NOT yet shipped)

```
location: ~/.claude/hooks/research-before-capability-claim-gate.py
event: PreToolUse Write|Edit
matcher: partner-facing path + draft body contains capability-claim patterns
patterns to detect:
  - "(does|doesn't|supports|works with|runs on) [product-name]"
  - "[product] (has|lacks|added|removed) [feature]"
  - "(tier|version) N of [product]"
  - "[product] only/never/always [action]"
  - "no [vendor] subscription"  (the literal Rick-question shape)
action:
  - count capability-claim hits
  - if count >= 1 AND no prior WebSearch / WebFetch / gh in last N tool calls:
      emit additionalContext = "Capability claim detected: '<sample>'. AA#4 gate suggests verification before write. Run WebSearch or WebFetch first."
  - if research was done recently (within last 5 tool calls): silent (already grounded)
output: augmentation, not block
```

Hook would have prevented all 3 wrong drafts on the Rick-OpenAI question. Build cost ~50 LoC.

## ↦ Holding for Will-approval

Substrate-modifying. PreToolUse on Write/Edit is critical-path. Hold before ship.
