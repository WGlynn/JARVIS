---
name: Self-Theater Audit Gate
description: The same multi-pass audit we run on AI-delivered code, turned inward as an automated pre-ship gate. Don't ship what you wouldn't accept from Gemini. Runs zero-new-dependency in-house checks.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** every check we apply when reviewing someone else's AI-delivered artifact must also run against our own builds, automated, as a ship gate. Asymmetry between "what we'd reject" and "what we'd ship" is the hole that produces our own theater.

**Why:** after reviewing Gemini's Lineage IDE plugin (2026-04-18), we identified theater via the dep diff. Then we built our own minimal version — and inherited the same risk of shipping theater of our own. The fix is not vigilance (vigilance decays); the fix is a gate that runs unconditionally.

**How to apply:**

1. **Codify each manual check as a script.** Zero new dependencies if possible — pure Node over the repo on disk is portable and ages well. Each check is a named pass with a thresholded verdict.
2. **Wire into a `preship` / `audit:all` npm script.** The gate runs on `preship` (before `vite build`) and optionally in CI. Hard fails exit 1.
3. **Seven passes** (from Lineage IDE plugin, 2026-04-18 — generalize to other stacks):
   - Theater (dep, env, marker)
   - Correctness (`tsc --noEmit`, `any` / `@ts-ignore` / unhandled promises)
   - Performance (bundle size, render-time `Math.random()`, inline `[...Array(N)]`)
   - Security (`dangerouslySetInnerHTML`, `eval`, `new Function`, `innerHTML=`, insecure URLs)
   - Resources (unpaired listeners, timers, workers, rAF)
   - Accessibility (empty buttons without aria-label, `<img>` without alt, `<input>` without label)
   - Dependencies (version discipline, `npm audit` high-or-critical)
4. **Hard vs soft fails.** Hard fails block ship (exit 1). Soft fails warn but pass. Tune thresholds from observation — the ratio, not the raw count, is usually the right metric.
5. **Warnings that persist are either real or false positives** — if false, refine the heuristic; if real, document the exception. Do not accumulate unacknowledged warnings.

**Applied instances:**
- Lineage IDE plugin: `scripts/theater-check.mjs` (pass 1 only) + `scripts/audit-all.mjs` (all 7 passes). `npm run audit:all` runs all seven. `preship` script chains `lint → audit:all → build`. Ships with 0 fail, 2 warn (both false positives from heuristic limitations — known, acknowledged). (`Desktop/lineage-ide-plugin-minimal/scripts/`.)

**Anti-patterns:**
- Manual "I'll remember to check" discipline. Fails under time pressure. The gate IS the discipline.
- Vendor tooling (eslint + plugin + plugin + plugin). Every plugin is itself a dep that can rot. In-house Node scripts are simpler, version-stable, and auditable.
- Silent warnings. Warnings that pile up become invisible. Force a ✗ / ⚠ / ✓ summary that forces daily eyes on the totals.

**Related primitives:**
- [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md) — the Pass 1 check in abstract form.
- [Verbal → Gate](primitive_verbal-to-gate.md) — "I'll check for X" without a hook = violation. Applied to build audits.
- [System-Importance → Gate](primitive_system-importance-to-gate.md) — meta-rule: important constraints become hooks.
- [Always = Gate](primitive_always-equals-gate.md) — "we always audit" = script, not memory.

**Standing instruction:** any quality check you apply manually more than once becomes a scripted pass in the audit suite within the same session. Manual review is a debugging tool; the gate is the product.
