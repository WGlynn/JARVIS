#!/usr/bin/env python3
"""
time-logic-gate.py

PreToolUse hook on Write / Edit / NotebookEdit.
Scans drafted content for temporal claims that imply duration / since-when /
implied history WITHOUT a verifiable anchor in the same passage. Surfaces a
verify-then-assert reminder so the writer either substitutes a verified
anchor or marks the claim [unverified] before ship.

Source primitive: memory/primitive_time-logic-anti-hallucination-gate.md
"""
import json
import re
import sys


# Patterns that introduce a temporal claim. Each one fires the gate.
TEMPORAL_PATTERNS = [
    # Duration claims with no anchor in the same sentence
    r"\bfor (about |roughly |approximately )?\b(a |several |multiple |many )?(year|years|month|months|week|weeks|day|days|hour|hours)\b",
    r"\b(I've|we've|I have|we have) been [a-z]+ing\b",
    r"\bover (the )?(last|past) [a-z0-9]+ (year|years|month|months|week|weeks|day|days|hour|hours)\b",
    # Since-when claims
    r"\bsince (then|when|that time)\b",
    r"\bsince [0-9]{4}\b",
    # Implied-history phrases
    r"\bafter all this time\b",
    r"\bover the years\b",
    r"\bfor years\b",
    r"\blong[- ]running\b",
    # Recency adverbs that often slip in without anchoring
    r"\b(recently|lately|nowadays)\b(?!.*\b(2025|2026|today|yesterday|last week)\b)",
]

# Patterns that are valid anchors. If any appear in the same passage as a
# temporal claim, the gate does not fire.
ANCHOR_PATTERNS = [
    r"\b20\d{2}-\d{2}-\d{2}\b",          # explicit ISO date
    r"\b20\d{2}\b",                      # year mentioned
    r"\b(today|yesterday|this morning|this afternoon|tonight)\b",
    r"\boriginSessionId\b",
    r"\bcommit [a-f0-9]{7,}\b",          # git sha
    r"\bSHA [a-f0-9]{7,}\b",
    r"\b\[unverified\]\b",                # explicit honesty tag
    r"\bper user[- ]stated\b",
    r"\bsystem clock\b",
    r"\bfile mtime\b",
]

# File-path patterns the gate watches. The gate is most load-bearing on
# partner-facing drafts, memory primitives, and essay-grade artifacts. It
# does NOT fire on internal code comments or json files.
WATCHED_PATH_PATTERNS = [
    r"/desktop/[^/]*[_-]reply[-_.]",
    r"/desktop/[^/]*[_-]draft[-_.]",
    r"/desktop/[^/]*[_-]post[-_.]",
    r"/desktop/[^/]*[_-]essay[-_.]",
    r"/memory/(primitive|feedback|project|reference)_[^/]+\.md",
    r"/papers/[^/]+\.md",
    r"/jarvis-monorepo/[0-9]{2}-[^/]+/[^/]+\.md",
    r"/jarvis-os-public/memory/[^/]+\.md",
]


def is_watched(path):
    if not path:
        return False
    norm = path.replace("\\", "/").lower()
    return any(re.search(p, norm) for p in WATCHED_PATH_PATTERNS)


def find_temporal_claims(content):
    """Return list of (pattern, snippet) for temporal claims without anchors nearby."""
    if not content or not isinstance(content, str):
        return []
    hits = []
    for pat in TEMPORAL_PATTERNS:
        for m in re.finditer(pat, content, re.IGNORECASE):
            start = max(0, m.start() - 200)
            end = min(len(content), m.end() + 200)
            passage = content[start:end]
            has_anchor = any(re.search(a, passage, re.IGNORECASE) for a in ANCHOR_PATTERNS)
            if not has_anchor:
                snippet = content[max(0, m.start() - 40):min(len(content), m.end() + 40)]
                hits.append((m.group(0), snippet.replace("\n", " ").strip()))
    return hits


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return

    event = payload.get("hook_event_name", "")
    if event != "PreToolUse":
        print(json.dumps({}))
        return

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit", "NotebookEdit"):
        print(json.dumps({}))
        return

    tool_input = payload.get("tool_input", {})
    path = tool_input.get("file_path", "")
    if not is_watched(path):
        print(json.dumps({}))
        return

    content = ""
    if tool == "Write":
        content = tool_input.get("content", "")
    elif tool == "Edit":
        content = tool_input.get("new_string", "")
    elif tool == "NotebookEdit":
        content = tool_input.get("new_source", "")

    hits = find_temporal_claims(content)
    if not hits:
        print(json.dumps({}))
        return

    # Cap surfaced hits to first 3 so the message stays scannable
    lines = [
        f"[TIME-LOGIC GATE] {len(hits)} temporal claim(s) without nearby anchor "
        f"in {path}. Per [P·time-logic-anti-hallucination-gate], verify-then-assert "
        f"or mark [unverified]. Anchors accepted: ISO date, year, today/yesterday, "
        f"commit SHA, file mtime, user-stated, system clock.",
        "",
        "Triggered passages:",
    ]
    for trigger, snippet in hits[:3]:
        lines.append(f"  - `{trigger}` near: ...{snippet}...")
    if len(hits) > 3:
        lines.append(f"  - (+{len(hits) - 3} more)")
    lines.append("")
    lines.append("Augmentation, not block. Revise or tag, then proceed.")

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": "\n".join(lines),
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
