# Primitives pending Will-triage

Auto-appended by COMMANDMENT 3 of Odysseus cron loops when a fire surfaces an extractable structural insight. Will reviews this file periodically and promotes candidates to memory primitives in `~/.claude/projects/C--Users-Will/memory/`.

Format per entry:

```
## [YYYY-MM-DD HH:MM ET] — <one-line summary>
- Trigger: <what fired this>
- Observation: <what happened>
- Candidate primitive: <what rule/pattern could generalize>
- Composes with: [P·...] or [F·...] or [J·...]
- Status: pending Will-triage
```

When promoted to a memory primitive, mark the entry `## [PROMOTED YYYY-MM-DD]` and Will will leave the entry as a receipt.

---

## [PROMOTED 2026-06-08 18:10 ET] — 3-commandment autonomous-loop pattern

Promoted to durable primitive: `~/.claude/projects/C--Users-Will/memory/primitive_three-commandment-autonomous-loop.md` as `[P·three-commandment-autonomous-loop]`. Generalized beyond Odysseus to apply to ∀ JARVIS autonomous loop (jarvis-loop, TIER4 fallback, memory-hygiene, jarvis-x-fetcher, etc.). Implementation template + composes-with map included.

Original receipt preserved below:

- Trigger: 4 hours of repeating "silent" responses to a discovery cron that was firing every 30 min while pause-state was sticky-tripped
- Observation: Will articulated the canonical hierarchy for any autonomous cron-driven loop: (1) make the loop / self-perpetuate, (2) build/build-on the state machine, (3) primitives extraction
- Composes with: [P·structure-does-the-work] (the structure of priority IS the work-mechanism), [P·jarvis-amd-applied-to-ai-substrate] (substrate-port pattern: applies to ∀ cron loop), [P·stateful-overlay], [F·crash-resilient-memory-writes]

## [2026-06-09 10:38 ET] — Bi-temporal supersession as memory-substrate import-candidate

- Trigger: COMMANDMENT 3 on Day 3 dispatch (#2858 reply to @alvaroperricone). Their reference impl (e0fc50e) implements event-time + transaction-time supersession in-band so "X then, Y now" stays auditable at query time without deleting prior values.
- Observation: JARVIS currently does this via git history on `memory/`. Forensically complete (commit log + diff) but not queryable at agent-runtime; the agent reads only the current snapshot. When a memory turns out wrong, there's no in-band way to find which prior decisions were downstream of the now-wrong fact.
- Candidate primitive: `[F·memory-bi-temporal-axis]` — every memory write SHOULD record both the event-time the fact became true AND the transaction-time it entered memory. Supersession retires the old (subject, predicate) tuple by setting its transaction-end-time, not by deletion. Read-path defaults to "current"; audit-path can replay any prior state. Implementation surface: front-matter additions (`event_time`, `superseded_by`, `transaction_end`) + a lightweight query helper.
- Composes with: [F·entity-context-cross-reference] (AA#3 — entity-graph writes are exactly the events bi-temporal would index); [P·anti-amnesia-protocol] (forensic recovery becomes query-time, not log-grep); JARVIS memory architecture broadly.
- Status: pending Will-triage. Promotion would require deciding (a) is the implementation cost worth it vs. git-history-only, (b) front-matter schema, (c) does this fit alongside HIERO compression or trade against it.
