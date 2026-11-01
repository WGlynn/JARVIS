"""Keep the Jarvis TG bot alive on this PC (Will 2026-10-28).

The bot exits with code 1 in 8 places (failed polling restarts, memory pressure, ...) and expects a
cloud platform to restart it. On this PC nothing did, so one bad minute could leave it down until
someone noticed. This runs every 5 minutes from the OS task JARVIS-BotKeeper:

  - bot process (pid in ~/jarvis-bot-logs/pid.txt) alive  -> nothing.
  - dead -> run scripts/restart-local.ps1 (test-gated: refuses to start onto failing tests/lint),
    record kind keeper_restart / keeper_restart_failed in ~/jarvis-feed/health.jsonl, which the
    error-triage loop reads.

Stop it on purpose: create ~/.claude/state/jarvis-bot-keeper.off (the keeper then leaves a stopped
bot stopped). At most one restart attempt per 10 minutes, so a bot that crashes on boot is not
restarted in a tight loop.
"""
import json
import os
import subprocess
import time
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
BOT = os.path.join(HOME, "vibeswap", "jarvis-bot")
PID_FILE = os.path.join(HOME, "jarvis-bot-logs", "pid.txt")
LOG = os.path.join(HOME, "jarvis-bot-logs", "keeper.log")
HEALTH = os.path.join(HOME, "jarvis-feed", "health.jsonl")
OFF = os.path.join(HOME, ".claude", "state", "jarvis-bot-keeper.off")
LAST = os.path.join(HOME, ".claude", "state", "jarvis-bot-keeper.last")
MIN_GAP_S = 10 * 60
CONFIRM_S = 30
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{now()} {msg}\n")


def health(kind, **extra):
    os.makedirs(os.path.dirname(HEALTH), exist_ok=True)
    with open(HEALTH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now(), "kind": kind, "where": "bot-keeper", **extra}) + "\n")


def bot_alive():
    try:
        pid = int(open(PID_FILE, encoding="utf-8").read().strip())
    except (OSError, ValueError):
        return False, None
    out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                         capture_output=True, text=True, creationflags=NO_WINDOW).stdout
    return ("node" in out.lower()), pid


def main():
    if os.path.exists(OFF):
        return
    alive, pid = bot_alive()
    if alive:
        return
    # Confirm 30s later: a planned restart-local.ps1 run has a brief gap between stopping the old
    # process and writing the new pid, and must not be mistaken for a crash.
    time.sleep(CONFIRM_S)
    alive, pid = bot_alive()
    if alive:
        return
    try:
        if time.time() - os.path.getmtime(LAST) < MIN_GAP_S:
            log(f"bot down (pid {pid}) but last restart attempt < 10 min ago; waiting")
            return
    except OSError:
        pass
    open(LAST, "w").close()
    log(f"bot down (pid {pid}); running restart-local.ps1")
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        os.path.join(BOT, "scripts", "restart-local.ps1")],
                       cwd=BOT, capture_output=True, text=True, timeout=600, creationflags=NO_WINDOW)
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
    if r.returncode == 0 and "started PID" in r.stdout:
        log(f"restarted: {tail[0]}")
        health("keeper_restart", previous_pid=pid, result=tail[0][:200])
    else:
        log(f"restart FAILED rc={r.returncode}: {tail[0]}")
        health("keeper_restart_failed", previous_pid=pid, rc=r.returncode, result=tail[0][:200])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # never die silently: leave a trace the triage loop reads
        try:
            log(f"keeper error: {e}")
            health("keeper_restart_failed", error=str(e)[:200])
        except Exception:
            pass
