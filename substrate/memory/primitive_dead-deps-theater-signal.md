---
name: Dead Deps as Theater Signal
description: Declared-but-unimported dependencies reveal a codebase built as a stage set, not a running program. First-pass health check on any AI-delivered artifact: diff package.json against actual import statements.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** when reviewing any codebase — especially AI-generated — diff the declared dependency list against the set of actually-imported modules. Declared-but-unimported deps are a tell: the system was built to look like a product, not to be one. Treat them as a primary health-check metric, not a minor cleanup.

**Why:** an AI code generator optimizing for "looks right" will include deps that match the README or comments, even when nothing imports them. The Gemini-delivered Lineage plugin (2026-04-18) declared `@google/genai`, `express`, `dotenv`, `tsx`, and `@types/express` — zero imports of any. The pattern reveals the generator's target was "plausible package.json for an IDE plugin" rather than "working IDE plugin." Every future AI-delivery review should lead with this diff; it catches theater faster than reading the code.

**How to apply:**
1. **On first receipt of an AI-delivered codebase**, run dep-vs-import diff before reading code.
   - `grep -rhEo "from ['\"][^'\"]+['\"]" src/ | sort -u` vs `jq -r '.dependencies, .devDependencies | keys[]' package.json`
2. **For each declared-not-imported dep, classify:**
   - **Placeholder** — meant for future wiring (e.g., `@google/genai` declared for an un-wired Gemini integration). Decision: keep + document OR delete + defer.
   - **Byproduct** — comes with a template the generator copied (e.g., `dotenv` in a Vite template that uses `loadEnv`). Decision: delete.
   - **Stage dressing** — declared because IDE plugins often have it (e.g., `express` in a Vite-only SPA). Decision: delete, flag generator's pattern-matching as suspect.
3. **Count the theater ratio:** (dead deps) / (total deps). Over 20% is a strong "stage set, not program" signal. Over 40% means the reviewer should expect all other capabilities to also be theater.
4. **Propagate the check.** Also diff: config files that reference env vars nothing reads; components imported-but-never-rendered; event handlers bound-but-never-fired; types declared-but-never-used.

**Applied instances:**
- Lineage IDE plugin (2026-04-18): 5 dead deps out of 13 (38%). Theater ratio predicted — and did predict — that core capabilities (Rosetta transliteration, Gemini translation, DAG persistence) would all be absent. They were. Fix: strip deps, stash the showcase build as DEFERRED, build a minimal functional version. (`Desktop/lineage-ide-plugin-showcase_DEFERRED.zip` vs `Desktop/lineage-ide-plugin-minimal.zip`.)

**Related primitives:**
- [Deferred Showcase Branching](primitive_deferred-showcase-branching.md) — what to do when theater is delivered.
- [Anti-Hallucination Protocol](primitive_anti-hallucination-protocol.md) — general discipline of verifying claims against ground truth; this is its package-manifest application.
- [Citation Hygiene Gate](primitive_citation-hygiene-gate.md) — a dep is a claim; an unused dep is an unfulfilled claim.

**Standing instruction:** first read of any AI-delivered codebase is `package.json` diffed against `import` statements. Reading code before this check wastes the context window on code that may not be what the package advertises.
