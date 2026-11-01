#!/usr/bin/env python3
"""Stop hook: seal the newest handoff into the coarse chain, then auto-backup.

Closes the loop Will asked for (2026-08-12): every session close chains the new
handoff to the past and replicates it to >= 2 nodes.

Contract (WWWD-projected -- "never lose the chain" AND "never wedge me"):
  - LOCAL SEAL IS HARD: if the local seal fails (genuine corruption risk), that is
    a real bug worth surfacing loudly -- but we still never block the Stop (a wedged
    session-close risks a force-kill that loses MORE state than it protects).
  - REMOTE QUORUM IS FAIL-LOUD: if fewer than QUORUM nodes back up, we write a
    pending-backup flag that the next boot screams about + the next Stop retries.
    Set STRICT_BLOCK=True to instead hard-block session close on sub-quorum
    (Will's stated fail-closed preference; default off as the un-wedgeable form).
  - IDEMPOTENT + THROTTLED: seal is a no-op when the newest handoff is unchanged;
    backup only fires when a NEW block was actually sealed (or a retry is pending),
    so routine Stops cost nothing.
"""
import json
import os
import subprocess
import sys
from datetime import datetime

HOME = os.path.expanduser("~")
CHAIN = os.path.join(HOME, ".claude", "session-chain")
PENDING_FLAG = os.path.join(CHAIN, "handoff-chain", ".backup-pending")
STRICT_BLOCK = False  # flip to True for hard fail-closed session-close on sub-quorum


def _load(name):
    import importlib.util
    path = os.path.join(CHAIN, name)
    spec = importlib.util.spec_from_file_location(name.replace("-", "_").replace(".py", ""), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    if payload.get("stop_hook_active"):
        print(json.dumps({}))
        return 0

    ts = datetime.now().isoformat()
    notes = []

    # 1) LOCAL SEAL (hard-correctness, never blocks)
    sealed_new = False
    try:
        hc = _load("handoff-chain.py")
        status, res = hc.seal(ts)
        if status == "sealed":
            sealed_new = True
            notes.append(f"sealed seq {res['seq']} ({res['file']})")
        elif status == "noop":
            notes.append("chain: no new handoff")
        else:
            notes.append(f"chain seal: {status} {res}")
    except Exception as e:
        notes.append(f"[WARN] local seal errored: {e}")

    # 2) BACKUP -- only when a new block sealed OR a prior backup is still pending
    retry_pending = os.path.exists(PENDING_FLAG)
    if sealed_new or retry_pending:
        try:
            cb = _load("chain-backup.py")
            successes, results = cb.run()
            if successes >= cb.QUORUM:
                notes.append(f"backup quorum {successes}/{len(results)} PASS")
                try:
                    os.remove(PENDING_FLAG)
                except FileNotFoundError:
                    pass
            else:
                down = [n for n, (ok, _) in results.items() if not ok]
                notes.append(f"backup SUB-QUORUM {successes}/{len(results)} (down: {','.join(down)})")
                with open(PENDING_FLAG, "w", encoding="utf-8") as f:
                    f.write(ts + "\n")
                if STRICT_BLOCK:
                    print(json.dumps({
                        "decision": "block",
                        "reason": (
                            f"Experience-chain backup below quorum ({successes}/{len(results)}). "
                            f"Down: {', '.join(down)}. Session close blocked (STRICT_BLOCK). "
                            "Restore a remote or set STRICT_BLOCK=False."
                        ),
                    }))
                    return 0
        except Exception as e:
            notes.append(f"[WARN] backup errored: {e}")
            with open(PENDING_FLAG, "w", encoding="utf-8") as f:
                f.write(ts + " ERR\n")

    # non-blocking: emit nothing to the model channel (Stop schema is top-level only)
    # side-effect log for the boot witness to read
    try:
        with open(os.path.join(CHAIN, "handoff-chain", ".last-stop.log"), "w", encoding="utf-8") as f:
            f.write(ts + " | " + " | ".join(notes) + "\n")
    except Exception:
        pass
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
