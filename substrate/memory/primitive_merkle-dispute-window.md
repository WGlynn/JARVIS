---
name: Merkle Commit-Dispute-Finalize
description: Self-reported numeric metrics feeding economic reward distribution need a commit-dispute-finalize window, not direct updates. Pattern extracted from C10-AUDIT-3 (cellsServed). Applies to any (reporter → claim → weight) flow where the claim isn't trustlessly verifiable from other on-chain state.
type: primitive
originSessionId: 5ba12ced-49bc-424a-9145-a73ee63cbeb6
---
# Merkle Commit-Dispute-Finalize

## The Rule

**When a self-reported numeric claim feeds economic reward distribution — and the claim can't be derived from other on-chain state — route it through a commit-dispute-finalize window, never directly into state.**

Direct self-report:
```solidity
function reportScore(uint256 score) external { state.score = score; weight = f(score); } // bad
```

Commit-dispute-finalize:
```solidity
function commitScore(uint256 score, bytes32 merkleRoot) external { pending[msg.sender] = (score, root, now); }
function challengeScore(bytes32 actor, uint256 leafIndex) external payable { ... }
function respondToChallenge(bytes32 actor, bytes32 leafValue, bytes32[] calldata proof) external { ... }
function finalizeScore(bytes32 actor) external { /* after window, no challenge */ state.score = pending.score; }
function claimDisputeSlash(bytes32 actor) external { /* response-deadline expired */ slash; }
```

The claim is a *commitment* to a Merkle tree whose leaves are the individual sub-claims. The challenger names a leaf index; the reporter must prove membership with a valid Merkle proof. No proof, or invalid proof → slash.

## When it applies

All three must hold:
1. **A user-submitted number** directly or proportionally drives reward distribution, weight, or some other economic benefit to that user.
2. **The number cannot be verified** from the contract's own state or other on-chain state (off-chain ground truth).
3. **The economic value of a sybil'd claim exceeds the bond + gas to defend a real one.**

If (1) fails, there's no incentive to lie. If (2) fails, verify directly — simpler. If (3) fails, just cap the claim; dispute-response isn't worth the gas.

## The Contract Pattern

```solidity
// Tunable per-contract
uint256 constant CHALLENGE_WINDOW = 1 hours;      // delay before finalization
uint256 constant RESPONSE_WINDOW = 30 minutes;    // reporter's window to respond
uint256 constant BOND = 10e18;                    // challenger stake
uint256 constant SLASH_BPS = 1000;                // 10% of reporter's collateral

struct PendingReport {
    uint256 count;
    bytes32 merkleRoot;
    uint256 commitAt;
    uint256 finalizeAt;
    address challenger;
    uint256 challengeIndex;
    uint256 challengerBond;
    uint256 challengeDeadline;
    bool resolved;
}

// Leaf format: keccak256(abi.encode(uint256 index, <payload>))
// The (index, payload) binding is load-bearing — challenger names index,
// reporter must produce payload matching that index, ruling out both
// "wrong payload" and "no payload at that position" at once.
```

## State Invariants

1. **One in-flight per subject**: the pending slot must be empty or resolved before a new commit lands.
2. **Window monotonicity**: finalizeAt > commitAt; challengeDeadline > challenge submission time.
3. **Slash clamped to stake**: `slash = min(stake × SLASH_BPS / 10_000, stake)` — never underflow.
4. **Resolved flag is terminal**: once true, the struct is frozen (finalized, refuted, or slashed). Operator must commit a NEW report (clears the slot).
5. **Bond is return-path-exclusive**: successful refute → bond to operator; successful slash → bond to challenger. Never both, never neither.

## Applied Instances

| Contract | Self-reported field | Status |
|----------|---------------------|--------|
| ShardOperatorRegistry (C10-AUDIT-3) | `cellsServed` per operator | ✅ IMPLEMENTED — `commitCellsReport` / `challengeCellsReport` / `respondToChallenge` / `claimChallengeSlash` / `finalizeCellsReport` |
| AttributionBridge | merkleRoot of (address, score) pairs for Shapley rewards | ❌ LIVENESS THEATER — 24h challenge period declared but no challenge function. See C11-D fix. |

## Candidates for future application

- **VibeDeviceNetwork.submitData** — device-reported `dataPoints` accumulates into a global counter; off-chain reward distribution likely proportional. Currently no validation.
- **VibeReputation / BehavioralReputationVerifier** — scoring paths that feed reputation-weighted rewards.
- **TruePriceOracle** — already has authorized-signer model; a challenge-window layer would strengthen it without breaking the trust model (just adds a finalization delay).
- **TWAP oracle updates in VibeAMM** — if self-reported via a user-submitted checkpoint function (not internally computed), they're vulnerable.

## Design traps to avoid

- **Leaf without position**: `leaf = keccak256(payload)` lets a reporter produce ANY leaf from their tree to defeat a challenge on any index. Always encode position: `leaf = keccak256(abi.encode(index, payload))`.
- **Challenger pays nothing**: free challenges enable griefing (force response every few minutes). Bond must be non-trivial.
- **Response hash of wrong thing**: response must verify specifically `keccak256(abi.encode(challengeIndex, responseValue))` matches a proof into the COMMITTED root — not a new root, not a different hash scheme.
- **Slash doesn't update weight**: if stake drops via slash, totalWeight must update immediately (same tx) or downstream reward accounting diverges.
- **Finalize during active challenge**: allowing finalize while challenger is waiting on response is a bypass. Check `challenger == address(0)` OR `challengeDeadline < block.timestamp && slash claimed`.

## Library extraction (deferred)

The pattern is mature at 1 use site; 2+ use sites will justify extracting a `MerkleDisputeGate` library. Don't generalize prematurely — the first reuse will reveal what the abstraction actually needs.

**Why:** Self-reported economic inputs are the single largest category of DeFi rug vector. A sybil with zero cost to lie will always dominate honest reporters on Shapley-weighted distributions. The only known trustless solution is cryptoeconomic: raise the cost of lying above the reward.

**How to apply:** When adding any function that lets a user submit a number that affects their share of a reward pool, reach for this pattern first. If the cost of implementing the pattern exceeds the economic harm a liar could cause, use a simple cap instead. Don't skip and hope.
