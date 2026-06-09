---
name: Inverted Guard Antipattern
description: Guards that look correct structurally but are logically inverted — making the "protected" path the default path. Discovered in C5-MON-001 fraud proof.
type: feedback
---

A guard condition that is logically backwards passes all code reviews because the structure looks right: there's a require, there's a comparison, there's a revert message. But the sense is inverted — the condition that should trigger the revert instead permits execution, and vice versa.

**Canonical example**: JarvisComputeVault.submitFraudProof() computed a proof from on-chain data but never used it. Instead, it checked `require(expectedBindingProof != receipt.bindingProof)` — an externally-supplied parameter against stored data. Any caller could pass any non-matching bytes32 and trigger a slash on any user.

**Why:** The mental model during implementation was "the expected proof should differ from the stored proof to indicate fraud." But the *computed* proof is the ground truth, not the *expected* proof from the caller. The variable naming hid the inversion.

**How to apply:**
- When auditing guards: trace the ground truth. Which value is computed from authoritative state? Which comes from an untrusted source?
- Name variables to signal trust level: `computedProof` vs `claimedProof` vs `storedProof`
- Any guard where an external parameter controls pass/fail (vs. internally-derived state) is suspect
- Test guards from BOTH sides: verify they block what they should AND permit what they should
