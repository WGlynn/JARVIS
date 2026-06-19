#!/usr/bin/env python3
"""
git-commit-landed-gate.py

PostToolUse(Bash) gate. When a Bash command runs `git commit`, check the command
OUTPUT for the success line `[<branch> <hash>]`. If it is absent (and the run is
not a benign no-op), augment context with a loud reminder to VERIFY the commit
landed before claiming committed/pushed.

Catches the exact failure mode of 2026-06-19: a pre-commit hook silently BLOCKED
every commit (changes left STAGED), and a backgrounded `git commit && git push`
chain reported exit 0, so success was relayed unverified. It also fires on ANY
backgrounded commit (output = "running in background", no success line) -- those
genuinely ARE unverified at PostToolUse time and should be checked.

Augmentation gate, NOT a block. The commit still runs; this only reminds.

Source primitive: memory/feedback_verify-commit-landed-never-trust-background-exit.md
Structural enforcer per [P-universal-coverage-hook] / [F-claim-needs-structural-enforcer].
"""
import json
import re
import sys

# A real commit prints e.g. "[master a606ba0] subject" (root commit: "[master (root-commit) ...]").
SUCCESS = re.compile(r"\[[^\]\n]+\s[0-9a-f]{7,}\]")
# Legit no-ops -- not a landed commit, but not a failure worth a loud warning either.
BENIGN = ("nothing to commit", "no changes added to commit", "nothing added to commit")


def stringify(resp):
    if isinstance(resp, str):
        return resp
    try:
        return json.dumps(resp)
    except (TypeError, ValueError):
        return str(resp)


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return

    if payload.get("hook_event_name", "") != "PostToolUse":
        print(json.dumps({}))
        return
    if payload.get("tool_name", "") != "Bash":
        print(json.dumps({}))
        return

    command = payload.get("tool_input", {}).get("command", "") or ""
    if "git commit" not in command:
        print(json.dumps({}))
        return

    out = stringify(payload.get("tool_response", ""))

    # Landed: success line present -> silent. Benign no-op -> silent.
    if SUCCESS.search(out) or any(b in out.lower() for b in BENIGN):
        print(json.dumps({}))
        return

    backgrounded = "running in background" in out.lower()
    why = (
        "the command was backgrounded, so its commit result is NOT in this output"
        if backgrounded
        else "no '[branch hash]' success line appeared -- the commit was likely BLOCKED "
        "by a pre-commit hook (changes left STAGED) or otherwise failed"
    )
    msg = (
        "[GIT-COMMIT-LANDED GATE] A `git commit` ran but did not visibly land: "
        f"{why}. Per [[verify-commit-landed-never-trust-background-exit]], do NOT claim "
        "committed/pushed yet. VERIFY: `git rev-parse HEAD` advanced past the prior commit "
        "AND `git rev-parse origin/<branch>` == HEAD AND the tree is clean. A backgrounded "
        "`&&`-chain exit code is not proof. Read the actual `[branch hash]` and `a..b ref` lines."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }))


if __name__ == "__main__":
    main()
