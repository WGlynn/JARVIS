---
name: Stop-event hookSpecificOutput.additionalContext is invalid
description: Stop-event hooks MUST NOT emit hookSpecificOutput.additionalContext — schema rejects, error floods UI every turn. Valid emit shapes are top-level only.
type: primitive
originSessionId: e988777c-acf3-4b43-96e2-910590095433
---

# [P·stop-event-schema-restriction]

## Constraint

∀ Stop-event hook ⇒ `hookSpecificOutput` field ⊅ `additionalContext` key.

Claude Code schema permits `hookSpecificOutput.additionalContext` ONLY on event ∈ {UserPromptSubmit (required), PostToolUse (optional), PostToolBatch (optional)}.

Stop / StopFailure / PreToolUse / SessionStart / PreCompact ⇒ ✗ `hookSpecificOutput.additionalContext`.

## Symptom

Violation ⇒ schema-validation rejection ∀ Stop event ⇒ error-blob + expected-schema dump rendered to UI window ∀ turn ⇒ flood.

The hook's payload is silently dropped — intended behavior never fires. Failure is invisible from the script's exit code (0) — only the UI shows the rejection.

## Valid Stop emit shapes

Top-level fields only:
- `{}` — silent, no effect
- `{"continue": false}` — let stop proceed
- `{"decision": "block", "reason": msg}` — force continuation, `reason` re-prompted as system message
- `{"systemMessage": msg}` — surface guidance without blocking
- `{"stopReason": msg}` — annotate stop event
- `{"suppressOutput": true}` — silence the hook's stdout

To inject continuation guidance at Stop: use `{"decision": "block", "reason": msg}`. This is the canonical force-continue idiom.

## Regression history

- 2026-05-14 — `post-generation-reflect.py` first hit, patched with `{}` emit + side-channel file for next-prompt recall (see in-source comment lines 260-263).
- 2026-05-28 — `autonomous-continue.py` + `wwwd-correction-detector.py` discovered with same bug. Both patched (autonomous-continue → `decision:block`+`reason`, wwwd-correction-detector → silent `{}`).

Pattern-repeat (2 regressions after the initial fix) ⇒ memory ¬ sufficient ⇒ gate-candidate per [P·universal-coverage-hook].

## Gate-form (eventual right shape, not yet implemented)

Per [P·always-equals-gate] + [P·universal-coverage-hook]: this constraint binds hook-AUTHOR-time, not hook-runtime. Right shape =

- PostToolUse Write|Edit on `~/.claude/hooks/*.py` ∧ `~/.claude/session-chain/*.py` matcher
- Scan for `hookSpecificOutput.*additionalContext` AND `hook_event_name.*Stop` co-occurrence in script source
- Emit warning to author when detected

Until gate ships: this primitive surfaces in deep-recall on any hook-authoring prompt + before any Stop-hook write.

## How to apply

When writing or editing a Stop-event hook (registered in `settings.json` → `hooks.Stop[]`):

1. ✗ `hookSpecificOutput.additionalContext`
2. ✓ top-level fields per valid-emit-shapes above
3. If you need state to persist for the next prompt (the original use case of additionalContext): write to a side-channel file + read it in a UserPromptSubmit hook on the next turn. See `post-generation-reflect.py` ↔ `post-generation-recall.py` for the canonical pair.
4. Smoke-test: `echo '{"hook_event_name":"Stop"}' | python <script.py>` — output must parse as JSON AND match the Stop schema (no `hookSpecificOutput` ∨ `hookSpecificOutput` with only valid sub-keys).

## Related

- [P·universal-coverage-hook] — parent: this is a coverage requirement that should be hook-enforced
- [P·always-equals-gate] — parent: "Stop hooks must X" is a hook-candidate, not memory-candidate
- [P·fruit-of-poisoned-tree] — sister: when this bug shows up, sweep all sibling Stop hooks before declaring fix complete
