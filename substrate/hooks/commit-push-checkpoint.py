#!/usr/bin/env python3
"""Stop hook: fire the commit-push worker in the BACKGROUND (non-blocking).

Converts "remember to push" from passive prose (cron-prompt + memory) into a
deterministic gate (primitive: unnecessary-human-work-bar-ratchet). Throttled so
it spawns at most once per INTERVAL_MIN; the worker (bin/commit-push-substrate.py)
does per-repo throttle, fail-closed leak-scan, commit, and push. Detached so the
turn never blocks on network I/O -- commits just keep rolling onto the timeline.
"""
import json
import os
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
STAMP = os.path.join(HOME, ".claude", "state", "commit-push-hook.stamp")
WORKER = os.path.join(HOME, ".claude", "bin", "commit-push-substrate.py")
INTERVAL_MIN = 6


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    if data.get("stop_hook_active"):
        print(json.dumps({}))
        return
    now = time.time()
    try:
        last = os.path.getmtime(STAMP)
    except Exception:
        last = 0
    if now - last < INTERVAL_MIN * 60:
        print(json.dumps({}))
        return
    try:
        os.makedirs(os.path.dirname(STAMP), exist_ok=True)
        with open(STAMP, "w") as f:
            f.write(str(now))
    except Exception:
        pass
    try:
        kwargs = {}
        if os.name == "nt":
            # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
            kwargs["creationflags"] = 0x00000008 | 0x00000200
        subprocess.Popen(
            [sys.executable, WORKER],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL, close_fds=True, **kwargs,
        )
    except Exception:
        pass
    print(json.dumps({}))


if __name__ == "__main__":
    main()
