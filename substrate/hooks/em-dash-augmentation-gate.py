#!/usr/bin/env python3
"""
em-dash-augmentation-gate.py

When a partner-facing draft is written, scan for em-dashes (U+2014, U+2013).
If present, augment Claude's context with a reminder to scrub them before delivery.

Augmentation gate, NOT a block. Em-dashes remain permitted in memory primitives,
code comments, internal analysis. The gate fires only on partner-facing draft
paths so that conversations-with-humans output gets scrubbed.

Source primitive: memory/feedback_em-dash-filter-for-conversations.md (not bundled
in this public repo; the rule is self-explanatory once you read the hook).

NOTE FOR FORK USERS: add your own partner-name patterns to PARTNER_FACING_PATTERNS
below. The list shipped here is intentionally generic. The hook fires on any path
that looks like a partner-facing draft by SHAPE (file ends in -reply / -draft /
-email / -letter / -pitch / -post / -message / -thread / -dm / -outreach, lives
under Desktop or a similar drafts folder). Add specific names ("/desktop/alice[_-]",
"/desktop/bob[_-]", etc.) if you want the hook to fire on those even when the
shape doesn't match.
"""
import json
import re
import sys


PARTNER_FACING_PATTERNS = [
    # Generic shape patterns. Match any draft whose filename signals it is
    # destined for an external reader.
    r"/desktop/[^/]*[_-]reply[-_.]",
    r"/desktop/[^/]*[_-]draft[-_.]",
    r"/desktop/[^/]*[_-]pitch[-_.]",
    r"/desktop/[^/]*[_-]letter[-_.]",
    r"/desktop/[^/]*[_-]email[-_.]",
    r"/desktop/[^/]*[_-]message[-_.]",
    r"/desktop/[^/]*[_-]post[-_.]",
    r"/desktop/[^/]*[_-]thread[-_.]",
    r"/desktop/[^/]*[_-]dm[-_.]",
    r"/desktop/outreach[_-]",
    r"/desktop/outreach_pitches/",
    # Date-prefixed drafts with platform keywords anywhere after the date.
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*linkedin",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*medium",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*ethresearch",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*email",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*letter",
    # Start-of-name platform shortcuts.
    r"/desktop/ethresearch[_-]",
    r"/desktop/medium[_-]",
    r"/desktop/linkedin[_-]",
    r"/desktop/telegram[_-]",
    # Add your own partner-specific patterns here:
    # r"/desktop/<partner-handle>[_-]",
]


def is_partner_facing(path):
    if not path:
        return False
    norm = path.replace("\\", "/").lower()
    return any(re.search(pat, norm) for pat in PARTNER_FACING_PATTERNS)


def count_em_dashes(content):
    """Count em-dash characters in the content.

    U+2014 is the canonical em-dash. U+2013 (en-dash) is also flagged
    because it gets used as an em-dash substitute and reads the same way
    in partner-facing prose.
    """
    if not content or not isinstance(content, str):
        return 0
    return content.count("—") + content.count("–")


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return

    event = payload.get("hook_event_name", "")
    if event != "PostToolUse":
        print(json.dumps({}))
        return

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit", "NotebookEdit"):
        print(json.dumps({}))
        return

    tool_input = payload.get("tool_input", {})
    path = tool_input.get("file_path", "")

    if not is_partner_facing(path):
        print(json.dumps({}))
        return

    content = ""
    if tool == "Write":
        content = tool_input.get("content", "")
    elif tool == "Edit":
        content = tool_input.get("new_string", "")
    elif tool == "NotebookEdit":
        content = tool_input.get("new_source", "")

    count = count_em_dashes(content)
    if count == 0:
        print(json.dumps({}))
        return

    msg = (
        f"[EM-DASH AUGMENTATION GATE] {count} em-dash(es) detected in "
        f"partner-facing draft at {path}. Partner-facing drafts must filter "
        f"em-dashes before delivery. Replace with comma, period, colon, or "
        f"parens depending on context: mid-clause em-dash -> comma or "
        f"sentence-split; parenthetical em-dash -> parens; range/connection "
        f"em-dash -> 'to'/'vs' or split. Edit the file to scrub before send. "
        f"This gate augments awareness, it does not block the write."
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
