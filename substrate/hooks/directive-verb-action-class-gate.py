#!/usr/bin/env python3
"""
directive-verb-action-class-gate.py

PreToolUse on Write / Edit. Eliminates the failure CLASS of "agent ships
essay/prose when user-directive requires implementation/mechanism."

The agent does not detect this failure case-by-case anymore. The gate
fires structurally on every Write into an essay-class path AFTER an
implementation-class directive, and surfaces a structural-honesty
warning that the writer is producing description when they should be
producing mechanism.

Applies the eliminate-the-class-not-the-instance principle from
[P·class-dissolution-vs-case-defeat] and [P·cybersec-self-elimination-purpose]
to the agent's own failure modes.

Source primitive: memory/feedback_work-on-layer-means-implementation-not-essay.md
"""
import json
import os
import re
import sys


# Verbs that indicate implementation/mechanism work. When the most recent
# user message contains one of these, ship-code is the default.
IMPLEMENTATION_VERBS = [
    r"\bwork on\b",
    r"\b(implement|wire|hook|gate|build|ship|fix|patch|deploy)\b",
    r"\b(deep(en|ness)?|depth)\b",
    r"\b(improve|enhance|harden|strengthen|tighten)\b",
    r"\bmake (it|that|this|things|x|y) (better|stronger|fail|fire|work)\b",
    r"\b(add|create|introduce) (a |the )?(hook|gate|primitive|mechanism|rule)\b",
    r"\b(sync|merge|consolidate|unify|migrate)\b",
    r"\beliminate\b",
    r"\bclass[- ]elimination\b",
    r"\bsubstrate work\b",
]

# Verbs that indicate documentation/description work. When the most recent
# user message contains one of these, essay-creation is the default.
DOCUMENTATION_VERBS = [
    r"\b(document|describe|explain|write (about|a paper|an essay|a post))\b",
    r"\b(announce|publish|share|post)\b",
    r"\b(blog|medium|essay|paper)\b",
    r"\b(summarize|recap|overview)\b",
    r"\bwrite (it )?up\b",
]

# File-path patterns that ARE essay/documentation artifacts. Writes to these
# paths AFTER an implementation-directive are the class-elimination target.
ESSAY_PATH_PATTERNS = [
    r"/jarvis-monorepo/[0-9]{2}-[^/]+/[^/]+\.md$",   # layer essays
    r"/jarvis-monorepo/papers/[^/]+\.md$",            # papers
    r"/desktop/[^/]*medium[-_]",                       # Medium drafts
    r"/desktop/[^/]*paper[-_.]",                       # paper drafts
    r"/desktop/[^/]*essay[-_.]",                       # essay drafts
    r"/jarvis-monorepo/[^/]+\.md$",                    # root-level monorepo docs
]

# File-path patterns that ARE implementation artifacts. Writes here count
# as ship-code, not essay-creation.
IMPLEMENTATION_PATH_PATTERNS = [
    r"\.py$",
    r"\.sol$",
    r"\.ts$",
    r"\.tsx$",
    r"\.js$",
    r"\.jsx$",
    r"\.rs$",
    r"\.toml$",
    r"settings\.json$",
    r"/hooks/[^/]+",
    r"/scripts/[^/]+",
    r"/memory/(primitive|feedback|project|reference)_[^/]+\.md$",  # primitives ARE mechanisms
    r"/cron-prompts/[^/]+",
]


def classify_directive(text):
    """Return 'implementation', 'documentation', or 'ambiguous'."""
    if not text:
        return "ambiguous"
    text = text.lower()
    impl = any(re.search(p, text, re.IGNORECASE) for p in IMPLEMENTATION_VERBS)
    docs = any(re.search(p, text, re.IGNORECASE) for p in DOCUMENTATION_VERBS)
    if impl and not docs:
        return "implementation"
    if docs and not impl:
        return "documentation"
    return "ambiguous"


def classify_target(path):
    """Return 'essay', 'implementation', or 'other'."""
    if not path:
        return "other"
    norm = path.replace("\\", "/").lower()
    if any(re.search(p, norm) for p in IMPLEMENTATION_PATH_PATTERNS):
        return "implementation"
    if any(re.search(p, norm) for p in ESSAY_PATH_PATTERNS):
        return "essay"
    return "other"


def read_last_user_message():
    """Best-effort: read the last user prompt from the transcript file.

    Claude Code writes a transcript per session. The path is provided in
    the hook payload under `transcript_path`. We tail the file for the
    most recent user-turn content.
    """
    # Defer to the hook payload (passed in by main()); this helper is
    # called with the path string after the payload is parsed.
    return ""


def find_recent_directive(transcript_path):
    if not transcript_path or not os.path.exists(transcript_path):
        return ""
    try:
        with open(transcript_path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except (OSError, UnicodeDecodeError):
        return ""
    # The transcript is JSONL. Walk backward for the most recent user message.
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "user":
            content = obj.get("message", {}).get("content", "")
            if isinstance(content, list):
                # Aggregate text blocks
                parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", ""))
                return " ".join(parts)
            if isinstance(content, str):
                return content
    return ""


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
    if tool not in ("Write", "Edit"):
        print(json.dumps({}))
        return

    tool_input = payload.get("tool_input", {})
    path = tool_input.get("file_path", "")
    target_class = classify_target(path)

    # Only fire on writes to essay-class paths. Implementation-class writes
    # are always fine; "other" paths are not in scope.
    if target_class != "essay":
        print(json.dumps({}))
        return

    transcript_path = payload.get("transcript_path", "")
    directive = find_recent_directive(transcript_path)
    directive_class = classify_directive(directive)

    if directive_class != "implementation":
        print(json.dumps({}))
        return

    # Implementation-class directive, essay-class target. The class-elimination
    # trigger. Surface a structural warning.
    excerpt = directive.replace("\n", " ").strip()[:200]
    msg = (
        f"[DIRECTIVE-VERB GATE] You are about to Write/Edit an essay-class "
        f"artifact ({path}), but the most recent user directive reads as "
        f"implementation-class: \"{excerpt}\". This is the failure CLASS "
        f"that [F·work-on-layer-means-implementation-not-essay] eliminates. "
        f"Per [P·class-dissolution-vs-case-defeat], do not write a description "
        f"of the mechanism; ship the mechanism. Acceptable implementation-class "
        f"artifacts: hooks under hooks/, primitives under memory/, cron-prompts/, "
        f"scripts/, .py/.sol/.ts files. If this essay write is genuinely required "
        f"alongside the implementation (e.g., README index update after a hook "
        f"shipped), proceed; if it is the agent defaulting to prose, STOP and "
        f"ship code first."
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": msg,
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
