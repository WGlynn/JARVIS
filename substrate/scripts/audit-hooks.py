#!/usr/bin/env python3
"""
audit-hooks.py

Behavior-persistence test harness. Verifies that every hook registered
in ~/.claude/settings.json actually exists on disk, is parseable Python,
and produces sensible output when fired with a synthetic payload.

Designed to catch silent breakage: a hook gets renamed, the settings.json
path goes stale, a syntax error sneaks in, or the hook's expected payload
shape drifts. No real user invocation exercises every hook regularly —
this script does.

Usage:
    python audit-hooks.py                   # full audit, structured report
    python audit-hooks.py --json            # machine-readable JSON output
    python audit-hooks.py --fix             # offer to fix obvious issues
                                            # (currently: report-only; --fix
                                            # reserved for future automation)

Exit codes:
    0 = all hooks healthy
    1 = warnings (non-critical: e.g. unexpected output format)
    2 = errors (critical: missing file, syntax error, crash on test payload)
"""
from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
from pathlib import Path


SETTINGS = Path.home() / ".claude" / "settings.json"

# A synthetic payload by event type. Each hook receives JSON on stdin.
# These payloads are minimal-valid for each event so we can exercise the
# hook's parsing + path-watching logic without a real session.
SYNTHETIC_PAYLOADS = {
    "SessionStart": {
        "hook_event_name": "SessionStart",
        "session_id": "audit-synthetic",
        "transcript_path": "",
        "cwd": str(Path.cwd()),
    },
    "UserPromptSubmit": {
        "hook_event_name": "UserPromptSubmit",
        "prompt": "audit-synthetic test prompt",
        "transcript_path": "",
    },
    "PreToolUse": {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "C:/Users/Will/audit-synthetic-target.md",
            "content": "synthetic content for audit",
        },
        "transcript_path": "",
    },
    "PostToolUse": {
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "C:/Users/Will/audit-synthetic-target.md",
            "content": "synthetic content for audit",
        },
        "tool_response": {"success": True},
        "transcript_path": "",
    },
    "Stop": {
        "hook_event_name": "Stop",
        "transcript_path": "",
    },
    "Notification": {
        "hook_event_name": "Notification",
        "message": "audit-synthetic notification",
    },
    "SubagentStop": {
        "hook_event_name": "SubagentStop",
        "transcript_path": "",
    },
}


def load_settings():
    if not SETTINGS.exists():
        return None
    try:
        return json.loads(SETTINGS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return {"_parse_error": str(e)}


def extract_hook_path(command: str) -> str | None:
    """Pull the .py file path out of a 'python /path/to/hook.py [args]' command."""
    m = re.search(r"python\s+([^\s]+\.py)", command)
    return m.group(1) if m else None


def enumerate_hooks(settings: dict):
    """Yield (event, matcher, command, path) tuples for every hook in settings."""
    hooks_block = settings.get("hooks", {})
    for event, event_groups in hooks_block.items():
        for group in event_groups:
            matcher = group.get("matcher", "*")
            for hook in group.get("hooks", []):
                cmd = hook.get("command", "")
                path = extract_hook_path(cmd)
                yield event, matcher, cmd, path


def file_check(path: str | None) -> tuple[str, str]:
    if not path:
        return "ok", "non-python command (skipping file check)"
    p = Path(path)
    if not p.exists():
        return "error", f"missing file: {path}"
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as e:
        return "error", f"read failed: {e}"
    if "def main" not in text and "__main__" not in text:
        return "warn", "no recognized entry point (main / __main__)"
    return "ok", f"{len(text)} bytes"


def syntax_check(path: str | None) -> tuple[str, str]:
    if not path or not Path(path).exists():
        return "skipped", ""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", path],
            capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="replace"
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return "error", str(e)
    if result.returncode != 0:
        return "error", (result.stderr or "").strip()[:200]
    return "ok", "compiles clean"


def smoke_fire(path: str | None, event: str) -> tuple[str, str]:
    """Fire the hook with a synthetic payload. Should return JSON; no exception."""
    if not path or not Path(path).exists():
        return "skipped", ""
    payload = SYNTHETIC_PAYLOADS.get(event)
    if payload is None:
        return "skipped", f"no synthetic payload for event {event}"
    try:
        result = subprocess.run(
            [sys.executable, path],
            input=json.dumps(payload),
            capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="replace"
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return "error", f"fire failed: {e}"
    if result.returncode != 0:
        return "error", f"non-zero exit ({result.returncode}): {(result.stderr or '').strip()[:200]}"
    out = (result.stdout or "").strip()
    if not out:
        return "ok", "silent (valid for many gates)"
    try:
        parsed = json.loads(out)
    except json.JSONDecodeError:
        return "warn", f"stdout not JSON: {out[:120]}"
    if not isinstance(parsed, dict):
        return "warn", f"stdout JSON is not object: {type(parsed).__name__}"
    return "ok", f"emitted {len(out)} bytes valid JSON"


def safe_print(s: str) -> None:
    """Print without crashing on terminals that can't encode arbitrary unicode."""
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", errors="replace").decode("ascii"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--fix", action="store_true", help="(reserved) attempt to fix issues")
    args = parser.parse_args()

    settings = load_settings()
    if settings is None:
        print(f"settings not found at {SETTINGS}", file=sys.stderr)
        return 2
    if "_parse_error" in settings:
        print(f"settings parse error: {settings['_parse_error']}", file=sys.stderr)
        return 2

    rows = []
    error_count = 0
    warn_count = 0
    for event, matcher, cmd, path in enumerate_hooks(settings):
        name = Path(path).name if path else "(non-py)"
        file_status, file_msg = file_check(path)
        syn_status, syn_msg = syntax_check(path)
        fire_status, fire_msg = smoke_fire(path, event)
        worst = "ok"
        for s in (file_status, syn_status, fire_status):
            if s == "error":
                worst = "error"
                break
            if s == "warn" and worst == "ok":
                worst = "warn"
        if worst == "error":
            error_count += 1
        elif worst == "warn":
            warn_count += 1
        rows.append({
            "event": event,
            "matcher": matcher,
            "name": name,
            "path": path or "",
            "file": {"status": file_status, "msg": file_msg},
            "syntax": {"status": syn_status, "msg": syn_msg},
            "smoke": {"status": fire_status, "msg": fire_msg},
            "verdict": worst,
        })

    if args.json:
        print(json.dumps({
            "ok": error_count == 0 and warn_count == 0,
            "errors": error_count,
            "warnings": warn_count,
            "hooks": rows,
        }, indent=2))
    else:
        safe_print(f"audit-hooks: {len(rows)} registered hook entry/entries")
        safe_print(f"  errors:   {error_count}")
        safe_print(f"  warnings: {warn_count}")
        safe_print("")
        symbol = {"ok": "OK ", "warn": "WARN", "error": "ERR ", "skipped": "skip"}
        for r in rows:
            safe_print(f"  [{symbol[r['verdict']]}] {r['event']:18s} {r['matcher']:18s} {r['name']}")
            for stage in ("file", "syntax", "smoke"):
                st = r[stage]
                if st["status"] != "ok" and st["status"] != "skipped":
                    safe_print(f"          {stage}: {st['status']:5s} {st['msg']}")

    if error_count:
        return 2
    if warn_count:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
