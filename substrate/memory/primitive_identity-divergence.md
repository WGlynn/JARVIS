---
name: Identity Divergence Across Trust Boundaries
description: When two contracts independently derive the same logical identifier with different fields, cross-contract flows silently fail
type: feedback
---

# Identity Divergence Across Trust Boundaries

When Contract A and Contract B both compute an identifier for the same logical entity (e.g., a cross-chain order), any field mismatch makes the cross-contract flow silently fail. Each contract is internally consistent — the bug lives only in the seam.

**Why:** Discovered in R1 Integration (2026-04-03). CrossChainRouter computes commitId from (depositor, hash, srcEid, dstEid, srcTimestamp). CommitRevealAuction computes commitId from (user, hash, bytes32(0), batchId, block.timestamp). Both are valid IDs — they just don't match. The result: cross-chain orders commit successfully on both sides but can never be revealed.

**How to apply:** When two contracts share an identifier:
1. One contract should be the SOLE authority for ID generation
2. The other should receive the ID, not recompute it
3. If both must compute: extract the hash schema into a shared library function
4. Integration tests must verify ID round-trips across every contract boundary
