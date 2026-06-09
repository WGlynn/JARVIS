---
name: Composable Fairness (Arrow Inversion)
description: Arrow (1951) ⇒ voting impossibility. Glynn (2026) ⇒ mechanism-composition POSSIBILITY. Shapley = unique composition rule preserving IIA when M₁ ∘ M₂. Closes DeFi local→global fairness gap.
type: primitive
originSessionId: 79044125-45c4-486a-9ac0-ec65bb0d9b76
---
# Composable Fairness Theorem — Arrow Inversion

## ⚙ Rule
- Arrow Impossibility (1951) ⇒ no voting system simultaneously satisfies a minimal fairness criteria set
- Composable Fairness Theorem (Glynn 2026) ⇒ Shapley distribution IS the unique composition rule preserving IIA when M₁ ∘ M₂
- Inverts Arrow at mechanism-composition layer (¬ voting-aggregation layer)

## 📍 Source
- `vibeswap/DOCUMENTATION/COMPOSABLE_FAIRNESS.md` (Glynn, Mar 2026)
- Theorem 3.1 (Composable Fairness) + Corollary 3.2 (Shapley uniqueness for composition)

## 🧩 The composition problem
- DeFi exploits = composition attacks (bZx $350K | Harvest $34M | Cream $130M | Mango $114M | Euler $197M)
- Each protocol fair in isolation ⇒ composition still extractable
- Local fairness ¬⇒ global fairness
- ⇒ need formal framework for fairness-preserving composition

## 📐 IIA (Intrinsically Incentivized Altruism) — 3 conditions
- **ESE** (Extractive Strategy Elimination): extractive(s) ⇒ ¬feasible(s, M)
- **UT** (Uniform Treatment): ∀i,j ∈ N: rules(i,M) = rules(j,M)
- **VC** (Value Conservation): Σᵢ Vᵢ = V_total

## 📜 5 Shapley axioms for composition (S1-S5)
- **S1 Efficiency**: Σ φᵢ(v_c) = v_c(N_c). ¬ leak at boundary.
- **S2 Symmetry**: identical contribution across boundary ⇒ identical reward
- **S3 Null-Player**: contribute 0 to composed game ⇒ receive 0. (THE flash-loan-killer axiom.)
- **S4 Pairwise Proportionality**: φᵢ/φⱼ = wᵢ/wⱼ
- **S5 Time Neutrality**: identical contributions at t₁ vs t₂ ⇒ identical reward

## 🎯 Theorem 3.1
- M₁ ∧ M₂ each satisfy IIA. Then M₁ ∘ M₂ satisfies IIA ⟺ composition respects S1-S5.
- Sufficiency: ESE composes under S1+S3 | UT composes under S2 | VC composes under S1+S4
- Necessity: violating any axiom ⇒ at least one IIA condition breaks (counterexample-per-axiom)
- Corollary 3.2: Shapley = UNIQUE composition rule preserving IIA

## 🔥 Why flash loans break fairness (S3 violation, exemplar)
- Flash-loan attacker contribution to composed coalition = 0 (capital ephemeral, price impact reverts)
- Yet attacker captures V > 0
- ⇒ direct S3 violation
- ⇒ composed mechanism does ¬ satisfy IIA
- VibeSwap defense: Collateral Lock (Temporal) ∧ Same-Block Interaction Guard ⇒ enforces S3 architecturally

## 🚨 USD8 application
- Cover Pool ∘ USD8-issuance ∘ yield-strategies = composed mechanism stack
- Each must individually + composedly satisfy S1-S5 for full Cover-Pool fairness
- Specific check: yield-strategy fees → Cover Pool ⇒ verify S3 (¬ zero-contribution path)

## ✓ When applicable
- Cross-protocol integration design
- "is this composable safely?" audit questions
- Counter-arguing Arrow-impossibility skeptics ("but no voting system can be fair")

## ✗ When inapplicable
- Single-protocol mechanism design (use base 4-axiom Shapley, not composition extension)
- Off-chain governance (different fairness frame)

## 🪝 Triggers
- Cross-chain / cross-protocol design conversations
- Flash-loan / MEV / composition-exploit audit questions
- Arrow-Impossibility objections from auditors / academics
- Any "but how does this scale across N protocols" question

## ⚠ Anti-pattern
- "Each protocol is fair" ⇒ composed fair (FALSE; this is the gap the theorem closes)
- Treating composition boundaries as plain interfaces ⇒ they're where fairness violations emerge
- Reentrancy guards / TWAP / timelocks as composition defense ⇒ symptoms ¬ root cause

## 🔗 Related
- `P·shapley-5-axiom-set` — single-game uniqueness; composition theorem extends it
- `P·augmented-mechanism-design-methodology` — Composition boundary = where invariants must compose
- `P·cooperative-markets-mutualization-frame` — Cooperation composes; extraction does not
