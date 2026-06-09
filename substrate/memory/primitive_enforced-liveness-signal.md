---
name: Enforced Liveness Signal
description: If a contract defines a liveness mechanism (heartbeat, activity window, staleness grace), some on-chain code path MUST consume that signal to gate privileged action or allow eviction. Unused liveness constants are security theater.
type: primitive
originSessionId: 5ba12ced-49bc-424a-9145-a73ee63cbeb6
---
# Enforced Liveness Signal

## The Rule

**A liveness primitive — heartbeat timestamp, activity counter, grace window constant — is not a security measure unless some code path reads it and changes behavior based on it.** Defining `HEARTBEAT_GRACE = 48 hours` and storing `lastHeartbeat` per actor without ANY function consuming those values is not "protection we'll wire up later." It's a NOP that creates a false sense of security.

Every liveness signal needs at least ONE of:
1. A **gate**: privileged actions (claim, report, withdraw, vote) revert if the actor is stale
2. A **permissionless eviction**: anyone can remove a stale actor from the active set
3. A **weighted penalty**: stale actors' weight/reward decays or zeros until they refresh

Without one of these, the liveness signal is architecturally decorative.

## Why

A heartbeat is a promise: *"as long as you keep proving you're alive, you keep your privileges"*. If the contract never checks whether the promise was kept, the privileges are granted regardless. An attacker can register once with whatever cheap commitment the system accepts, then walk away — continuing to accrue rewards, weight, or votes indefinitely.

The failure mode is invisible to unit tests written at the happy path:
```solidity
function test_heartbeat() { user.heartbeat(); assertEq(shard.lastHeartbeat, block.timestamp); }  // passes, proves nothing
```

The bug is a LINE OF CODE that isn't there — nothing reads `lastHeartbeat` in a branch-changing way. Only adversarial review (or "what happens if I never heartbeat again?") surfaces it.

## Applied Instance

**C10-AUDIT-2 (HIGH, ShardOperatorRegistry):**
- `HEARTBEAT_INTERVAL` and `HEARTBEAT_GRACE` constants existed
- `heartbeat()` function wrote `lastHeartbeat`
- **No function read `lastHeartbeat`** — operator could register, report max cellsServed, disconnect permanently, and continue claiming rewards forever
- Fix applied three gates simultaneously:
  1. `_isStale` internal check
  2. `reportCellsServed` and `claimRewards` revert when stale
  3. Permissionless `deactivateStaleShard(bytes32)` eviction with stake-returned-no-slash semantics
- Also extracted the primitive: anyone can reap, no authorization gate on eviction (attacker-resistant via the `ShardNotStale` check)

The lesson: the grace window was defined; the enforcement wasn't. For 6 days of the contract's lifetime, the liveness constants were theater.

## Detection Rule

For any contract with a `lastX`, `heartbeat`, `activity`, `uptime`, or similar timestamp state variable, grep for consumers:

```bash
grep -n 'lastHeartbeat\|lastActivity\|uptime' contracts/**/*.sol
```

- If the variable is only **written**, never read → liveness theater. Add at least one gate or eviction path.
- If the variable is read only in a view function that nothing else uses → liveness theater. Views don't enforce anything.
- If a `GRACE` or `INTERVAL` constant is defined but the only reference is the constant declaration itself → liveness theater.

The quickest fix is usually a view like `_isStale(actor) internal view` consumed by the privileged paths and an externally-callable `deactivateStale(id)` for eviction.

## Design Guidance

When you ADD a liveness signal to a contract, design the enforcement path in the same PR:

1. Write the `isStale(actor)` or `_isStale(actor)` computation first
2. Identify every privileged action the actor can take (claim, vote, report, withdraw)
3. Gate each one on `!_isStale(actor)` OR explicitly document why it's safe to let stale actors call it
4. Add a permissionless eviction — never require owner/governance to clean up; it doesn't scale

Without step 2-4, the liveness state variable should not exist. Either enforce it or delete it.

**Why:** Liveness promises without enforcement are reward-drain vectors. Silent accumulation by offline/dead actors steals from honest participants who are paying the opportunity cost to stay live.

**How to apply:** Every time you add a liveness timestamp, write the eviction function in the same commit. Every time you audit a contract with a liveness mechanism, grep for the enforcement path. If it's missing, it's a HIGH — unused liveness is theater.
