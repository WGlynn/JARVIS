#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story Mode corpus reweighter -- a log that gets CONSUMED.

Reads <user>_selections.jsonl + <user>_impressions.jsonl (what the user picked,
and every menu impression) and surfaces the menu's health: catch-rate (recall@10,
PRIMARY) and precision@3 (SECONDARY). Closes one loop end-to-end as the template.
Runnable standalone or on a cron. (Formerly "AFK corpus reweighter"; renamed
2026-06-12.) See [P.story-mode-menu-objective] for the formal objective.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")
SIG_DIR = os.path.join(HOME, ".claude", "projects", "C--Users-Will", "memory",
                       "_system", "story_signatures")
USER = os.environ.get("STORY_USER") or os.environ.get("AFK_USER", "will")
ALPHA = 0.15  # EMA learning rate; bounded so no single pick dominates


def main() -> int:
    sigp = os.path.join(SIG_DIR, f"{USER}.json")
    selp = os.path.join(SIG_DIR, f"{USER}_selections.jsonl")
    try:
        sig = json.load(open(sigp, encoding="utf-8"))
        moves = sig["signature_moves"]
    except Exception as e:
        print(f"reweight: cannot load corpus: {e}"); return 0
    picks = []
    try:
        for line in open(selp, encoding="utf-8"):
            line = line.strip()
            if line:
                picks.append(json.loads(line))
    except FileNotFoundError:
        print("reweight: no selections yet"); return 0
    except Exception:
        pass
    if not picks:
        print("reweight: no selections to consume"); return 0

    # META/LOOP picks signal something DIFFERENT from a single-move pick: picking the
    # "Loop 1->3->5 autonomously" item is a BATCH-APPROVAL of the items it references, not
    # an endorsement of its own (usually slot-10) position. Scoring it as a regular pick
    # double-distorts -- it drags precision@3 down as a fake low-slot "miss" AND credits the
    # wrong slot. So: exclude meta picks from positional precision@3, and track them as their
    # own signal (loop-approval = an autonomy/batch-trust dimension). Honors p["meta"]=="loop"
    # once the gate tags it (see [F.story-mode-loop-pick-is-distinct-signal]); inert until then.
    regular = [p.get("picked") for p in picks
               if isinstance(p.get("picked"), int) and p.get("meta") != "loop"]
    n = len(regular)
    # the loop-approval signal excluded from `regular` above (inert until the gate tags meta=="loop").
    loop_approvals = sum(1 for p in picks
                         if isinstance(p.get("picked"), int) and p.get("meta") == "loop")
    top3 = sum(1 for x in regular if x <= 3)
    health = top3 / n if n else 0.0  # precision@3 over REGULAR picks only -- SECONDARY

    # PRIMARY objective: recall@10 (catch-rate). Of all menu impressions, how
    # often did the user pick a listed item vs. type something off-menu. This
    # is the number the picks-only log could never produce -- it needs the
    # impressions denominator (every turn classified pick/off_menu).
    impp = os.path.join(SIG_DIR, f"{USER}_impressions.jsonl")
    impressions = on_menu = 0
    try:
        for line in open(impp, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            impressions += 1
            # "paraphrase_pick" = the gate's TELEMETRY-ONLY fuzzy match of a free-text turn
            # against the last menu (detection decoupled from routing — the prompt still goes to
            # the model verbatim, only the impression is reclassified, so there is no wrong-action
            # risk). Counts as a catch in recall@10. Inert until the gate emits this kind.
            if r.get("kind") in ("pick", "paraphrase_pick"):
                on_menu += 1
    except FileNotFoundError:
        pass
    except Exception:
        pass
    catch = (on_menu / impressions) if impressions else None

    # ORDER-AWARENESS ([P.will-choice-ordering-priority-function]): when the user multi-picks,
    # ascending order means they took the menu top-to-bottom (ranking trusted); a reorder encodes
    # their own priority (the menu mis-ranked). Rate of ascending multi-picks = ranking-alignment.
    multi, ascending = 0, 0
    try:
        for line in open(impp, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            pk = r.get("picked") or []
            if r.get("kind") == "pick" and isinstance(pk, list) and len(pk) > 1:
                multi += 1
                if pk == sorted(pk):
                    ascending += 1
    except Exception:
        pass
    ranking_alignment = (ascending / multi) if multi else None

    sig["_reweight"] = {
        "selections_consumed": n,
        # PRIMARY
        "impressions": impressions,
        "catch_rate_recall_at_10": (round(catch, 3) if catch is not None else None),
        # SECONDARY
        "top3_hit_rate_precision_at_3": round(health, 3),
        # META/LOOP: a distinct signal (batch-approval / autonomy-trust), NOT a positional pick.
        # Counted as catches in recall, excluded from precision@3. Credit should propagate to the
        # items the loop references once the gate logs them (logging-side TODO, see feedback note).
        "loop_approvals": loop_approvals,
        "loop_approval_share_of_picks": (round(loop_approvals / (n + loop_approvals), 3)
                                         if (n + loop_approvals) else 0.0),
        "verdict": ("no impressions logged yet" if catch is None else
                    "catching well" if catch >= 0.6 else
                    "menu misses too often -- intent escaping the 10"),
        "catch_rate_note": "LOWER BOUND -- counts numeric picks only; a menu item "
                "chosen by paraphrase logs as off-menu. Maximize this; precision@3 "
                "is secondary. Anti-blandness guard (penalize catches via standing-"
                "move slots vs situation-specific 1-7) is DEFINED but not yet "
                "instrumented -- needs per-item move-class logging.",
    }
    json.dump(sig, open(sigp, "w", encoding="utf-8", newline="\n"), indent=2)
    cstr = f"{catch:.0%}" if catch is not None else "n/a"
    print(f"reweight: {n} picks / {impressions} impressions - catch-rate {cstr} - "
          f"precision@3 {health:.0%} ({sig['_reweight']['verdict']})")
    return 0


if __name__ == "__main__":
    main()
