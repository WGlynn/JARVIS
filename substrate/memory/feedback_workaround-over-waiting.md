---
name: Workarounds over waiting — never let builds block for hours
description: Will's directive after discovering the forge build was 2.4 hours due to optimizer+via_ir config, fixed to 28 seconds by disabling optimizer. "From now on if something is taking too long we're gonna look for workarounds."
type: feedback
---

# Workarounds Over Waiting (2026-03-20)

If something is taking too long, stop and find a workaround. Don't let a process run for hours without questioning it.

**Why:** The forge build ran for 2.4 hours then OOMed. The fix (disable optimizer for local dev) took 2 minutes and reduced build time to 28 seconds. A 1000x improvement from questioning a default config. Will said: "from now on if something is taking too long we're gonna look for workarounds. Because that 1000x improvement took literally minutes to build."

**How to apply:**
- If a build/deploy/test takes > 5 minutes, immediately investigate alternatives
- 2 failures on the same approach → STOP and pivot (from token-efficiency feedback)
- Question default configs — they're optimized for someone else's machine
- Local dev doesn't need production optimization settings
- CI is the source of truth for correctness; local is for speed
