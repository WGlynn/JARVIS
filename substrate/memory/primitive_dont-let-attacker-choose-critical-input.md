---
name: dont-let-attacker-choose-critical-input
description: "Security-critical inputs (ordering, identity, time, oracle) must be sourced where the attacker cannot choose them; a free/tx-chosen value is self-assertion, not a check. Cross-layer mechanism-design invariant."
metadata: 
  node_type: memory
  type: project
  visibility: public
  originSessionId: 287f8a4e-59f1-4e65-a256-73ed6b29ac3f
---

**Invariant:** ∀ mechanism ⇒ identify the SECURITY-CRITICAL input(s) ⇒ source each from a place the ADVERSARY CANNOT CHOOSE. attacker-chosen critical-input ≡ self-assertion ¬ verification. (dual of "trust the right oracle.")

- ✗ accept-by-shape ∨ free-arg ∨ free-witness ∨ tx-chosen-field for anything the security rests on.
- ✓ source ∈ {compile-time-const, consensus/header, commit-reveal, identity-bound singleton, trusted-oracle}.

**Test:** ∀ critical input ⇒ ask "can the tx-assembler pick this value to their own advantage?" yes ⇒ HOLE.

**Cross-layer recurrences (same invariant, 3 independent sites, 2026-06-13):**
- ORDERING — MEV / front-running = attacker chooses tx order. fix = commit-reveal + uniform-price ⇒ the choice is REMOVED, not detected. [[primitive_class-dissolution-vs-case-defeat]].
- IDENTITY — a dependency accepted by SHAPE (right size/format) ¬ by IDENTITY (right code + instance) ⇒ attacker substitutes a forged one. fix = COMPILE-TIME identity binding. CAUTION (recursive trap): if the "expected identity" is itself a tx-supplied arg, the attacker chooses THAT too ⇒ no binding. the expected value must live where the attacker has no write access. + singleton (type-id) + UTXO-liveness for freshness.
- TIME — time-decayed weights read from a tx-chosen `now` ⇒ attacker picks the timestamp that favors their side. fix = header/consensus-sourced time, never a witness field.

**Why load-bearing:** the RECURSIVE TRAP is the deep point — even the reference value you compare against is gameable if the attacker supplies it. the check is only real when BOTH the input AND its expected-value are attacker-unreachable (binary ∨ consensus ∨ prior-commit). this is [[primitive_structure-does-the-work]] applied at the input boundary: make the honest path the only writable one.

composes: [[primitive_dissolve-attack-surface]] ∧ [[primitive_class-dissolution-vs-case-defeat]] ∧ [[primitive_honesty-as-structural-load-bearing-property]] ∧ [[primitive_structure-does-the-work]] ∧ [[feedback_ground-security-in-vibeswap-design-and-philosophy]].
