#!/usr/bin/env python3
"""
partner-draft-formalize-gate.py

UserPromptSubmit hook. Detects partner-facing draft intent in the user's
prompt and reminds Claude to save the draft to disk BEFORE producing the
chat output. Length-agnostic: 1-line TG replies belong on disk same as
1500-word emails.

Source primitive: memory/feedback_formalize-replies-to-docs.md
Lapse caught: 2026-05-18 (3+ drafts produced inline this session; Will
asked "where is the tom reply located?" and noted the lapse pattern).
Origin: Will - "the lapse counts for something going forward in order to
reduce future instances."

Companion to:
  - em-dash-augmentation-gate.py (scrubs em-dashes in on-disk drafts)
  - atomic-reflection-gate.py (catches decision-moments before pivot)
"""
import json
import re
import sys


# High-precision partner-draft intent patterns.
# Lean toward over-fire (benign reminder) over under-fire (real lapse).
DRAFT_INTENT_PATTERNS = [
    # Explicit "draft" verb + message-noun
    r"\bdraft\b[^.?!]*\b(reply|response|message|email|post|tweet|comment|memo|dm|note|letter)\b",
    # write/prepare/make + draft-noun
    r"\b(write|prepare|make|give\s+me)\b[^.?!]*\b(reply|response|message|email|draft|post|tweet|memo|letter)\b",
    # reply / respond / response to (someone)
    r"\b(reply|respond|response)\s+to\s+\w+",
    # what should I (say/send/tell/write/reply)
    r"\bwhat\s+(should|do|can|would)\s+(i|we|you)\s+(say|send|tell|write|reply|respond|message)\b",
    # channel + message-noun
    r"\b(linkedin|telegram|tg|twitter|email|medium|ethresearch|discord|substack|x\s*post|tweet)\b[^.?!]{0,50}\b(post|message|reply|response|draft|comment|note)\b",
    # send/DM/ping + name + message-noun
    r"\b(send|dm|message|ping)\s+\w+\b[^.?!]{0,40}\b(message|reply|note|response|draft)\b",
    # write/send back to X
    r"\b(write|send)\s+back\s+to\s+\w+",
    # how do I respond
    r"\bhow\s+(should|do|would|can)\s+(i|we)\s+(say|send|respond|reply|write)\b",
]


def matches_draft_intent(text):
    if not text or not isinstance(text, str):
        return False
    low = text.lower()
    for pat in DRAFT_INTENT_PATTERNS:
        if re.search(pat, low):
            return True
    return False


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return

    event = payload.get("hook_event_name", "")
    if event != "UserPromptSubmit":
        print(json.dumps({}))
        return

    prompt = payload.get("prompt", "")
    if not matches_draft_intent(prompt):
        print(json.dumps({}))
        return

    msg = (
        "[FORMALIZE-DRAFT GATE] Partner-facing draft intent detected in this prompt. "
        "Before producing the draft text in chat, save it to disk first at "
        "`~/Desktop/[recipient]-[topic]-YYYY-MM-DD.md` "
        "(use -v2, -v3 for revisions). Then reference the saved path in your reply. "
        "Per [F·formalize-replies-to-docs]: copy-paste from terminal mangles formatting; "
        "on-disk drafts paste cleanly AND fire the em-dash augmentation gate + other "
        "PreToolUse gates that only compose with on-disk Writes. "
        "Length-agnostic - even 1-line TG replies belong on disk."
    )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": msg,
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
