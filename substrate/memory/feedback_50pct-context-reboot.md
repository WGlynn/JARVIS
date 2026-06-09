---
name: 50% Context Reboot Protocol
description: Save state and reboot session at 50% context remaining — that's when quality degrades
type: feedback
---

Always save state and reboot at 50% context remaining. That's when output quality starts degrading.

**Why:** Will observed that Jarvis "gases out" around 50% context. Earlier threshold (was 10%) wasn't catching the degradation in time.

**How to apply:** Monitor context usage. At ~50% remaining, STOP current work, commit everything, write block header to SESSION_STATE.md, push to both remotes, and tell Will to reboot. Don't try to push through — the compound interest of a fresh context outweighs finishing one more task with degraded output.
