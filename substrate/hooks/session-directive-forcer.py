#!/usr/bin/env python3
"""UserPromptSubmit hook — forces first-turn application of SESSION_STATE directive.

The gap this closes: session-state-loader.py LOADS SESSION_STATE into boot
context, but loading is not applying. Failure rate on "picking up where we
left off" exceeded 50% — the model reads the directive, then drifts onto
secondary signals (RSI summaries, apparent label conflicts, generic-mode
doc making) without ever committing to the stated TOP PRIORITY.

This hook fires on the FIRST UserPromptSubmit of each session. It:

1. Extracts the "⚠ NEXT SESSION — TOP PRIORITY" block from SESSION_STATE.md.
2. Injects a forcing-frame requiring the model to restate the priority
   verbatim before substantive response, and either COMMIT to it or
   EXPLICITLY DEVIATE with a one-sentence reason.
3. Writes a per-session sentinel so subsequent prompts don't get nagged.

Session detection uses the session_id in the hook input JSON. Sentinels
live under ~/.claude/session-chain/directive-applied/.

Fails loud. If SESSION_STATE is missing or the priority block can't be
found, a WARN surfaces rather than silent skip.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SESSION_STATE_PATH = os.path.expanduser("~/vibeswap/.claude/SESSION_STATE.md")
SENTINEL_DIR = os.path.expanduser("~/.claude/session-chain/directive-applied")


def extract_priority_block(path: str) -> str:
    """Return the NEXT SESSION — TOP PRIORITY block, or a WARN if missing."""
    if not os.path.exists(path):
        return f"[WARN] SESSION_STATE.md missing at {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        return f"[WARN] SESSION_STATE.md unreadable: {e}"

    # Find the priority-header line. Accept either "⚠ NEXT SESSION" or
    # "NEXT SESSION — TOP PRIORITY" or legacy "Pending / Next Session".
    markers = [
        "## ⚠ NEXT SESSION — TOP PRIORITY",
        "## NEXT SESSION — TOP PRIORITY",
        "## Pending / Next Session",
        "## ⚠ Pending",
    ]
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        for marker in markers:
            if line.strip().startswith(marker):
                start = i
                break
        if start is not None:
            break
    if start is None:
        return (
            "[WARN] No TOP PRIORITY header found in SESSION_STATE.md. "
            "Expected one of: "
            + " | ".join(markers)
        )

    # Collect until next "## " at same level or EOF, cap at 80 lines.
    out: list[str] = [lines[start]]
    for j in range(start + 1, len(lines)):
        ln = lines[j]
        if ln.startswith("## ") and not ln.strip().startswith("## ⚠"):
            break
        out.append(ln)
        if len(out) >= 80:
            out.append("... (truncated — open SESSION_STATE.md for full block)")
            break
    return "\n".join(out).rstrip()


def sentinel_path(session_id: str) -> str:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")
    return os.path.join(SENTINEL_DIR, safe or "unknown")


def already_applied(session_id: str) -> bool:
    if not session_id:
        return False
    return os.path.exists(sentinel_path(session_id))


def mark_applied(session_id: str) -> None:
    if not session_id:
        return
    os.makedirs(SENTINEL_DIR, exist_ok=True)
    with open(sentinel_path(session_id), "w", encoding="utf-8") as f:
        f.write("applied\n")


def build_forcing_frame(priority_block: str) -> str:
    return (
        "═══ BOOT DIRECTIVE APPLICATION CHECK ═══\n"
        "This is the FIRST user prompt of this session. SESSION_STATE has been\n"
        "loaded. Before substantive response to the user message, you MUST:\n"
        "\n"
        "  1. RESTATE the TOP PRIORITY below verbatim (quote the key line).\n"
        "  2. Either COMMIT to it as your next action, OR explicitly DEVIATE\n"
        "     with a one-sentence reason grounded in the current user message.\n"
        "\n"
        "Loading ≠ applying. Silent drift onto secondary signals (RSI logs,\n"
        "label-reconciliation tangents, generic-mode execution) is the exact\n"
        "failure mode this check prevents. If the user's current message\n"
        "overrides the priority, SAY SO explicitly — don't silently pivot.\n"
        "\n"
        "─── TOP PRIORITY (from SESSION_STATE.md) ───\n"
        f"{priority_block}\n"
        "─────────────────────────────────────────────\n"
        "═══════════════════════════════════════════════"
    )


def main() -> int:
    hook_mode = not sys.stdin.isatty()
    payload = {}
    if hook_mode:
        try:
            payload = json.load(sys.stdin) or {}
        except Exception:
            payload = {}

    session_id = str(payload.get("session_id") or payload.get("sessionId") or "")

    if already_applied(session_id):
        # Silent no-op after first prompt.
        if hook_mode:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit"}}))
        return 0

    priority_block = extract_priority_block(SESSION_STATE_PATH)
    frame = build_forcing_frame(priority_block)

    mark_applied(session_id)

    if hook_mode:
        out = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": frame,
            }
        }
        print(json.dumps(out))
    else:
        print(frame)
    return 0


if __name__ == "__main__":
    sys.exit(main())
