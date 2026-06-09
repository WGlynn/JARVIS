---
name: Observer Effect Discipline
description: A measurement that causes the latency it measures is worse than no measurement. Instrumentation must be side-effect-free on the hot path, and preferably toggleable so it only runs when someone is looking.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** the measurement layer must not perturb the layer it is measuring. If adding a gauge slows the hot path, the gauge is reading its own noise, not the system. Instrumentation is side-effect-free on hot paths; display is deferred to off-path ticks.

**Why:** in physics the observer effect is fundamental; in software it is a choice. A `console.log` in a tight loop, a `setState` on every keystroke to display keystroke latency, a `performance.mark` that triggers a render — all of these measure a system that includes their own cost. Results are polluted from the first sample. Worse, the instrumentation becomes the bottleneck, and "fixing performance" means removing the gauges, which makes the problem invisible rather than solved.

**How to apply:**
1. **Hot path writes to refs, not state.** The measurement lands in a mutable ref or a ring buffer. No re-render is triggered.
2. **Display layer reads on a different schedule.** `requestAnimationFrame` once per frame, or a polling effect at the UI's refresh rate. Display never gates the measurement.
3. **Toggle the display.** If nobody is looking, don't paint. Hide the HUD by default; open on demand. You do not cause the latency you do not display.
4. **Measure the measurement once.** Benchmark your instrumentation overhead in isolation. If it exceeds 1% of the measured path, the gauge is the bottleneck.
5. **Keep measurement monotonic.** `performance.now()` not `Date.now()`. Never reset counters except via explicit control.

**Applied instances:**
- Lineage IDE plugin: keystroke latency stored in ref on `onInput`; display flushed via `requestAnimationFrame`. Frame-time HUD only ticks when HUD is open (`perfHudOpen` state gates the display setState). (`lineage-ide-plugin-minimal/src/App.tsx`.)

**Anti-patterns:**
- Calling `setState` inside the thing you are timing. The setState triggers reconciliation, which dominates the timing.
- Logging every event to `console.log`. `console.log` is surprisingly slow and blocks the main thread.
- Measuring from inside a `useEffect` that depends on the thing you are measuring. The effect schedule is part of the latency.

**Related primitives:**
- [NC-Max Bottleneck Breaking](primitive_nc-max-bottleneck-breaking.md) — measurement is the precondition for finding the real constraint.
- [Slash-Before-Count](primitive_slash-before-count.md) — related discipline: don't count what you don't need. Here: don't measure what you're not displaying.

**Standing instruction:** before adding instrumentation, answer "where does this measurement get stored, and on what schedule is it displayed?" If the storage is state and the schedule is immediate, the gauge is poisoning the reading.
