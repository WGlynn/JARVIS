#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liveness witness for cron PRODUCTIVITY + FIRING (in-system alarm).

The gap this closes
-------------------
cron-keeper.py witnesses that crons stay REGISTERED (resets the expiry clock,
self-heals scheduled_tasks.json). Nothing witnessed two other axes:
  * PRODUCE -- did the loop body write its output log?
  * FIRE    -- did the cron's prompt actually get injected on schedule?
A loop can be registered yet silently stop producing for weeks, or the scheduler
can stop firing it entirely (machine asleep, wedged). Both hid in the dark.

What it does (all registry-grounded, warn-only, mutates nothing, returns 0)
--------------------------------------------------------------------------
Ground truth = the live task registry (scheduled_tasks.json). For every CURRENTLY
REGISTERED cron type:
  PRODUCE axis -- if it declares a per-fire output log (_<type>-log.md), check the
      log's mtime against max(3x cadence, 18h). Missing/stale -> alarm.
  FIRE axis    -- read _<type>-heartbeat.log (written by cron-fire-heartbeat.py on
      every cron UserPromptSubmit). If it EXISTS and is stale -> alarm. If ABSENT,
      stay silent: absence means "not yet observed since the heartbeat hook was
      installed", not death (cold-start-safe, per the index-budget cry-wolf lesson).
  CROSS        -- output stale/missing BUT fire fresh = FIRED-BUT-PRODUCED-NOTHING,
      the exact loop-body-dead case; flagged loudest.

Auto-discovery replaces the old hand-curated CHECKS dict (which drifted: it missed
logs that existed and could never cover new loops). The trust boundary the previous
author guarded is preserved structurally:
  * EXCLUDE_OUTPUT -- logs whose mtime is bumped by non-cron paths (persistence-sweep
    is touched by precompact-persistence-snapshot.py) are not trusted for PRODUCE.
  * ORPHAN logs -- a _<type>-log.md whose type is NOT registered = a deregistered
    loop's leftover; reported as informational, never as an alarm.

Cadence overrides live in CADENCE; unknown types use DEFAULT_CADENCE_H and are
labelled so the threshold basis is honest.

Derived: TRP2 round 2026-08-10 (fire-axis blind spot + CHECKS curation-drift),
extending the RSAW 2026-08-08 finding. Composes [P.universal-coverage-hook] and
[P.boot-hook-fail-loud]. ASCII-only output (Windows cp1252 console).
"""

import json
import time
from pathlib import Path

CLAUDE = Path.home() / ".claude"
CRON_PROMPTS = CLAUDE / "cron-prompts"
REGISTRY = CLAUDE / "scheduled_tasks.json"

# Known cadence (hours) per type. Unknown types fall back to DEFAULT_CADENCE_H.
CADENCE = {
    "skill-mining": 4,
    "simplicity-loop": 8,
    "odysseus-issue-help": 3,
    "odysseus-discovery": 4,
    "odysseus-daily-cadence": 12,
    "story-mode-self-improve": 12,
}
DEFAULT_CADENCE_H = 12

# Output-log name overrides for types whose log deviates from the _<type>-log.md
# convention (knowledge convention cannot derive). simplicity-loop writes
# _simplicity-log.md, NOT _simplicity-loop-log.md (a stale duplicate).
LOG_NAME = {"simplicity-loop": "_simplicity-log.md"}

# PRODUCE-axis: output logs whose mtime is untrustworthy (written by non-cron paths).
EXCLUDE_OUTPUT = {"persistence-sweep"}  # precompact-persistence-snapshot.py bumps it


def _out_log_name(typ):
    return LOG_NAME.get(typ, "_" + typ + "-log.md")


def _registered_types():
    try:
        d = json.load(open(REGISTRY, encoding="utf-8"))
    except Exception:
        return set()
    tasks = d if isinstance(d, list) else (
        d.get("tasks") or d.get("scheduled_tasks") or list(d.values()))
    import re
    rx = re.compile(r"type:\s*([a-z0-9][a-z0-9-]{2,})")
    types = set()
    for t in tasks if isinstance(tasks, list) else []:
        if isinstance(t, dict):
            mm = rx.search(t.get("prompt", "") or "")
            if mm:
                types.add(mm.group(1))
    return types


def _age_h(p: Path, now: float):
    return (now - p.stat().st_mtime) / 3600.0 if p.exists() else None


def main():
    now = time.time()
    registered = _registered_types()
    if not registered:
        return  # registry unreadable -> stay silent rather than false-alarm

    produce_stale, fire_stale, fired_no_output, orphans = [], [], [], []

    for typ in sorted(registered):
        cadence = CADENCE.get(typ, DEFAULT_CADENCE_H)
        thr = max(3 * cadence, 18)
        out_log = CRON_PROMPTS / _out_log_name(typ)
        hb_log = CRON_PROMPTS / ("_" + typ + "-heartbeat.log")

        out_age = None if typ in EXCLUDE_OUTPUT else _age_h(out_log, now)
        has_out_decl = out_log.exists() and typ not in EXCLUDE_OUTPUT
        fire_age = _age_h(hb_log, now)  # None => not yet observed (benign)

        # PRODUCE: only alarm when a trusted output log exists but is stale.
        if has_out_decl and out_age is not None and out_age > thr:
            produce_stale.append((typ, out_age, thr))
        # FIRE: only alarm when heartbeat data exists and has gone stale.
        if fire_age is not None and fire_age > thr:
            fire_stale.append((typ, fire_age, thr))
        # CROSS: fired recently but its output log is stale/missing => body dead.
        if fire_age is not None and fire_age <= thr:
            if has_out_decl and (out_age is None or out_age > thr):
                fired_no_output.append((typ, fire_age, out_age))

    # ORPHAN: an output log claimed by no registered cron. "Claimed" is
    # override-aware, so a deviating log name (e.g. _simplicity-log.md) is not
    # mistaken for an orphan, and a stale convention-named duplicate whose type
    # is still registered is simply ignored (not an alarm).
    claimed = {_out_log_name(t) for t in registered}
    for lg in sorted(CRON_PROMPTS.glob("_*-log.md")):
        typ = lg.name[1:-7]  # strip leading _ and -log.md
        if lg.name in claimed or typ in registered or typ in EXCLUDE_OUTPUT:
            continue
        orphans.append((typ, _age_h(lg, now)))

    if not (produce_stale or fire_stale or fired_no_output or orphans):
        return

    print("=== CRON WITNESS: PRODUCTIVITY + FIRING ===")
    print("Ground truth = live scheduled_tasks.json. Registered crons whose FIRE or "
          "PRODUCE signal has gone stale (loop may be dead though still registered):")

    if fired_no_output:
        print("  [FIRED-BUT-NO-OUTPUT -- loop body likely dead]")
        for typ, fa, oa in fired_no_output:
            out = "MISSING" if oa is None else f"{oa/24:.1f}d old"
            print(f"    {typ:<26} fired {fa:.1f}h ago but output log {out}")
    if produce_stale:
        print("  [PRODUCE stale -- no fresh output log]")
        for typ, age, thr in produce_stale:
            print(f"    {typ:<26} {age/24:.1f}d stale (threshold {thr:.0f}h)")
    if fire_stale:
        print("  [FIRE stale -- scheduler may have stopped injecting]")
        for typ, age, thr in fire_stale:
            print(f"    {typ:<26} last fire {age/24:.1f}d ago (threshold {thr:.0f}h)")
    if orphans:
        print("  [orphan logs -- cron deregistered, log lingering (informational)]:")
        for typ, age in orphans:
            a = "?" if age is None else f"{age/24:.1f}d"
            print(f"    {typ:<26} {a} old ({typ} not in registry)")
    print("  => registry-grounded; FIRE axis needs cron-fire-heartbeat.py data to "
          "accumulate (absent heartbeat = not-yet-observed, not an alarm).")


if __name__ == "__main__":
    main()
