---
name: intent-retroactive-reward-stack
description: Bounties (intent-centric, price set before work) and contribution-DAG (retroactive, value computed after) are different reward models but NOT alternatives. They stack as different layers — bounty = market-driven immediate income, DAG = math-invariant long-term fair share. Same shape as commit-reveal + ShapleyDistributor.
type: primitive
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## The two models

### Bounty / intent-centric
- Poster defines task + price upfront
- Worker takes, completes, gets paid
- Pricing @ task-creation by poster
- Examples: Gitcoin bounties, Replit bounties, classic RFP / contracting

### Retroactive / DAG
- Work happens, scope emerges, contributors find lanes
- Value computed after-the-fact ∀ observed outcomes
- Shapley axioms enforce fairness given v
- Examples: EF Deep Funding, Hypercerts, Optimism RetroPGF

## Why bounty-alone ≠ solution to attribution-bottleneck

Rick-framed bottleneck: "contributors get screwed by dishonest systems."

Bounty-alone failure modes that preserve the bottleneck:
1. **Mis-pricing** ⇒ poster prices low, worker eats gap. Trust-breakage relocates from manager → task-poster, not eliminated
2. **Premature scope-lock** ⇒ real work scope emerges; bounty forces upfront commit; mismatch w/ reality
3. **Single-contributor bias** ⇒ pays PR-author only; ideas-contributors who shaped approach get nothing
4. **Inspiration chain loss** ⇒ per `[P·fractalized-shapley-games]`: real contrib = fractal DAG of influence. Chat-comment seeds PR. Bounty pays PR-author, not seed-contributor. Same trust-breakage, structurally.

⇒ bounty alone keeps the central-authority pricing point Rick wants to dissolve. Just relocates it.

## The synthesis ⇒ stack them

- **Bounty layer** = intent / market / immediate-income-certainty (worker knows minimum)
- **DAG layer** = retroactive / math-invariant / long-term-fair-share via gov-NFT
- Same shape as VibeSwap commit-reveal (intent) + ShapleyDistributor (math invariant)
- Same shape as `[F·augmented-mechanism-design-paper]`: augment market w/ math invariant, ¬ replace

## Cross-coverage ⇒ each solves what the other can't (Will-articulated 2026-05-14 06:40 ET)

**Bounty layer fixes what DAG-alone can't:**
| Problem | Fix |
|---|---|
| Income certainty | worker knows minimum before starting |
| Action-triggering | priced tasks attract takers; pure DAG has no upfront action signal |
| Onboarding | new contributor has no DAG-history; bounty = guaranteed-floor entry point |
| Cold-start bootstrap | early-DAG Shapley vector unstable; bounties carry until signal accumulates |

**Shapley DAG fixes what bounty-alone can't:**
| Problem | Fix |
|---|---|
| Inspiration chains | upstream contributors (chat, ideation) get credit |
| Multi-contributor attribution | collaborative work shared via Shapley axioms |
| Emergent scope | real scope often > pre-priced scope; DAG captures overflow |
| Long-term value capture | bounty = one-shot; DAG = ongoing rev-share as work compounds |

**Deeper framing**: bounty handles the **ex-ante** problem (worker needs to know what they get; system needs to trigger action). DAG handles the **ex-post** problem (true value observed AFTER; truth needs to flow back). Neither can do both jobs alone ⇒ compose ¬ substitute.

This is the strongest single-frame argument for the stacked design.

## Hybrid mechanic

- Worker takes $500 bounty ⇒ gets $500 USD8 immediately
- Worker also gets soulbound gov-NFT recording contribution
- Over time, periodic Shapley settlements pay additional USD8 based on DAG-position
- Bounty floor guaranteed; upside uncapped; upside emerges from math
- Captures everything bounties miss: inspiration chains + multi-contributor work + scope-emergence + retroactive truth-up

## Why this is the strongest Rick-pitch

1. Honors his instinct ⇒ his bounty experiment runs as designed
2. DAG = augmentation, ¬ replacement (AMD pattern)
3. Fixes the contributor-screw failure mode bounty-alone still has
4. Maps cleanly to his "USD8 OR gov token" framing:
   - bounty pays in USD8 immediately (intent layer)
   - gov-NFT entitles to ongoing USD8 settlements (retroactive layer)
   - both flow in USD8; the NFT is the persistent claim

## Use ∀ partner-chat

- Rick's GitHub-forum-bounty experiment ⇒ ✓ run as v0 intent layer
- ✗ frame DAG as "instead of bounties"
- ✓ frame DAG as "on top of bounties, captures the value bounties miss"
- The AMD pattern fits perfectly here ⇒ lean on it

## Connects

- `[P·contribution-dag-replaces-ip]` — parent claim; intent-retroactive-stack is one implementation pattern
- `[P·hybrid-rep-nft-contribution-marker]` — gov-NFT mechanic that makes the retroactive layer work
- `[P·shapley-mutation-instability-dissolution]` — answers the audit-pushback on the retroactive layer
- `[P·fractalized-shapley-games]` — explains why inspiration chains are load-bearing (bounty-alone failure mode #4)
- `[F·augmented-mechanism-design-paper]` — the parent methodology (augment market with math invariant)
- `[J·deepfunding-research]` — pure-retroactive precedent
- Gitcoin bounties + Optimism RetroPGF + Hypercerts (external) — prior art on each side

## Origin

Will-asked 2026-05-14 06:33 ET: Rick's GitHub-forum-bounty proposal is intent-centric, the contribution-DAG is retroactive, these are different directions — is he going the wrong way?

Answer: he's going one of two right ways; the bigger right way is both. The synthesis stacks them as different layers and fixes the contributor-screw failure mode his bounty-alone system would still have.
