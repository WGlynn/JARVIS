#!/usr/bin/env python3
"""
entity-attribution-gate.py

PreToolUse on Write / Edit. Catches the open-set @<handle> fabrication
failure mode (the @bemarodriguez / @VanillaSugarCookie pattern from
2026-06-09).

When drafted content contains an @<handle> in an attribution context
(adjacent to "comment by", "PR by", "reply", "said", "wrote", etc.)
on a partner-facing or essay-class artifact, surface a verify-then-assert
warning. The writer should resolve the handle via the platform API
(gh api, etc.) rather than assert a plausible-sounding string.

Source spec: 03-anti-hallucination/entity-attribution-gate.md
"""
import json
import re
import sys


# Pattern: an @-handle in an attribution context.
# Capture the handle + surrounding context so the warning can show it.
ATTRIBUTION_CONTEXT_PATTERNS = [
    r"(?:comment(?:ed)? by|PR by|review(?:ed)? by|reply by|said|wrote|posted|authored?(?:\sby)?|opened\sby)\s*[:\-]?\s*@([A-Za-z0-9][A-Za-z0-9\-_]{1,38})\b",
    r"@([A-Za-z0-9][A-Za-z0-9\-_]{1,38})\s+(?:'s|said|wrote|posted|argued|noted|commented)",
    r"by\s+@([A-Za-z0-9][A-Za-z0-9\-_]{1,38})\b",
]

# Handles already in the local entity registry / appear in this conversation's
# verified-context are exempt. The hook can't read conversation state from
# here, so the exemption is implemented as: if the handle appears with a
# nearby explicit URL containing it (github.com/<handle> or twitter.com/<handle>),
# treat as verified.
URL_VERIFICATION_PATTERN = r"(?:github\.com|twitter\.com|x\.com|linkedin\.com/in)/{handle}\b"

WATCHED_PATH_PATTERNS = [
    r"/desktop/[^/]*[_-]reply[-_.]",
    r"/desktop/[^/]*[_-]draft[-_.]",
    r"/desktop/[^/]*[_-]post[-_.]",
    r"/desktop/[^/]*[_-]essay[-_.]",
    r"/desktop/[^/]*[_-]announcement[-_.]",
    r"/memory/(primitive|feedback|project|reference)_[^/]+\.md",
    r"/papers/[^/]+\.md",
    r"/jarvis-monorepo/[0-9]{2}-[^/]+/[^/]+\.md",
    r"/jarvis-monorepo/papers/[^/]+\.md",
    r"/cron-prompts/_advice-contribution-graph",
]


def is_watched(path):
    if not path:
        return False
    norm = path.replace("\\", "/").lower()
    return any(re.search(p, norm) for p in WATCHED_PATH_PATTERNS)


def find_attribution_handles(content):
    """Return list of (handle, context_snippet) for un-URL-verified handles."""
    if not content or not isinstance(content, str):
        return []
    hits = []
    seen = set()
    for pat in ATTRIBUTION_CONTEXT_PATTERNS:
        for m in re.finditer(pat, content, re.IGNORECASE):
            handle = m.group(1)
            if handle.lower() in seen:
                continue
            # Check if there's a URL anchor for this handle anywhere in the content
            url_pat = URL_VERIFICATION_PATTERN.replace("{handle}", re.escape(handle))
            if re.search(url_pat, content, re.IGNORECASE):
                continue
            seen.add(handle.lower())
            start = max(0, m.start() - 50)
            end = min(len(content), m.end() + 50)
            snippet = content[start:end].replace("\n", " ").strip()
            hits.append((handle, snippet))
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

    hits = find_attribution_handles(content)
    if not hits:
        print(json.dumps({}))
        return

    lines = [
        f"[ENTITY-ATTRIBUTION GATE] {len(hits)} unverified @handle attribution(s) "
        f"in {path}. Per the entity-attribution gate ([P·time-logic-anti-hallucination-gate] sibling), "
        f"verify each handle via the platform API (gh api repos/.../pulls/N; gh api graphql; etc.) "
        f"before asserting. The agent confabulated handles twice on 2026-06-09 "
        f"(@bemarodriguez, @VanillaSugarCookie); this gate is the structural fix.",
        "",
        "Unverified handles in attribution context:",
    ]
    for handle, snippet in hits[:5]:
        lines.append(f"  - @{handle} near: ...{snippet}...")
    if len(hits) > 5:
        lines.append(f"  - (+{len(hits) - 5} more)")
    lines.append("")
    lines.append("Augmentation, not block. Verify or mark [author unverified], then proceed.")

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": "\n".join(lines),
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
