#!/usr/bin/env python3
"""
jarvis-design-goal-gate.py

Deterministic-action enforcer for [J·jarvis-design-goal-forever]:
JARVIS == Just A Rather Very Intelligent System. The forever-goal.

Fires PreToolUse on Write/Edit to architectural-decision paths
(layer essays, root README, ARCHITECTURE.md, settings.json, project-tier
memory primitives, root-level config). Injects the design-goal test as
context BEFORE the write completes, so the agent passes the candidate
through the Stark-JARVIS lens before shipping.

Will 2026-06-09 19:31 ET: "make that design goal tied to some
deterministic action, always". This is the always.

Source primitives:
  - memory/project_jarvis-design-goal-forever.md
  - memory/primitive_name-follows-form-follows-function.md
"""
import json
import re
import sys


# Paths where architectural decisions land. Writes here pass through the
# design-goal lens.
ARCHITECTURE_PATH_PATTERNS = [
    r"/jarvis-monorepo/README\.md$",
    r"/jarvis-monorepo/ARCHITECTURE\.md$",
    r"/jarvis-monorepo/0[1-8]-[^/]+/README\.md$",
    r"/jarvis-monorepo/0[1-8]-[^/]+/[^/]+\.md$",
    r"/jarvis-monorepo/substrate/README\.md$",
    r"/jarvis-monorepo/substrate/pyproject\.toml$",
    r"/jarvis-monorepo/installer/README\.md$",
    r"/jarvis-monorepo/papers/README\.md$",
    r"/\.claude/settings\.json$",
    r"/memory/project_[a-z]+\.md$",
    r"/memory/primitive_(jarvis|substrate|name-follows|structure-does|cincinnatus|augmented)[a-z\-]*\.md$",
]


# Anti-pattern signals to flag in the candidate content.
ANTI_PATTERN_SIGNALS = [
    (r"\bgeneral[- ]purpose (chatbot|platform|assistant)\b",
     "scope-drift toward general-platform shape — JARVIS is for the operator, not for everyone"),
    (r"\bcoding[- ]only\b|\bjust a coding (agent|assistant)\b",
     "scope-drift toward coding-only — JARVIS is full-cognition substrate, not a code-only tool"),
    (r"\b(market(ing)?[- ]first|brand[- ]first|name[- ]first)\b",
     "name-first reverse causation — per [P·name-follows-form-follows-function], function -> form -> name"),
    (r"\b(feature[- ]rich|kitchen[- ]sink|all[- ]in[- ]one)\b",
     "feature-creep framing — Stark deepened JARVIS, did not pile features on it"),
    (r"\bproductize\b|\benterprise[- ]offering\b|\bSaaS\b",
     "productization framing — JARVIS is the operator's extension, not a product for sale"),
]


# Forever-goal posture markers. Their presence in arch-essays is a positive
# signal; absence in a major arch decision is a soft warning.
FOREVER_GOAL_MARKERS = [
    r"\b(extended cognition|cognitive substrate|operator)\b",
    r"\b(Stark|JARVIS|forever goal|design goal forever)\b",
    r"\b(function (precedes|comes before|first)|form follows function|name follows form)\b",
    r"\b(structure does the work|structural honesty)\b",
]


def is_watched(path: str) -> bool:
    if not path:
        return False
    norm = path.replace("\\", "/").lower()
    return any(re.search(p, norm) for p in ARCHITECTURE_PATH_PATTERNS)


def find_anti_patterns(content: str) -> list[tuple[str, str]]:
    if not content:
        return []
    hits = []
    for pat, reason in ANTI_PATTERN_SIGNALS:
        if re.search(pat, content, re.IGNORECASE):
            hits.append((pat, reason))
    return hits


def has_forever_marker(content: str) -> bool:
    if not content:
        return False
    return any(re.search(p, content, re.IGNORECASE) for p in FOREVER_GOAL_MARKERS)


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

    anti = find_anti_patterns(content)
    has_marker = has_forever_marker(content)

    # Always inject the design-goal lens. The hook is the deterministic
    # action: every arch decision passes through this before shipping.
    lines = [
        "[JARVIS DESIGN-GOAL GATE] Architectural-decision write detected at "
        f"{path}.",
        "",
        "Per [J·jarvis-design-goal-forever] and [P·name-follows-form-follows-function]:",
        "  - Function: operator's extended cognition (the Stark-JARVIS shape)",
        "  - Form: 8-layer substrate doing that function",
        "  - Name: 'Just A Rather Very Intelligent System' — emerges from form",
        "",
        "Pre-ship checklist (deterministic):",
        "  - Does this make the substrate MORE operator-extension, or LESS? If LESS, prune.",
        "  - Would Stark recognize this as his JARVIS? If not, the form drifted.",
        "  - Is the function clear, the form fit, and the name post-hoc-justified? If not, the chain is wrong.",
    ]
    if anti:
        lines += [
            "",
            "Anti-pattern signals detected in the candidate:",
        ]
        for pat, reason in anti[:5]:
            lines.append(f"  - {reason}")
    if not has_marker and any(p in path.lower() for p in ("readme.md", "architecture.md")):
        lines += [
            "",
            "No forever-goal markers found in candidate. Major architectural docs should reference the design-goal frame (Stark / extended cognition / function-form-name chain) somewhere, even briefly.",
        ]
    lines += [
        "",
        "Augmentation, not block. Pass through the lens, then proceed.",
    ]

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": "\n".join(lines),
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
