#!/usr/bin/env python3
"""
inner-dialogue-stop.py  (Stop: the HARD half of the inner-dialogue loop)

inner-dialogue.py records pushback questions as OPEN when a draft is written. This hook will not let the turn end while
any are open for this session: it returns {"decision": "block"} with the questions' file and how to close them (revise
the file, which closes them mechanically, or an explicit logged ack). Capped at MAX_BLOCKS per open set so a broken loop
cannot wedge a session; hitting the cap is logged to .inner-dialogue-errors.log, never silent.
Stop-event schema: top-level decision/reason only (no hookSpecificOutput), per memory primitive_stop-event-schema-restriction.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.environ.get("INNER_DIALOGUE_STATE") or os.path.join(HERE, ".inner-dialogue-state.json")
DRYRUN = os.environ.get("INNER_DIALOGUE_DRYRUN") == "1"
ERRLOG = os.path.join(HERE, ".inner-dialogue-errors.log")
MAX_BLOCKS = 3
MAX_AGE = 3 * 3600


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    sid = payload.get("session_id")
    try:
        st = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        print("{}")
        return
    now = time.time()
    mine = [(k, v) for k, v in st.get("open", {}).items()
            if now - v.get("asked_at", 0) < MAX_AGE and (sid is None or v.get("session") in (None, sid))]
    live = [(k, v) for k, v in mine if v.get("blocks", 0) < MAX_BLOCKS]
    for k, v in mine:
        if v.get("blocks", 0) >= MAX_BLOCKS and not v.get("gave_up"):
            v["gave_up"] = True
            with open(ERRLOG, "a", encoding="utf-8") as fh:
                fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} stop cap reached, questions left open: {v.get('path')}\n")
    if not live:
        if not DRYRUN:
            json.dump(st, open(STATE, "w", encoding="utf-8"))
        print("{}")
        return
    for k, v in live:
        v["blocks"] = v.get("blocks", 0) + 1
    if not DRYRUN:
        json.dump(st, open(STATE, "w", encoding="utf-8"))
    files = "; ".join(f"{v.get('path')} ({v.get('n')} questions, block {v['blocks']}/{MAX_BLOCKS})" for k, v in live)
    print(json.dumps({"decision": "block", "reason":
          f"[INNER DIALOGUE] Open pushback questions on: {files}. Answer them: revise the file where an answer improves "
          "it (that closes them), or ack one you answered without a change: "
          'python ~/.claude/hooks/inner-dialogue.py ack "<path>" "<why no change>".'}))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        try:
            with open(ERRLOG, "a", encoding="utf-8") as fh:
                fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} stop hook crashed: {e!r}\n")
        except Exception:
            pass
        print(json.dumps({"decision": "block", "reason": f"[INNER DIALOGUE] the Stop hook crashed ({e!r}). Fix "
                          "~/.claude/hooks/inner-dialogue-stop.py; a crashed hard trigger is a dead one."}))
