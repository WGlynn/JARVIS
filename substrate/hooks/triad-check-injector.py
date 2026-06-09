#!/usr/bin/env python3
"""UserPromptSubmit hook: inject Correspondence Triad check on design-decision prompts.

Context
-------
The Correspondence Triad (see memory/MEMORY.md [META-PRINCIPLE]) is three meta-
principles that should fire before any mechanism-design commitment:
  1. Substrate-Geometry Match — does the mechanism's scaling match the substrate's
     natural form (fractal, golden-ratio, power-law)?
  2. Augmented Mechanism Design — does it augment via math-enforced invariants
     rather than replace the system outright?
  3. Augmented Governance — does it preserve the hierarchy
     Physics (P-001) > Constitution (P-000) > Governance (DAO votes)?

The triad is preloaded via MEMORY.md, but "preloaded" != "actively applied."
This hook detects design-decision keywords in the user's prompt and injects
an explicit triad-check reminder so the three questions fire before commitment.

Contract
--------
- stdin: JSON { prompt, session_id, cwd, ... }
- stdout: JSON { hookSpecificOutput: { hookEventName, additionalContext } } when
  design-keywords matched; empty otherwise (silent exit).
- stderr: observability logging.

Design
------
Narrow firing. The triad should NOT fire on every turn — only when the prompt
signals a design decision is being made. Conversation, routine code edits,
documentation tasks don't need the gate.
"""
import json
import os
import sys

# Design-decision keywords. Substring match, case-insensitive. One hit = fire.
DESIGN_KEYWORDS = [
    # Mechanism-design framings
    "mechanism design", "mechanism-design", "design decision",
    "which approach", "which mechanism", "should we use",
    "design choice", "design a ", "refactor to",
    # Economic calibration
    "bond size", "challenge window", "slash split", "slash percentage",
    "voting threshold", "quorum", "parameter calibration",
    "economic parameter", "emission curve", "tokenomics",
    "fee curve", "fee schedule", "rate limit design",
    # Mechanism primitives
    "auction design", "orderbook design", "amm curve",
    "reward distribution", "incentive structure",
    "governance design", "token architecture",
    # Design-trap triggers
    "first-available", "standard approach", "ecosystem default",
    "everyone uses", "best practice for",
    # New-primitive signals
    "new primitive", "new mechanism", "adding a ",
    "designing a new", "propose a mechanism",
    # Explicit invocation
    "correspondence triad", "triad check", "run the triad",
    "substrate geometry", "augmented governance",
    # A-vs-B framings (strong design signal)
    " vs ", " versus ", "tradeoff between",
]

# Negative filters — if prompt contains these, suppress even on keyword match.
# (Avoids spurious fires on conversational mentions of design history.)
SUPPRESS_IF = [
    "already decided", "already shipped", "already deployed",
    "last session", "previous cycle", "closed in cycle",
]

TRIAD_CHECK = """[CORRESPONDENCE TRIAD — design-decision detector fired]

A mechanism-design keyword was detected in your prompt. Before committing to a design, run the three checks:

**1. Substrate-Geometry Match** (the "what" — geometric correspondence)
   - What is the substrate's natural geometric form? (fractal / power-law / heavy-tailed / golden-ratio)
   - Does the candidate mechanism's scaling match that form, or is it linear/binary applied to a non-linear substrate?
   - If mismatched: the candidate is likely a First-Available Trap. See `memory/primitive_substrate-geometry-match.md`.

**2. Augmented Mechanism Design** (the "how" — methodology)
   - Does the candidate augment the existing system with math-enforced invariants, or does it replace it outright?
   - Are fairness/safety properties structural (by construction) or discretionary (by policy)?
   - For economic parameters (bond/window/slash/quorum): read the augmented mechanism design paper FIRST. See `memory/feedback_augmented-mechanism-design-paper.md`.

**3. Augmented Governance** (the "how-maintained" — accountability)
   - Does it preserve the hierarchy: Physics (P-001 Shapley invariants) > Constitution (P-000 Fairness) > Governance (DAO free within those)?
   - Can a 51% vote break any invariant? If yes, the math isn't load-bearing enough.
   - See `memory/primitive_augmented-governance.md`.

If all three pass: commit. If any fail or are unclear: decompose further before committing. Skip this check explicitly (with reason) if the decision is below design granularity (typo fix, test update, etc.)."""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        print(f"[triad-check] stdin parse failed: {e}", file=sys.stderr)
        return 0

    prompt = (payload.get("prompt") or "").lower()
    if not prompt:
        return 0

    # Suppress on ambient / retrospective language
    for suppress in SUPPRESS_IF:
        if suppress in prompt:
            return 0

    # Detect design keywords
    hits = [kw for kw in DESIGN_KEYWORDS if kw in prompt]
    if not hits:
        return 0

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": TRIAD_CHECK,
        }
    }
    print(json.dumps(out))
    print(f"[triad-check] fired on: {hits[:3]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
