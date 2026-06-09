---
name: Settlement-Time Binding
description: Parameters that affect economic outcomes must be bound at settlement time, not creation time. Creation-time binding enables front-running between creation and settlement.
type: feedback
---

# Settlement-Time Binding

Any parameter that determines how value is distributed must be read at the moment of distribution, not when the game/auction/pool was created.

**Why:** TRP R24 (N06) found that ShapleyDistributor applied halving at game creation, not settlement. A creator could manipulate the halving schedule by timing game creation relative to era boundaries. R24 (N03) found quality weights could be front-run because they were set before settlement. Both are the same primitive: creation-time binding creates a manipulation window.

**How to apply:**
1. Identify every parameter that affects value distribution (halving schedule, quality weights, fee rates, price oracles)
2. Ask: "Can someone change this parameter between when the game starts and when it settles?"
3. If yes, either snapshot at commitment time (so changes don't affect committed participants) or read at settlement time (so the latest value applies uniformly)
4. Never allow a parameter to be both mutable AND bound at creation time — that's the manipulation window

**Generalization:** This is the DeFi equivalent of TOCTOU (time-of-check to time-of-use). Any system with a delay between commitment and execution must bind economic parameters at execution, not commitment. Applies to: batch auctions, governance proposals, vesting schedules, reward distributions.
