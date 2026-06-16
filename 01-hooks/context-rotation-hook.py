#!/usr/bin/env python3
"""Stop hook: context-rotation, ELASTICITY-TIERED.

Rotation is value-elastic, not a hard cutoff. See
02-persistence/context-rotation-elasticity.md.

The hook knows only the COST tier (token count). It does NOT know the thread's
VALUE tier -- that judgment stays with the model. So each tier crossing refreshes
the handoff (unconditional safety floor) and hands the model the tier-appropriate
framing to apply against the live thread's value:

  C1  200k-350k  elastic    -> handoff saved, CLEAR TO CONTINUE; rotate only if low-value
  C2  350k-600k  deliberate -> continue for high-value only; +50k value-checks
  C3  >=600k      ceiling     -> recommend rotate even mid-thread (coherence+cost), unless override

Guardrails:
  - anti-over-abuse (operator): a low-value thread at C1 should rotate.
  - anti-under-utilize (model): a high-value thread below C3 is NEVER pressured to retire.

Fires once per tier per session (per-tier marker files in STATE_DIR).
Thresholds tunable via env: CTX_TIER_C1 / CTX_TIER_C2 / CTX_TIER_C3.
"""
import json
import os
import sys

C1 = int(os.environ.get("CTX_TIER_C1", os.environ.get("CTX_HANDOFF_THRESHOLD", "200000")))
C2 = int(os.environ.get("CTX_TIER_C2", "350000"))
C3 = int(os.environ.get("CTX_TIER_C3", "600000"))
STATE_DIR = os.path.expanduser("~/.claude/hooks/.ctx-handoff")

# highest-first so we pick the current tier
TIERS = [(C3, "c3"), (C2, "c2"), (C1, "c1")]


def latest_ctx(tp: str) -> int:
    try:
        with open(tp, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 250_000))
            chunk = f.read().decode("utf-8", "replace")
        for line in reversed(chunk.splitlines()):
            if '"usage"' not in line:
                continue
            try:
                j = json.loads(line)
            except Exception:
                continue
            if j.get("type") != "assistant":
                continue
            u = (j.get("message") or {}).get("usage") or {}
            return (
                (u.get("input_tokens") or 0)
                + (u.get("cache_read_input_tokens") or 0)
                + (u.get("cache_creation_input_tokens") or 0)
            )
    except Exception:
        pass
    return 0


HANDOFF = (
    "First refresh the handoff (safety floor, unconditional): update the auto-memory "
    "project file for this topic, and a HANDOFF.md if a natural project folder exists "
    "-- current state, key decisions and why, open threads / next steps, file paths. "
    "Never include secrets, tokens, account numbers, or PII."
)


def reason_for(tier: str, k: int) -> str:
    if tier == "c1":
        return (
            f"CONTEXT TIER C1 (~{k}k, elastic zone). {HANDOFF} "
            "Then apply the elasticity rule: judge THIS thread's value. If it is an "
            "active / high-value thread (emotional, strategic, irreversible work in flight, "
            "multi-step build, or the user is engaged), tell the user plainly that context "
            f"is ~{k}k, the handoff is saved (list the locations), and they are CLEAR TO "
            "CONTINUE -- rotation is available, not required. Do NOT pressure the user to "
            "retire a live, valuable thread; that is the anti-under-utilize guardrail. Only "
            "recommend rotating if the thread is low-value or winding down."
        )
    if tier == "c2":
        return (
            f"CONTEXT TIER C2 (~{k}k, deliberate zone). {HANDOFF} "
            "Then: continue only for genuinely high-value live work, and state a one-line "
            "value-check when you do. If the thread is routine or resumable cleanly, recommend "
            f"rotating now (context ~{k}k, handoff saved, list locations). Re-check each +50k."
        )
    return (
        f"CONTEXT TIER C3 (~{k}k, ceiling -- coherence and cost risk). {HANDOFF} "
        f"Then recommend the user rotate to a fresh chat even mid-thread (context ~{k}k, handoff "
        "saved, list locations); the new chat auto-loads memory and continues. Continue only on "
        "an explicit user override."
    )


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("stop_hook_active"):
        return
    sid = data.get("session_id") or ""
    tp = data.get("transcript_path") or ""
    if not sid or not tp:
        return
    ctx = latest_ctx(tp)
    if ctx < C1:
        return

    # current tier = highest threshold ctx has crossed
    cur = None
    for thr, name in TIERS:
        if ctx >= thr:
            cur = name
            break
    if cur is None:
        return

    os.makedirs(STATE_DIR, exist_ok=True)
    cur_marker = os.path.join(STATE_DIR, f"{sid}.{cur}")
    if os.path.exists(cur_marker):
        return

    # mark current tier AND all lower tiers, so a lower-tier message never fires late
    order = ["c1", "c2", "c3"]
    for name in order[: order.index(cur) + 1]:
        try:
            with open(os.path.join(STATE_DIR, f"{sid}.{name}"), "w") as f:
                f.write(str(ctx))
        except Exception:
            pass

    k = ctx // 1000
    print(json.dumps({"decision": "block", "reason": reason_for(cur, k)}))


if __name__ == "__main__":
    main()
