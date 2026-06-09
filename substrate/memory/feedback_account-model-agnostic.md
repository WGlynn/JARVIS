---
name: account-model-agnostic
description: ∀ security-property-preserving primitive ⇒ design substrate-port-pattern-portable across Ethereum-account-model ∧ CKB-Cell/UTXO ∧ Solana-program-account. Specify the property; instantiate per chain via chain-native primitive. Initial instance 2026-03-20 (verification contracts); generalized 2026-05-14 (canonical tokens).
type: feedback
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## Rule

∀ security-property-preserving primitive (verification logic, canonical asset, attestation contract, etc.):
1. Spec the property abstractly (pure inputs → bool / state-transition)
2. ✗ encode chain-native data-structure assumption into the spec
3. Instantiate per chain via the chain-native primitive that satisfies the property
4. External semantic ≡ across chains; implementation ⊥ per substrate

## Why

Will-frame 2026-03-20: be ahead of blockchain-architecture changes. Account-model-only design = lock-in. Cell-model (CKB) verification-oriented. Pure verification ports directly.

Will-frame 2026-05-14 (generalization): "we require an engineer solution, not an Ethereum solution." Available-code defaults (ERC-20 + AccessControl + UUPS) violate this principle at the token-design layer same as account-state-dependent verification violated it at the verification-contract layer.

Same `[P·substrate-geometry-match]` argument at different layers. Same `[P·substrate-port-pattern]` ⇒ DIRECT-PORT / REINTERPRET / DROP discipline.

## Instances

### 2026-03-20 — Verification contracts (original)
- ∀ verification fn: `pure` or `view` only. Inputs → bool.
- State updates: separate contract/fn from verification
- ✗ global state access in verification logic
- VerifiedCompute pattern: verify(inputs, claimedResult) → bool
- State management: wrapper calls verifier
- CKB: verifier ≡ lock script; wrapper ≡ type script
- EVM: verifier ≡ pure fn; wrapper ≡ stateful contract

### 2026-05-14 — Canonical tokens (generalization)
- ∀ canonical-messaging token: security-model = UTXO-grade (conservation per-operation, provenance structural, ✗ privileged minter)
- DIRECT-PORT to UTXO chains: Cell w/ attestation-hash baked into data field; type-script enforces canon rules
- REINTERPRET on account-model chains: ERC-20-interface externally; inline BLS-attestation-verification on mint; provenance via AttestationConsumed events; conservation enforced by "every mint ↔ verified-burn-elsewhere"
- ✗ SupplyAccountant (conservation emerges from attestation-chain)
- ✗ AccessControl mint role (BLS sig = trust root)
- ✗ UUPS proxy (canonical = same-forever; bytecode IS identity on EVM via CREATE2 deterministic addr)
- External semantic: same canonical asset everywhere; cross-chain provenance traceable via attestation graph

## Working list of where this principle applies

| Primitive | Chain-native shape |
|---|---|
| Verification logic | EVM: pure fn / CKB: lock script |
| Canonical tokens | EVM: ERC-20 + inline-attestation / CKB: Cell w/ type-script / Solana: program-owned account |
| Attestation verification | EVM: precompile-assisted BLS / CKB: RISC-V BLS lib / Solana: ed25519/BLS native |
| Conservation laws | EVM: receipt-bound balances OR external invariant check / CKB: per-spend UTXO conservation / Solana: program-enforced |
| Provenance trails | EVM: events / CKB: cell history / Solana: account transaction log |
| Multi-sig validator quorum | EVM: BLS aggregate / CKB: lock script multi-sig / Solana: SPL multi-sig |

## How to detect the failure mode

Trigger phrases (per `[F·readily-available-code-default-trap]`):
- "Use OpenZeppelin's X"
- "Standard pattern is Y"
- "ERC-20-style" / "ERC-721-style"
- "Account-balance model"
- "Just like LayerZero / Wormhole / CCIP does"
- "OZ has a helper"

⇒ STOP ∧ apply AA#0 (`[F·audit-aa0-substrate-geometry-first]`) ∧ derive minimal-shape from required properties before reaching for available code.

## Connects

- `[P·substrate-geometry-match]` — parent meta-principle
- `[P·substrate-port-pattern]` — DIRECT-PORT / REINTERPRET / DROP discipline (the operational arm)
- `[P·cell-knowledge-architecture]` (CKA) — UTXO model applied to knowledge (one instance up)
- `[F·audit-aa0-substrate-geometry-first]` (AA#0) — audit-time application
- `[F·readily-available-code-default-trap]` — failure-mode this primitive prevents
- `[P·first-available-trap]` — sibling at mechanism-design layer
- `[P·parallelism-convergence-2017]` — same shape one fractal level up (Transformers + UTXO independently converged on parallelism)

## Origin

Original 2026-03-20 (Will-named for verification contracts).
Generalized 2026-05-14 11:00 ET (Will-flagged during post-LayerZero canonical-messaging spec audit; L4 recall layer surfaced the original primitive after the canonical-token instance was derived independently).
