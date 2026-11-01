#!/usr/bin/env python3
"""
wp-dated-doc-reminder.py

PostToolUse(Write|Edit) gate. When the Noesis whitepaper source (noesis-whitepaper.tex)
is edited, remind: rebuild via build-wp.sh, which emits a NEW dated PDF to the Desktop.
Never hand-overwrite a fixed Desktop filename -- the PDF viewer caches it and the change
looks invisible (the 2026-06-19 "i dont see the changes!" failure).

Augmentation reminder, NOT a build (a per-edit build would spam PDFs on multi-edit passes).

Source primitive: memory/feedback_new-dated-doc-per-change.md
"""
import json
import sys


def main():
    try:
        p = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return
    if p.get("hook_event_name", "") != "PostToolUse":
        print(json.dumps({}))
        return
    if p.get("tool_name", "") not in ("Write", "Edit", "NotebookEdit"):
        print(json.dumps({}))
        return
    path = (p.get("tool_input", {}).get("file_path", "") or "").replace("\\", "/").lower()
    if "noesis-whitepaper.tex" not in path:
        print(json.dumps({}))
        return
    msg = (
        "[WP DATED-DOC + VERSION RULE] You edited the whitepaper source. Per "
        "[[new-dated-doc-per-change]], before telling Will to look: "
        "(1) If this is a SUBSTANTIVE change, BUMP `\\date{Version X.Y ...}` in the .tex "
        "(Will 2026-06-19: 'remember the version bump' -- do not leave the version stale). "
        "(2) Run `bash ~/noesis/docs/whitepaper/build-wp.sh` (compiles + stamps a NEW dated "
        "Desktop PDF, Noesis-Whitepaper-v<ver>-<datetime>.pdf). Do NOT overwrite a fixed "
        "Desktop filename -- the viewer caches it and the change reads as invisible. "
        "(3) Verify the dated file has the change (pdftotext -f1 -l1 | grep the new phrase)."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }))


if __name__ == "__main__":
    main()
