---
name: classify
description: Classify a task description to recommend the cheapest viable Claude tier (haiku / sonnet / opus). Manual companion to ~/.claude/hooks/coordination-mechanism-gate.py — use when dispatching a subagent or considering an Agent spawn and you want a pre-flight cost-sanity check. Per [J·jarvis-coordination-mechanism] (a partner chat).
---

# /classify — pre-flight tier recommendation

You are routing a task to the cheapest viable Claude tier. Inputs:

- `$ARG` — the task description being considered

## Classification rules

**HAIKU** if any of:
- short description (<80 chars)
- starts with: list / count / show / print / read / fetch / get / check
- domain: weather / date / time / status / version
- simple file ops: rename / move / copy / delete (one file)

**OPUS** if any of:
- design / architecture / spec / implement / build / refactor / migrate
- security / audit / verification / formal-verification
- multi-step / cross-cutting / plan / strategy / roadmap
- side-by-side / comparison / landscape / survey of N>2 things

**SONNET** otherwise (default mid-tier; research, analysis, one-domain compare).

## Output shape

One line:

```
TIER: <haiku|sonnet|opus> · because <1-clause reason> · cost-direction <↓ savings if downgrading from sonnet | = no change | ↑ upgrade>
```

Example outputs:

- `$ARG = "check current time"` → `TIER: haiku · because trivial fetch · cost-direction ↓ savings`
- `$ARG = "summarize the README"` → `TIER: sonnet · because mid-complexity summarization · cost-direction = no change`
- `$ARG = "design the security audit framework for CKB cells"` → `TIER: opus · because substantive architecture+security · cost-direction ↑ upgrade from default`

## Sibling

- Hook auto-fires this classification at spawn-time via PreToolUse Agent matcher (`coordination-mechanism-gate.py`). This skill is the manual surface for pre-spawn sanity check.
- Full project context: `memory/project_jarvis-coordination-mechanism-a partner-2026-06-10.md`.
