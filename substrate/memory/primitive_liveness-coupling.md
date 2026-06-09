---
name: Liveness Coupling Through Mandatory External Calls
description: When a critical path (settlement) makes a mandatory external call without try/catch, the external contract's failure halts the entire protocol
type: feedback
---

# Liveness Coupling Through Mandatory External Calls

When a critical protocol function (e.g., batch settlement) makes a mandatory external call to a non-critical subsystem (e.g., fee forwarding to treasury), the non-critical subsystem gains veto power over the critical path. If the external call reverts, the entire operation fails.

**Why:** Discovered in R1 Integration (2026-04-03). VibeSwapCore.settleBatch() calls _forwardPriorityBids() which calls treasury.receiveAuctionProceeds() without try/catch. If treasury is paused, upgraded badly, or out of gas, ALL batch settlement halts. Priority bid forwarding is economically important but not settlement-critical — orders should still clear even if fee distribution temporarily fails.

**How to apply:** For every external call in a critical path:
1. Ask: "If this reverts, should the entire operation fail?"
2. If NO → wrap in try/catch, queue for retry, emit event
3. If YES → the external contract is part of the critical path and needs the same uptime guarantees
4. Fee distribution, analytics, and notifications are almost never settlement-critical
