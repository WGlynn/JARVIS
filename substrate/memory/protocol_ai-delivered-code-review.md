---
name: AI-Delivered Code Review Protocol
description: Ordered sequence for reviewing a codebase delivered by another AI (Gemini, GPT, etc.) or handed off from an unknown source. Leads with theater detection so context isn't wasted on code that doesn't match its advertised capabilities.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**When to invoke:** user hands you an archive / repo / directory produced by a model (often from AI Studio, Lovable, v0, Replit, similar). User's implicit ask is usually "review this the way you would."

**Sequence (ordered — do not skip steps):**

1. **Unpack and list.** Unzip into a scratch folder. Enumerate all files. Count lines per source file. Goal: know the shape before reading contents.

2. **Theater check — FIRST read.** Open `package.json` (or equivalent). Diff declared deps against actually-imported modules. See [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md). If theater ratio > 20%, flag immediately in the review — every capability downstream is now suspect.

3. **Config sweep.** `vite.config.ts`, `tsconfig.json`, `.env.example`, `README.md`. Note env vars referenced but not read. Note declared aliases unused. Note build scripts that reference tools not in deps.

4. **Read main module top-to-bottom.** For most AI-delivered SPAs this is one large `App.tsx` or `main.py`. Do not skim. Capture:
   - Unused imports
   - Dead state
   - Side effects in state updaters (React footgun)
   - Closure-over-stale-state in effects
   - Deprecated APIs (`.substr()`, etc.)
   - Memory leaks (timeouts without unmount guard)
   - Hard-coded viewport reads (`window.innerWidth` on render)
   - Whitespace where a CSS class doesn't exist in the chosen framework (Tailwind v4 silent no-ops)

5. **Verify against the handoff / stated spec.** If a handoff doc came with the code, check each claim. Aesthetic rules, functional claims, constraint rules (iframe, no alerts, no window.open). Note drift.

6. **Structure the review.** Severity-ordered (HIGH / MEDIUM / LOW). Each finding cites `file:line`. End with:
   - Dead weight list
   - Aesthetic drift list
   - Philosophy compliance call
   - Minimal-change list (NOT a refactor; match what the handoff permits)

7. **Decide the path.** Is the artifact salvageable as-is (Path A, commit to full wiring) or should it become the DEFERRED showcase (Path B, strip to minimal working version)? See [Deferred Showcase Branching](primitive_deferred-showcase-branching.md).

8. **If Path B: execute the minimal rewrite.** Do not refactor in place. Scaffold a parallel directory. Copy shared files (tsconfig, index.html, main entry). Write a new App.tsx that keeps the aesthetic where it earns its keep. Drop theater.

9. **Type-check + build.** `tsc --noEmit` must be clean. `vite build` (or equivalent) must succeed. Without both, the review is incomplete.

10. **Re-zip + HANDOFF.md.** Every delivered artifact gets a handoff doc pointed at the next AI/human. Tone. Constraints. What was dropped and why. What to build next.

**Standing variations:**
- If handoff is Agile-audience ([REDACTED-NDA]-class), tone down the Brutalist vocabulary in the HANDOFF doc.
- If the artifact is production-adjacent (not prototype), add a security-review pass after step 4.
- If the artifact is a library (not app), the theater check becomes "what's exported but not used by any dependent?"

**Related primitives:**
- [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md)
- [Deferred Showcase Branching](primitive_deferred-showcase-branching.md)
- [Path Commitment Protocol](protocol_path-commitment.md)

**Applied instances:**
- Lineage IDE plugin (2026-04-18) — full 10-step protocol executed. Theater ratio 38%. Path B chosen. Minimal rewrite shipped with sub-10ms perf instrumentation. Showcase stashed as `_DEFERRED`.
