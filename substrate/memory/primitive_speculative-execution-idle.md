---
name: Speculative Execution Over Idle Gaps
description: Expensive deterministic work that will eventually be needed should run during idle time so the user's commit moment is near-free. Generalizes to hashing, prefetching, pre-compilation, pre-rendering.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** any deterministic work whose input is available before the user commits should run speculatively during idle time. At commit, the result is already cached — commit latency drops to pointer-copy.

**Why:** NC-Max's two-step confirmation pre-disseminates transactions so the block commit is near-free. CPU branch prediction is the same pattern at the chip level. The user's perceived latency is the work done *after* their commit; anything done *before* is invisible. If the work is deterministic and the input is stable, there is no reason to pay for it at commit time.

**How to apply:**
1. **Find the deterministic prefix** of an expensive operation. Hashing, signing, serialization, compilation, layout — anything whose output depends only on already-known inputs.
2. **Schedule it during idle gaps.** `requestIdleCallback` in browsers, `setTimeout` fallback for Safari/Firefox holdouts, `setImmediate` in Node, worker threads for heavier work.
3. **Cache keyed by the deterministic input.** Re-speculating on the same input is waste; skip if the cache is still valid.
4. **At commit, check the cache first.** On hit, use the pre-computed result. On miss (user committed faster than idle could run), fall back to synchronous compute and log a "speculation miss" metric.
5. **Instrument speculation miss rate.** If misses are frequent, the idle window is too rare — consider running on typing pauses or `input` events with debounce instead.

**Applied instances:**
- Lineage IDE plugin: SHA-256 of the cell hashed on idle, cached by byte count. `persist()` reads the hash in O(1). Speculation miss counted in the log. (`lineage-ide-plugin-minimal/src/App.tsx`, speculative hash effect.)

**Candidates for future application:**
- Merkle root pre-computation in batch auctions (commit phase has 8s of idle — speculate the batch root during it).
- IPFS CID pre-computation in any content-addressed store.
- Strategy evaluation pre-runs in agent orchestration.
- Compilation of contract bytecode during edit sessions, not on deploy.

**Related primitives:**
- [NC-Max Bottleneck Breaking](primitive_nc-max-bottleneck-breaking.md) — speculative execution is the "attack the real constraint" tactic for any commit-gated latency.
- [Running Total](primitive_running-total-pattern.md) — a synchronous cousin: compute incrementally as inputs arrive rather than all-at-once at commit.

**Standing instruction:** when staring at a commit-latency budget, ask "what part of this work could have run already?" before asking "how do I make this faster?"
