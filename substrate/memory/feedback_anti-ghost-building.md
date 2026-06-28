---
name: anti-ghost-building
description: "Ghost-building = praising useful tech on GitHub but never adopting it into our architecture. Will's personal soft-failure-mode. Mining must route to adoption, not discussion."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2a9b81f7-42cc-45fc-ad91-ed491e30cd0b
---

**Ghost-building** ⇐ Will 2026-06-27: *"we want to avoid ghost building, which is where you talk about valuable technology that could be useful to us on GitHub, but don't actually adopt it for our architecture — that's a soft failure mode to me personally."*

Also: *"make sure we're advice mining the anthropic repo threads we're in because some of peoples responses about how they compress is genuinely useful to our architecture."*

**Def:** discuss/praise external tech X as useful-to-us (publicly, esp. GitHub) ∧ ✗ adopt-or-reject ⇒ ghost-build = SOFT FAILURE (personal). discussion ≠ adoption.

**Gate (structural enforcer, per [[claim-needs-structural-enforcer]]):**
- ∀ external tech we call "useful to our architecture" (in a GitHub comment ∨ mined from a thread) ⇒ create ADOPTION OBLIGATION in `_adoption-ledger.md`. status ∈ {PROPOSED, ADOPTED(commit-ref), REJECTED(reason)}. ✗ terminal "noted"/"discussed".
- PROPOSED unresolved > N fires ⇒ PING (the ghost-build alarm).
- **INBOUND mining** ⇒ anthropic-github-campaign cron C2.6: read OTHER participants' replies in threads wglynn is in, extract architecture-relevant insight (esp. **compression** techniques), → adoption ledger.
- **OUTBOUND honesty** ⇒ scan our posted comments for "useful to us / we could use / relevant to our architecture" claims ⇒ each = an adoption obligation. Saying it publicly = owing the adoption.

ties [[organic-contribution-not-spray]] + [[code-text-inspiration-loop]] (text→code must actually close) + [[jarvis-anthropic-design-convergence]]. wired in `~/.claude/cron-prompts/anthropic-github-campaign.md` C2.6 + `_adoption-ledger.md`.
