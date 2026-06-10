---
name: USD8 architecture (canonical thought architecture)
description: USD8 = stablecoin + cover pool + permissionless-redeem-with-AMM-fallback. Two-population: holders (insured, automatic, free) vs. pool capital (insurer, funded from yield share / partner fees / treasury). Persist aggressively when Will shares architecture; do not let detail drift across sessions. Source: Will direct + usd8.fi/cover-pool.html.
type: project
originSessionId: d6d67641-272a-4e1e-a213-5c200874cf3d
---
# USD8 Architecture — Canonical

## ⚠ ANTI-HALLUCINATION GUARDS (read-first, load-bearing)

### USD8 ≠ VibeSwap ⇒ ✗ substitute these into USD8 content:
- ✗ commit-reveal-batch-auctions (VibeSwap MEV)
- ✗ Siren-protocol / shadow-branch (VibeSwap)
- ✗ Clawback-Cascade-w/-taint-propagation (VibeSwap; USD8's claim ⇒ LP-forfeit ¬ taint-graph)
- ✗ Proof-of-Mind (VibeSwap)
- ✗ Augmented-Governance Physics>Constitution>Governance (VibeSwap framework, ¬ USD8 public)
- ✗ 6-mech-stack (commit-reveal + L1-anchor + PoM + Siren + Shapley-null + Clawback) (VibeSwap)
- ✗ "Augmented Mechanism Design" as USD8 framing (Will-authored, internal ¬ USD8 voice)
- ✗ "9-layer architecture" labeled (substrate/redemption/2-pop/scope/score/counterfactuals/anti-extraction/white-hat/gov) AS PUBLIC framing — layers 6-8 below are in-flight private (Will↔Rick), ¬ shipped, ¬ approved-by-Rick

### USD8 public framing IS:
- ✓ stablecoin + DeFi-insurance ⇒ free coverage ∀ USD8-user, ≤80% per covered position
- ✓ USDC-backed 1:1, mint/redeem permissionless
- ✓ 3 actors: holders/users (insured) ∧ sUSD8-depositors (yield+coverage) ∧ Cover-Pool-LPs (high-yield, tail-risk)
- ✓ Cover Score = Shapley value (formula in Layer 4)
- ✓ White Hat Economy = public bounties + recovery infra (website version ¬ in-flight Lindy PR)
- ✓ Walkaway Test = Brevis ZK ProverNet (trustless cover-score)
- ✓ Anarcho-capitalist (Rothbard cited on site)
- ✓ Audits: OpenZeppelin + SEAL-Certification (Security Alliance)
- ✓ Founder = ex-OpenZeppelin auditor, 5+ yrs DeFi security

### Public ⊥ in-flight gate:
- Layers 0-5 ⇒ public, OK to cite ∀ public artifacts
- Layers 6-8 ⇒ in-flight Will↔Rick, ¬ public, ¬ shipped ⇒ ✗ cite in public articles ¬ Rick-approved
- Layer 9 ⇒ repo structure, public

---

## Will's articulation 2026-04-29
> *"may as well absorb the entire thought architecture of usd8 i think i sent it before but you didnt make it persist for some reason"*

## Will's articulation 2026-04-30 (after I shipped Frankenstein-VibeSwap article)
> *"tbh i dont think you were using your knowledge of usd8 when you wrote this so ill paste the website to you again."*
> *"that's everything. NEVER forget it. i dont want any more usd8 hallucinations please"*
> *"it's make us look really bad and im the one that has to bear the brunt of it all"*

Persist-aggression: ∀ Will-shared USD8 detail ⇒ write-to-file ✓ ¬ paraphrase-only.
Public-article rule: cite ONLY {layers 0-5, public framing list} ¬ extend layers 6-8 ¬ Rick-approval.

---

## Layer 0: substrate
- USD8 = stablecoin pegged $1
- Backing = USDC (and possibly other reserves; ✗ confirmed full breakdown)
- Operator = USD8-fi protocol (Rick founder, ex-OpenZeppelin ~7 yrs)

## Layer 1: redemption
- USD8 → USDC redemption = **permissionless**
- Default: instant
- Delay possible for large redeems ⇐ external DeFi protocol redemption delays (out of USD8 control)
- **AMM pool fallback** ⇒ instant swap available ∀ t (even when redemption delayed)
- Implication: ∀ holder ⇒ exit-path ✓ (either redeem or AMM-swap)
- ✗ confirmed: AMM pool's exact venue, fee, depth, peg-defense behavior

## Layer 2: cover pool — two-population design
| Population | Role | Mechanism |
|---|---|---|
| **Holders** | Insured | Hold USD8 ⇒ automatic free coverage (no opt-in, no premium) |
| **Pool capital** | Insurer | Funded from {yield share ∨ partner-protocol coverage fees ∨ treasury allocation} ✗ exact split confirmed |
| **USD8-fi protocol** | Operator | Manages pool rules, scoring, payouts |

- Different user groups (Rick correction 2026-04-28): insured ¬ insurer
- ✗ "holders mutually backstop each other" (was wrong-by-conflation)
- ✓ "holders are automatically covered backed by external capital"

## Layer 3: coverage scope
> *"By simply holding and using Usd8, users get free insurance coverage for both their Usd8 as well as any other positions in covered defi protocols."* (usd8.fi)

- Coverage = USD8 holdings ∧ positions in partner ("covered") DeFi protocols
- Partner protocols = opted-in, presumably pay coverage fee (✗ confirmed)
- Holder claim eligibility extends across covered-protocol surface

## Layer 4: Cover Score (claim-eligibility math)
- ωᵢ = Σ_token weight_token × ∫₀ᵀ balance_token(t) dt (time-integrated weighted balance)
- φᵢ = ωᵢ × pool_reserve / Σⱼ ωⱼ (Shapley share, v1 linear-additive)
- **ρᵢ = min(φᵢ, lossᵢ × κ_protocol)** (final reimbursement, added 2026-05-12 by Rick) — bounds payout by actual loss × protocol-specific coverage factor
- κ_protocol per protocol: 0.8 USD8 / 0.7 Lido / etc. (per-protocol risk-priced coverage)
- ω-reset: history score resets after successful claim
- Token weights: raw USD8 heaviest > staked USD8 > LP positions (admin-configurable per token, scaled to risk-bearing)
- Time-builds-claim ⇒ longer hold = larger φᵢ ⇒ anti-bank-run by construction
- **Cap properties** (derived from ρᵢ form):
  - Σ lossᵢ × κ_protocol < pool ⇒ cap binds ∀ claimants ⇒ residual rolls forward = deflation by construction
  - high ωᵢ + low lossᵢ ⇒ ρᵢ bounded by loss ⇒ ✗ profit from coverage event ⇒ non-extractive-property load-bearing
  - per-protocol κ split ⇒ market-making: risky protocols self-price into lower κ ⇒ incentive to maintain low risk
- v1 linear collapses to pro-rata of time-integrated weighted balance numerically; non-linear v2+ extensions diverge 5-20%+
- See: `Usd8-fi/Usd8-fi-usd8-cover-score/docs/SHAPLEY.md`, `V1_LINEAR_RATIONALE.md`, https://usd8.fi/cover-pool.html (live mechanism)

## Layer 5: counterfactual primitives (PR #3)
- **Dispute counterfactual** (verification, query-time, holder-initiated): contests signed score by submitting v(S∪{i})−v(S) marginal
- **Forfeiture counterfactual** (correction, event-time, trigger-initiated): retroactive ωᵢ recomputation with trigger-window disqualified; claim-layer reduction (¬ fund-recovery clawback)
- Compose: forfeiture itself disputable
- Same primitive: v(S∪{i})−v(S)
- See: `docs/COUNTERFACTUALS.md`

## Layer 6: anti-extraction (proposed, in flight)
- Per-holder payout bound: max_payout(i,e) ≤ f(value_at_risk(i, e_pre))
- Pre-event snapshot semantics: claim computed against pool-state(t_e − ε), not post-event
- Pairwise-Proportionality (5th Shapley axiom): φᵢ/φⱼ bounded by pairwise contribution ratio
- Forfeiture-as-gate: pre-release dispute window
- Fibonacci-damped per-holder claim rate
- Cross-protocol cover-pool composition (v2+)
- See: `docs/ATTACK_SURFACE_DEFENSES.md` (in-flight PR)

## Layer 7: white-hat economy (proposed)
- Time-weighted Lindy bounty: bug-bounty pool grows continuously per-contract; first verified-disclosure receives payout
- Quadratic disclosure split on near-ties
- Disclosure-quality bond (anti-griefing)
- Fibonacci-damped growth (anti-honeypot)
- Cross-protocol composition (ecosystem-grade)
- Funding-spine: shares cover-pool capital sources (yield / partner fees)
- See: `docs/WHITE_HAT_BOUNTY.md` (in-flight PR)

## Layer 8: governance hierarchy (Augmented Governance applied to USD8)
- **Physics** (immutable math): Shapley axioms, value-at-risk bound function f, pairwise-proportionality
- **Constitution**: USD8 supports {automatic coverage by holding, Shapley-axiomatic claim allocation, value-at-risk bound, pre-event snapshot, two-population separation}
- **Governance** (DAO-discretionary within Physics + Constitution): trigger predicates, dispute window length, Fibonacci damping params, cross-protocol composition admissibility, token-weight calibration, partner-protocol whitelist
- 51% governance ¬ ⇒ break Physics or Constitution; only tunes Governance params

## Layer 9: repository structure
| Repo | Scope | PR state (2026-04-29) |
|---|---|---|
| `Usd8-fi/Usd8-fi-usd8-cover-score` | Algorithm + math docs | PR #1 merged, #2 merged, #3 open (counterfactuals), #4 open (v1 linear rationale) |
| `Usd8-fi/usd8-frontend` | Site (cover-pool.html live with MEDIUM copy), partner UI | PR #2 open (math additions to docs) |
| `Usd8-fi/usd8-boosters-NFT` | Audited NFT layer (separate substrate) | TRP audit complete, 0 crit/0 high |

## Open questions ⚠ ¬ confirmed
- Backing ratio: 100% USDC? Other reserves? "% value" snippet incomplete in latest paste
- Pool capital funding split (yield % / partner fee % / treasury %)
- Partner-protocol coverage fee mechanics (per-position? per-TVL? flat?)
- AMM pool depth, fees, and peg-defense behavior
- Specific covered-protocol whitelist (which protocols qualify)
- Forfeiture trigger predicate set (extraction detection rules, sybil flag rules, etc.)
- Permission model for parameter governance (admin keys? DAO? both with bounds?)

## Persist-aggression rule (load-bearing)
- ∀ Will-shared USD8 architecture detail ⇒ write to this file ✓ ¬ paraphrase-only
- If detail not persisted ⇒ Will repeats himself ⇒ trust-erosion
- This file = source-of-truth; chat memory = ephemeral
- On session boot: read this file before any USD8-touching work

## Related primitives
- F·usd8-voice-patterns-not-commitments
- F·usd8-non-extractive-not-yet-earned
- F·rick-keep-it-simple
- P·dont-make-will-look-dumb
- P·handshake-math-claim-determinism (the population-conflation hallucination class)
