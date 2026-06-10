---
name: shapley-mutation-instability-dissolution
description: Pairwise-Shapley scores change when the contribution graph grows. This LOOKS like an instability bug; it dissolves via 4 structural moves (Bayesian-update reframe + fractal-locality + settlement-vs-state split + reputation-vs-revenue token separation). Rick-readable answer to the most common audit-grade pushback on Shapley-based attribution.
type: primitive
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## The concern

- Pairwise-Shapley vector ≡ f(graph)
- ∀ new contrib added ⇒ pairwise matrix updates ⇒ Shapley vector updates ∀ existing contributors
- ⇒ contributor's "score" ≠ fixed; changes as graph grows
- audit-grade objection: "feels unstable, unfair, hard to settle"

## Dissolution stack (4 moves)

### 1. Reframe as Bayesian-update, ¬ score-nerf
- Shapley is relational ∀ construction: φ_i = E[marginal-contrib | coalition-ordering]
- N → N+1 ⇒ v changes ⇒ φ_i ∀ existing-players MUST change ⇒ math, ¬ bug
- D adds synergy w/ A ⇒ A score ↑ correctly
- D substitutes A ⇒ A score ↓ correctly
- Frame: ¬ "A got nerfed" ✓ "A's measured-impact updated as we got more composition-data"
- Same shape as Bayesian posterior on new evidence ⇒ auditors read this immediately

### 2. Fractal decomposition bounds blast radius
- Per `[P·fractalized-shapley-games]`: DAG = hierarchical
- Shapley @ cluster-level + redistribute within cluster
- D joins cluster Y ⇒ only cluster Y contributors see update; cluster X unchanged
- Platform-scale: 1K tasks × ~5 contribs each ⇒ new contrib affects ~5 scores, ¬ 5K globally
- Mutation = locally-contained property of the hierarchy itself

### 3. Settlement-vs-state separation
- 3 layers:
  - **State** = live Shapley vector, recomputes continuously, fluctuates
  - **Settlement** = periodic checkpoint (weekly/monthly), Shapley frozen + paid
  - **True-up** = longer-interval reconciliation if drift accumulated
- Paid-out value = monotonic regardless of live-state volatility
- Same shape as: stock price fluctuates ∧ dividends pay periodically. Ex-date freezes payment.
- Contributor certainty: once paid for period P, payment final.

### 4. Reputation-token ⊥ revenue-share split
- **Reputation token**: 1/validated-contribution, NON-DILUTABLE, MONOTONIC ⇒ never decreases
- **Revenue share**: dynamic, follows live Shapley, stable-in-expectation over horizons
- Reputation = the work happened. Fixed forever.
- Revenue share = current claim on future redistribution. Fluctuates locally; expected-value stable.
- Rick-message-2026-05-14 already gestures: "USD8 or gov token entitled to future rev share"
  - USD8 = periodic-settlement payment
  - Gov-token = revenue-share-entitlement (dynamic Shapley layer w/ reputation backing)

## Bottom-line frame

> "The instability isn't real for contributors. Reputation tokens are fixed. Settled revenue payments are fixed. Only forward-looking expected-value of their revenue-share entitlement updates as the graph grows — and that's the right behavior. Same property that makes equity ownership work despite market cap fluctuating."

## Use ∀ partner-chat

- Rick raises mutation-instability concern ⇒ load this stack
- Default lens ∀ any audit-grade pushback on Shapley-based attribution
- The 4 moves compose; rarely need to deploy all 4. Usually moves 1 + 4 close it.
- Bayesian-update + reputation/revenue-split = the minimum-viable-dissolution

## Connects

- `[P·fractalized-shapley-games]` — move 2 lives here
- `[P·cooperative-game-elicitation-stack]` — Shapley operates on v, ¬ produce v. v lives in elicitation layer.
- `[F·augmented-mechanism-design-paper]` — the mech-design family this primitive belongs to
- `[P·contribution-dag-replaces-ip]` — parent claim; this primitive answers the strongest audit-pushback on the parent
- `[J·deepfunding-research]` — EF Deep Funding handles same problem via periodic-settlement-cadence
- `[F·jul-is-primary-liquidity]` — 3-token role separation precedent (JUL=money, VIBE=gov, CKB=state-rent)

## Origin

Will-asked 2026-05-14 06:06 ET ∀ Rick partner-prep stack: "the contribution dag also uses pairwise comparisons to value contributions from lowest to highest, but that score will literally change every time the graph changes. how do we wrestle with that?"

The 4-move dissolution synthesized from existing primitives (fractalized-shapley + cooperative-game-elicitation-stack) + standard cooperative-game-theory practice (periodic settlement, reputation/equity split). Captured as standalone primitive because this is the highest-frequency objection to Shapley-based attribution; pre-built dissolution stack saves re-derivation in future partner conversations.
