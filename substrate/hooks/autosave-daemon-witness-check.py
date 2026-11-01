#!/usr/bin/env python3
"""
Boot staleness check for the autosave freeze-insurance daemon (in-system alarm).

Pairs with bin/autosave-daemon.sh -- a SEPARATE long-lived process (so a frozen
or killed Claude session cannot take the snapshot down with it) that copies the
active working dirs to ~/.claude/.autosave/<timestamp> every 10 min and appends a
line to ~/.claude/.autosave/autosave.log on every snapshot.

That daemon has no supervisor: it is not wired to SessionStart, not an OS
scheduled task, and nothing reads its log. So when it dies (frozen host, reboot,
OOM, manual kill) the freeze-insurance silently goes OFF and nothing alarms -- the
exact silent-failure class already fixed for crons and crash-recovery.

This hook, wired into SessionStart, reads autosave.log and surfaces LOUD when the
freeze-daemon's liveness is in doubt:

  - log MISSING     -> the daemon has never run (or its dir was wiped)
  - log UNREADABLE  -> corrupted / permission problem; treat as dead
  - log STALE       -> last snapshot is older than the threshold => the daemon is
                       almost certainly dead and long autonomous runs are running
                       with NO freeze-insurance right now

Fresh log (a snapshot within the threshold) -> SILENT (a clean boot adds zero noise).

This is the "absence is loud" half of the freeze-insurance design: a marker the
daemon writes on every heartbeat, checked at boot, so a dead daemon is a visible
alarm instead of an invisible non-event.

Warn-only: this hook prints to stdout and always exits 0. It can never block boot.
Restarting the daemon is a separate, human-decided action (see the restart hint).
"""

import time
from pathlib import Path

LOG = Path.home() / ".claude" / ".autosave" / "autosave.log"
PIDFILE = Path.home() / ".claude" / ".autosave" / "PID"
# The daemon snapshots every 10 min; >1 day of silence means it is almost
# certainly dead rather than merely between snapshots.
STALE_DAYS = 1.0
RESTART_HINT = "bash ~/.claude/bin/autosave-daemon.sh &"


def _last_line(path):
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return None
    for ln in reversed(lines):
        if ln.strip():
            return ln.strip()
    return ""


def main():
    if not LOG.exists():
        print("=== FREEZE-DAEMON WITNESS: MISSING ===")
        print("The autosave freeze-insurance daemon has NEVER written a log (or its dir was wiped).")
        print("Long autonomous runs currently have NO freeze-insurance. This is the alarm working, not a false one.")
        print(f"restart: {RESTART_HINT}")
        return

    try:
        mtime = LOG.stat().st_mtime
    except Exception as e:
        print("=== FREEZE-DAEMON WITNESS: UNREADABLE ===")
        print(f"{type(e).__name__}: {e} -- treat the freeze-insurance daemon as dead.")
        print(f"restart: {RESTART_HINT}")
        return

    age_days = (time.time() - mtime) / 86400.0

    if age_days > STALE_DAYS:
        last = _last_line(LOG)
        pid_txt = ""
        try:
            if PIDFILE.exists():
                pid_txt = PIDFILE.read_text(encoding="utf-8", errors="replace").strip()
        except Exception:
            pid_txt = ""
        print("=== FREEZE-DAEMON WITNESS: STALE/DEAD ===")
        print(f"Last autosave snapshot was {age_days:.1f}d ago; threshold is {STALE_DAYS}d.")
        if last:
            print(f"last log line: {last}")
        if pid_txt:
            print(f"stale PID file records pid {pid_txt} (likely a long-gone process).")
        print("The freeze-insurance daemon is almost certainly DEAD -- long autonomous runs are unprotected.")
        print(f"restart: {RESTART_HINT}")
    # fresh snapshot within threshold -> silent by design


if __name__ == "__main__":
    main()
