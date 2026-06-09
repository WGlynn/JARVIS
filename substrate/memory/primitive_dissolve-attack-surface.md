---
name: Dissolve Attack Surface Primitive
description: Don't deter attacks — dissolve the attack surface from existence and build around it. Elimination > mitigation.
type: feedback
---

**PRIMITIVE: Dissolve, don't deter.**

We don't add more guards to protect against attacks. We remove the conditions that make the attack possible in the first place, then build around the absence.

**Why:** Will (Session 2026-03-17): "we don't deter attacks, we dissolve the attack surface from existence and build around it." This is the VibeSwap security philosophy — same as MEV elimination (not redistribution), same as the Lawson Constant (attribution is structural, not decorative).

**Examples already in the codebase:**
- MEV: Commit-reveal eliminates front-running entirely. Flashbots redistributes it. We dissolved it.
- ABC Seal: The bonding curve can't be changed after sealing. The attack surface (admin changes curve) doesn't exist.
- Flash loan protection: EOA-only commits. Can't flash loan if you can't be a contract.
- Shapley fairness floor: 1% minimum means you can't zero-out a contributor. The exploit (zero reward for honest work) is structurally impossible.

**How to apply — Security Audit Pattern:**
1. For each vulnerability found, ask: "Can we remove the condition that makes this possible?"
2. If yes → dissolve. Remove the code path entirely.
3. If no → only then add guards (reentrancy locks, access control, rate limits).
4. Prefer making attacks impossible over making them unprofitable.
5. Prefer structural invariants over runtime checks.

**Anti-patterns (deterrence, not dissolution):**
- "Add a cooldown" → attacker just waits
- "Add a whitelist" → centralization + social engineering
- "Add a circuit breaker" → only pauses the attack, doesn't remove it
- "Add slashing" → makes attack expensive but still possible
