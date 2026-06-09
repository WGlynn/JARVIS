---
name: Slash-Before-Count
description: In consensus/governance voting, detect and slash equivocation BEFORE counting vote weight — otherwise tainted weight persists even after slashing
type: feedback
---

Slash-Before-Count: equivocation detection must precede vote accounting.

**Why:** NCI-013 found that the original NakamotoConsensusInfinity.sol detected equivocation AFTER adding vote weight to the proposal. The equivocator's weight persisted on both proposals even after slashing. This means a whale could push a proposal over the 2/3 threshold using tainted weight.

**How to apply:** In any voting/consensus system with slashing:
1. Check for conflicting behavior BEFORE modifying proposal state
2. If detected, slash the actor and return (don't revert — revert rolls back the slash)
3. Use O(1) equivocation detection (mapping, not array iteration)

The "don't revert" part is critical — `revert` after state mutation undoes the mutation. Slash + return keeps the slash persistent.
