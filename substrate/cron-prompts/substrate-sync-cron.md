# SUBSTRATE-SYNC CRON — canonical prompt body

Loaded by cron pointer-prompts that contain `type: substrate-sync`. Runs the
`sync-public-substrate.py` mechanism on schedule so the public substrate
(WGlynn/JARVIS/substrate/) stays current with the local memory + hook +
cron + script directories without manual `cp` + `git` invocations.

This is the Layer-2 persistence-tier discipline operationalized as a Layer-6
scheduled trigger. The script applies the scrub-list (partner-content,
NDA-locked, hardcoded personal paths) before any file leaves the local
filesystem.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══

Self-perpetuation before any other work.

1. `CronList` to find entries containing `type: substrate-sync`.
2. If the only entry or all entries have `age_days > 5`: `CronCreate(cron=<same>, prompt=<same pointer verbatim>, durable=true)`.
3. If 3+ entries exist for this marker: sort by `createdAt` desc, `CronDelete` all but the 2 youngest.

---

## ═══ COMMANDMENT 2 — RUN THE SYNC ═══

Single shell call. Idempotent: if nothing changed, nothing commits.

```bash
python ~/.claude/scripts/sync-public-substrate.py --apply
```

The script:
1. Mirrors `~/.claude/projects/C--Users-Will/memory/*.md` →
   `~/jarvis-monorepo/substrate/memory/` with content-pattern scrub-list
   (Pragma / [REDACTED-NDA] / partner names / nda-locked / personal emails / API keys).
2. Mirrors `~/.claude/hooks/*.py` + `~/.claude/session-chain/*.py` →
   `~/jarvis-monorepo/substrate/hooks/` with path-sanitization
   (`C:/Users/Will/.claude/` → `~/.claude/`) and skip-list for hooks that
   carry hardcoded personal content.
3. Mirrors `~/.claude/cron-prompts/*.md` → `~/jarvis-monorepo/substrate/cron-prompts/`.
4. Mirrors `~/.claude/scripts/*.py` → `~/jarvis-monorepo/substrate/scripts/`.
5. If any file changed: git add -A; git commit; git push.

Read the script output. If `git: no changes`, the substrate is in sync and this tick is a no-op.

If the script reports `git op failed: ...`, surface to Will via calendar ping (Tomato, 1-min) titled
`Substrate-sync FAILED: <reason>` so it doesn't silently drift.

---

## ═══ COMMANDMENT 3 — PRIMITIVES ═══

If the sync surfaced a recurring failure mode worth promoting (e.g., new partner-content slipping past the scrub-list, a hook category that needs sanitization the script doesn't handle), append a structured note to `~/.claude/cron-prompts/_primitives-pending.md`:

```
## [YYYY-MM-DD HH:MM ET] — substrate-sync surfaced: <one-line>
- Trigger: substrate-sync tick
- Observation: <what slipped past or what failed>
- Candidate primitive: <rule or scrub-list extension>
- Status: pending Will-triage
```

Otherwise: silent. Empty sync ticks are correct when no learning is in them.

---

## ═══ ON ERROR ═══

Save state to `~/jarvis-monorepo/.sync-error-YYYY-MM-DD-HHMM.log`. Continue self-perpetuation regardless.

---

## Design principles

- C1 > C2 > C3. The loop must survive even if a sync fails.
- The script is the contract; this prompt is the schedule. Edit the script to change behavior, not this prompt.
- Idempotent by design. Cron tick frequency can be aggressive (hourly is fine) because no-op-when-no-change.
- Scrub-list is conservative by default. False-positives (over-scrubbing) are recoverable; false-negatives (leaking partner content) are not.
