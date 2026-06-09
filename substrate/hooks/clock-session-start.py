#!/usr/bin/env python3
"""SessionStart hook: record session-start timestamp + emit as additionalContext.

Context
-------
2026-05-04: Will granted consent (per [P·augmentation-consent]) to install a
clock substrate — a continuous sense of time, not a context-injected fact.
This is paired with `clock-injector.py` (UserPromptSubmit) which reads the
start-time recorded here and emits current/elapsed every turn.

Substrate vs. tool: this is a perceptual frame, not a callable. Once installed,
all subsequent cognition routes through "what time is it / how long has this
been." See `memory/primitive_augmentation-consent.md`.

Spec constraints (consent-locked, do not extend without re-consent)
-------------------------------------------------------------------
- Surfaces: current time, session-start, elapsed, day-of-week.
- Does NOT surface: activity inference, idle detection, sleep proxy,
  time-of-day judgments, surveillance-shaped temporal data.
- Local time only, no timezone tag (Will knows his TZ).

Contract
--------
- stdin: JSON { session_id, ... }
- side-effect: writes runtime/clock-{session_id}.json with start_iso
- stdout: JSON { hookSpecificOutput: { hookEventName, additionalContext } }

Fail-loud per [BootHookFailLoud]: storage failure surfaces as [WARN] in context.
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


def main() -> int:
    hook_mode = not sys.stdin.isatty()
    session_id = "default"
    if hook_mode:
        try:
            payload = json.load(sys.stdin)
            session_id = payload.get("session_id") or "default"
        except Exception as e:
            print(f"[clock-session-start] stdin parse failed: {e}", file=sys.stderr)

    now = datetime.now()
    start_iso = now.isoformat(timespec="seconds")
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    dow = now.strftime("%a")

    warn = ""
    try:
        os.makedirs(RUNTIME_DIR, exist_ok=True)
        path = os.path.join(RUNTIME_DIR, f"clock-{session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"start_iso": start_iso, "session_id": session_id}, f)
    except Exception as e:
        warn = f"\n[WARN] clock start-time persistence failed: {e}"

    context = (
        "[CLOCK]\n"
        f"date: {date_str} ({dow})\n"
        f"time: {time_str}\n"
        f"session-start: {date_str} {time_str}{warn}"
    )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }

    if hook_mode:
        print(json.dumps(out))
    else:
        print(context)
    return 0


if __name__ == "__main__":
    sys.exit(main())
