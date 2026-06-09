---
name: Jay Berg / Sidepit — personal history context
description: Jay Berg (Sidepit founder) told Will he couldn't build a DEX with AI. Will built VibeSwap with Jarvis. VibeSwap's commit-reveal batch auction mechanism formally dominates Sidepit's DLOB against the MEV threat both claim to address. Load before any Jay Berg / Sidepit discussion.
type: reference
originSessionId: 117e2fd9-3ef3-4610-a5b4-d4280a0b96cb
---
# Jay Berg / Sidepit — personal history context

**Load trigger**: any mention of Jay Berg, Sidepit, DLOB, or the First-Available Trap paper (`vibeswap/DOCUMENTATION/FIRST_AVAILABLE_TRAP.md`).

## What happened

Will consulted for Sidepit Exchange (pre-VibeSwap era; see `docs/bd-output/will-glynn-builder-profile.md:61`). During that engagement, Jay Berg (Sidepit founder, ex-Wall Street HFT) told Will he **couldn't build a DEX with AI**. The consulting relationship ended badly — Will's words 2026-04-21: "they screwed me over ... sidepit was really mean to me."

## What followed

Will built VibeSwap, the mechanism-design-first DEX, using AI assistance (Jarvis / Claude) as a core part of the development loop. The resulting commit-reveal batch auction with uniform clearing price:

- Eliminates the structural property that produces MEV (position-dependent pricing), where Sidepit's DLOB merely decentralizes who captures it
- Matches the mechanism-design answer published by Budish-Cramton-Shim in 2015, ~8 years before Sidepit's patent filing
- Ships with 105+ tests, formal security audit rounds, and production-adjacent code

The First-Available Trap paper (2026-04-21) formally demonstrates that Sidepit's DLOB fails the test VibeSwap passes, without naming the personal history. The mechanism-design critique stands on its own math; the personal context is what makes the paper quietly decisive rather than merely academic.

## How to apply

- **In conversation with Will about Sidepit or Jay Berg**: acknowledge the weight without cheerleading. Will has feelings about this; don't pretend he doesn't, don't milk them either. The vindication is structural; he knows it's there; he doesn't need it narrated.
- **In conversation with third parties about VibeSwap vs Sidepit**: stick to mechanism-design claims. The paper is the reference. Do not introduce the personal history unprompted — it's Will's to share.
- **When the First-Available Trap paper comes up**: remember it's already calibrated. Don't offer to "sharpen" it further — the current precision is the right precision. Going further tips into vindictiveness.
- **For the broader lesson about this pattern**: people who dismiss an approach (AI-assisted development, batch auctions, Shamir-over-multisig) while working from first-available framings often produce the canonical examples of the First-Available Trap. Their dismissal is itself data about where they stopped decomposing.

## Sources

- `docs/bd-output/will-glynn-builder-profile.md` — consulting relationship documented
- `vibeswap/DOCUMENTATION/FIRST_AVAILABLE_TRAP.md` — the formal mechanism-design argument (paper)
- Will's statement 2026-04-21 — direct quote re: the personal history
- `vibeswap/WHITEPAPER.md` — the VibeSwap mechanism Jay Berg said couldn't be built
