---
name: M-01 commit-reveal secret storage refactor (PENDING)
description: VibeSwapCore stores plaintext secret in SwapParams during commit — needs design refactor to store only hash. Dedicated session required.
type: project
---

**M-01**: VibeSwapCore `commitSwap` stores `secret` in plaintext in `pendingSwaps[commitId].secret`. Anyone can read it via `eth_getStorageAt` before reveal, breaking commit-reveal confidentiality.

**Why it matters:** This is the foundational security property of the entire DEX. If secrets leak, front-running is possible again. The commit-reveal scheme's integrity depends on this.

**Fix:** Remove `secret` from `SwapParams` struct. Store only the commitment hash during commit. User provides secret during reveal, contract verifies `hash(order || secret) == commitment`. The secret never touches chain storage.

**Why it needs its own session:** Touches commit flow, reveal verification, settlement path, frontend swap hook, and potentially the cross-chain router. One wrong move breaks the auction. Not a background sweep fix.

**How to apply:** Dedicated refactor session. Read every function that touches `SwapParams.secret`, map the data flow, then surgically remove the field and rewire reveal verification.
