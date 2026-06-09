---
name: Dead Guard Anti-Pattern
description: Inherited guard modifiers without corresponding state updates create security theater — the check passes forever
type: feedback
---

# Dead Guard Anti-Pattern

When a contract inherits a base with guard modifiers (e.g., `whenBreakerNotTripped`) but never calls the corresponding state mutation (e.g., `_updateBreaker`), the guard becomes security theater. It compiles, it looks protective, it never fires.

**Why:** Discovered in R1 Integration (2026-04-03). VibeSwapCore inherits CircuitBreaker and uses `whenBreakerNotTripped(VOLUME_BREAKER)` on commitSwap/revealSwap. But `_updateBreaker` is never called anywhere in VibeSwapCore. The breaker's accumulator stays at 0 forever. The modifier is a no-op.

**How to apply:** When inheriting a stateful guard base contract:
1. Grep for every `when*` modifier usage — verify each has a corresponding state update call
2. If you guard with a breaker, you MUST update that breaker somewhere in the same contract
3. If the update happens in a different contract (e.g., AMM updates volume, Core checks it), they share no state — the check is dead
4. Consider: should the guard be on the contract that UPDATES the state, not one that merely CHECKS it?
