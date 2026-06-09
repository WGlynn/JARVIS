---
name: Deposit Identity Propagation
description: When a proxy acts on behalf of a user across trust boundaries, the original depositor identity must be explicitly threaded through every operation. Loss of identity = loss of funds.
type: feedback
---

# Deposit Identity Propagation

When contract A calls contract B on behalf of user U, B sees A as msg.sender — not U. If B records A as the depositor, U loses claim to their funds.

**Why:** CrossChainRouter accumulated 10+ TRP findings (R21-R48) from this single root cause. The router acts as a proxy for cross-chain users, but every downstream contract recorded the router's address instead of the user's. Five separate findings (NEW-03, NEW-04, NEW-10, L-01, H-03) all trace to the same architectural gap.

**How to apply:**
1. Every function that accepts deposits on behalf of another address must take an explicit `address depositor` parameter
2. Never derive depositor from msg.sender when the caller is a contract/router
3. Cross-chain flows need explicit identity transformation at every hop
4. Recovery/refund functions must send to the recorded depositor, not the current caller
5. Test: call the function from a different address than the intended depositor — does the right person get credited?

**Generalization:** This applies to ANY proxy pattern — meta-transactions, forwarders, relayers, routers, keepers. The identity of the beneficiary must be a first-class parameter, not inferred from execution context.
