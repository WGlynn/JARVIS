---
name: Settlement State Durability
description: Cross-chain / async settlement callbacks that silent-catch for channel safety must layer (1) durable failure record, (2) permissionless retry, (3) downstream gate on pending-state counter. Any single layer is a half-fix. Extracted from C15+C20 (2026-04-16).
type: primitive
originSessionId: 3f731476-3cfc-4cea-97e7-84c17cd7bd13
---
# Settlement State Durability

## The Rule

**When an async settlement callback MUST silent-catch (LayerZero channel, inbound message, trusted-caller requirement), the caller is obligated to layer three defenses. Fewer than three leaves a consistency gap.**

1. **Durable failure record** — silent catch writes a flag and emits an event. Observability alone is not enough; the flag is what the retry path reads.
2. **Permissionless retry** — anyone can re-drive the state machine from the flag. Auth on retry defeats the purpose; the liveness of consistency must not depend on a single caller.
3. **Downstream gate on pending-state counter** — every dependent action (withdraw, settle, claim) checks a counter that decrements ONLY on terminal transition. The gate closes the double-spend window even when the retry path lags.

Any single layer is a **half-fix**. Shipping a half-fix is acceptable if the remaining surface is documented and the closure is queued — but never claim the class is closed until all three layers land.

## Why

C15 fixed the silent-catch at `CrossChainRouter._handleSettlementAck`: if `markCrossChainSettled` reverted (gas starvation, paused core, reentrancy guard), the router emitted `SettlementAckFailed` and flipped a flag. Permissionless `retrySettlementMark(commitHash)` (CrossChainRouter.sol:847) re-drove the mark. Good, but incomplete.

The gap: between "silent catch" and "retry", the deposit at `VibeSwapCore` was still withdrawable. Trader receives output on destination chain, then calls `withdrawDeposit(tokenIn)` on source → classic cross-chain double-spend. Retry latency IS the attack window.

C20 closed the gap at the withdrawal side. `pendingCrossChainCount[trader][token]` (VibeSwapCore.sol:235) increments on order creation (line 775), decrements on PENDING/REFUND_REQUESTED → SETTLED (line 829-830) or REFUND_REQUESTED → REFUNDED (line 899-900). `withdrawDeposit` reverts `CrossChainOrdersPending()` if counter > 0 (line 699).

Now even if retry is delayed indefinitely, withdrawal stays blocked. Three independent defenses, each closing a different attack surface.

## When It Applies

All three must hold:
1. **Async callback** — the state transition lives on a message-passing boundary (LayerZero, cross-rollup bridge, Chainlink CCIP, or any out-of-contract trigger).
2. **Silent catch required** — reverting would freeze the messaging channel, blackhole funds in the bridge, or prevent operator rotation. The catch is not optional.
3. **Catch carries safety invariants** — the operation being caught has implications beyond "this one thing failed." If the catch hides a consistency bug, the invariants are affected.

If (1) fails, use normal revert-on-failure. If (2) fails, just revert. If (3) fails, the catch is pure observability and a log event suffices.

## The Contract Pattern

```solidity
// Layer 1: durable failure record in the callback
function _handleAck(Message calldata m) internal {
    try target.apply(m) {
        emit AckApplied(m.id);
    } catch {
        ackFailed[m.id] = true;           // durable flag, not just event
        emit AckFailed(m.id);
    }
}

// Layer 2: permissionless retry
function retryAck(bytes32 id) external nonReentrant {
    if (!ackFailed[id]) revert NotPending();
    target.apply(pending[id]);            // revert if still broken — retry again
    delete ackFailed[id];
    emit AckRetried(id, msg.sender);
}

// Layer 3: downstream gate on counter
mapping(address => mapping(address => uint256)) public pendingCount;

function createOrder(...) external { pendingCount[user][token]++; ... }
function terminalTransition(...) internal {
    if (pendingCount[user][token] > 0) pendingCount[user][token]--;
    ...
}
function dependentAction(...) external {
    if (pendingCount[msg.sender][token] > 0) revert OrdersPending();
    ...
}
```

## State Invariants

1. **Counter monotonicity**: increments ONLY on creation, decrements ONLY on a terminal transition (SETTLED, REFUNDED — not PENDING or REFUND_REQUESTED).
2. **Decrement idempotency**: the terminal transition may fire via multiple paths (natural settle, retry, refund). Counter must not underflow if fired twice — guard with `if (counter > 0)` before decrement.
3. **Retry is stateless re-entry**: calling `retryAck` on a non-failed id reverts; calling it twice is safe (second call reverts `NotPending`).
4. **Gate reads counter, not flag**: `dependentAction` must check the counter, not the `ackFailed` flag. The flag is for retry liveness; the counter is for consistency.
5. **Storage gap reduced by counter slot**: UUPS-upgradeable contracts must shrink the `__gap` to account for the new mapping.

## Applied Instances

| Contract pair | Silent-catch callback | Retry | Counter gate | Status |
|---------------|----------------------|-------|--------------|--------|
| CrossChainRouter ↔ VibeSwapCore (settle path) | `_handleSettlementAck` silent-catches `markCrossChainSettled` | `retrySettlementMark` (permissionless, CrossChainRouter.sol:847) | `pendingCrossChainCount` (VibeSwapCore.sol:235), gate at `withdrawDeposit:699` | ✅ COMPLETE (C15 layers 1+2, C20 layer 3) |
| CrossChainRouter ↔ VibeSwapCore (refund path) | `executeCrossChainRefund` | same retry path via REFUND_REQUESTED → REFUNDED | same counter, decrements on line 899-900 | ✅ COMPLETE |
| AttributionBridge settlement (if added) | — | — | — | ⚠️ check before adding async settlement here |

## Candidates for Future Application

- **LayerZero inbound messages elsewhere** — any `_lzReceive` that touches state with economic implications. Grep for `try ... catch` in message handlers.
- **Oracle callbacks** — if TruePriceOracle or any Chainlink callback mutates state beyond price, apply the three-layer test.
- **Bridge deposit/withdrawal pairs in general** — any two-sided protocol where one side fires async toward the other carries this class.

## Design Traps to Avoid

- **Layer 1 without Layer 2**: durable flag but no public retry → consistency depends on a privileged caller noticing the event. If that caller is down or misconfigured, the gap stays open indefinitely.
- **Layer 2 without Layer 1**: public retry function reading transient state (tx-level memory, last-block flag) — the retry has nothing to re-drive. Must read a persistent flag.
- **Layer 1+2 without Layer 3**: this is the C15 state, documented as partial. Correct fix is NOT to leave it indefinitely but to schedule the Layer 3 closure. **A half-fix with a documented backlog is superior to delaying both; a half-fix without a backlog is regression.**
- **Gate on the wrong key**: counter keyed by `(trader, token)` must match the dimension the withdrawal path reads. If `withdrawDeposit(token)` is per-token but counter is per-order-id, the gate doesn't fire.
- **Decrement on non-terminal state**: decrementing on `PENDING → IN_FLIGHT` opens the window. Only decrement when the order leaves the attack surface (SETTLED or REFUNDED).
- **Counter drift under retry**: if retry decrements the counter AND the natural settle path also decrements, counter goes negative. Idempotent decrement (guard with `> 0`) fixes this, but better is: only the terminal transition decrements, never the retry itself.

## Library Extraction (Deferred)

Pattern has 1 complete use site (router↔core settle/refund). A second use site — e.g., oracle callback or separate bridge — would justify extracting a `SettlementStateDurability` abstraction. Shape is likely:
- `AsyncCallbackHarness` — wraps try/catch + flag
- `PendingCounterGate` — mapping + increment/decrement + check

Don't generalize at n=1. The second use site will reveal what the abstraction actually needs.

## Relation to Other Primitives

- **Post-Upgrade Init Gate** (C9) — same shape: explicit + permissionless recovery step. Both make recovery a named, callable action rather than a hope.
- **Enforced Liveness Signal** — heartbeat constants without gates are theater. The Layer-3 counter is the anti-theater mechanism for this class.
- **Triage-Before-Fix Discipline** (C16 candidate) — C20 only happened because C15's incomplete closure was documented on the backlog, not forgotten.

## How to Apply

When reviewing any new async settlement path:
1. Identify the callback that silent-catches.
2. Ask: "If this catch hides a consistency bug, what downstream action could exploit the window?"
3. Find the downstream action. It MUST read a counter that only terminal transitions decrement.
4. If all three layers aren't present, either add them or document the gap on the backlog with severity.

**Why (meta):** Cross-chain double-spend is the single largest class of bridge exploit. The pattern above is the minimum viable defense. Any simpler structure has a known attack against it — this is not over-engineering, it is the floor.
