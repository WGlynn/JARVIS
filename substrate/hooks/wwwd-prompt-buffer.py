#!/usr/bin/env python3
"""
WWWD Prompt Buffer — UserPromptSubmit hook
==========================================

Captures the current user prompt to a buffer file so the Stop-event
`wwwd-correction-detector.py` can actually read it.

Why this exists
---------------
The correction detector was a measurement artifact: it read the preceding
user message from Stop-payload keys (`user_message` / `last_user_message` /
`messages`) that Claude Code's Stop payload NEVER populates. Result: the
correction numerator was stuck at ~0/9695 (0.0%), which read falsely as
"the WWWD projection is always right" when the truth was "never measured."

The prompt IS available in the UserPromptSubmit payload (`prompt`), so we
buffer it here at prompt time. The detector reads the buffer at Stop time.

We also record the gate-fire log length as it stands BEFORE this turn's
gate-fires accrue. That's the attribution boundary: a correction in this
turn's prompt is about the PRIOR turn's output, so the detector attributes
it to a gate-fire entry with index < prior_gate_fire_count.

Warn-only, never blocks: always exits 0.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
GATE_FIRE_LOG = MEMORY_DIR / "_system" / "wwwd_gate_fires.jsonl"
BUFFER = MEMORY_DIR / "_system" / "wwwd_last_prompt.json"


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    prompt = data.get("prompt") or data.get("user_prompt") or ""

    # Count entries that exist BEFORE this turn's gate-fires -> attribution
    # boundary for the detector (a correction is about the PRIOR turn).
    # Basis MUST match the detector, which iterates read_text().splitlines()
    # positionally; count all splitlines (not non-blank) so a stray blank line
    # can't desync the boundary.
    prior_count = 0
    try:
        if GATE_FIRE_LOG.exists():
            prior_count = len(GATE_FIRE_LOG.read_text(encoding="utf-8").splitlines())
    except Exception:
        prior_count = 0

    try:
        BUFFER.parent.mkdir(parents=True, exist_ok=True)
        BUFFER.write_text(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt": prompt[:2000],
            "prior_gate_fire_count": prior_count,
        }), encoding="utf-8")
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
