---
name: GraduationCurveBootstrap
description: ∀ new-pool launch ⇒ exponential fee-decay anchored to mcap floor ≡ bootstrap-incentive. fee = fee_max · e^(-λ·(mcap - mcap_min)). High-fee@launch ⇒ low-fee@maturity. Rewards early LP risk-taking ¬ permanent fee-drag. Origin Freedom-repo (Dec 2024, pre-VibeSwap sketches, salvaged 2026-06-10). No current VibeSwap analog; FibonacciScaling targets per-user throughput ⊥ pool-maturity axis.
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Graduation-Curve Bootstrap Mechanic

## Glyph

```
graduation-curve ≡ fee = fee_max · e^(-λ·(mcap - mcap_min))
  · fee_max  ⇒ launch-fee ceiling
  · mcap_min ⇒ floor-anchor (below ⇒ flat fee_max)
  · λ        ⇒ decay-rate (steepness)
∀ new pool: bootstrap-incentive ≡ high-fee@launch ⇒ low-fee@maturity.
✓ rewards early-LP risk-taking ¬ permanent fee-drag.
✗ ⊥ FibonacciScaling (per-user throughput axis ≠ pool-maturity axis).
```

## ⇒ Rule

- ∀ new pool needing bootstrap ⇒ consider graduation-curve as fee overlay
- Floor below mcap_min ⇒ flat fee_max (early-LP protection)
- Above floor ⇒ exponential decay (graduation-as-pool-matures)
- Compose with ShapleyDistributor (orthogonal): graduation = fee-shape, Shapley = fee-recipient

## ∃ Why

- Freedom-repo (WGlynn/Freedom, Dec 2024 → Feb 2026) had this curve in Rust sketches.
- 1.5y pre-VibeSwap. Salvaged 2026-06-10 during repo triage.
- VibeSwap has no pool-maturity fee decay; FibonacciScaling is per-user volume throttle.
- CKB-cell-script port may need launch mechanic ⇒ this shape worth re-derivation.
- Pattern also encodes Will's old instinct for staleness (Freedom had `fallback_last_updated` timestamp 1.5y before [F·everything-needs-a-staleness-check]).

## ↦ Apply To

- ∀ new-pool CKB cell-script design ⇒ evaluate as launch mechanic
- VibeAMM bootstrap phase ⇒ optional curve overlay (¬ replace, layer)
- siblings: [F·fibonacci-scaling] (orthogonal axis), [J·shapley-distributor] (orthogonal mechanism)

## ⊥ Anti-Pattern

- ✗ permanent high fees ⇒ pool can't graduate, kills liquidity post-launch
- ✗ no floor ⇒ launch-fee oscillates, attacker can game initial mcap
- ✗ linear decay ⇒ too aggressive early ∨ too slow late; exponential matches LP-confidence S-curve
