# MEMORY_AUDIT_ARSENAL — audit-specific primitives index
<!-- MEMORY-SPEC: v1 (2026-04-21) — see memory/MEMORY_FORMAT_SPEC.md -->

**Load trigger**: self-audit pass ∨ TRP round ∨ post-fork verification ∨ Will-says "self audit as you build"

**Origin**: Will 2026-05-08 — *"add that as an Audit specific primitive, we can have a growing arsenal of audit specific primitives as we go"*

## Parent class

[**O·cross-context-protocol (CCP)**](protocol_cross-context-protocol.md) — META-PRIMITIVE. ∀ output ⇒ reconcile against contexts that could invalidate it. AA#1-N are children, each routing a specific output-class to its specific cross-reference contexts.

## Arsenal

| # | Primitive | Output type | Cross-ref contexts |
|---|---|---|---|
| AA#1 | [P·audit-fork-loses-hardness](primitive_audit-fork-loses-hardness.md) | fork/refactor | parent's rejection branches + semantic clauses |
| AA#2 | [F·claim-needs-structural-enforcer](feedback_claim-needs-structural-enforcer.md) | documented safety/fairness claim | code that should structurally enforce it (worst-case input rejected by formula) |
| AA#3 | [F·entity-context-cross-reference](feedback_entity-context-cross-reference.md) | named-entity list (targets, mentions, links) | memory: relationships, abandonments, NDA-locks, in-flight conversations |

## How to use

∀ build session w/ fork ∨ refactor ∨ audit-fix ⇒
1. load this file
2. apply each AA primitive's how-to-apply checklist as gate
3. surface findings inline + capture new shapes ⇒ AA#N+1

## Growth

new audit-shape recognized in session ⇒ ¬ silent-keep ⇒ write `primitive_audit-<name>.md` ∧ add row here. Same atomicity as code primitives.
