---
name: Fairness Fixed Point (Iterated Shapley)
description: Single-round Shapley fair ≠ iterated Shapley fair. Existence ✓ (Brouwer). Uniqueness ✗ open. Stability of balanced FP conjectured. VibeSwap mitigations bound drift. Empirical verification queued.
type: primitive
originSessionId: 79044125-45c4-486a-9ac0-ec65bb0d9b76
---
# Fairness Fixed Point — Iterated Shapley Convergence

## ⚙ Rule
- Shapley provably fair for SINGLE round. Iteration is separate question.
- Iterated Shapley = Rₜ₊₁ = Shapley(v_τ(Rₜ)) where τ = trust-graph derived from R
- Feedback loops can: converge-fair ✓ | converge-unfair ✗ | oscillate | wander

## 📍 Source
- `vibeswap/DOCUMENTATION/THE_FAIRNESS_FIXED_POINT.md` (250 lines, 2026-04-22)
- Already shipped: `Desktop/from-vibeswap/fairness-fixed-point-cover-pool.pdf`

## 📐 The 3 fixed-point questions
- **Existence**: ∃ R*: R* = iterate(R*)? ⇒ ✓ Brouwer (continuous map ∘ compact set)
- **Uniqueness**: only one FP, or multiple? ⇒ ✗ likely multiple (non-linear, path-dependent, trust-cap discontinuities)
- **Stability**: do nearby states flow toward (stable) or away (unstable)? ⇒ conjectured stable for balanced FP via spectral radius < 1 (averaging composition)

## 🎯 3 scenarios (parameter-dependent)
- **A: Drift→founder dominance** ⇒ trust(new) = trust(old) + 0.01·reward, no cap ⇒ Alice ~80% of pool. UNFAIR FP.
- **B: Bounded with decay** ⇒ trust decay 5%/round + cap ⇒ Alice ~40-50%. STABLE BOUNDED FP.
- **C: Contribution-matched** ⇒ Alice delegates as rewards grow, others step up ⇒ Long-run marginal contribution. STABLE FAIR FP. (VibeSwap aims here.)

## 🛡 VibeSwap mitigations bounding drift
- Trust-weight cap at 3.0× ⇒ founders ¬ unbounded
- 15% per-hop decay in trust-graph BFS ⇒ ¬ concentration
- Six-hop max BFS ⇒ ¬ founder-influence inheritance by distant users
- Three-branch attestation: Executive ∧ Judicial ∧ Legislative ⇒ ¬ single-branch capture
- Constitutional axioms P-000 ∧ P-001 ⇒ ¬ self-amplifying wealth-capture

## 💥 5 ways to break convergence
- Reward→trust multiplier too aggressive ⇒ rapid compounding (mitigation: cap)
- Reward accumulation → voting power directly ⇒ permanent leverage (mitigation: voting follows TRUST not accumulated rewards; trust decays)
- Acceptance threshold tuned for founders ⇒ single-attestation passes (mitigation: quadratic / multi-branch)
- Tribunal capture ⇒ judicial branch = bias amplifier (mitigation: random jury from high-trust pool)
- Governance capture of constitutional amendments ⇒ backstop fails (mitigation: P-000/P-001 ¬ governance parameters; amendment requires fork)

## 📊 Drift-monitoring metrics
- Rolling-window Shapley distribution shift
- Gini coefficient of trust-weights
- Founder-hop-distribution (% rewards by hop-distance from founders)
- Multi-branch concurrency (executive vs tribunal vs governance ratios)

## 🚨 USD8 application
- USD8 Cover Pool will run Shapley iteratively (per-round fee distribution)
- Same fixed-point analysis applies
- Adopt VibeSwap mitigations OR run empirical convergence on USD8's specific params
- ASK Rick: which scenario does USD8 target? Default: C (contribution-matched)

## ✓ When applicable
- Any Shapley application running in iterated rounds (vs one-shot)
- Trust-graph + reward-feedback systems
- "is this stable long-term?" architecture questions

## ✗ When inapplicable
- Single-shot Shapley distributions (¬ iteration)
- Where trust ¬ feeds back into next round

## 🪝 Triggers
- Long-horizon mechanism stability questions
- Founder-rights / early-contributor concentration concerns
- USD8 Cover Pool roadmap (per-round fee distribution = iterated)

## ⚠ Anti-pattern
- "Shapley is fair" as if it answers iterated case ⇒ FALSE, single-round only
- Aggressive trust-weight multipliers ⇒ Scenario A
- Skipping mitigations because "it'll probably converge" ⇒ "probably" ¬ "proven"

## 🔗 Related
- `P·shapley-5-axiom-set` — single-round axioms (foundation, not iterated FP)
- `P·composable-fairness-arrow-inversion` — composition layer; iteration = different layer
- `feedback_augmented-mechanism-design-paper` — mitigation parameters live in §
