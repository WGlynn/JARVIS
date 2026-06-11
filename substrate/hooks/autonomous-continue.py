#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autonomous-Continue Gate
========================

Stop-event hook. Per `feedback_autonomous-production-default.md`:

  ∀ active session ⇒ continue-producing = default.
  ack-w/o-follow-on = failure.
  end-of-unit ⇒ scan-next-work ¬ idle.

This hook fires at the end of every assistant turn and scans for signals
that there is pending work the model should pick up rather than wait
for the user. If signals found, it injects `additionalContext` reminding
the assistant to continue.

Detection signals (any one triggers continue-reminder):

  1. **In-flight agents**: any task files at
     ~/.claude/projects/<slug>/<session-id>/tasks/*.output that are
     non-empty + open (no completion marker found in last 5 minutes)

  2. **Recent pool dispatch**: AUDIT_INDEX.md or any cycle workspace at
     ~/audits/**/AUDIT_INDEX.md mentions "in-flight" agents

  3. **WAL ACTIVE epoch**: vibeswap/.claude/WAL.md has ACTIVE marker without
     a recent CLEAN close

  4. **TaskList pending**: presence of `~/.claude/state/tasks-pending.json`
     with non-empty array

When any fires, the hook emits a continue-prompt the assistant sees on
its next turn. Augmentation, never blocks.
"""

import json
import sys
import os
import time
from pathlib import Path

HOME = Path.home()
SESSION_ROOT = HOME / ".claude" / "projects"
AUDIT_ROOT = HOME / "audits"
WAL_PATH = HOME / "vibeswap" / ".claude" / "WAL.md"
TASKS_PENDING = HOME / ".claude" / "state" / "tasks-pending.json"

# A task is considered "in-flight" if its output file was touched in the
# last 30 minutes AND we have not seen a JSON-shaped completion record
# inside it yet.
IN_FLIGHT_WINDOW_SECONDS = 30 * 60

# Signal sources older than this are treated as stale, not live. Prevents
# leftover WAL ACTIVE markers and old AUDIT_INDEX 'in-flight' tokens from
# spamming continue-signals forever. 2026-06-10: caught firing on May 17
# WAL + May 24 AUDIT_INDEX.
STALE_SIGNAL_SECONDS = 7 * 24 * 60 * 60


def find_inflight_agents() -> list[str]:
    """Scan task-output dirs for agents that look still-running."""
    matches: list[str] = []
    if not SESSION_ROOT.exists():
        return matches
    cutoff = time.time() - IN_FLIGHT_WINDOW_SECONDS
    # Walk every project's tasks dir
    for proj in SESSION_ROOT.iterdir():
        if not proj.is_dir():
            continue
        for session_dir in proj.iterdir():
            if not session_dir.is_dir():
                continue
            tasks_dir = session_dir / "tasks"
            if not tasks_dir.exists():
                continue
            for outfile in tasks_dir.glob("*.output"):
                try:
                    st = outfile.stat()
                except FileNotFoundError:
                    continue
                if st.st_mtime < cutoff:
                    continue  # stale, treat as resolved
                # Heuristic: if file has no `"status": "completed"` substring,
                # treat as in-flight. Cheap scan, last 4KB only.
                try:
                    with outfile.open("rb") as f:
                        f.seek(max(0, st.st_size - 4096))
                        tail = f.read().decode("utf-8", errors="ignore")
                    if '"status": "completed"' in tail or '"status":"completed"' in tail:
                        continue
                    matches.append(outfile.stem)
                except Exception:
                    continue
    return matches


def find_inflight_audit_cycles() -> list[str]:
    """Look at any AUDIT_INDEX.md files for the literal token 'in-flight'.
    Stale files (mtime > STALE_SIGNAL_SECONDS) are skipped — old completed
    cycles often retain the token without being live."""
    matches: list[str] = []
    if not AUDIT_ROOT.exists():
        return matches
    cutoff = time.time() - STALE_SIGNAL_SECONDS
    for idx in AUDIT_ROOT.glob("**/AUDIT_INDEX.md"):
        try:
            if idx.stat().st_mtime < cutoff:
                continue
            text = idx.read_text(encoding="utf-8")
        except Exception:
            continue
        if "in-flight" in text.lower():
            matches.append(str(idx.relative_to(HOME)))
    return matches


def wal_active() -> bool:
    if not WAL_PATH.exists():
        return False
    try:
        if WAL_PATH.stat().st_mtime < time.time() - STALE_SIGNAL_SECONDS:
            return False  # WAL hasn't been touched in >7d — stale, not live
        with WAL_PATH.open(encoding="utf-8") as f:
            title = f.readline()
    except Exception:
        return False
    # Title line is the canonical epoch status by convention:
    # "# Write-Ahead Log — ACTIVE (...)" vs "— CLEAN (...)". The body keeps
    # historical epochs with their own ACTIVE headers, and closure notes may
    # mention ACTIVE in prose — a substring scan of the first 2KB false-fired
    # on a freshly CLOSED WAL (2026-06-10).
    return "ACTIVE" in title.upper()


def pending_tasks_count() -> int:
    if not TASKS_PENDING.exists():
        return 0
    try:
        data = json.loads(TASKS_PENDING.read_text(encoding="utf-8"))
    except Exception:
        return 0
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict) and isinstance(data.get("tasks"), list):
        return len(data["tasks"])
    return 0


TEMP_TASKS = Path(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp") / "claude"
LIVE_AGENT_WINDOW_SECONDS = 10 * 60


def background_agent_alive() -> bool:
    """True when a harness background-agent task file was touched recently.

    Background agents stream JSONL to %TEMP%/claude/<proj>/<session>/tasks/*.output
    while they run. A fresh mtime means work is provably in flight, so a
    WAL-ACTIVE-only signal is a sanctioned wait, not idling. Re-blocking every
    Stop in that state is a loop without same-state dedup (the exact
    anti-pattern in [F·design-loops-not-prompts]) — suppress instead.
    """
    try:
        now = time.time()
        for p in TEMP_TASKS.rglob("tasks/*.output"):
            st = p.stat()
            # Streaming harness: fresh mtime = live. Write-on-completion
            # harness: the file is created 0-byte at spawn and stays empty
            # until the agent finishes, so empty+recent = still running.
            if st.st_mtime > now - LIVE_AGENT_WINDOW_SECONDS:
                return True
            if st.st_size == 0 and st.st_mtime > now - 6 * 3600:
                return True
    except Exception:
        pass
    return False


def main() -> int:
    try:
        _payload = json.load(sys.stdin)
    except Exception:
        _payload = {}

    inflight_agents = find_inflight_agents()
    inflight_cycles = find_inflight_audit_cycles()
    wal_dirty = wal_active()
    n_pending = pending_tasks_count()

    # Same-state dedup: WAL-ACTIVE as the lone signal + a live background agent
    # means the wait was already declared and the work is running. Stay silent.
    if (
        wal_dirty
        and not inflight_agents
        and not inflight_cycles
        and not n_pending
        and background_agent_alive()
    ):
        print(json.dumps({}))
        return 0

    signals = []
    if inflight_agents:
        signals.append(f"{len(inflight_agents)} subagent(s) still running: {', '.join(inflight_agents[:6])}")
    if inflight_cycles:
        signals.append(f"audit cycle workspace marked 'in-flight': {inflight_cycles[0]}")
    if wal_dirty:
        signals.append("WAL.md epoch ACTIVE (not closed)")
    if n_pending:
        signals.append(f"{n_pending} pending tasks queued at {TASKS_PENDING}")

    if not signals:
        print(json.dumps({}))
        return 0

    msg = (
        "[AUTONOMOUS CONTINUE GATE]\n"
        "Pending work detected. Per `feedback_autonomous-production-default.md`:\n"
        "  ∀ active session ⇒ continue-producing = default · ack-w/o-follow-on = failure.\n\n"
        "Signals:\n"
        + "\n".join(f"  · {s}" for s in signals)
        + "\n\nAction: continue producing on the next turn. Do not idle, do not wait for "
          "user approval unless genuinely blocked. If pool is at capacity and you are "
          "waiting on agent returns, that IS continuing — but say so explicitly rather "
          "than going silent. Orchestrate during dispatch per RSAW Phase 2.5."
    )

    out = {
        "decision": "block",
        "reason": msg,
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
