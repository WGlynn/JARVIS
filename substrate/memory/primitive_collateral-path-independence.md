---
name: Collateral Path Independence
description: Every code path that touches user collateral must independently validate it. Shared validation between paths creates bypass vectors.
type: feedback
---

# Collateral Path Independence

If there are N ways to reach a state change involving user funds, all N paths must independently validate collateral. Validating in one path and assuming the others "must have gone through it" is how funds get stolen.

**Why:** TRP R46 (R1-F02) found that CommitRevealAuction had three reveal paths (direct reveal, batch reveal via Core, cross-chain reveal via Router). Only one path validated that the revealer had actually deposited collateral. The other two paths assumed the deposit existed because "you can't get here without depositing" — but cross-chain reveals could.

**How to apply:**
1. List every function that can change user-facing state (reveals, settlements, withdrawals, claims)
2. For each: trace every call path that reaches it (direct, via orchestrator, via router, via keeper)
3. Each path must validate: (a) deposit exists, (b) deposit amount matches, (c) depositor identity matches
4. Never rely on "the caller must have already checked" — the caller might be a new integration you didn't anticipate
5. Defense in depth: validate at the leaf, not just the entry point

**Generalization:** This is the principle of independent verification applied to smart contracts. In traditional security it's "defense in depth." In formal methods it's "every function's preconditions must be checked at the function boundary, not assumed from calling context." Trust boundaries shift when new integrations are added — the only safe assumption is that any public/external function can be called by anyone.
