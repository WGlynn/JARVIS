#!/usr/bin/env python3
"""
Boot liveness check for the session chain (in-system alarm).

The session chain (chain.py) is a hash-linked persistence trail. It advances
when checkpoints are finalized into blocks and index.json is rewritten. Nothing
at boot READS the chain for recall (recall serves off the memory corpus), so if
the chain stops advancing it fails SILENTLY -- exactly what happened on
2026-07-31, unnoticed for a week.

This hook, wired into SessionStart, makes that failure LOUD:

  - index MISSING     -> chain never initialized
  - index EMPTY (0B)  -> index corrupted/truncated; append_block would restart at
                         id 0 and OVERWRITE block-0000 (silent data loss). CRITICAL.
  - index UNREADABLE  -> corrupted JSON; treat as broken
  - index STALE       -> not advanced in > STALE_DAYS while sessions kept running
                         (heartbeat proves activity) => the chain is dead but the
                         rest of the system is alive. The silent-failure signature.

Healthy + advancing -> SILENT (a clean boot adds zero noise).

This is the "absence is loud" pattern, same as crash-backtest-witness-check.py:
a monotonic signal (index.json mtime) checked at boot so a chain that stopped
advancing is a visible alarm, not an invisible non-event.

NOTE: this does NOT itself repair or retire the chain -- that is a Will decision
(rebuild the ~19.5k-block index vs honestly retire the subsystem). It only
guarantees the failure can never again hide.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

CHAIN_DIR = Path(__file__).parent
INDEX_FILE = CHAIN_DIR / "index.json"
HEARTBEAT_FILE = CHAIN_DIR / "shield" / "heartbeat.json"
STALE_DAYS = 3.0
HEAL_HINT = "python ~/.claude/session-chain/chain.py status   (then decide: rebuild index vs retire)"


def _mtime_age_days(p):
    """Age in days of a path's mtime, or None if unavailable."""
    try:
        mt = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
        return (datetime.now(timezone.utc) - mt).total_seconds() / 86400.0
    except Exception:
        return None


def _sessions_active_recently():
    """
    True if the shield heartbeat shows the system was alive more recently than
    the chain advanced -- i.e. sessions happened but the chain did not move.
    Returns (active_recently, heartbeat_age_days) best-effort.
    """
    age = _mtime_age_days(HEARTBEAT_FILE)
    if age is None:
        return None, None
    return (age < STALE_DAYS), age


def main():
    # 1. Missing entirely.
    if not INDEX_FILE.exists():
        print("=== SESSION-CHAIN LIVENESS: INDEX MISSING ===")
        print("index.json does not exist -- the chain was never initialized or was deleted.")
        print("The persistence trail is NOT recording. This is the alarm working.")
        print(f"decide: {HEAL_HINT}")
        return

    size = INDEX_FILE.stat().st_size

    # 2. Empty / truncated -- the CRITICAL case (silent-overwrite risk).
    if size == 0:
        idx_age = _mtime_age_days(INDEX_FILE)
        active, hb_age = _sessions_active_recently()
        print("=== SESSION-CHAIN LIVENESS: INDEX EMPTY (CORRUPTED) ===")
        print("index.json is 0 bytes. append_block() computes the next id from")
        print("len(index['blocks']); with an empty index the next finalize would")
        print("RESTART at id 0 and OVERWRITE block-0000 -- silent data loss.")
        if idx_age is not None:
            print(f"index untouched for {idx_age:.1f}d.")
        if active:
            print(f"heartbeat active {hb_age:.1f}d ago => system alive, chain dead. Silent-failure signature.")
        print("The chain is NOT advancing. Do not trust it as a persistence layer until fixed.")
        print(f"decide: {HEAL_HINT}")
        return

    # 3. Present but unreadable.
    try:
        idx = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print("=== SESSION-CHAIN LIVENESS: INDEX UNREADABLE ===")
        print(f"{type(e).__name__}: {e} -- index.json is corrupted JSON.")
        print(f"decide: {HEAL_HINT}")
        return

    n_blocks = len(idx.get("blocks", []))
    head = (idx.get("head") or "(genesis)")[:8]

    # 4. Stale: not advanced in > STALE_DAYS while sessions kept running.
    idx_age = _mtime_age_days(INDEX_FILE)
    active, hb_age = _sessions_active_recently()
    if idx_age is not None and idx_age > STALE_DAYS:
        # Only LOUD if the system itself was active more recently than the chain
        # moved -- otherwise a stale index just means "no sessions lately", which
        # is not a failure.
        if active:
            print("=== SESSION-CHAIN LIVENESS: STALE (dead while sessions ran) ===")
            print(f"index.json last advanced {idx_age:.1f}d ago (head {head}, {n_blocks} blocks),")
            print(f"but the heartbeat shows activity {hb_age:.1f}d ago. Sessions ran; the chain did not move.")
            print("This is the silent-failure signature: alive system, dead persistence trail.")
            print(f"decide: {HEAL_HINT}")
        # stale but no recent activity -> not a failure -> silent
        return

    # healthy + advancing -> silent by design


if __name__ == "__main__":
    main()
