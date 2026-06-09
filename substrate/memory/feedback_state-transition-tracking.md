---
name: State Transition Tracking
description: Memory files must track state transitions (status changes over time), not just initial snapshots. Use date-ordered status tables.
type: feedback
---

Memory files for active projects must track state transitions, not just the initial plan. When something changes (application accepted/rejected, ticket bought/refunded, person replied), UPDATE the memory with the new state AND the date.

**Why:** Will had a full conversation about getting a comp ticket and refunding a purchased one. None of it was persisted. Next session loaded stale state ("Tickets: GA $150") and missed the entire thread. Will had to re-explain.

**How to apply:** For active project memories, use a status tracker table (most recent first) so any session can scan current state in seconds. Format:

```
| Date | Item | Transition | Detail |
```

Every time a status changes in conversation, update the tracker. Don't just overwrite — append the transition so the history is visible. Open items get a separate checklist below.
