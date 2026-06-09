---
name: ForkLosesHardness (Audit Arsenal #1)
description: ∀ fork(parent-primitive) ⇒ silent-drop-of-security-property risk. Same shape as Polkadot XCM audit-fix-introduces-bug. List parent-constraints; verify each preserved ∨ explicitly relaxed.
type: feedback
originSessionId: 34e87bf6-eae5-43bc-9344-bf390a9a4218
---
# F·fork-loses-hardness — Audit Arsenal #1

**Origin**: 2026-05-08 self-audit post-LayerZero v0.1.

**Will-frame**:
> *"every state reachable by the old control flow either reaches the same end-state in the new flow, or explicitly errors."*

## Pattern

fork(parent) ⇒ import-formula ∧ ✗ import-semantics ⇒ compile-passes ∧ test-passes ∧ silent-fail security-property.

## Sub-shapes (v0.1 caught 3)

| ID | parent-constraint | fork-drop | fix |
|---|---|---|---|
| C-1 | auth ¬ caller-supplied-arg | `msg.sender == token` w/ token=arg ⇒ attacker passes own addr | single check: hub ∨ (registered[sender] ∧ sender==token) |
| C-2 | slash one-shot per challenge | 5%·current-bond geometric decay ⇒ ✗ ejection | offense-counter ∧ force-eject @ Nth |
| H-2 | commit→challenge-window→bond-challenge→Merkle-proof-or-slash | owner-callable instant, ✗ challenge-window | v0.2: port full cycle |

## Why

> *"every state reachable by the old control flow either reaches the same end-state in the new flow, or explicitly errors."* — Will

formula-imported ⊥ semantics-imported. ⇒ surrounding-clause loss = silent.

## How to apply

∀ fork(audited-primitive):
1. enumerate parent: ∀ revert ∧ ∀ modifier ∧ ∀ formula
2. ∀ rejection-branch parent ⇒ ∃ equivalent fork ∨ explicit-relax-w/-reason
3. ∀ formula(parent) ⇒ check semantic-precondition still holds
4. modifier-stacking ⇒ collapse to single explicit check
5. caller-supplied-arg in auth-predicate ⇒ broken-auth ⇒ refactor

## Generalization

¬ Solidity-only. ∀ inheritance ∧ ∀ fork ∧ ∀ prompt-template-fork ⇒ same shape.

## Lineage

- AA#1: this file
- AA#2..N: TBD (growing arsenal per Will 2026-05-08)
- Index: `MEMORY_AUDIT_ARSENAL.md`
- Spec instance: `vibeswap/docs/research/papers/post-layerzero-self-audit-v0.1.md`
