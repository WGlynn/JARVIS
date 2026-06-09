---
name: Doc/Code Drift Detector
description: Automate the check that HANDOFF.md / README.md claims agree with the actual code. Line counts, view names, keyboard bindings, and command manifests are scannable. Pass 8 of the Self-Theater Audit Gate.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** the HANDOFF / README is a contract. If the contract says "App.tsx is ~350 lines" and the file is 978, the contract is lying. Add a scripted pass to the audit gate that compares documented claims against the code and blocks ship on hard drift.

**Why:** Gemini v3 (2026-04-18) passed our 7-pass audit cleanly (0 dep theater, 0 schema theater, tsc clean, npm audit clean) but the HANDOFF it shipped still said "App.tsx is ~350 lines" — and the file was 978. The original Self-Theater Audit Gate caught the dep/marker/schema classes of theater but missed **documentation theater**: a doc that advertises a minimal plugin while the code ships a multi-view dashboard. If the doc and the code disagree, a downstream reviewer trusts the wrong source. Silent drift. This pass closes that hole.

**How to apply:**

Four sub-checks, all regex-based, no new deps. Add as Pass 8 of the audit suite.

1. **Line-count claims** — scan HANDOFF for phrases like `<file.ts> is ~<N> lines`. Resolve each to the actual source file, compare: > 40% drift → HARD fail, > 15% → warn.
2. **View claims** — if HANDOFF mentions "view" wording, extract `activeView === 'X'` patterns from source. Warn if code has ≥ 2 views but HANDOFF mentions none of them by name and has no navigation section.
3. **Command claims** — if HANDOFF lists `Commands: help, clear, ...`, match against `case 'X':` patterns in source. Warn on orphaned claims (command in doc but not in code).
4. **Keyboard claims** — parse modifier-glyph tokens (`⌘S`, `⌘\`` etc.) from HANDOFF's keyboard section; compare against actual `e.key === 'X'` handlers. Warn on unbacked claims. (Core keys `s`, `p`, `` ` `` allowed without match because shortcut helpers vary by implementation.)

**Tuning:**
- Line-count drift threshold: 40% hard, 15% soft. Under 15% is within noise for an actively-edited file.
- Allow-list: well-known command names (`save`, `clear`, `help`, `status`, `perf`) pass without strict match because they're often called through indirection.
- Strip markdown escapes before comparing keyboard tokens — `⌘\\`` parsing artifacts produce false positives otherwise.

**Applied instances:**
- `scripts/audit-all.mjs` Pass 8 in both `Desktop/lineage-ide-plugin-minimal/` and the reviewed `Desktop/lineage-ide-plugin-gemini-v3-review/`. Catches line-count drift, view claims, command manifests, and keyboard bindings.
- Detected on first run: Gemini v3's HANDOFF claimed "App.tsx is ~350 lines" while the file was 978 (164% drift). Hard fail. Forced the HANDOFF rewrite that made the reviewed-v3 ship clean.

**Anti-patterns:**
- **"I'll remember to update the doc when I change the code."** Fails under time pressure. The gate IS the memory.
- **Excluding the doc from the audit.** If the gate doesn't see the HANDOFF, drift accumulates silently.
- **Checking only line counts.** Claims about views, commands, keyboard are the substantive surface — not just byte counts.
- **Hard-failing on every drift.** Minor growth is normal; use soft thresholds for plausible cases.

**Related primitives:**
- [Self-Theater Audit Gate](primitive_self-theater-audit-gate.md) — the umbrella. This is Pass 8.
- [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md) — Pass 1. Same discipline applied to package.json.
- [Anti-Stale Feed](primitive_anti-amnesia-protocol.md) — the meta-rule: claims must be verified against current state. Doc-drift is that rule enforced on the handoff itself.
- [Verbal → Gate](primitive_verbal-to-gate.md) — a documented claim without a code binding is a verbal promise. Gate it.

**Standing instruction:** every HANDOFF.md / README.md in any project where we run an audit suite must be scanned by the doc-drift pass. If the doc and the code disagree beyond thresholds, ship is blocked until one of them is corrected. Usually the doc; sometimes the code had drifted from the intent and the doc was right.
