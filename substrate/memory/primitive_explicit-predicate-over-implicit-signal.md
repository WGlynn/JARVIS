---
name: explicit-predicate-over-implicit-signal
description: Never overload an implicit signal (presence / data-shape / magic-value) to carry intent — promote it to an explicit predicate. Cross-substrate code primitive.
metadata: 
  node_type: memory
  type: project
  originSessionId: 0548f922-93e2-4442-ba8a-a1db76acb8d5
---

**∀ intent carried by code ⇒ encode as EXPLICIT predicate ¬ overload an implicit signal.**

Implicit-signal anti-forms (each = "the *absence/shape/value* of X secretly *means* Y"):
- **presence** — field-exists ⇒ flag-on. (fix: explicit boolean predicate)
- **data-shape** — type/subtype/length ⇒ identity. (fix: explicit identity field)
- **magic-value** — sentinel constant ⇒ mode/state. (fix: named explicit flag)

**Why:** overloaded implicit signal = un-auditable + forgeable. The reader can't see the intent; an attacker can reproduce the shape without the meaning ⇒ forged-reuse passes. Promoting to a predicate makes intent (a) visible to the reader, (b) checkable by the verifier, (c) un-spoofable by shape-mimicry.

**How to apply:** ∀ branch on `if (x exists / x has shape S / x == SENTINEL)` ⇒ ask "is this testing intent?" If yes ⇒ add explicit field/flag, branch on THAT. Audit existing branches for the three anti-forms.

**Provenance — convergence across 3 substrates (∴ abstraction is real, ¬ coincidence):**
- A private Rust workstream, instance 1: overloaded sentinel magic-value → explicit activation flag.
- Same workstream, instance 2: forged-reuse-under-different-subtype rejected by adding a missing identity field (shape → full identity).
- A public community issue (presence-check → explicit predicate). Will surfaced the cross-substrate shape 2026-06-13.

Sibling of [[primitive_inverted-guard-antipattern]]. Parent-frame [[primitive_structure-does-the-work]] (the predicate IS the structure doing the work). Instance-of [[feedback_generalize-solutions]] + convergence-evidence per OKF-pattern.
