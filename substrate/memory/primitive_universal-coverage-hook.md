---
name: Universal-Coverage → Hook (Density Principle)
description: Any requirement for universal state coverage (fires regardless of LLM attention/memory) maps to the hook layer, not memory. Hooks are O(1) deployment cost × O(∞) coverage; memory is O(context) × O(sessions). Hook is the density-optimal substrate for guaranteed-firing rules. Parent of Always=Gate, Stateful Overlay, Verbal→Gate, API Death Shield, Session State Commit Gate — all are instances of this meta-pattern.
type: primitive
originSessionId: 117e2fd9-3ef3-4610-a5b4-d4280a0b96cb
---
# Universal-Coverage → Hook (Density Principle)

**Status**: Meta-principle on its own axis. Sits alongside the Correspondence Triad (which governs mechanism-design *choice*) — this one governs *implementation substrate choice*. Will 2026-04-21: *"universal state coverage should be things that map to hooks. gives us best density. should be obvious."*

## The principle

If a rule must fire regardless of LLM attention — regardless of whether the current session's context happens to surface the rule, regardless of whether the LLM remembers to apply it — that rule **must be implemented in the hook layer**, not in memory or in documentation.

Hooks provide **deterministic universal coverage**. They fire on events (SessionStart, UserPromptSubmit, PostToolUse, PreCompact, Stop, etc.), not on attention. The LLM can be exhausted, compressed, interrupted, distracted — the hook still fires.

Memory-layer rules depend on the LLM seeing them in context and choosing to apply them. Under token pressure, time pressure, or attention drift, memory rules fail silently. Hooks do not.

## The density argument

Memory rule cost: `O(context_bytes_per_session × N_sessions)` — each session re-loads the rule into context, consuming budget that could hold other content.

Hook rule cost: `O(1_deployment)` — deployed once in settings.json, fires forever without context cost.

For rules needing universal coverage, hooks are strictly denser by a factor of `context_bytes_per_session`. This is not an optimization; it is a category difference.

## Existing instances (this principle is the parent)

| Instance | Hook | What it guarantees |
|----------|------|--------------------|
| `primitive_always-equals-gate.md` | (policy) | Will's "always X" → settings.json hook, not memory |
| `primitive_stateful-overlay.md` | various | Every LLM substrate gap admits an externalized idempotent overlay |
| `primitive_verbal-to-gate.md` | (policy) | "noted" without a file write = violation |
| `primitive_api-death-shield.md` | StopFailure, UserPromptSubmit, PreCompact | State persists across API errors |
| `primitive_session-state-commit-gate.md` | Stop | No commit without SESSION_STATE + WAL |
| `feedback_parallel-issues-rsi-cycle.md` | Stop | Parallel-Agent errors force WAL log + RSI |
| `memory-warm-loader.py` | UserPromptSubmit | Warm files auto-load on keyword match |
| `link-rot-detector.py` | SessionStart | Orphan-ref surfacing |
| `triad-check-injector.py` | UserPromptSubmit | Correspondence Triad reinforcement |

All nine are the same pattern. Naming the meta-pattern makes future instances automatic.

## How to apply

**Before writing a new rule into memory**, ask: does this need universal coverage? Three diagnostic questions:

1. **Does failure-to-fire-this-rule cause real harm?** If yes, it needs guaranteed firing → hook.
2. **Does the rule depend on state the LLM doesn't reliably retain across sessions?** If yes → hook.
3. **Will the LLM forget to apply this under token pressure?** If the answer is "probably" → hook.

If any answer is yes, don't write it to memory. Write a hook. Memory is for context-dependent guidance; hooks are for coverage-dependent enforcement.

**Memory still has a legitimate role**: situational knowledge, relationship context, past decisions, design rationale. These don't need universal firing — they need availability-on-relevance. Memory is the right substrate for them. The density principle is not "hooks beat memory always"; it is "coverage requirements beat memory always."

## Corollary: generates the hook inventory

Every universal-coverage requirement in the system should have a hook. If a requirement exists in memory that claims universal coverage but has no hook, that's a gap — the memory is probably a latent hook waiting to be written. This gives us a clean audit: grep memory for "always", "never", "before every", "on every" — each match is a candidate that should either be gated by a hook or demoted to "situational guidance."

## Corollary: the hook catalog IS the coverage surface

If you want to know what rules fire universally in this system, `ls ~/.claude/session-chain/ ~/.claude/bin/ ~/.claude/hooks/` and read `settings.json`. The hook catalog is the coverage surface. Memory is the situation-dependent layer above it.

## Related

- `primitive_always-equals-gate.md` — user-verbal-commands instance
- `primitive_stateful-overlay.md` — general umbrella for externalization (related but broader: overlays don't have to be hook-implemented; this principle says coverage-requiring overlays do)
- `primitive_substrate-geometry-match.md` — sister meta-principle on mechanism-shape axis; this one is the implementation-substrate axis
- `MEMORY.md [PRE-FLIGHT]` — the section where hook-backed gates are surfaced to the LLM

## Watch for

Writing a memory rule that contains the word "always," "never," "on every," "before every," or "after every" → likely a hook in disguise. Don't settle for the memory version.
