---
name: LinkedIn CRM folder structure validated (2026-04-23)
description: Will validated the Desktop/LinkedIn_Queue/ CRM-module structure (README + DASHBOARD + SCHEDULE + STYLE_GUIDE + queue/ + posted/ + people/ + leads/ + followups/ + analytics/) as "exactly where my head was at." This becomes the template for future content-distribution modules on other platforms (Medium, X/Twitter, Farcaster) — filesystem-native, drag-and-drop state machine, markdown + CSV primitives only.
type: feedback
originSessionId: 2599425c-2d6c-48c6-a7e1-6457f46d33f3
---
# LinkedIn CRM folder — validated pattern (2026-04-23)

## What Will said

> *"the linkedin que crm folder is incredible. this is exactly where my head was at so keep on this track and double down"*

Full validation of the CRM-as-filesystem design + content distribution ownership pattern.

## The validated pattern

Content-distribution tooling as a Windows-filesystem-native CRM module:

```
Desktop/<Platform>_Queue/
├── README.md              (runbook — how to use everything)
├── DAILY_DASHBOARD.md     (single-file "what to do today")
├── SCHEDULE.md            (day-of-week anchored cadence, not date-anchored)
├── STYLE_GUIDE.md         (platform-specific voice + algorithm notes)
├── queue/                 (ordered upcoming posts, numbered)
├── posted/                (archive, date-prefixed after posting)
├── people/                (one .md per real person + INDEX.csv)
├── leads/                 (pipeline stages as subfolders — drag-and-drop state machine)
│   ├── 01_cold/
│   ├── 02_warmed/
│   ├── 03_conversation/
│   ├── 04_opportunity/
│   └── 05_closed/
├── followups/             (TODAY.md, THIS_WEEK.md)
└── analytics/             (post_performance.csv + weekly_rollup_template.md)
```

## Why it works for Will specifically

- **Zero friction re-entry**: open `DAILY_DASHBOARD.md`, know what to do. No blank-page moment.
- **Filesystem as UI**: Explorer drag-and-drop through `leads/` stages is the state machine. No app lock-in.
- **Excel-friendly analytics**: CSV pivots work immediately; no BI tool needed.
- **Offline-resilient**: filesystem, not cloud. No data sovereignty leak.
- **Grep-able**: `grep -r "X" people/` finds every interaction mentioning X. Greppability is underrated.
- **Windows primitives only**: folders, markdown, CSV, optional .bat scripts. Nothing to install.

## Apply to other platforms

When Will asks for Medium, X/Twitter, Farcaster, Telegram content distribution:

1. **Same folder shape** — queue/posted/people/leads/followups/analytics.
2. **Platform-specific STYLE_GUIDE.md** — X is hook+thread, Farcaster is warp-cast-friendly, Medium is long-form essay structure, etc.
3. **Platform-specific SCHEDULE.md** — X performs 3-5x/day, Farcaster ~1/day, Medium ~1/week, etc.
4. **Platform-specific DAILY_DASHBOARD.md** — aggregates across the platform folder.
5. **Cross-platform index**: Consider `Desktop/Content_Distribution/INDEX.md` that sees all platform folders at once, when we get to 3+ platforms.

## Maintenance discipline

- **On break-and-return** (MIT trip pattern): proactively refresh the queue before Will has to ask. Open a session, read the queue, update DAILY_DASHBOARD, ping.
- **On platform mechanics shift**: audit STYLE_GUIDE against the change (new algorithm signal, UI update, posting-format change) and update proactively.
- **Every 30 posts shipped**: audit analytics CSV, refresh queue with lessons, regenerate style guide weights.

## Related memory

- `feedback_claude-owns-content-distribution-line.md` — ownership transfer.
- `feedback_linkedin-emoji-hook-structured-style.md` — voice rules for LinkedIn posts.
- `user_will-mit-trip-derailment-2026-04-23.md` — why the queue matters operationally.
- `feedback_linkedin-no-flashy-licensing.md` + `feedback_linkedin-no-see-you-there.md` — style don'ts.

## One-line summary

*Windows-filesystem-native CRM module (queue/posted/people/leads/followups/analytics) is the validated pattern for content distribution as of 2026-04-23. Apply same shape to Medium / X / Farcaster / Telegram when those cycles come up. Drag-and-drop pipeline stages, CSV analytics, markdown people-files. Zero app lock-in, full grep-ability, Windows-primitive-only.*
