---
name: hook-event-schema-discipline
description: ∀ Claude Code hook ⇒ verify event-specific output schema BEFORE ship. Stop ✗ supports hookSpecificOutput.additionalContext. Schema-rejection = silent ⇒ bugs persist invisibly. 16h dead L4 = empirical cost.
type: primitive
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## Claim

- Different hook events accept ⊥ output shapes
- Schema-validator rejects mismatched output ¬ blocks hook exit ✓
- ⇒ misconfigured hook fires ∀ ∞ × silently-discards output
- ✗ observable symptom in assistant context

## Event ↔ output-shape map (2026-05-14)

| Event | hookSpecificOutput | additionalContext |
|---|---|---|
| PreToolUse | ✓ | ✓ (+ permissionDecision) |
| UserPromptSubmit | ✓ | ✓ |
| PostToolUse | ✓ | ✓ |
| PostToolBatch | ✓ | ✓ |
| SessionStart | ✓ (observed-working) | ✓ |
| Stop | ✗ | ✗ |
| PreCompact | ? | ? |
| StopFailure | ? | ? |

∀ event ¬ supporting hookSpecificOutput ⇒ valid top-level fields:
- `continue` ∨ `suppressOutput` ∨ `stopReason` ∨ `decision`
- `reason` ∨ `systemMessage` ∨ `permissionDecision`
- ✗ `systemMessage` = user-visible-notification ¬ context-injection (⊥ semantic)

## Failure mode this primitive prevents

- 2026-05-13: `post-generation-reflect.py` shipped w/ Stop + hookSpecificOutput.additionalContext
- Author (Claude) generalized ∀ PreToolUse / UserPromptSubmit / SessionStart templates
- ✗ verified Stop-specific schema
- Hook ran ~16h × N reflections × schema-rejected ∀ N
- L4 layer = dead-on-arrival ∧ ✗ observable symptom

## Discipline ∀ new hook

1. Identify event type {Stop, PreToolUse, ...}
2. Check schema ∀ THAT specific event ⇒ ✗ assume hookSpecificOutput.additionalContext works
3. Smoke-test via Claude-Code event-injection ¬ just `python hook.py`
   - Raw-script test ✓ passes silently ∀ schema-rejected output
4. Verify injected-context appears in assistant view ≥ 1× ⇒ ✗ appears ⇒ schema reject
5. ∀ event ¬ supporting hookSpecificOutput ⇒ two-stage pattern:
   - Stage A: hook persists output → file (JSONL)
   - Stage B: schema-valid hook on next compatible event reads + injects
   - Canonical instance: `post-generation-recall.py` reads `post_gen_reflections.jsonl` on UserPromptSubmit

## Connects

- `[P·universal-coverage-hook]` — hooks O(1)×O(∞) ✓ iff output actually delivered
- `[F·boot-hook-fail-loud]` — sibling discipline; hooks ✗ silent-fallback
- `[F·ship-time-verification-surface]` — done = user-can-use; hook-runs ¬ delivered ⇒ ¬ done

## Origin

Will-flagged 2026-05-14 10:08 ET ← Claude Code surfaced 6 Stop-hook errors in conv. Pattern: author multiple hooks ∀ working-template ¬ verify event-specific schema = structural failure mode. 16h dead L4 = empirical cost.
