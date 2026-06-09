---
name: Crypto Primitive Selection
description: Decision tool for picking the right cryptographic primitive. Crypto engineering is mostly selection, not invention — match primitive to claim shape. Hash / ZK / Merkle / TEE / MPC / FHE / commit-reveal each fit specific claim classes.
type: primitive
originSessionId: 9557e3af-8773-411b-9ed4-941961f9e5ec
---
# Crypto Primitive Selection

**Rule**: When designing a verification layer, pick the primitive whose shape matches the claim. Every primitive hides something specific and reveals something specific. Mismatches over-engineer (expensive) or under-prove (insufficient).

**Why:** 2026-04-23, building Jarvis-as-a-Service verifiable-claims layer. Will asked for a guide when he observed he needed to understand the primitive choices. Full treatment in `jarvis/docs/crypto-primitive-selection.md`.

---

## Decision tree (quick recall)

| Claim shape | Primitive | What it hides |
|---|---|---|
| "This is the canonical code" | **Hash** (SHA-256) | Nothing |
| "Aggregate over private inputs" | **ZK** (zkVM / SNARK) | Inputs |
| "Deterministic over append-only state" | **Merkle** | Nothing by default |
| "Cross-operator binary integrity" | **TEE** (SGX / SEV / Nitro) | Enclave memory |
| "N-party private compute" | **MPC** | Each party's inputs from others |
| "Compute on encrypted data" | **FHE** | Data + computation from server |
| "Commit now, reveal later" | **Commit-reveal** | Value until reveal |

---

## Selection heuristic

1. **What's private?** Sets the class.
2. **Who's prover / verifier?** One-to-many → ZK. N-party → MPC. Hardware-attested → TEE.
3. **Cost budget?** Per-call ZK is expensive; amortize via batching or use TEE.
4. **Is computation public + deterministic?** Merkle + replay beats ZK.
5. **Temporal binding?** Commit-reveal for future reveal; hash for static identity.

---

## Anti-pattern core

- **Hash for private aggregate** — doesn't hide inputs (use ZK)
- **ZK for public deterministic compute** — 100× overhead for zero privacy gain (use Merkle)
- **Merkle for cross-operator binary** — doesn't cover code behavior (use TEE)
- **FHE for prove-properties-of-closed-code** — wrong shape; FHE is compute-on-encrypted, need ZK + TEE
- **TEE where hardware-vendor trust unacceptable** — pair with ZK or use non-TEE primitives

---

## JARVIS / VibeSwap applications

**JARVIS layers**:
- v0 binary identity → Hash
- v1 cost claims → ZK (private receipts → public ratio)
- v2 grounding → Merkle (archive → digest replay)
- v3 federated shard integrity → TEE

**VibeSwap**:
- Batch auction orders → commit-reveal (MEV prevention)
- Shapley distribution → ZK + Merkle
- Cross-chain settlement → Merkle + ZK

Same selection discipline, different substrate.

---

## Full reference

`jarvis/docs/crypto-primitive-selection.md` — complete primitive reference + anti-pattern table + decision tree.

## Related primitives

- **First-Available Trap** — using the default primitive without matching to claim shape is the cryptographic variant
- **Substrate-Geometry Match** — primitive-to-claim matching is the same discipline as mechanism-to-substrate matching
- **Augmented Mechanism Design** — verifiable claims via primitives IS augmented mechanism design at the verification layer
- **Generate-Verify Decomposition** — each primitive is a generate-verify loop (prover generates claim, verifier checks)
