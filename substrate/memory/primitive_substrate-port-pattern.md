---
name: Substrate-port pattern
description: Classify each component on mechanism-port: DIRECT-PORT ∨ REINTERPRET ∨ DROP. ¬ force-fit.
type: primitive
originSessionId: 05f950b5-8ab9-47f5-a2b2-b8336ce1e9ef
---
# Substrate-port pattern

## Rule
- mechanism-port = per-component classification
- ¬ all-or-nothing
- ¬ force-fit ⇒ ✗ substrate-mismatch

## 3 classes
| class | when | output |
|---|---|---|
| **DIRECT-PORT** | substrate-match ✓ ∧ semantics-stable | drop in as-is, zero/minimal modification |
| **REINTERPRET** | structure ✓ ∧ inputs require redefinition | same formula, USD8-substrate inputs |
| **DROP** | substrate-mismatch ⇒ ✗ ∨ would smuggle governance into math | omit + explain reason in writeup |

## Usage marker
- ✓ name the classification per component in the spec
- ✓ explain WHY for DROPs explicitly
- ✗ silent omission ⇒ reads as oversight not deliberate

## Examples (USD8 ports from VibeSwap)

### Shapley fee routing (5 components)
- Direct contribution → DIRECT-PORT (capital is intrinsically observable in both substrates)
- Enabling tenure → REINTERPRET (logarithmic curve ✓; tenure measurement adjusts for cooldown)
- Scarcity → DROP (cover pool has no natural order-imbalance signal; using it would smuggle governance into math)
- Stability → REINTERPRET (formula ✓; trigger redefined as claim-surge instead of price-volatility)
- Quality multiplier → DIRECT-PORT (Sybil-resistant reputation works in any substrate)

### History compression (5 candidate accumulators)
- IncrementalMerkleTree → DIRECT-PORT (proven, audit-grade, substrate-agnostic)
- KZG → DROP (trusted setup; pairing cost; no benefit at our query rate)
- Verkle → DROP (pre-production; tooling immature)
- MMR → DROP (solves unbounded-growth we don't have)
- RSA accumulator → DROP (trusted setup; expensive; non-membership not needed)

## Why
- Naive port = "copy entire mechanism" ⇒ inherits substrate-specific assumptions ⇒ silent breakage
- Naive reject = "build from scratch" ⇒ wastes proven audit history
- Per-component classification ⇒ inherits exactly the parts that fit, drops what doesn't, with explicit reason

## Triggers
- mechanism-port discussion (USD8 ← VibeSwap, or any cross-protocol primitive transfer)
- "should we use X here?" Q ⇒ apply 3-class lens
- spec-writing for substrate transfer ⇒ table-format the classifications

## Anti-patterns
- ✗ "VibeSwap does X so USD8 should X" without classification
- ✗ "X is too AMM-specific so we drop everything"
- ✗ classifications silently in head, not in writeup

## Related
- substrate-geometry-match (parent)
- augmented-mechanism-design (when REINTERPRET, augment ¬ replace)
- first-available-trap (when DROP, name what you rejected and why)
