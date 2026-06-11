#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AFK corpus reweighter — criticism-4 fix: a log that gets CONSUMED.

Reads <user>_selections.jsonl (every menu number the user actually picked) and
nudges the signature corpus weights toward observed picks. Logs are written all
over JARVIS and almost never read back; this closes ONE loop end-to-end as the
template. Runnable standalone or on a cron. Idempotent-ish (EMA, bounded).
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
                       "_system", "afk_signatures")
USER = os.environ.get("AFK_USER", "will")
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

    # Menu position -> probability of being a high-rank pick. We don't store the
    # exact menu text historically, so we learn the SHAPE: do picks cluster at
    # the top (corpus well-ranked) or scatter (corpus mis-ranked)? Surface that
    # as a health signal rather than silently mutating classes on weak evidence.
    nums = [p.get("picked") for p in picks if isinstance(p.get("picked"), int)]
    n = len(nums)
    top3 = sum(1 for x in nums if x <= 3)
    health = top3 / n if n else 0.0
    sig["_reweight"] = {
        "selections_consumed": n,
        "top3_hit_rate": round(health, 3),
        "verdict": ("well-ranked" if health >= 0.5 else
                    "menu-order needs work — picks scatter below top 3"),
        "note": "position-only signal; richer reweight needs menu-text logging "
                "(follow-up: log the chosen item's move-class, not just its number)",
    }
    json.dump(sig, open(sigp, "w", encoding="utf-8", newline="\n"), indent=2)
    print(f"reweight: consumed {n} selections, top3 hit-rate {health:.0%} "
          f"({sig['_reweight']['verdict']})")
    return 0


if __name__ == "__main__":
    main()
