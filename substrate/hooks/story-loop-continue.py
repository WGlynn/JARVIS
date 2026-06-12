#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story Mode autonomous-loop driver (Stop hook).

When ~/.claude/state/story-loop.json is active with remaining > 0, blocks the
Stop event and instructs the agent to self-select the highest-WWWD-confidence
item from its last menu and execute it -- self-play autopilot. Decrements each
fire; the counter is the hard backstop. Fail-safe: no file or remaining<=0 =>
silent normal stop. See [P.story-mode-autonomous-loop].

Per [P.stop-event-schema-restriction]: emit ONLY top-level {decision, reason}
to continue, or {} to stop. NEVER hookSpecificOutput.additionalContext.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STATE = os.path.join(os.path.expanduser("~"), ".claude", "state", "story-loop.json")

GUARD = (
    "LOOP MODE -- {n} iteration(s) remain after this one. Self-play: from the numbered "
    "menu at the end of your LAST response, pick the SINGLE highest-WWWD-confidence item "
    "(the one Will would most likely choose) and execute it now, then end with a fresh menu. "
    "GUARDRAILS -- STOP the loop and hand back to Will (delete the loop file, say 'loop "
    "complete', do NOT continue) if ANY hold: (a) no item is a clear favorite / the fork is "
    "ambiguous; (b) the top item crosses an irreversible or outward-facing line (send, publish, "
    "deploy, delete, push-to-public, message a person); (c) you would repeat the previous turn "
    "(delta must be > 0)."
)


def main() -> int:
    try:
        st = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        print(json.dumps({}))            # fail-safe: no loop => normal stop
        return 0
    rem = int(st.get("remaining", 0))
    if rem <= 0:
        try:
            os.remove(STATE)
        except OSError:
            pass
        print(json.dumps({}))
        return 0
    st["remaining"] = rem - 1
    try:
        json.dump(st, open(STATE, "w", encoding="utf-8"))
    except Exception:
        pass
    print(json.dumps({"decision": "block", "reason": GUARD.format(n=rem - 1)}))
    return 0


if __name__ == "__main__":
    main()
