# Story Mode Lite

Story Mode without the machinery. The full version is a set of local hooks, so it only runs where
Claude Code can reach your filesystem: terminal, desktop app, IDE. **Lite runs anywhere Claude Code
runs, including the web app**, because it is pure instruction, no hooks.

What you keep: the thing that matters. Every turn ends in a ranked menu you steer by number, and you
can chain picks (`5,4,1`) to queue a sequence.

What you give up (these need the local hooks + filesystem): the self-tuning corpus that learns your
hand, the catch-rate telemetry, and the autonomous self-play loop. Lite is the experience, not the
engine.

## Drop-in

Paste this into your project's `CLAUDE.md` (or save it as a Skill). That is the whole install.

```
## Story Mode
At the end of EVERY response, append a menu titled exactly:
"Story Mode — reply with a number, or chain several in order (e.g. 3 or 5,4,1):"
- List the ~10 most likely next moves I would want, most-likely first.
- Each item is a complete instruction under 10 words, executable when I reply with just its number.
- 7 items shaped to the live decision, 3 standing moves I reach for often.
- If I reply with a number, execute that menu item with no confirmation.
- If I reply with a list like 5,4,1, execute those items in order.
- Always show the multi-pick example in the title so the chaining is obvious.
```

## Why it works without hooks

The full Story Mode uses a hook to *guarantee* the menu fires every turn and to *log* your picks for
learning. Lite asks the model to do the same thing by instruction. It is less ironclad (a model can
forget where a hook cannot), and it does not learn, but the loop, menu, number-reply, multi-pick, is
identical. For most people meeting Story Mode for the first time, Lite is the whole point.

## Upgrade path

When you want the menu to learn your hand and to be able to run itself, move to the full hook stack:
[`STORY-MODE.md`](./STORY-MODE.md).
