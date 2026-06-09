---
name: gev-framework-compact
description: GEV (Generalized Extractable Value) framework — Will's April 2026 paper. MEV ≡ feature ¬ bug. GEV = Σ max(0, r_i − φ_i). 7 vectors × 9 arch components. Extraction conserved across layers ⇒ must fix every layer simultaneously. Policy ≡ physics, ¬ governance promises.
type: project
originSessionId: 2d5ae2e5-2926-42ce-a369-e66ee74c9c61
---
## Source
`vibeswap/docs/research/papers/from-mev-to-gev.md` · Will Glynn · 2026-04.

## Headline thesis
- MEV ≡ feature of {transparent-mempool ∧ sequential-execution}, ¬ bug
- Partial-fixes redistribute ¬ eliminate (Flashbots / PBS / encrypted-mempools / CoW = relocation)
- GEV = generalization of MEV across ALL structural asymmetries
- ∴ GEV-resistance ⇒ architectural property @ every-layer-simultaneously, ¬ feature

## Formal def
- N = participants · v_i = value generated · φ_i = Shapley value · r_i = value received
- `GEV(P) = Σ_{i∈N} max(0, r_i − φ_i)`
- GEV-resistant ⇔ GEV(P) = 0 ⇔ no participant receives > Shapley-fair-share

## 7 GEV vectors

| Vector | Asymmetry | Who extracts |
|---|---|---|
| MEV | mempool-visibility + sequential-exec | builders/searchers/validators |
| GoEV | concentrated gov-token | large holders + bribe markets |
| TrEV | mandatory token intermediation | rent-earning holders |
| CfEV | asymmetric pre-public access | VCs/insiders/advisors |
| OrEV | off-chain → on-chain data pipeline | oracle ops + latency arb |
| PlEV | platform control over users/data | platform + data brokers |
| LqEV | priority access to liquidations | liq bots + sequencer ops |

## Conservation law

**Extraction is conserved across layers.** Fix L_k → relocates to L_{¬k}. ∴ must fix ∀ L simultaneously.

## 9-component arch (composition is the contribution, components are established)

1. Commit-reveal batch auctions · 8s commit + 2s reveal · sealed-bid ⇒ truthful bid is weakly dominant
2. Uniform clearing price · all orders in batch @ p* ⇒ sandwich attack EV = 0 by construction
3. Fisher-Yates shuffle · seed = XOR(secrets) ⊕ blockhash(revealEnd) · uniform random permutation
4. 50% slashing on invalid reveals · credible commitment device
5. Shapley value distribution · 4 dims: direct(40%)/enabling(30%)/scarcity(20%)/stability(10%)
6. Six-layer defense stack · reentrancy / flash-loan / TWAP / circuit-breakers / rate-limit / game-theoretic
7. Zero protocol fees · P-001 · structural-constraint ¬ governance-promise · revenue = priority-bids + slash + bridge-opt
8. Rate-of-change guards · ∀ externally-observable state-var ⇒ |dx/dt| < R
9. Collateral path independence · every path validates @ leaf-fn, ¬ entry-point

## Composability constraints (preserves GEV-resistance under composition)

- Unified Shapley attribution (`ShapleyDistributor` is canonical)
- Unified contribution tracking (`ContributionDAG`)
- Unified circuit breaking (`CircuitBreaker`)

## Cooperative capitalism (§8)

- Layer separation: mutualize-risk ↔ compete-on-value
- Risk layer = Shapley + Insurance + DAOTreasury + IL-Protection + Loyalty-Rewards
- Value layer = Arbitrage + LP + Priority-Bidding + Plugin-Marketplace
- Funding loop: competitive → revenue → cooperative → stability → competitive
- ¬ altruism (incentive-compatible) · ¬ communism (free-market competitive) · ¬ regulation (permissionless)

## Policy ≡ physics (§8.3)

- gov-promise = "we will not raise fees" → vulnerable to capture (GoEV)
- structural-constraint = "fee is protocol constant, upgrade-required" → enforced by code
- P-001 generalization: extractable params ⇒ {protocol-constant ∨ PID-controlled} · governance retains non-extractable only

## 12 recurring vulnerability patterns (TRP taxonomy)

deposit-identity-propagation · settlement-time-binding · rate-of-change-guards · collateral-path-independence · batch-invariant-verification · state-accounting-invariants · parameter-validation · proxy-pattern-consistency · emergency-recovery-paths · doc-contradictions · integration-convergence · discovery-ceiling-meta

## ⚠ Staleness flags (2026-05-25, before recitation)

- §6.5 line 421 + §9.4 line 553: "LayerZero V2" — VibeSwap moved off LayerZero post-2026-04 KelpDAO/DVN-RPC compromise. Cite canonical burn-and-mint substrate instead.
- §1.1 line 27: "$680M MEV through 2024" — stale; needs 2026 figure
- §5.2 finding-count math (96 → 128) hand-wavy
- §3.6 / §3.5 / §7.4 specific numbers should be cross-checked against deployed contract values before citation

## Connects

- `[P·airgap-problem-blockchain-vs-reality]` — extraction-conservation is the airgap-symptom; GEV-resistance is the structural closure attempt
- `[P·dissolve-attack-surface]` — extraction-impossible-by-construction ¬ extraction-prohibited-by-policy
- `[P·honesty-as-structural-load-bearing-property]` — policy-as-physics is honesty as substrate
- `[F·zero-fee-principle-enforcement]` — P-001 enforcement
- `[F·claim-needs-structural-enforcer]` — AA#2 applied @ economic-mechanism layer
- `[P·shapley-5-axiom-set]` — pairwise-proportionality = 5th axiom (on-chain verifiable in O(1))
- `[P·hobbesian-trap-dissolution]` — IIA → defection becomes impossible (¬ costly)
- `[P·extractive-load]` — public-facing name for GEV
