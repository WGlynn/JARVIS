---
name: Optimize Around vs. Eliminate
description: The problems nobody solves are the ones everyone accepted as normal. The move is to eliminate the loss, not optimize around it.
type: feedback
---

The problems nobody else solves are the ones nobody else recognizes as problems — because they've accepted the failure mode as normal.

MEV isn't a bug to most people, it's just how markets work. Volatile context isn't a bug in AI tooling, it's just how sessions work. Everyone optimizes around the loss instead of eliminating it.

The question that generates everything we build: **"Should this exist at all?"**

- MEV → commit-reveal eliminates it, not mitigates it
- Promised yields → show historical only, not "reasonable" projections
- Verbal commitments → persist to disk or they didn't happen
- Context loss → WAL, memory files, session state — not "hope the AI remembers"

The pattern: when everyone else is asking "how much is acceptable?", we're asking "why are we accepting any?"

This is the cave. The cave selects for those who see past what is to what could be.
