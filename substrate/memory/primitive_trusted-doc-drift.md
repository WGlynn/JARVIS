---
name: Trusted Document Drift
description: Facts embedded in trusted documents (CKB/SKB/GKB) drift faster and more dangerously than orphan files — because trusted docs are loaded on boot and assertions are made from them without verification.
type: feedback
---

# Trusted Document Drift

Orphan files that nobody reads cause zero harm. Stale facts in documents that are loaded on every session and treated as ground truth cause compounding errors.

**Why:** RSI R0 v1 found the SKB claimed 98 contracts and 76 test files. Actual: 379 contracts, 516 test files — 3.9x and 6.8x stale respectively. The GKB "Last sync" timestamp said 2026-04-02 but the facts were from February. Every session that loaded the GKB inherited false beliefs about the codebase size.

Meanwhile, 122 orphan files existed harmlessly — they weren't referenced, so they couldn't mislead.

**How to apply:**
1. When running R0 (density), prioritize verifying FACTS in trusted docs over pruning orphan files
2. Counts, dates, and status claims are the highest-drift fields — grep for numbers and verify
3. "Last sync" timestamps are only meaningful if facts were re-verified during sync
4. The Anti-Stale Feed protocol applies to the CKB/GKB itself, not just external claims

**Generalization:** In any knowledge system, the most dangerous errors are in the most trusted documents. Rarely-read files can't mislead. Frequently-loaded files with stale facts create systematic bias. Verify the foundations, not just the edges.
