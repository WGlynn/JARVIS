#!/usr/bin/env python3
"""
Liveness witness for the WWWD correction-capture pipeline (in-system alarm).

The WWWD self-compounding loop depends on ONE thing being recorded: when Will
corrects a projection, that correction must land in the gate-fire log's
`correction` field so it becomes training signal for the next projection. The
gate itself (hooks/wwwd-gate.py) fires constantly and writes the denominator
(one row per decision moment). The numerator -- the corrections -- is written
by a SEPARATE Stop-event hook (hooks/wwwd-correction-detector.py).

Until 2026-08-08 that detector was effectively dead: it read the preceding user
message from Stop-payload keys (`user_message` / `last_user_message` / a
messages[] array) that the Claude Code Stop event never delivers, so it almost
never saw text and almost never wrote the numerator. That is now REPAIRED --
wwwd-correction-detector.py reads the user message from the prompt buffer written
each turn by hooks/wwwd-prompt-buffer.py (UserPromptSubmit), where the message IS
available (wwwd-correction-detector.py:152-162). `gate_revision_occurred` is
flipped by that same detector when a correction is captured.

Consequence: the log shows a "~0% correction rate", which reads like "the
projection is always right / Will never corrects" but is actually "the numerator
was never captured." Unmeasured denominator, not real signal. That silent
misread is the exact silent-failure class already fixed for crons, crash
recovery, and the autosave daemon.

This witness reads wwwd_gate_fires.jsonl and surfaces LOUD when the
correction-capture pipeline appears dead:

  - log MISSING       -> the gate has never fired (or its dir was wiped)
  - log UNREADABLE     -> corrupted / permission problem
  - CAPTURE DEAD       -> gate fired recently (denominator is live) but the
                          lifetime + last-7d correction-capture fraction is
                          ~0 => the numerator pipeline is broken, and any
                          "0% correction rate" is UNMEASURED, not real.

If the capture fraction is materially non-zero (the pipeline is actually
recording corrections) -> SILENT (a healthy loop adds zero boot noise).

Warn-only: prints to stdout and always exits 0. It can never block boot. The
repair (buffering the user message on the UserPromptSubmit side) SHIPPED
2026-08-08; a persistent ~0% fraction now means the buffer/detector pipeline has
regressed, NOT that the Stop payload lacks the message.

This is the "absence is loud" half of the WWWD loop: a marker the pipeline is
supposed to be writing, checked at boot, so a dead numerator is a visible alarm
instead of a self-congratulatory "0% corrections."
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
GATE_FIRE_LOG = MEMORY_DIR / "_system" / "wwwd_gate_fires.jsonl"

# Window for the "recent" fraction.
RECENT_DAYS = 7.0
# If the gate has NOT fired within this many days the denominator itself is
# stale (the gate, not just the capture, may be down) -- report that too.
GATE_STALE_DAYS = 3.0
# Lifetime capture fraction at/below this is treated as "pipeline dead".
# The empirical number is 1 / ~9600 ~= 0.0001; anything under a per-mille is a
# dead numerator, not a rare-but-working loop.
DEAD_FRACTION = 0.001
FIX_HINT = "buffer/detector pipeline regressed -- check hooks/wwwd-prompt-buffer.py (UserPromptSubmit wiring) + wwwd-correction-detector.py buffer read (~lines 152-162)"


def _parse_ts(entry):
    ts = entry.get("timestamp")
    if not isinstance(ts, str):
        return None
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def main():
    if not GATE_FIRE_LOG.exists():
        print("=== WWWD CORRECTION-CAPTURE WITNESS: MISSING ===")
        print("The WWWD gate-fire log does not exist -- the gate has never fired (or its dir was wiped).")
        print(f"expected: {GATE_FIRE_LOG}")
        print(f"repair: {FIX_HINT}")
        return

    try:
        raw = GATE_FIRE_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as e:
        print("=== WWWD CORRECTION-CAPTURE WITNESS: UNREADABLE ===")
        print(f"{type(e).__name__}: {e} -- treat the correction-capture pipeline as unverifiable.")
        print(f"repair: {FIX_HINT}")
        return

    now = datetime.now(timezone.utc)
    recent_cutoff = now.timestamp() - RECENT_DAYS * 86400.0

    total = 0
    total_corrected = 0
    total_revision = 0
    recent_total = 0
    recent_corrected = 0
    last_ts = None

    for ln in raw:
        ln = ln.strip()
        if not ln:
            continue
        try:
            entry = json.loads(ln)
        except Exception:
            continue
        total += 1
        has_correction = entry.get("correction") is not None
        if has_correction:
            total_corrected += 1
        if entry.get("gate_revision_occurred") is True:
            total_revision += 1

        ts = _parse_ts(entry)
        if ts is not None:
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            tsec = ts.timestamp()
            if last_ts is None or tsec > last_ts:
                last_ts = tsec
            if tsec >= recent_cutoff:
                recent_total += 1
                if has_correction:
                    recent_corrected += 1

    if total == 0:
        print("=== WWWD CORRECTION-CAPTURE WITNESS: EMPTY ===")
        print("The gate-fire log exists but has zero parseable rows.")
        print(f"repair: {FIX_HINT}")
        return

    lifetime_fraction = total_corrected / total
    gate_age_days = (now.timestamp() - last_ts) / 86400.0 if last_ts is not None else None
    gate_stale = gate_age_days is not None and gate_age_days > GATE_STALE_DAYS

    # Healthy: the numerator is materially non-zero -> the loop is recording
    # corrections -> stay silent.
    if lifetime_fraction > DEAD_FRACTION and not gate_stale:
        return

    # Otherwise: loud. Either the numerator is dead or the whole gate went quiet.
    print("=== WWWD CORRECTION-CAPTURE WITNESS: CAPTURE APPEARS DEAD ===")
    print(
        f"correction-capture pipeline appears dead: {total_corrected}/{total} lifetime "
        f"({lifetime_fraction*100:.4f}%), gate_revision_occurred={total_revision}/{total}."
    )
    if recent_total > 0:
        print(
            f"last {int(RECENT_DAYS)}d: {recent_corrected}/{recent_total} gate-fires carried a captured correction."
        )
    else:
        print(f"last {int(RECENT_DAYS)}d: no gate-fires with parseable timestamps in the recent window.")
    if gate_age_days is not None:
        print(f"most recent gate-fire: {gate_age_days:.1f}d ago" + (" -- the DENOMINATOR itself is stale (gate may be down)." if gate_stale else "."))
    print(
        "Read this correctly: a ~0% correction rate here is UNMEASURED, not 'the projection is always right'."
    )
    print(
        "The numerator flows via hooks/wwwd-prompt-buffer.py (UserPromptSubmit) -> wwwd_last_prompt.json ->"
    )
    print(
        "wwwd-correction-detector.py (Stop). A dead numerator now means that pipeline regressed, not a payload gap."
    )
    print(f"repair: {FIX_HINT}")


if __name__ == "__main__":
    main()
