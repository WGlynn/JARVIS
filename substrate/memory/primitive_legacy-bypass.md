---
name: Legacy Bypass
description: Backward-compatibility functions that skip new safety mechanisms create parallel paths where the unsafe path remains available. Discovered in C5-CON-001.
type: feedback
---

When a new, safer mechanism is added alongside an old one for "backward compatibility," the old function becomes an escape hatch that bypasses all new protections. Comments saying "will be removed in Phase 2" are not enforcement.

**Canonical example**: NakamotoConsensusInfinity had `requestStakeWithdrawal()` (7-day unbonding) alongside the legacy `withdrawStake()` (immediate). Any validator could simply call `withdrawStake()` to skip the entire unbonding period. Flash loan → register → vote → withdrawStake in one block.

**Why:** The developer's mental model was "new users will use the new function, old integrations need the old one temporarily." But attackers don't follow conventions — they use whichever function is most advantageous.

**How to apply:**
- When adding a safer replacement, DEPRECATE the old function immediately (revert with message)
- Never leave two paths to the same state transition with different safety properties
- "Phase 2 cleanup" items that are security-relevant must be Phase 1 items
- Backward compatibility is a feature concern, not a security exception
