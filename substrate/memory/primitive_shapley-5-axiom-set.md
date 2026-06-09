---
name: Shapley 5-Axiom Set + Anti-MLM Construction
description: Shapley = unique distribution satisfying Efficiency ∧ Symmetry ∧ Linearity ∧ Null-Player. VibeSwap adds Pairwise-Proportionality (5th, on-chain). Anti-MLM by construction (Σ φ = v(N) ⇒ ¬ compounding).
type: primitive
originSessionId: 79044125-45c4-486a-9ac0-ec65bb0d9b76
---
# Shapley 5-Axiom Set + Anti-MLM Construction

## ⚙ Rule
- Shapley value (Lloyd Shapley, 1953) = *unique* fair distribution rule for cooperative games
- 4 classical axioms ⇒ Efficiency ∧ Symmetry ∧ Linearity ∧ Null-Player
- VibeSwap adds Pairwise-Proportionality (5th, on-chain verifiable via `PairwiseFairness.sol`)
- Anti-MLM ⇒ Σ φᵢ = v(N) ⇒ rewards bound by realized revenue ⇒ ¬ compounding

## 📍 Source
- `vibeswap/DOCUMENTATION/SHAPLEY_REWARD_SYSTEM.md` (619 lines, Glynn Mar 2026)
- Implementation: `vibeswap/contracts/incentives/ShapleyDistributor.sol` (~1100 LOC, 82 tests)
- Lawson Constant: `keccak256("FAIRNESS_ABOVE_ALL:W.GLYNN:2026")`

## 📐 Formal definition
- φᵢ(v) = Σ_{S⊆N\{i}} [|S|! (n-|S|-1)! / n!] · [v(S∪{i}) - v(S)]
- Marginal contribution averaged over all join-orderings
- Weighting ⇒ each ordering equally likely

## 📜 4 classical axioms
- **Efficiency**: Σᵢ φᵢ = v(N). All value distributed. ¬ surplus, ¬ deficit.
- **Symmetry**: identical marginal contributions ⇒ identical reward. ¬ identity / seniority / status bias.
- **Linearity (Additivity)**: φᵢ(v+w) = φᵢ(v) + φᵢ(w). Independent games sum cleanly.
- **Null-Player**: zero marginal contribution ⇒ zero reward. ¬ participation trophies.

## 📜 5th axiom (VibeSwap extension)
- **Pairwise Proportionality**: |φᵢ·wⱼ − φⱼ·wᵢ| ≤ ε. On-chain verifiable. O(1) check.

## 🛡 Anti-MLM by construction (4 mechanisms)
- MLM ⇒ obligations compound across levels ⇒ Σ → 100%+ revenue ⇒ collapse / inflate / Ponzi
- Shapley ⇒ Σ φᵢ = v(N) exactly ⇒ obligations CAN'T compound
- Enforcing axioms: Efficiency (= revenue) ∧ Event-isolation (¬ cascade) ∧ Null-Player (¬ rewards-without-contribution) ∧ Symmetry (¬ hierarchy)

## 🎯 Event-based scoping (load-bearing design choice)
- ¬ one network-wide game (O(2ⁿ), intractable)
- Each value-creating event = independent cooperative game
- Coalitions 2-10 participants ⇒ exact computation in microseconds
- Coalitions > 15 ⇒ Monte Carlo M=10k samples, < 1% error

## ⚖ Quality weights (do ¬ create value)
- Modify characteristic function: vᵢ_weighted = vᵢ · qᵢ / avg(q)
- Null-player axiom STILL HOLDS ⇒ high-quality non-contributor still gets 0
- Updated at epoch boundaries ⇒ ¬ continuous gaming

## 🚨 USD8 application
- Cover Pool fee distribution = direct-port (see `feedback_rick-keep-it-simple` + `shapley-fee-routing-spec.pdf`)
- 5 of 6 weight components transfer (drop Scarcity — ¬ natural sides in Cover Pool)
- Brevis-verified inputs ⇒ axiomatic + cryptographic + Walkaway-resilient simultaneously

## ✓ When applicable
- Multi-party value attribution where contributions heterogeneous
- Referral / LP fee / governance reward / cross-chain fee distribution
- Anywhere "proportional to capital" is the wrong default

## ✗ When inapplicable
- Single-party value capture (¬ coalition)
- v(N) = 0 cases (¬ rewards regardless)
- Where contributions perfectly fungible (Σ φ = pro-rata trivially)

## 🪝 Triggers
- Any reward-distribution design discussion
- Audit conversations: "is this MLM?" / "is this fair?"
- Cross-DAO value sharing
- USD8 / Cover Pool / VibeSwap LP / ContributionDAG context

## ⚠ Anti-pattern
- Network-wide single-game Shapley ⇒ O(2ⁿ) intractable
- Individual multipliers (¬ coalition-wide) ⇒ breaks symmetry ⇒ gameable
- Time-weighted variants without Time Neutrality axiom ⇒ early-bird bonuses break UT
- Treating Shapley as preference / heuristic ⇒ it's the UNIQUE solution, ¬ a choice

## 🔗 Related
- `P·composable-fairness-arrow-inversion` — uniqueness extends to mechanism COMPOSITION
- `P·fairness-fixed-point-iterated-shapley` — single-round fair ≠ iterated fair; FP analysis
- `P·cooperative-markets-mutualization-frame` — Shapley = math behind multilevel-selection Cooperative Capitalism
- `P·augmented-mechanism-design-methodology` — Shapley = Verification invariant
