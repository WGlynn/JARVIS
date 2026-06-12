#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story Mode gate (UserPromptSubmit).

When ~/.claude/state/story-mode.flag exists, every assistant response must end
with a numbered menu of the top-10 most probable user responses (signature
corpus at memory/_system/story_signatures/<user>.json) so the user can reply
with a single number -- or chain several ("5,4,1") -- from a phone.

Story Mode = gamified vibe coding: the original choose-your-own-adventure game
loop, on an LLM. (Formerly "AFK mode"; renamed 2026-06-12, old aliases kept.)

Interprets bare-number prompts: "3" runs menu item 3 from the previous assistant
response; "5,4,1" runs items 5,4,1 in order; every turn is logged for corpus
learning. Per [P.always-equals-gate]: 'with every response' = hook-enforced.
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
FLAG = os.path.join(HOME, ".claude", "state", "story-mode.flag")
SIG_DIR = os.path.join(HOME, ".claude", "projects", "C--Users-Will", "memory",
                       "_system", "story_signatures")
USER = os.environ.get("STORY_USER") or os.environ.get("AFK_USER", "will")

ON_CMDS = ("story on", "story mode on", "activate story mode",
           "afk on", "afk mode on", "activate afk mode")
OFF_CMDS = ("story off", "story mode off", "afk off", "afk mode off")


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
    if p in OFF_CMDS:
        try:
            os.remove(FLAG)
        except OSError:
            pass
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "[STORY MODE] Deactivated. Stop appending menus. Confirm briefly."}}))
        return 0
    if p in ON_CMDS:
        os.makedirs(os.path.dirname(FLAG), exist_ok=True)
        with open(FLAG, "w") as f:
            f.write(str(time.time()))

    # story loop N  /  story loop off  -- arm/disarm the autonomous self-play loop
    lm = re.fullmatch(r"story\s+loop\s+(off|\d{1,2})", p)
    if lm:
        LOOP = os.path.join(HOME, ".claude", "state", "story-loop.json")
        arg = lm.group(1)
        if arg == "off":
            try:
                os.remove(LOOP)
            except OSError:
                pass
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                "additionalContext": "[STORY MODE] Loop disarmed. Back to manual picks."}}))
            return 0
        n = max(1, min(int(arg), 20))  # hard cap 20 iterations
        os.makedirs(os.path.dirname(FLAG), exist_ok=True)
        with open(FLAG, "w") as f:
            f.write(str(time.time()))   # loop implies Story Mode on
        with open(LOOP, "w", encoding="utf-8") as f:
            json.dump({"remaining": n}, f)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
            "additionalContext": (f"[STORY MODE] Autonomous loop ARMED for {n} iterations. At each "
            "turn's end, self-select the single highest-WWWD-confidence menu item and execute it "
            "(self-play autopilot). GUARDRAILS: stop + hand back on an ambiguous fork, an "
            "irreversible/outward-facing action (send/publish/deploy/delete/push/message), or a "
            "repeat. 'story loop off' disarms. Begin now: do the work the top item of your last "
            "menu implies, then show a fresh menu.")}}))
        return 0

    if not os.path.exists(FLAG):
        print(json.dumps({}))
        return 0

    # ---- selection + impression logging (catch-rate / recall@10) ----
    # A pick is a single number OR a comma/space list, each in 1..10 ("5,4,1").
    # Every Story-Mode-active, non-toggle turn is ONE menu impression; classifying
    # it pick-vs-off-menu gives the denominator catch-rate needs.
    picks = []
    mm = re.fullmatch(r"\s*(\d{1,2}(?:\s*[, ]\s*\d{1,2})*)\s*", p)
    if mm:
        cand = [int(x) for x in re.findall(r"\d{1,2}", mm.group(1))]
        if cand and all(1 <= x <= 10 for x in cand):
            picks = cand

    is_toggle = p in ON_CMDS
    sel_note = ""
    if not is_toggle:
        kind = "pick" if picks else "off_menu"
        try:
            with open(os.path.join(SIG_DIR, f"{USER}_impressions.jsonl"), "a",
                      encoding="utf-8") as f:
                f.write(json.dumps({"t": time.time(), "kind": kind, "picked": picks}) + "\n")
        except Exception:
            pass
        if picks:
            # legacy per-pick log the reweighter consumes for precision@3
            try:
                with open(os.path.join(SIG_DIR, f"{USER}_selections.jsonl"), "a",
                          encoding="utf-8") as f:
                    for x in picks:
                        f.write(json.dumps({"t": time.time(), "picked": x}) + "\n")
            except Exception:
                pass
            items = ", ".join(str(x) for x in picks)
            sel_note = (f"\nUSER PICKED MENU ITEM(S) {items}: execute item(s) {items} from the "
                        "numbered menu at the end of YOUR PREVIOUS response, in order, exactly "
                        "as written. Do not ask for confirmation.")

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

    ctx = ("[STORY MODE ACTIVE] End EVERY response with a numbered menu. Title it EXACTLY "
           "'Story Mode -- reply with a number, or chain several in order (e.g. `3` or `5,4,1`):' "
           "so the multi-select affordance is ALWAYS visible -- a first-time user must see "
           "they can pick more than one. List the 10 most probable next replies from this "
           "user, derived from their signature-response corpus and the live decision at hand. "
           "Most-likely first. Each item must be a complete actionable instruction (<= 10 "
           "words) executable when the user replies with just its number(s). LOOP-SUGGESTION: "
           "when the next several moves are high-confidence, low-risk, and same-thread, include "
           "ONE item offering to run them as an autonomous loop (e.g. 'Loop the next N "
           "autonomously') -- the user arms it by replying 'story loop N'."
           + sig_rules + sel_note)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit", "additionalContext": ctx}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
