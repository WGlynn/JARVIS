#!/usr/bin/env python3
"""UserPromptSubmit hook: inject current-time / session-start / elapsed every turn.

Pair of `clock-session-start.py`. See that file for consent context and spec
constraints. This script is the per-turn perceptual surface.

Contract
--------
- stdin: JSON { session_id, prompt, ... }
- reads: runtime/clock-{session_id}.json (written by SessionStart hook)
- stdout: JSON { hookSpecificOutput: { hookEventName, additionalContext } }

Fail-loud: missing start-file surfaces as [WARN] (means SessionStart hook
didn't fire — diagnostic, not silent fallback).

Spec constraints (consent-locked, do not extend without re-consent)
-------------------------------------------------------------------
- Surfaces: now, session-start, elapsed, day-of-week.
- Does NOT surface: idle/activity inference, sleep proxy, time-judgments.
- Pre-commit: clock does not violate [NoRestSuggestions]. The injected text
  must not editorialize on time (no "late", "long session", etc.) — facts only.
"""
import json
import os
import sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RUNTIME_DIR = os.path.expanduser("~/.claude/runtime")


def fmt_elapsed(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h {mins}m"
    days, hrs = divmod(hours, 24)
    return f"{days}d {hrs}h"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        print(f"[clock-injector] stdin parse failed: {e}", file=sys.stderr)
        return 0

    session_id = payload.get("session_id") or "default"
    path = os.path.join(RUNTIME_DIR, f"clock-{session_id}.json")

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    dow = now.strftime("%a")

    start_pretty = None
    elapsed_str = None
    warn = None

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            start_iso = data.get("start_iso")
            if start_iso:
                start_dt = datetime.fromisoformat(start_iso)
                start_pretty = start_dt.strftime("%Y-%m-%d %H:%M:%S")
                elapsed = int((now - start_dt).total_seconds())
                elapsed_str = fmt_elapsed(elapsed)
        except Exception as e:
            warn = f"clock state unreadable: {e}"
    else:
        warn = (
            f"start-file missing at {path} — "
            "SessionStart hook didn't fire or session_id mismatch"
        )

    lines = [
        "[CLOCK]",
        f"date: {date_str} ({dow})",
        f"time: {time_str}",
    ]
    if start_pretty and elapsed_str is not None:
        lines.append(f"session-start: {start_pretty}")
        lines.append(f"session-elapsed: {elapsed_str}")
    if warn:
        lines.append(f"[WARN] {warn}")

    context = "\n".join(lines)

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
