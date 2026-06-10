---
name: NoBullshitDoTheResearch
description: ∀ factual answer ⇒ verify before asserting. ✗ speculate-then-frame-as-known. ✗ "I think X / probably Y / likely Z" laundered as fact. When uncertainty exists, WebSearch / gh / Read first, answer second. Standing rule per Will 2026-06-10 after speculative claim about JARVIS+OpenAI portability was corrected by actual research (Codex CLI ships claude-compatible hook system w/ CLAUDE_PLUGIN_ROOT env var). Validated with "because it works".
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
