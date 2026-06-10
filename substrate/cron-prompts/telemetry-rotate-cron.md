# TELEMETRY-ROTATE CRON — canonical prompt body

Loaded by cron pointer-prompts that contain `type: telemetry-rotate`. Runs daily; rotates stale jsonl telemetry into monthly buckets, compacts old buckets to tar.gz.

Per [P·class-elimination-not-instance-patch]: this cron class-eliminates "telemetry logs grow unbounded and slow down grep / saturate disk" by enforcing rotation + compaction without manual intervention.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══

1. `CronList` → entries with `type: telemetry-rotate`.
2. If only entry or all > 5 days: `CronCreate` durable backup with same schedule + pointer.
3. If 3+ entries: keep 2 youngest by createdAt, delete rest.

---

## ═══ COMMANDMENT 2 — RUN THE ROTATION ═══

```bash
python ~/.claude/hooks/_telemetry_rotate.py --compact
```

Behavior:
- Stale jsonl files (mtime > 7d): moved into `YYYY-MM/` subdir under `_system/`
- Monthly buckets > 1 month old: tar.gz'd, original dir removed
- Idempotent: re-running is safe; only acts on stale items

Read the output:
- `rotated=N` reports daily-roll count
- `compacted=N` reports monthly-archive count
- Errors print to stderr

---

## ═══ COMMANDMENT 3 — PRIMITIVES ═══

If rotation surfaces a recurring failure mode (e.g., a specific jsonl growing 100MB+/day, or rotation hitting permission errors), append to `~/.claude/cron-prompts/_primitives-pending.md` with structured note.

Otherwise silent. Empty rotation ticks are correct when nothing is stale.

---

## Design principles

- C1 > C2 > C3. The loop survives even if rotation fails.
- The script is the contract; this prompt is the schedule.
- Idempotent. Daily cadence is fine; running more often is wasted compute but not harmful.
