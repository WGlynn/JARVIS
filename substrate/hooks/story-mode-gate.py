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

# Wind-down signals: when the user is CLEARLY done for the session (or done with
# Story Mode), appending another menu is redundant and tone-deaf at a sign-off.
# Per Will 2026-06-17: exit Story Mode on these; the post-wind-down menu is OPT-IN
# (resume requires an explicit "story on"). Substring match on the lowercased prompt,
# biased toward suppression -- a missed menu costs nothing; a sign-off menu annoys.
WIND_DOWN = (
    "wind down", "winding down", "wind it down", "wind things down",
    "stop here", "stop for now", "stop for the", "lets stop", "let's stop",
    "ok stop", "okay stop", "stop story", "exit story", "end story", "kill story",
    "handoff", "hand off", "hand it off", "hand things off",
    "going to bed", "go to bed", "off to bed", "going to sleep", "im going to sleep",
    "head to bed", "heading to bed", "gonna sleep", "gonna crash", "im crashing",
    "goodnight", "good night", "gnight", "g'night", "night night",
    "call it a night", "call it here", "call it for", "calling it", "call it a day",
    "wrap up", "wrap it up", "wrapping up", "lets wrap", "let's wrap",
    "done for the", "im done for", "thats it for", "that's it for",
    "thats all for", "that's all for", "im done here", "we're done", "were done",
    "signing off", "sign off", "log off", "logging off",
    "im out", "i'm out", "heading out", "im heading out",
    "see you tomorrow", "see you in the morning", "talk tomorrow", "ttyl",
    "no menu", "no more menu", "skip the menu", "drop the menu", "stop the menu",
)


def is_wind_down(p: str) -> bool:
    """True if the prompt clearly signals the user is done (session or Story Mode).
    Phrase match for multi-word signals + whole-message match for bare 'stop'/'done'
    (which are too common to substring-match safely)."""
    if any(s in p for s in WIND_DOWN):
        return True
    bare = p.strip().strip(".!").strip()
    return bare in ("stop", "done", "im done", "i'm done", "that's all", "thats all",
                    "wind down", "thats it", "that's it", "enough", "k done")


def last_menu_lettered(tp: str) -> bool:
    """True if the previous assistant turn rendered the Story Mode menu with
    letter keys (a-j). Collision-resistance-by-construction (Will's ECDSA frame):
    when a content list and the menu coexist, the menu lives in the LETTER
    keyspace and content in the NUMBER keyspace -- disjoint alphabets, so a bare
    token decodes to exactly one namespace. This check is the parse-side recovery
    for the rare case the render side forgot to switch."""
    if not tp or not os.path.exists(tp):
        return False
    try:
        with open(tp, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 300_000))
            chunk = f.read().decode("utf-8", "replace")
        last_text = None
        for line in reversed(chunk.splitlines()):
            if '"assistant"' not in line:
                continue
            try:
                j = json.loads(line)
            except Exception:
                continue
            if j.get("type") != "assistant":
                continue
            c = (j.get("message") or {}).get("content")
            text = ""
            if isinstance(c, str):
                text = c
            elif isinstance(c, list):
                for part in c:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text += part.get("text", "")
            if text.strip():
                last_text = text
                break
        if not last_text:
            return False
        idx = last_text.find("Story Mode -- reply")
        if idx < 0:
            return False
        tail = last_text[idx:]
        return bool(re.search(r"(?m)^\s*\*{0,2}[a-j][).]\s", tail))
    except Exception:
        return False


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
    tp = payload.get("transcript_path") or ""

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

    # ---- wind-down exit (Will 2026-06-17) ----
    # The user is CLEARLY done for the session / done with Story Mode. Appending
    # another menu here is redundant and tone-deaf at a sign-off. Deactivate Story
    # Mode and tell the model NOT to render a menu this turn. Resume is OPT-IN: the
    # menu only comes back when the user explicitly re-enables ("story on"). Guard:
    # never fire on a bare menu pick (a numeric/letter selection is engagement, not
    # a wind-down), so the model still cleanly handles a picked terminal item.
    is_pick_token = bool(re.fullmatch(r"\s*([a-jA-J]|\d{1,2})(\s*[, ]\s*([a-jA-J]|\d{1,2}))*\s*", raw_lower := prompt.strip())) and len(prompt.strip()) <= 24
    if is_wind_down(p) and not is_pick_token:
        try:
            os.remove(FLAG)
        except OSError:
            pass
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "[STORY MODE] The user is winding down -- do NOT append a menu this turn. "
                "Respond naturally and close out. Story Mode is now OFF; it resumes only when "
                "the user opts back in (\"story on\"). Do not mention this gate unless asked.")}}))
        return 0

    # ---- selection + impression logging (catch-rate / recall@10) ----
    # A pick is a single number OR a comma/space list, each in 1..10 ("5,4,1").
    # Every Story-Mode-active, non-toggle turn is ONE menu impression; classifying
    # it pick-vs-off-menu gives the denominator catch-rate needs.
    picks = []
    pick_letters = False
    content_pick = False  # a bare number that belongs to a content list, not the menu
    raw = prompt.strip()
    # Letter keyspace (a-j) = menu picks in list-isolation mode. Disjoint from the
    # number keyspace by construction, so the two never collide (Will's ECDSA frame).
    lm2 = re.fullmatch(r"([a-jA-J](?:\s*[, ]\s*[a-jA-J])*)", raw)
    if lm2 and len(raw) <= 24:
        letters = [c.lower() for c in re.findall(r"[a-jA-J]", lm2.group(1))]
        picks = [ord(c) - 96 for c in letters]
        pick_letters = True
    else:
        mm = re.fullmatch(r"\s*(\d{1,2}(?:\s*[, ]\s*\d{1,2})*)\s*", p)
        if mm:
            cand = [int(x) for x in re.findall(r"\d{1,2}", mm.group(1))]
            if cand and all(1 <= x <= 10 for x in cand):
                # COLLISION GUARD: if the last menu was lettered, bare numbers are a
                # content-list selection -- hand them to the model, don't hijack as picks.
                if last_menu_lettered(tp):
                    content_pick = True
                else:
                    picks = cand

    # Inline modifier: "N: <instruction>" (also N. / N -) runs a SINGLE item with a
    # short tweak, e.g. "3: only the auth part" or "3 - use sonnet". Case-preserved
    # from the raw prompt. Only fires when the bare-number parse above didn't match.
    modifier = ""
    if not picks:
        mod_m = re.match(r"\s*(\d{1,2})\s*[:.\-]\s+(.+)", prompt.strip(), re.DOTALL)
        if mod_m and 1 <= int(mod_m.group(1)) <= 10:
            picks = [int(mod_m.group(1))]
            modifier = mod_m.group(2).strip()

    is_toggle = p in ON_CMDS
    # Cron-injection guard: a prompt that begins "type: <marker>" is an autonomous
    # cron pointer, not a human reply to a menu. Logging it as off-menu pollutes the
    # catch-rate denominator with turns no menu could anticipate. Skip the impression.
    is_cron_injection = bool(re.match(r"\s*type:\s*\S", prompt))
    # Meta/activation guard: bare "story mode" / "story" / "menu" are activation or
    # meta phrases, NOT a human reply to a menu. (ON_CMDS requires "... on"; bare
    # "story mode" fell through to off_menu and polluted the catch-rate denominator
    # with a turn no menu could anticipate -- same class as the cron-injection guard.
    # The menu still renders below; only the impression log is skipped.)
    is_meta = p in ("story mode", "story", "menu", "story status", "story mode status")
    sel_note = ""
    if not is_toggle and not is_cron_injection and not is_meta and not content_pick:
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
        else:
            # Off-menu regret mining: the freetext typed INSTEAD of a menu item is the
            # highest-signal training data -- it's exactly what the 10 items failed to
            # anticipate. Capture it so menu-gen / the reweighter can learn the miss.
            try:
                with open(os.path.join(SIG_DIR, f"{USER}_offmenu.jsonl"), "a",
                          encoding="utf-8") as f:
                    f.write(json.dumps({"t": time.time(),
                                        "prompt": prompt.strip()[:500]}) + "\n")
            except Exception:
                pass
        if picks:
            items = (", ".join(chr(96 + x) for x in picks) if pick_letters
                     else ", ".join(str(x) for x in picks))
            multi = len(picks) > 1
            if multi:
                sel_note = (
                    f"\nUSER PICKED MENU ITEM(S) {items}: execute them as a CHAIN from the numbered "
                    f"menu at the end of YOUR PREVIOUS response, per the Story-Mode chained-pick "
                    f"contract:\n"
                    f"1. ORDER IS LITERAL (presumption): run in the typed sequence ({items}), not numeric "
                    f"order -- order encodes intent. This is the default; rule 8 is the sanctioned exception.\n"
                    f"2. CONTRADICTION: if two picked items are mutually exclusive (an action and its "
                    f"hold/negation, or two divergent pivots), the LATER item in the chain wins; skip "
                    f"the earlier one and state in ONE line what you dropped and why. Never execute both.\n"
                    f"3. TERMINAL: if a picked item is a hold/stop/react-first item, execute everything "
                    f"before it, then STOP and hand back; drop and note any items after it.\n"
                    f"4. DEPENDENCY: keep the typed order; only if that order makes an item impossible "
                    f"(it needs an earlier item's result that won't exist yet) run the prerequisite "
                    f"first and note the reorder.\n"
                    f"5. PARTIAL FAILURE: if an item fails, STOP the chain, report what completed, "
                    f"surface the failure, show a fresh menu -- do not blind-continue past a broken premise.\n"
                    f"6. NO-OP/REPEAT: skip an item already satisfied this session and note it "
                    f"(repetition-is-useless).\n"
                    f"7. CONFIRMATION: an explicitly-picked item IS authorization -- do not re-ask, even "
                    f"for irreversible/outward actions. EXCEPTION: if contradiction/dependency resolution "
                    f"would route you into an irreversible/outward action that was NOT cleanly chosen, "
                    f"pause and confirm.\n"
                    f"8. SENSIBLE REORDER: you MAY reorder the chain when a reordering objectively improves "
                    f"the outcome WITHOUT changing intent (e.g. run a capture/commit/verify step after the "
                    f"items it must capture; dedup before an expensive step) -- UNLESS the user signalled a "
                    f"strict order ('in this order', 'strictly', numbered-and-emphasised, or wording that "
                    f"makes the sequence load-bearing). Default ON. Always state the reorder in ONE line. "
                    f"Rule 1 is the presumption; this is when overriding it serves the user.\n"
                    f"Then show a fresh menu.")
            else:
                mod_clause = (f" MODIFIER -- apply this tweak to how you execute it: "
                              f"\"{modifier}\"." if modifier else "")
                sel_note = (f"\nUSER PICKED MENU ITEM(S) {items}: execute item {items} from the numbered "
                            f"menu at the end of YOUR PREVIOUS response, exactly as written.{mod_clause} An explicit "
                            f"pick IS authorization -- do not ask for confirmation. Then show a fresh menu.")

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
           "autonomously') -- the user arms it by replying 'story loop N'. "
           "QUALITY: the 10 items must span at least 5 distinct signature-move classes and "
           "contain NO near-duplicates -- no two items may be paraphrases of the same action. "
           "SAFETY: prefix any item that performs an irreversible or outward-facing action "
           "(send / publish / deploy / delete / push / message / email / post) with a leading "
           "'⚠ ' marker so a phone-tapper sees the consequence before tapping. "
           "MODIFIERS: a user may also reply 'N: <tweak>' to run item N with a small adjustment "
           "(e.g. '3: only the auth part'). "
           "COLLISION-RESISTANCE (disjoint keyspaces): if THIS response contains its own list the "
           "user picks from by number (ideas, files, drafts, search results, options to select), do "
           "NOT number the menu 1-10 -- that collides with the content list. Instead key the menu "
           "with LETTERS and title it EXACTLY 'Story Mode -- reply with a letter (a-j), or chain "
           "several (e.g. `c` or `e,d,a`); bare numbers select from the list above:'. Numbers then "
           "decode unambiguously to the content list, letters to the menu -- two disjoint "
           "namespaces that cannot collide by construction. With no content pick-list present, use "
           "the standard numbered menu and its standard title."
           + sig_rules + sel_note)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit", "additionalContext": ctx}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
