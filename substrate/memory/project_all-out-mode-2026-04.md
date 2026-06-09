---
name: All-Out Mode (2026-04, pre-funding)
description: Will's 2026-04-20 posture shift — funding imminent, "going all out." Shifts from relaxed-pace VibeSwap development to high-throughput ship mode. Default to parallel / aggressive execution.
type: project
originSessionId: feff45da-df5b-4228-8a3c-2871f583acc7
---
# All-Out Mode — 2026-04-20

Will's exact words: *"we're going to get funding soon i believe so we want to go all out these days"*

## What shifted
Context before 2026-04-20: [Day Job Priority](project_day-job-priority.md) was active — "financial stability first, VibeSwap pace relaxed, math doesn't expire." That posture traded VibeSwap velocity for job-search bandwidth.

With funding likely closing soon, that trade reverses. Now: VibeSwap velocity IS the priority.

## How to apply
- **Default to parallel execution.** When there are independent tasks (e.g. deploying 5 Fly shards), launch them all concurrently, don't serialize for "safety."
- **Lower the gate on experimental deploys.** Deploying untested code to production-adjacent shards is acceptable during this mode — speed of iteration beats zero-defect rollouts. The recovery cost is small (rollback + redeploy), the opportunity cost (slow pace during investor-facing window) is large.
- **Ship more artifacts.** When Will asks for a deck / page / doc / deploy, default to "I'll do it now" rather than "here are three options." Autonomy grant is active by default in this mode.
- **Polish the VC-facing surface.** Pitch decks, landing pages, papers, public docs — this is where quality still matters. All-out means MORE of these, not rougher ones. Undersell-overdeliver still holds for investor touches.
- **Don't re-ask for authorization already given.** "Ship it" / "deploy all the shards" / "your call" = permission for the full slate, not per-step check-ins.

## When to slow down (still)
- Destructive ops (reset --hard, force push main, drop table) — always confirm
- privacy-sensitive content — NDA gate still enforced
- Anything legal/reputational/financial affecting parties outside VibeSwap

## Expiry
If funding doesn't close by end of 2026-Q2, revisit. This posture assumes a specific runway window — don't carry "all out" into a year-long job search if the round stalls.

## Companion memories
- [Day Job Priority](project_day-job-priority.md) — the relaxed-pace posture this overrides (for now)
- [Autonomy grant](feedback_autonomy-grant-2026-04-13.md) — "your call" = execute the slate
- [Undersell + Overdeliver](feedback_undersell-overdeliver.md) — still holds for external touches
- [Important Work Is Worth Its Time](feedback_important-work-worth-time.md) — don't let "all out" become "sloppy"
