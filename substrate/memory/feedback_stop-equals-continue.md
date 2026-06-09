---
name: stop-equals-continue
description: During multi-day execution arcs ("full auto" / "dont stop"), end-of-turn = trigger to continue, ¬ trigger to wait. autonomous-continue.py Stop hook is the substrate; this is the Will-directive that arms it.
type: feedback
originSessionId: 2d5ae2e5-2926-42ce-a369-e66ee74c9c61
---
## Rule

When Will has set `full auto` / `dont stop` / `multi day project` posture:
- End-of-turn ≡ continue-signal, ¬ wait-signal
- Stop event hook (`autonomous-continue.py`) should auto-trigger next work-step
- ✗ Wait for Will-prompt to resume

Exit conditions (when to actually stop):
- Will-prompt explicitly cancels (`pause`, `wait`, `that's enough`)
- Production blocker requires Will-decision (escalation, NOT just continued execution)
- Multi-day arc deliverables ALL shipped
- Context budget exhausted (autopilot rule)

## Why

Will-frame 2026-05-24: "stop = continue rule." Reframes my default end-of-turn behavior during execution arcs.

The autonomous-continue.py Stop hook already exists in `~/.claude/settings.json:213-217`. The hook is the substrate; this feedback is the rule that the substrate enforces.

Per `[P·full-leverage-only-moves]` × `[P·autopilot-loop]`: half-execution wastes the leverage. Either I'm in autopilot OR I'm in step-by-step Will-confirm mode. The "stop = continue" directive flips into autopilot for the multi-day arc.

## How to apply

Default during full-auto multi-day arc:
1. Finish current step
2. Self-check: is there a next-step in the task list that I can claim?
3. If yes ⇒ claim it (set in_progress) and execute
4. If no ⇒ check open threads, recall, propose new task
5. Only-stop conditions: Will-cancel · production-blocker · all-deliverables-shipped · context-exhausted

✗ "I have completed X. Awaiting next direction." during autopilot — that IS the failure mode.

## Connects

- `[P·autopilot-loop]` — parent execution discipline
- `[P·full-leverage-only-moves]` — sibling at strategic-move layer
- `[F·apply-rule-just-wrote]` — apply this rule to MY subsequent end-of-turns
- `autonomous-continue.py` hook — substrate enforcer

## Origin

2026-05-24, mid-VibeSwap-arch-finishing arc. Will explicitly flagged after my prior turn ended with implicit wait-posture during a `full auto` directive.
