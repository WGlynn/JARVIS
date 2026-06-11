#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resource cgroup gate (PreToolUse Bash) — criticism-2 fix: a gate that GATES.

Converts the 'max 3 concurrent forge, 16GB ceiling' rule from memory PROSE
(an Always=Gate violation) into an enforced blocking decision. Counts live
heavy processes; DENIES the spawn that would exceed the cap. Deterministic,
can't false-lock a session (only blocks the over-cap heavy spawn).

Every actual denial is appended to gate_enforcement.log — closing the
'we never measure what a gate prevented' half of criticism 2.
"""
import json
import os
import re
import subprocess
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")
# local-only config (hardware limits stay out of committed files per
# feedback_local-vs-shared-constraints)
CFG = os.path.join(HOME, ".claude", "state", "resource-limits.json")
LEDGER = os.path.join(HOME, ".claude", "state", "gate_enforcement.log")
DEFAULTS = {"forge": 3, "heavy_total": 6}
# commands that count as a heavy spawn
HEAVY = re.compile(r"\b(forge\s+(test|build|coverage|snapshot)|npm\s+run\s+build|"
                   r"vite\s+build|cargo\s+(build|test)|python\s+-m\s+pytest)\b", re.I)
FORGE = re.compile(r"\bforge\s+(test|build|coverage|snapshot)\b", re.I)


def _ledger(entry: dict) -> None:
    try:
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def _live_counts() -> tuple[int, int]:
    """(forge_procs, heavy_total) currently running. Windows: tasklist."""
    forge = heavy = 0
    try:
        out = subprocess.run(["tasklist", "/v", "/fo", "csv"],
                             capture_output=True, text=True, timeout=5).stdout.lower()
        forge = out.count("forge.exe")
        heavy = forge + out.count("node.exe") // 1  # node build procs
    except Exception:
        # POSIX fallback
        try:
            out = subprocess.run(["ps", "-eo", "comm"], capture_output=True,
                                 text=True, timeout=5).stdout.lower()
            forge = out.count("forge")
            heavy = forge + out.count("vite") + out.count("pytest")
        except Exception:
            pass
    return forge, heavy


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({})); return 0
    if not isinstance(payload, dict):
        print(json.dumps({})); return 0
    ti = payload.get("tool_input") or {}
    if not isinstance(ti, dict):
        print(json.dumps({})); return 0
    cmd = ti.get("command") or ""
    if not isinstance(cmd, str) or not HEAVY.search(cmd):
        print(json.dumps({})); return 0

    cfg = dict(DEFAULTS)
    try:
        with open(CFG, encoding="utf-8") as f:
            cfg.update(json.load(f))
    except Exception:
        pass

    forge, heavy = _live_counts()
    is_forge = bool(FORGE.search(cmd))
    over = (is_forge and forge >= cfg["forge"]) or (heavy >= cfg["heavy_total"])
    if over:
        reason = (f"[RESOURCE GATE] DENIED — would exceed the hardware cap "
                  f"(forge {forge}/{cfg['forge']}, heavy {heavy}/{cfg['heavy_total']} "
                  f"on this 16GB box). Wait for a running build to finish, or run "
                  f"targeted (--match-path) instead. Adjust ~/.claude/state/"
                  f"resource-limits.json to override.")
        _ledger({"t": time.time(), "gate": "resource-cgroup", "action": "deny",
                 "cmd": cmd[:120], "forge": forge, "heavy": heavy})
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason}}))
        return 0
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    main()
