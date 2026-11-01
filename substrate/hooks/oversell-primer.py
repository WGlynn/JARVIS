#!/usr/bin/env python3
"""Oversell primer — the conversational tripwire for "am I overselling this?"

UserPromptSubmit. Injects one terse line every turn priming the self-check on the
conversational surface (the PreToolUse oversell-gate.py covers written artifacts).

IMPORTANT (Will, 2026-09-29): this banner is a TRIPWIRE, not the fix. Will said the
real change "requires a mindset shift in you" — teammate, not salesman. A hook cannot
manufacture the mindset; it can only catch the lapse. The durable shift lives in
[[feedback_teammate-not-salesman-lead-with-the-floor]]: lead with the honest floor
FIRST, then the upside. A salesman buries the caveat; a teammate states the true
state before the sell.
"""

import json
import sys

MSG = (
    '[OVERSELL CHECK] Teammate, not salesman. Before you call anything impressive / done / '
    'sellable / solid: state the honest floor FIRST — what is off-the-shelf, untested, or '
    'assumed — THEN the upside. Lead with the true state; pair every claim with its deflation '
    'or cut it. (Tripwire only; the real check is the mindset, not this line.)'
)


def main():
    try:
        json.load(sys.stdin)  # drain; content not needed
    except Exception:
        pass
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'UserPromptSubmit',
            'additionalContext': MSG,
        }
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
