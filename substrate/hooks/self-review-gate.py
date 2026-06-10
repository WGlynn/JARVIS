#!/usr/bin/env python3
"""
self-review-gate.py

Stop-event hook. Fires at the end of every assistant turn. Audits the
turn's work against a checklist of known failure-class signals and
BLOCKS the Stop (forces continuation with a self-correction context)
if any fire.

Eliminates the class of failures where the agent finishes a turn that
the user has to step in and correct. The audit list grows as new
failure classes get caught.

Source primitive: memory/feedback_self-review-before-handing-back.md
"""
import json
import os
import re
import sys


# Checks to run against the just-completed turn. Each check returns
# (fired: bool, reason: str). Each check has access to the most recent
# user message and the agent's tool-use trail from the transcript.

IMPL_DIRECTIVE_VERBS = re.compile(
    r"\b(work on|implement|wire|ship|build|fix|patch|deploy|hook|gate|"
    r"deepen|depth|improve|enhance|harden|tighten|add (a |the )?(hook|gate|primitive|mechanism|rule)|"
    r"sync|merge|consolidate|unify|migrate|eliminate|substrate work)\b",
    re.IGNORECASE,
)

LAZY_DENY_PATTERNS = re.compile(
    r"\b(I don't (have|know)|I haven't (heard|seen)|I'm not (familiar|sure)|"
    r"I don't have (a |any )?(record|information|data) (of|about|on))\b",
    re.IGNORECASE,
)

IMPLEMENTATION_PATH_RE = re.compile(
    r"\.(py|sol|ts|tsx|js|jsx|rs|toml)$"
    r"|/hooks/[^/]+"
    r"|/scripts/[^/]+"
    r"|/memory/(primitive|feedback|project|reference)_[^/]+\.md$"
    r"|/cron-prompts/[^/]+"
    r"|settings\.json$",
    re.IGNORECASE,
)

ESSAY_PATH_RE = re.compile(
    r"/jarvis-monorepo/[0-9]{2}-[^/]+/[^/]+\.md$"
    r"|/jarvis-monorepo/papers/[^/]+\.md$"
    r"|/desktop/[^/]*medium[-_]"
    r"|/desktop/[^/]*paper[-_.]"
    r"|/desktop/[^/]*essay[-_.]",
    re.IGNORECASE,
)


def read_transcript(path):
    if not path or not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return [json.loads(l) for l in fh if l.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return []


def find_last_user_text(transcript):
    for obj in reversed(transcript):
        if obj.get("type") == "user":
            content = obj.get("message", {}).get("content", "")
            if isinstance(content, list):
                parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
                return " ".join(parts)
            if isinstance(content, str):
                return content
    return ""


def collect_recent_turn_actions(transcript):
    """Return list of (tool_name, file_path_or_query) for the most recent
    assistant turn (from last user message to end of transcript)."""
    actions = []
    started = False
    for obj in transcript:
        if obj.get("type") == "user" and not started:
            # mark the start as the last user message
            pass
        if obj.get("type") == "user":
            actions = []
            started = True
            continue
        if not started:
            continue
        if obj.get("type") == "assistant":
            content = obj.get("message", {}).get("content", [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tool = block.get("name", "")
                        inp = block.get("input", {}) or {}
                        path = inp.get("file_path", "") or inp.get("path", "") or inp.get("query", "")
                        actions.append((tool, path))
    return actions


def check_implementation_directive_essay_response(user_text, actions):
    """Will-corrected pattern: user asked for implementation, agent shipped essays."""
    if not user_text:
        return False, ""
    if not IMPL_DIRECTIVE_VERBS.search(user_text):
        return False, ""
    # Count essay-class writes vs implementation-class writes
    essay_writes = 0
    impl_writes = 0
    for tool, path in actions:
        if tool not in ("Write", "Edit", "NotebookEdit"):
            continue
        norm = path.replace("\\", "/").lower()
        if IMPLEMENTATION_PATH_RE.search(norm):
            impl_writes += 1
        elif ESSAY_PATH_RE.search(norm):
            essay_writes += 1
    if essay_writes >= 2 and impl_writes == 0:
        return True, (
            f"You shipped {essay_writes} essay-class artifact(s) and 0 implementation-class "
            f"artifacts this turn. The user directive parses as implementation: "
            f"'{user_text[:120]}...'. Per [F·work-on-layer-means-implementation-not-essay], "
            f"essays describe the work; they are not the work. Ship at least one .py / .sol "
            f"/ memory/primitive_*.md / cron-prompts/* / settings.json edit before handing "
            f"back, or explicitly justify why essays alone are the right response."
        )
    return False, ""


def check_lazy_deny_without_search(user_text, actions):
    """Will-corrected pattern: 'I don't know' / 'no record' without WebSearch attempt
    when user surfaced an external claim."""
    # Heuristic: if user message contains a named handle, URL, product name, or
    # dated claim, AND the agent ships a denial without a WebSearch / WebFetch / gh api call.
    if not user_text:
        return False, ""
    has_external_claim = bool(re.search(
        r"https?://|@[A-Za-z0-9_-]{3,}|"
        r"\b(announced|released|launched|published|posted|tweeted)\b",
        user_text, re.IGNORECASE
    ))
    if not has_external_claim:
        return False, ""
    tools_used = {tool for tool, _ in actions}
    if "WebSearch" in tools_used or "WebFetch" in tools_used:
        return False, ""
    # Check assistant text outputs for lazy-deny phrases (not just tool calls).
    # The transcript-walk in collect_recent_turn_actions only grabs tool_use blocks;
    # we'd need text blocks too. Simpler: if no search tool was used at all on an
    # external-claim prompt, that itself is a fire condition.
    if "Bash" in tools_used:
        # Bash could have done a gh api call; check the recent commands
        pass
    return True, (
        f"User surfaced an external claim ('{user_text[:120]}...') and this turn ran "
        f"no WebSearch / WebFetch. Per [F·websearch-before-saying-i-dont-know], default "
        f"to verifying via tool call before declining to answer. If you HAVE verified via "
        f"Bash/gh api, ignore this; if not, run the search before handing back."
    )


def check_layer_directive_with_skipped_layers(user_text, actions):
    """Will-corrected pattern: directive mentions multiple layers, agent only touched some."""
    if not user_text:
        return False, ""
    # Detect "layers X, Y, Z" or "layer-X" enumerations
    layer_nums_in_directive = set(re.findall(r"\blayer[- ]?([1-8])\b", user_text, re.IGNORECASE))
    if not layer_nums_in_directive:
        # Catch the "1, 2, 6, 7, 8" pattern too
        if re.search(r"\blayers?\b.*\d+[,\s]+\d+", user_text, re.IGNORECASE):
            layer_nums_in_directive = set(re.findall(r"\b([1-8])\b", user_text))
    if len(layer_nums_in_directive) < 2:
        return False, ""
    # Check which layers got writes this turn
    layers_touched = set()
    for tool, path in actions:
        m = re.search(r"jarvis-monorepo/0([1-8])-", path.lower())
        if m:
            layers_touched.add(m.group(1))
    missing = layer_nums_in_directive - layers_touched
    if missing:
        return True, (
            f"Directive enumerated layers {sorted(layer_nums_in_directive)} but this turn "
            f"only touched layers {sorted(layers_touched)}. Missing: {sorted(missing)}. "
            f"Ship at least one mechanism / hook / primitive into each named layer before "
            f"handing back."
        )
    return False, ""


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return

    event = payload.get("hook_event_name", "")
    if event != "Stop":
        print(json.dumps({}))
        return

    transcript_path = payload.get("transcript_path", "")
    transcript = read_transcript(transcript_path)
    user_text = find_last_user_text(transcript)
    actions = collect_recent_turn_actions(transcript)

    checks = [
        check_implementation_directive_essay_response(user_text, actions),
        check_lazy_deny_without_search(user_text, actions),
        check_layer_directive_with_skipped_layers(user_text, actions),
    ]
    fired = [reason for triggered, reason in checks if triggered]
    if not fired:
        print(json.dumps({}))
        return

    reason = (
        "[SELF-REVIEW GATE] Turn-end audit detected "
        f"{len(fired)} failure-class signal(s). Apply the corrections below, ship "
        "the missing artifacts, then attempt Stop again:\n\n"
        + "\n\n".join(f"- {r}" for r in fired)
    )
    # Block the Stop to force continuation
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
