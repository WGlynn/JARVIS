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

    nums = [p.get("picked") for p in picks if isinstance(p.get("picked"), int)]
    n = len(nums)
    top3 = sum(1 for x in nums if x <= 3)
    health = top3 / n if n else 0.0  # precision@3 -- SECONDARY objective

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
            if r.get("kind") == "pick":
                on_menu += 1
    except FileNotFoundError:
        pass
    except Exception:
        pass
    catch = (on_menu / impressions) if impressions else None

    sig["_reweight"] = {
        "selections_consumed": n,
        # PRIMARY
        "impressions": impressions,
        "catch_rate_recall_at_10": (round(catch, 3) if catch is not None else None),
        # SECONDARY
        "top3_hit_rate_precision_at_3": round(health, 3),
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
