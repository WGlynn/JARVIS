---
name: State Observability Primitive
description: TRP R2 (knowledge loop) must track state transitions, not just insights. Stateless knowledge decays into stale assertions.
type: feedback
---

# State Observability — TRP Augmentation

## The Failure

TRP's knowledge recursion (R2) captures *insights* (what was learned) but not *transitions* (what changed). When a project item moves through states (submitted → accepted → rejected → alternative offered → accepted), only the initial state gets persisted. Future sessions load stale snapshots and re-ask questions the user already answered.

**Concrete example**: MIT speaker pitch went through 5 states across 2 sessions. Memory file still said "SENT." Next session didn't know about the rejection, the comp ticket, or the refund.

## The Primitive

**Every stateful object in a memory file must have an observable transition log.**

A stateful object is anything that can change between sessions: an application, a ticket, a PR, a deployment, a relationship, a contract status, an open question. If it has a "was X, now Y" moment, the transition must be recorded.

## Format

```markdown
## Status Tracker (most recent first)
| Date | Item | Transition | Detail |
|------|------|-----------|--------|
| 2026-04-04 | Ticket | COMP RECEIVED | Cameron offered comp. GA needs refund. |
| 2026-03-27 | Ticket | PURCHASED | GA $150 via Eventbrite. |
```

Most recent first = O(1) to find current state. History below = context for why.

## How This Augments TRP

### R0 (Compression)
Status tables are already compressed — one line per transition. No narrative bloat. A 5-state lifecycle becomes 5 rows instead of 5 paragraphs across 3 session transcripts that get lost to context compression.

### R1 (Adversarial Verification)
Stale state IS a verification failure. If R1 catches a code bug because the test asserts the wrong state, the same principle applies to knowledge: if memory asserts the wrong project state, the session operates on false premises. State observability is R1 applied to R2.

### R2 (Knowledge)
This is where it directly plugs in. R2 currently captures:
- What was discovered (primitives, patterns)
- What was decided (design choices, conventions)

R2 must ALSO capture:
- What changed (state transitions on active items)

The gap: R2 treats knowledge as *facts* (timeless) but projects contain *states* (time-bound). A fact doesn't need a timestamp. A state does.

### R3 (Capability)
State observability makes SESSION_STATE.md more useful. If every active project's memory has a status tracker, SESSION_STATE can reference the tracker instead of re-summarizing. "MIT: see status tracker in memory" instead of "MIT: we submitted, they replied, we need to refund..."

## Detection Rule

At session end (REBOOT/END), before persisting:

> **For each project memory touched this session: did any stateful item change? If yes, is the transition logged in the memory file?**

If the answer is "changed but not logged" — log it before closing.

## Anti-Pattern

Writing "Speaker: SENT" and never updating it. The initial write creates a false sense of persistence. The failure isn't forgetting — it's *remembering the wrong thing* because the memory calcified.

**Why:** Stateless knowledge decays into stale assertions. Stale assertions cause re-work and erode trust. State observability is the fix.

**How to apply:** Every project memory with active items gets a status tracker table. Every session that changes a state appends to the table. REBOOT checklist includes "status trackers current?"
