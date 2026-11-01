#!/usr/bin/env python3
"""
Boot staleness check for the two OS-scheduled persistence tasks (in-system alarm).

Pairs with two Windows Task Scheduler tasks that write logs but that NOTHING at
boot currently reads:

  - JARVIS-GitAutosave      -> bin/git-autosave.py, every 5 min, appends to
                               ~/.claude/.autosave/git-autosave.log on each run.
                               This is the every-5-min WIP snapshot (working dirs
                               committed + pushed to the private vault).
  - JARVIS-MemoryCorpusPush -> bin/memory-corpus-push.py, daily, appends to
                               ~/.claude/.autosave/memory-corpus-push.log. This is
                               the daily off-machine push of the mind corpus
                               (NDA-tainted files excluded), and it is the ONLY
                               path the memory WIP reaches the vault by, because
                               git-autosave fail-closed skips the memory repo push
                               whenever protected keywords appear in the snapshot
                               ("memory: NDA-ABORT push" lines in git-autosave.log).

Neither log is read by any boot hook (grep of session-chain/ and hooks/ for these
log names / task names returns empty). So if either scheduled task silently stops
-- disabled after a Windows update, non-zero LastResult, host renamed, credentials
expired -- the every-5-min WIP snapshot and/or the daily mind-corpus off-machine
push would die with ZERO alarm. That is the exact silent-failure class fixed for
crash-recovery (backtest witness) and for cron EXPIRY/registration (cron-keeper
resets the 7-day expiry clock). NOTE: cron OUTPUT/productivity liveness is a
SEPARATE, currently-open gap -- cron-keeper does not verify any cron produced work.

This hook, wired into SessionStart, reads the two logs' mtimes and surfaces LOUD
when either task's liveness is in doubt:

  - log MISSING     -> the task has never run (or its dir was wiped)
  - log UNREADABLE  -> corrupted / permission problem; treat as dead
  - log STALE       -> last write is older than the task's threshold => the Task
                       Scheduler task is almost certainly dead / disabled, and that
                       persistence path is currently OFF

Both fresh -> SILENT (a clean boot adds zero noise).

Thresholds are set generously past each task's own cadence so a fresh boot between
runs never false-alarms:
  - git-autosave runs every 5 min          -> stale if > 30 min (6 missed runs)
  - memory-corpus-push runs daily          -> stale if > 2 days (2 missed runs)

Warn-only: this hook prints to stdout and always exits 0. It can never block boot.
Re-enabling a dead scheduled task is a separate, human-decided action (see the
schtasks hints); this witness only makes the death visible.
"""

import time
from pathlib import Path

AUTOSAVE_DIR = Path.home() / ".claude" / ".autosave"

# Each entry: log filename, human label, Task Scheduler task name, stale threshold
# (minutes), one-line description of what dies when it goes stale, and the schtasks
# query hint to verify the task is still enabled.
CHECKS = [
    {
        "log": "git-autosave.log",
        "label": "GIT-AUTOSAVE",
        "task": "JARVIS-GitAutosave",
        "stale_min": 30.0,
        "cadence": "every 5 min",
        "dies": "the every-5-min WIP snapshot of the working dirs stops reaching the vault",
        "query": "schtasks /Query /TN JARVIS-GitAutosave",
    },
    {
        "log": "memory-corpus-push.log",
        "label": "MEMORY-CORPUS-PUSH",
        "task": "JARVIS-MemoryCorpusPush",
        "stale_min": 2.0 * 24 * 60,  # 2 days
        "cadence": "daily",
        "dies": "the daily off-machine push of the mind corpus stops (this is the ONLY "
                "path memory WIP reaches the vault, since git-autosave NDA-aborts the "
                "memory push)",
        "query": "schtasks /Query /TN JARVIS-MemoryCorpusPush",
    },
]


def _last_line(path):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return None
    for ln in reversed(lines):
        if ln.strip():
            return ln.strip()
    return ""


def _fmt_age(age_min):
    if age_min < 90:
        return f"{age_min:.1f} min"
    return f"{age_min / 60.0:.1f} hr"


def _fmt_threshold(stale_min):
    if stale_min < 90:
        return f"{stale_min:.0f} min"
    return f"{stale_min / 60.0 / 24.0:.0f}d" if stale_min >= 24 * 60 else f"{stale_min / 60.0:.0f} hr"


def check(spec):
    log = AUTOSAVE_DIR / spec["log"]

    if not log.exists():
        print(f"=== OS-TASK WITNESS: {spec['label']} MISSING ===")
        print(f"Task {spec['task']} ({spec['cadence']}) has NEVER written {spec['log']} (or its dir was wiped).")
        print(f"Effect: {spec['dies']}.")
        print("This is the alarm working, not a false one.")
        print(f"verify: {spec['query']}")
        return

    try:
        mtime = log.stat().st_mtime
    except Exception as e:
        print(f"=== OS-TASK WITNESS: {spec['label']} UNREADABLE ===")
        print(f"{type(e).__name__}: {e} -- treat task {spec['task']} as dead.")
        print(f"Effect: {spec['dies']}.")
        print(f"verify: {spec['query']}")
        return

    age_min = (time.time() - mtime) / 60.0
    if age_min > spec["stale_min"]:
        print(f"=== OS-TASK WITNESS: {spec['label']} STALE ===")
        print(f"Last write to {spec['log']} was {_fmt_age(age_min)} ago; "
              f"threshold is {_fmt_threshold(spec['stale_min'])} ({spec['cadence']}).")
        last = _last_line(log)
        if last:
            print(f"last log line: {last}")
        print(f"Task Scheduler task {spec['task']} is likely dead/disabled -- "
              f"{spec['dies']}.")
        print(f"verify: {spec['query']}")
    # fresh within threshold -> silent by design


def main():
    for spec in CHECKS:
        check(spec)


if __name__ == "__main__":
    main()
