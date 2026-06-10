---
name: WatchtowerPatternFromFiber
description: Third-party observers continuously verify off-chain state in payment channel networks; can challenge invalid state transitions on-chain before finalization. Adopted by Nervos Fiber v0.6.1 (Q1 2026) post-Force-Bridge exploit (June 2025, $3.9M loss). Borrowable security primitive for VibeSwap-on-CKB cross-chain bridges or state-channel mechanisms. Cell Model alone ⇏ auto-solve security.
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Watchtower Pattern (from Nervos Fiber)

## Glyph

```
watchtower ≡ third-party observer × continuous-attestation × challenge-on-invalid
∀ off-chain state transition ⇒ watchtower verifies
  invalid ⇒ on-chain challenge BEFORE finalization
  valid   ⇒ silent (no gas burn)
substrate-property:
  cell-model      ⇒ sovereign ownership ¬ auto-solve external-bridge security
  watchtower      ⇒ adds external-observer attestation layer
incentive: bond-stake + slashing-on-false-challenge + reward-on-valid-catch
```

## ∃ Why

- Force Bridge exploit 2025-06: $3.9M lost on Nervos cross-chain bridge
- Cell Model's sovereign-ownership protects against contract exploits within Nervos but ⇏ protect external bridge state
- Fiber v0.6.1 (Q1 2026) introduced watchtower as response
- Pattern generalizes: ∀ off-chain-then-finalize substrate (state channels, optimistic rollups, bridges) benefits from continuous-attestation observers

## ↦ For VibeSwap-on-CKB

- bridge-state validation between EVM-side ∧ CKB-side during pivot
- cell-script verification of complex multi-party transactions
- VibeSwap-canonical burn-and-mint messaging (post-LayerZero) ⇒ watchtower attestation as part of validator-bond stack
- compose with bonded-validator network + BLS12-381 threshold sigs

## ⇒ Pattern composition

- watchtower ⊥ ZK-proof (different cost/timing tradeoffs)
- watchtower ⊃ honest-1-of-N assumption (vs ZK's trustless)
- pairs well with VibeSwap Augmented-Mechanism-Design ⇒ structural-honesty layer

## ⊥ Anti-pattern

- ✗ assume cell-model security ⇒ external-bridge security (Force Bridge counter-example)
- ✗ single watchtower (single-point-of-failure)
- ✗ no economic incentive ⇒ watchtower runs unsustainably

## ↦ Siblings

- [R·research-batch-2026-06-10] ⇒ source of finding
- [J·vibeswap-ckb-sovereign-pivot] ⇒ where pattern would compose
- [P·honesty-as-structural-load-bearing-property] ⇒ watchtower economic-incentive ⊂ structural-honesty
- [P·airgap-problem-blockchain-vs-reality] ⇒ watchtower = one bridge-closure mechanism
