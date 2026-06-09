#!/usr/bin/env python3
"""
Stop hook: detect parallel Agent execution issues and trigger RSI cycle.

Reads the session transcript, finds the last assistant turn, counts concurrent
Agent tool uses, and checks for error signatures. If issues detected in parallel
execution, blocks the Stop with a reminder to log to WAL.md + run RSI cycle.

Rule: memory/feedback_parallel-issues-rsi-cycle.md
Meta: memory/primitive_always-equals-gate.md ("always" = hook)
"""
import json
import os
import sys
from pathlib import Path

ERROR_SIGNATURES = (
    '"is_error":true',
    '"is_error": true',
    "error:",
    "timed out",
    "timeout",
    "failed to",
    "exception:",
    "traceback",
    "inputvalidationerror",
)


def read_transcript(session_id: str):
    home = Path(os.path.expanduser("~"))
    # Transcript location on this machine
    candidates = [
        home / ".claude" / "projects" / "C--Users-Will" / f"{session_id}.jsonl",
    ]
    for path in candidates:
        if path.exists():
            try:
                return path.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception:
                return None
    return None


def last_assistant_tool_uses(lines):
    for line in reversed(lines):
        try:
            entry = json.loads(line)
        except Exception:
            continue
        if entry.get("type") != "assistant":
            continue
        message = entry.get("message", {})
        content = message.get("content", [])
        tool_uses = [c for c in content if isinstance(c, dict) and c.get("type") == "tool_use"]
        if tool_uses:
            return tool_uses
    return []


def find_agent_issues(lines, agent_ids):
    issues = []
    for line in lines:
        try:
            entry = json.loads(line)
        except Exception:
            continue
        if entry.get("type") != "user":
            continue
        message = entry.get("message", {})
        content = message.get("content", [])
        if not isinstance(content, list):
            continue
        for c in content:
            if not isinstance(c, dict):
                continue
            if c.get("type") != "tool_result":
                continue
            if c.get("tool_use_id") not in agent_ids:
                continue
            if c.get("is_error") is True:
                issues.append(c.get("tool_use_id"))
                continue
            result_text = json.dumps(c.get("content", "")).lower()
            if any(sig in result_text for sig in ERROR_SIGNATURES):
                issues.append(c.get("tool_use_id"))
    return issues


def main():
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    session_id = hook_input.get("session_id", "")
    if not session_id:
        sys.exit(0)

    lines = read_transcript(session_id)
    if not lines:
        sys.exit(0)

    tool_uses = last_assistant_tool_uses(lines)
    agent_uses = [t for t in tool_uses if t.get("name") == "Agent"]
    if len(agent_uses) < 2:
        sys.exit(0)

    agent_ids = {t.get("id") for t in agent_uses if t.get("id")}
    issues = find_agent_issues(lines, agent_ids)
    if not issues:
        sys.exit(0)

    reason = (
        f"PARALLEL-AGENT ISSUE DETECTED ({len(issues)}/{len(agent_uses)} agents returned errors). "
        f"Before proceeding: (1) log incident to vibeswap/.claude/WAL.md with timestamp, agents involved, "
        f"and nature of issue; (2) run an RSI cycle on the failure mode — what gate would have prevented it? "
        f"Resume the original task only after RSI completes. "
        f"Rule: memory/feedback_parallel-issues-rsi-cycle.md"
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
