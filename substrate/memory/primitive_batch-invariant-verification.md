---
name: Batch Invariant Verification
description: Snapshot state before batch execution, verify invariant after. Sequential operations within batches create ordering attacks.
type: feedback
---

# Batch Invariant Verification

In any system that processes multiple operations in a single transaction, the batch itself must preserve invariants — not just individual operations.

**Why:** TRP found this pattern across three contracts:
- R28 (AMM-01, CRITICAL): k-invariant violated during batch execution because fees were applied per-swap but k was only checked at the end — and the check was wrong. Fixed by capturing kBefore, verifying k doesn't decrease after the full batch.
- R16 (F02): Reserve updates during batch processing were sequential, giving priority bidders an advantage over later entries in the same batch.
- R16 (F03): Donation attack detection fired on legitimate large batches because the check ran before balance updates from earlier batch entries.

**How to apply:**
1. Before any batch loop: snapshot the invariant (k-value, total balance, reserve ratio)
2. Execute all operations in the batch
3. After the loop: verify the invariant still holds against the snapshot
4. Never check invariants WITHIN the loop against partially-updated state
5. For ordering fairness: use uniform clearing price (all trades at same price) rather than sequential execution

**Generalization:** This is the batch equivalent of database transaction isolation. Individual operations may temporarily violate invariants, but the batch as a whole must not. The snapshot-execute-verify pattern prevents both economic attacks (ordering manipulation) and logic errors (partial-state checks). Applies to: DEX batch settlement, governance proposal execution, multi-transfer operations, airdrop distributions.
