---
name: NC-Max Bottleneck Breaking
description: The bottleneck is never where instinct points. Measure every layer, find the real constraint, attack from the dimension nobody is optimizing. Applies universally — UI, distributed systems, any perf work.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** when chasing a performance target, do not optimize the layer everyone assumes is the constraint. Instrument every layer, find the real bottleneck, then attack it from a dimension the conventional framing doesn't consider.

**Why:** Ren Zhang's NC-Max (2020) broke Bitcoin's throughput-vs-latency tradeoff. The conventional framing said the choice was block size vs block interval. Zhang showed the real constraint was **block propagation time**, and broke the tradeoff by decoupling transaction dissemination from block dissemination — a dimension nobody was optimizing. Same pattern shows up in every domain: CPU caches vs clock speed, React reconciliation vs memoization, database write throughput vs index speed. The visible knob is rarely the bottleneck.

**How to apply:**
1. **Name the naive bottleneck.** Where does instinct point?
2. **Measure every layer.** Add instrumentation at each stage. The real constraint surfaces only with data.
3. **Identify the unexpected dimension.** If the coupled pair is "A vs B," look for the hidden C that both A and B depend on. Break C and the tradeoff collapses.
4. **Decouple what looks coupled.** UI state ≠ durability state. Transaction dissemination ≠ block dissemination. Throughput ≠ confirmation time. Find the hidden coupling; split it.
5. **Only then optimize.** Optimizing the wrong layer locks in the wrong tradeoff.

**Applied instances (this codebase):**
- Lineage IDE plugin — naive framing was "make React faster." Real constraint was that React state changed per keystroke. Fix: uncontrolled textarea, refs + rAF. Reconciliation eliminated entirely. (`lineage-ide-plugin-minimal/src/App.tsx`)
- Persist latency: naive framing was "make the save call fast." Real constraint was that UI state gated on backend ack. Fix: optimistic commit. Durability runs below the UI layer. (Same file, `persist()`.)

**Related primitives:**
- [Eliminate, Don't Optimize](primitive_optimize-around-vs-eliminate.md) — the corollary at the tactic level.
- [Running Total](primitive_running-total-pattern.md) — a specific case of attacking the hidden constraint (O(1) update vs O(n) recompute).
- [Parallelism Convergence](primitive_parallelism-convergence-2017.md) — 2017's Transformers + UTXO independently broke sequential bottlenecks.

**Standing instruction:** every new perf target starts with "name the naive bottleneck, then measure to find the real one." Do not skip the measurement step.
