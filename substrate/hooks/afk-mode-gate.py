#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AFK-mode gate (UserPromptSubmit).

When ~/.claude/state/afk-mode.flag exists, every assistant response must end
with a numbered menu of the top-10 most probable user responses (signature
corpus at memory/_system/afk_signatures/<user>.json) so the user can reply
with a single number from a phone.

Also interprets bare-number prompts: "3" means menu item 3 from the previous
assistant response, and logs the selection for corpus learning.
Per [P·always-equals-gate]: 'with every response' = hook-enforced, not advisory.
"""
import json
import os
import re
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")
FLAG = os.path.join(HOME, ".claude", "state", "afk-mode.flag")
SIG_DIR = os.path.join(HOME, ".claude", "projects", "C--Users-Will", "memory",
                       "_system", "afk_signatures")
USER = "will"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    prompt = payload.get("prompt") or payload.get("user_prompt") or ""
    if not isinstance(prompt, str):
        prompt = ""
    p = prompt.strip().lower()

    # toggle commands work even without the flag present
    if p in ("afk off", "afk mode off"):
        try:
            os.remove(FLAG)
        except OSError:
            pass
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "[AFK MODE] Deactivated. Stop appending menus. Confirm briefly."}}))
        return 0
    if p in ("afk on", "afk mode on", "activate afk mode"):
        os.makedirs(os.path.dirname(FLAG), exist_ok=True)
        with open(FLAG, "w") as f:
            f.write(str(time.time()))

    if not os.path.exists(FLAG):
        print(json.dumps({}))
        return 0

    # bare-number selection?
    sel = re.fullmatch(r"(\d{1,2})", p)
    sel_note = ""
    if sel:
        n = sel.group(1)
        try:
            with open(os.path.join(SIG_DIR, f"{USER}_selections.jsonl"), "a",
                      encoding="utf-8") as f:
                f.write(json.dumps({"t": time.time(), "picked": int(n)}) + "\n")
        except Exception:
            pass
        sel_note = (f"\nUSER PICKED MENU ITEM {n}: execute item {n} from the numbered "
                    "menu at the end of YOUR PREVIOUS response, exactly as written. "
                    "Do not ask for confirmation.")

    sig_rules = ""
    try:
        with open(os.path.join(SIG_DIR, f"{USER}.json"), encoding="utf-8") as f:
            sig = json.load(f)
        if isinstance(sig, dict):
            moves = sig.get("signature_moves")
            if isinstance(moves, list):
                keys = ", ".join(m.get("key", "?") for m in moves if isinstance(m, dict))
                sig_rules = (f"\nSignature-move classes (rank menu using these + live context): {keys}. "
                             f"{sig.get('menu_rules', '')}")
    except Exception:
        pass

    ctx = ("[AFK MODE ACTIVE] End EVERY response with a numbered menu titled 'AFK:' "
           "listing the 10 most probable next replies from this user, derived from "
           "their signature-response corpus and the live decision at hand. Most-likely "
           "first. Each item must be a complete actionable instruction (<= 10 words) "
           "executable when the user replies with just its number."
           + sig_rules + sel_note)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit", "additionalContext": ctx}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
