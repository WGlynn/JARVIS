#!/usr/bin/env python3
"""
Save Session State Trigger Hook
================================

UserPromptSubmit hook. Detects "save session state" phrase in user prompt
and injects an additionalContext system-reminder telling Claude to perform
the full multi-level persistence save:

  - Update vibeswap/.claude/SESSION_STATE.md with current session block header
  - Update vibeswap/.claude/WAL.md with latest tally
  - Capture new memory primitives if any session-substantive patterns emerged
  - Commit + dual-push memory repo (origin + backup)
  - Commit + dual-push vibeswap repo (origin + backup)
  - Commit + dual-push JARVIS repo if any pending
  - Confirm to user with summary

The hook only injects context; the model performs the save. This is
intentional — content writing requires reasoning that scripts cannot do
deterministically.

Spec: see [O·multi-level-persistence-framework] in memory.

Origin: 2026-05-07, Will: "add a hook to do this every time i say save
session state."
"""
import json
import re
import sys


TRIGGER_PATTERNS = [
    r'\bsave\s+session\s+state\b',
    r'\bsave\s+state\b',
    r'\bpersist\s+session\b',
    r'\bsync\s+session\s+state\b',
]

REMINDER_TEMPLATE = """[SAVE-SESSION-STATE TRIGGER FIRED]

The user invoked the save-session-state phrase. Per [O·multi-level-persistence-framework]:

EXECUTE THE FOLLOWING SAVE PROTOCOL:

1. Update `vibeswap/.claude/SESSION_STATE.md` — append a session block header capturing what shipped this session (themes, primitives saved, decisions made, active work pending).

2. Update `vibeswap/.claude/WAL.md` — refresh the latest tally line and append any new what-shipped items.

3. Capture any session-substantive patterns as memory primitives:
   - New patterns observed → primitive_X.md or feedback_X.md
   - Active engagements → project_X.md
   - External contacts → reference_X.md
   - Update MEMORY.md index for each new primitive.

4. Commit + dual-push memory repo:
   ```
   cd ~/.claude/projects/C--Users-Will/memory
   git add <new + modified files>
   git commit -m "memory: <session-summary>"
   git push origin main && git push backup main
   ```

5. Commit + dual-push vibeswap repo:
   ```
   cd ~/vibeswap
   git add .claude/SESSION_STATE.md .claude/WAL.md
   git commit -m "state: <session-summary>"
   git push origin master && git push backup master
   ```

6. If any JARVIS work pending:
   ```
   cd ~/JARVIS
   git status --short
   # commit + dual-push if anything pending
   ```

7. Verify all pushes succeeded (look for "To https://github.com/..." lines in output).

8. Report to user with summary: tally of commits dual-pushed, any unsaved items still pending, current state of multi-level hierarchy (which levels hold the latest state).

NOTE: this is the HARMONIC save invoking ALL existing persistence primitives.
Do NOT reinvent. Use:
  - `[P·anti-amnesia-protocol]` — WAL discipline
  - `[P·api-death-shield]` — crash protection (already firing on Stop/PreCompact)
  - `[F·atomic-commit-pacing]` — one logical change per commit
  - `[R·backup-remote-pattern]` — dual-push origin AND backup
  - `[F·session-state-commit-gate]` — no push without state update
  - `[P·hiero-no-prose-in-memory]` — operator-density on any new primitive
"""


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    prompt = data.get("user_prompt") or data.get("prompt") or ""
    if not isinstance(prompt, str):
        return 0

    if not any(re.search(pat, prompt, re.IGNORECASE) for pat in TRIGGER_PATTERNS):
        return 0

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER_TEMPLATE,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
