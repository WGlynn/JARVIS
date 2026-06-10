---
name: audit-aa0-substrate-geometry-first
description: AA#0 — ∀ architectural-audit ⇒ check substrate-geometry-match BEFORE AA#1 (fork-loses-hardness) ∧ AA#2 (claim-needs-structural-enforcer). The shape-of-the-primitive check catches available-code defaults that the constraint-preservation checks miss.
type: feedback
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## Rule

∀ architectural-audit:
1. **AA#0** ⇒ does the shape of this primitive substrate-geometry-match the problem, or is it the first-available data structure w/ bolt-on machinery compensating?
2. **AA#1** ⇒ does the fork preserve parent constraints?
3. **AA#2** ⇒ is the claim structurally enforced?

AA#0 fires FIRST. ∀ AA#1/AA#2 inside a wrong-shape primitive = polishing a misfit.

## Why

Existing audit arsenal catches:
- AA#1: constraint preservation under fork
- AA#2: claim → structural enforcer

✗ catches: primitive shape mismatched to substrate-natural-geometry.

ERC-20 (account-balance) applied to cross-chain conservation = available-code default. Conservation is UTXO-natural. AA#1/AA#2 ∀ ERC-20-shaped messaging-token = correct-but-on-wrong-base.

## Trigger

- ∀ contract design ⇒ AA#0 first
- ∀ data-structure choice ⇒ AA#0 first
- ∀ "default to OZ template / standard library / DeFi idiom" ⇒ AA#0 first

## Substrate-natural shapes (working list)

| Problem | Natural shape | Wrong-default shape |
|---|---|---|
| Cross-chain conservation | UTXO / Cell | ERC-20 account-balance |
| Per-event provenance | Receipt / event-log | Mutable storage |
| Single-trust-root verification | Inline crypto verify | Contract-to-contract delegation |
| Bounded-supply asset | Constructor-immutable cap | Governance-tunable cap |
| Identity ≡ bytecode | CREATE2 deterministic | Proxy w/ admin-controlled implementation |
| Conservation law | Per-spend-checkable | Per-batch invariant + accountant contract |

Apply `[P·substrate-geometry-match]` lens at the data-structure layer, not just the mechanism-design layer.

## Origin

Will-flagged 2026-05-14 11:00 ET during post-LayerZero canonical-messaging spec audit:
- I rubber-stamped ERC20Upgradeable + AccessControl
- Will: "is an erc-20 that's upgradeable really the right choice for a 'canonical messaging layer' / we require an engineer solution not an ethereum solution"
- Will follow-up: "you're using code that's readily available instead of searching for a true self-validating solution"

The first-principles check exposed UTXO-shaped tokens as the substrate-native alternative. The existing audit-arsenal (AA#1/AA#2) didn't catch this because both lenses operate on existing-primitive-correctness, not on shape-of-primitive.

## Connects

- `[P·substrate-geometry-match]` — parent principle; AA#0 is the audit-time application
- `[P·first-available-trap]` — the failure mode AA#0 catches at architectural granularity
- `[P·audit-fork-loses-hardness]` (AA#1) — sibling, fires AFTER shape-check passes
- `[F·claim-needs-structural-enforcer]` (AA#2) — sibling, fires AFTER shape-check passes
- `[F·entity-context-cross-reference]` (AA#3) — orthogonal axis (entity-level context)
- `[P·cross-context-protocol]` — META-parent of audit-arsenal
- `[P·cell-knowledge-architecture]` (CKA) — UTXO-applied-to-knowledge, instance of substrate-geometry-match at the data layer
