---
name: Lineage IDE Plugin
description: Minimal IDE plugin for the Lineage persistence layer — sub-10ms interaction target, speculative hashing, optimistic persist. Built 2026-04-18 by stripping a Gemini-delivered Substrate-aesthetic showcase down to one load-bearing loop. Showcase stashed as DEFERRED.
type: project
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
## What exists (2026-04-18)

**Desktop artifacts:**
- `Desktop/lineage-ide-plugin-minimal.zip` — shippable minimal build. React 19 / Vite 6 / Tailwind v4 / Motion / TypeScript. ~350 LOC `App.tsx`. Sub-10ms perf HUD. Type-check clean, build clean.
- `Desktop/lineage-ide-plugin-minimal/` — working source directory.
- `Desktop/lineage-ide-plugin-showcase_DEFERRED.zip` — Gemini's original delivery + the 2026-04-18 review fixes. Substrate-aesthetic dashboard. Revive when real Gemini wiring + real transliteration + real DAG client exist.
- `Desktop/lineage-ide-plugin-showcase-src_DEFERRED/` — source for the deferred showcase.
- `Desktop/lineage-ide-plugin (1).zip` — original Gemini delivery, untouched.

## Lineage scope

Standalone product repo at `C:/Users/Will/lineage/`. Persistence-layer-for-knowledge-work. The plugin is a UI into that persistence layer, not the persistence layer itself. Plugin's `persist()` is a stub — the hook point where the real Lineage DAG client lands.

## What the minimal plugin does (today)

- Single uncontrolled `<textarea>` — a Lineage cell.
- `⌘S` persist — optimistic, flips UI to `saved` instantly, durability reconciles below.
- Speculative SHA-256 hash — runs on `requestIdleCallback`, cached by byte count. `persist()` reads the hash in O(1).
- Perf HUD (`⌘P`) — keystroke ms, persist (UI) ms, frame ms, hash (speculative) ms, cell hash prefix.
- Terminal drawer (`⌘\``) — `help`, `clear`, `save`, `status`, `perf`.
- Substrate aesthetic preserved in palette + fonts + projection-field utility. Brutalist restraint; no theater.

## What it does NOT do (intentionally)

- No real Gemini call (no `@google/genai` dep — deleted).
- No Rosetta two-projection transliteration (was theater in showcase).
- No drift simulation, no shunt system, no oscillation dials, no fake security score, no "field state" view.
- No blocking save spinner. Optimistic commit is architectural, not an optimization.

## Design decisions locked

- **Uncontrolled textarea, ref-driven.** React state per keystroke is the bottleneck; eliminating it beats optimizing it.
- **Optimistic persist.** UI flips on intent, not backend ack. Durability is a layer below.
- **Speculative hashing.** Work done before commit is invisible to the user.
- **Observer-effect-safe HUD.** Frame HUD only ticks when open.
- **One `App.tsx`.** No premature file splits. Add Zustand (or similar) only when the coupling demands it.

## Next build (in priority order)

1. Replace the `persist()` stub with a real Lineage DAG client. Move hashing + signing + write into a Web Worker so the main thread stays at zero-latency. Reconcile to `error` on rejection, not on success.
2. IndexedDB shadow-buffer — write on typing pauses, `persist()` promotes. Enables offline-first + zero-latency durability.
3. Cell history — `history` terminal command, shows last N persisted cells with hash suffixes.
4. Minimal syntax highlight (Python first). Budget: < 5ms render, add as its own perf-HUD layer.
5. Only after 1–4: consider reviving the showcase's Rosetta two-projection UI.

## Connection to broader work

- **Plugin is a projection of the Stateful Overlay thesis** — externalized state (cells) live on disk/in-DAG; in-session state (textarea) is a view. Consistent with [Stateful Overlay primitive](primitive_stateful-overlay.md).
- **[REDACTED-NDA] workshop material** — the minimal build is a concrete demonstration of workflow patterns that generalize beyond VibeSwap. Primitives and protocols extracted from this build form the basis for the 2026-04-18 [REDACTED-NDA] report.
- **Class of tool, not instance.** The build pattern (review → path commitment → minimal rewrite with sub-10ms target) is the reusable asset. The IDE plugin is one instance.

## Primitives extracted from this build

- [NC-Max Bottleneck Breaking](primitive_nc-max-bottleneck-breaking.md)
- [Speculative Execution Over Idle Gaps](primitive_speculative-execution-idle.md)
- [Optimistic UI / Durability Layer Split](primitive_optimistic-ui-durability-split.md)
- [Observer Effect Discipline](primitive_observer-effect-discipline.md)
- [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md)
- [Deferred Showcase Branching](primitive_deferred-showcase-branching.md)

## Protocols extracted

- [AI-Delivered Code Review Protocol](protocol_ai-delivered-code-review.md)
- [Path Commitment Protocol](protocol_path-commitment.md)

## Commands

```bash
cd Desktop/lineage-ide-plugin-minimal
npm install
npm run dev     # http://localhost:3000
npm run lint    # tsc --noEmit
npm run build
```

## Keyboard

- `⌘S` — persist
- `⌘\`` — terminal drawer
- `⌘P` — perf HUD
