---
name: Optimistic UI / Durability Layer Split
description: UI state reflects user intent, not backend acknowledgment. Durability lives in a layer beneath the UI, reconciles on error, never gates perception. Breaks the network-latency-ties-UI-latency coupling.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** the user's perception of an action completing and the system's durable record of that action are two different layers. The UI state machine MUST flip on intent; durability reconciles below. Network latency lives under the UI, not inside it.

**Why:** the conventional "show spinner → wait for ack → show success" pattern couples UI latency to network latency. In local-first and optimistic designs, that coupling is the bottleneck. By flipping UI state on intent, perceived latency drops to the frame time of the local render (~1-5ms). The backend's round-trip — 50ms, 500ms, 5s — becomes invisible unless it fails, in which case the UI reconciles to an error state. On success it stays silent; success was already shown.

**How to apply:**
1. **Identify the two state layers.** UI state (what the user sees) vs durability state (what the system has persisted).
2. **Flip UI state immediately** on user intent. Do not wait for the backend.
3. **Run durability in the background.** Web Worker, async fetch, IndexedDB write — whatever the persistence substrate is.
4. **Reconcile only on failure.** If durability rejects, the UI downgrades to an error/retry state. On success, do nothing — the UI already reflects success.
5. **Measure UI latency separately from durability latency.** They are different SLAs. UI gets <10ms. Durability gets whatever the network budget allows.

**Key invariant:** if the durability layer fails, the UI must be able to distinguish "intent shown, durability failed" from "intent shown, durability pending" from "intent shown, durability succeeded." A status enum with at least `idle | saved | reconciling | error` is the minimum; a monotonic clock/version vector is the robust version.

**Applied instances:**
- Lineage IDE plugin: `persist()` flips to `saved` instantly, logs UI ms separately from durability ms. On real DAG rejection, would reconcile to `error` and offer retry. (`lineage-ide-plugin-minimal/src/App.tsx`.)
- VibeSwap cross-chain settlement: the three-layer async-settlement primitive (Settlement State Durability) is this pattern generalized — silent-catch flag + retry + downstream counter gate.

**Anti-patterns:**
- **Blocking spinner on save.** The user has already composed their thought; gating the UI on persistence adds latency for no reason.
- **Hiding errors.** If durability fails silently, the user loses data. Reconciliation MUST surface failure.
- **Committing durability optimistically AND the UI optimistically.** Do not write the UI layer's optimism into the durability layer. Durability is truth; UI is perception. Keep them separate.

**Related primitives:**
- [Settlement State Durability](primitive_settlement-state-durability.md) — the cross-chain version of this pattern.
- [NC-Max Bottleneck Breaking](primitive_nc-max-bottleneck-breaking.md) — the layer-decoupling methodology.

**Standing instruction:** when the UI includes a "Saving…" spinner, it is wrong unless the user can be provably hurt by optimistic display. Default to optimistic. Earn the spinner with a specific failure mode.
