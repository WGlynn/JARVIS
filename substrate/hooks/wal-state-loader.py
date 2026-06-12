#!/usr/bin/env python3
"""SessionStart hook: surface WAL.md state (CLEAN vs ACTIVE) at boot.

CLAUDE.md protocol chain:
    SESSION_STATE.md FIRST -> WAL.md check -> [ACTIVE?] YES -> AAP Recovery

No hook was enforcing the WAL check. If a prior session crashed leaving WAL
ACTIVE, the new session would silently miss it and resume without running
the Anti-Amnesia Protocol recovery path. This script converts the
memory-layer rule into hook-layer enforcement.

Reads the first ~30 lines of vibeswap/.claude/WAL.md. Emits the top epoch
status (CLEAN / ACTIVE) + the next-session directive line if present.

Fail-loud: missing WAL.md surfaces as [WARN] to Claude rather than silent.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

WAL_PATH = os.path.expanduser("~/vibeswap/.claude/WAL.md")
JARVIS_WAL_PATH = os.path.expanduser("~/.claude/WAL.md")
MAX_LINES = 35


def extract_top_epoch(path: str) -> tuple[str, bool]:
    """Return (summary, is_active). is_active=True requires boot-time AAP recovery."""
    if not os.path.exists(path):
        return (
            f"[WARN] WAL.md missing at {path}. "
            "CLAUDE.md protocol chain requires WAL check at boot. "
            "Restore or investigate before proceeding.",
            False,
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return f"[WARN] WAL.md unreadable: {e}", False

    out: list[str] = []
    for i, line in enumerate(lines):
        if i >= MAX_LINES:
            break
        if line.strip() == "---" and out:
            break
        out.append(line.rstrip())

    text = "\n".join(out)
    # Title line is the canonical epoch status by convention:
    # "# Write-Ahead Log — ACTIVE (...)" vs "— CLEAN (...)". Historical epochs
    # in the body keep their own ACTIVE headers and prose may mention ACTIVE;
    # only the title reflects the live epoch (heuristic scan false-fired on a
    # freshly CLOSED WAL, 2026-06-10).
    title = lines[0] if lines else ""
    is_active = "ACTIVE" in title.upper()
    return text.strip(), is_active


def main() -> int:
    hook_mode = not sys.stdin.isatty()
    if hook_mode:
        try:
            json.load(sys.stdin)
        except Exception:
            pass

    proj_summary, proj_active = extract_top_epoch(WAL_PATH)
    jarvis_summary, jarvis_active = extract_top_epoch(JARVIS_WAL_PATH)
    is_active = proj_active or jarvis_active

    if is_active:
        which = []
        if proj_active:
            which.append("vibeswap")
        if jarvis_active:
            which.append("JARVIS-wide")
        header = (
            f"[WAL ACTIVE ({' + '.join(which)}) -- prior session did not close cleanly]\n"
            "CLAUDE.md CRASH-recovery path required. Run AAP "
            "(cross-ref WAL manifest vs git log, auto-commit orphans) "
            "before resuming work.\n\n"
        )
    else:
        header = "[WAL status -- latest epoch (two-tier: project + JARVIS-wide)]\n"

    context = (
        header
        + "## vibeswap/.claude/WAL.md\n" + proj_summary
        + "\n\n## ~/.claude/WAL.md (JARVIS-wide)\n" + jarvis_summary
        + "\n\nFull files: vibeswap/.claude/WAL.md + ~/.claude/WAL.md"
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
