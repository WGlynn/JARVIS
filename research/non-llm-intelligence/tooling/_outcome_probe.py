#!/usr/bin/env python3
"""_outcome_probe.py -- WAL outcome-tagging: turn a gate warning + the subsequent edit into evidence.

The shared unlock for LOOP 2 (exit test), LOOP 5 (real calibration), LOOP 7 (allocator). Today's
telemetry logs that a gate FIRED, never whether the fire HELPED. This module supplies the missing link:
given a gate warning (which flagged some snippet in a target) and the next write to that same target,
classify the outcome and convert it to (strength, confidence) evidence for _truthvalue.EvidenceLedger.

  applied          flagged snippet was changed/removed on the next rewrite  -> the warning caused a fix  (+)
  ignored          flagged snippet survived a rewrite of the target          -> not applied (maybe a
                                                                                correct override)         (weak -)
  no-rewrite       target was never rewritten after the warning              -> no signal
  unrelated-change target changed but the flagged text wasn't there anyway   -> no signal

Deterministic, offline-testable, zero LLM calls. The live wiring (a PreToolUse recorder + a
subsequent-write resolver) is a separate, Will-gated hook change; THIS is the logic it would call.
Free to copy (JARVIS non-LLM intelligence architecture).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _truthvalue as _tv  # noqa: E402

# outcome -> (evidence_sign, weight). None sign = no evidence (don't feed the ledger).
_EVIDENCE = {
    "applied": (True, 1.0),           # strong positive: the warning was acted on
    "ignored": (False, 0.5),          # weak negative: survived a rewrite (could be a correct override)
    "no-rewrite": (None, 0.0),        # user never revisited the target -> no signal
    "unrelated-change": (None, 0.0),
    "no-signal": (None, 0.0),
}


def classify_outcome(flagged: str, prior: str, new: str) -> str:
    """Classify what happened to a flagged snippet between the warned write and the next one."""
    flagged = (flagged or "").strip()
    if not flagged:
        return "no-signal"
    if prior == new:
        return "no-rewrite"                    # target not rewritten after the warning
    in_prior, in_new = flagged in prior, flagged in new
    if in_prior and not in_new:
        return "applied"                       # flagged text changed/removed -> warning acted on
    if in_new:
        return "ignored"                       # flagged text survived a rewrite -> not applied
    return "unrelated-change"


def outcome_to_evidence(outcome: str) -> tuple[bool | None, float]:
    return _EVIDENCE.get(outcome, (None, 0.0))


@dataclass
class WarningLedger:
    """Records open gate-warnings and resolves them against later writes, feeding a truth-value ledger.

    A PreToolUse hook calls `warn(gate, key, flagged, content)` when it flags something; the next write
    to the same `key` (target) calls `resolve(key, new_content)`. Resolved outcomes accumulate as
    per-gate (strength, confidence) in the underlying EvidenceLedger -> each gate self-calibrates.
    """

    evidence: "_tv.EvidenceLedger" = field(default_factory=_tv.EvidenceLedger)
    _open: dict[str, tuple[str, str, str]] = field(default_factory=dict)  # key -> (gate, flagged, content)

    def warn(self, gate: str, key: str, flagged: str, content: str) -> None:
        self._open[key] = (gate, flagged, content)

    def resolve(self, key: str, new_content: str) -> str | None:
        rec = self._open.pop(key, None)
        if rec is None:
            return None
        gate, flagged, prior = rec
        outcome = classify_outcome(flagged, prior, new_content)
        sign, weight = outcome_to_evidence(outcome)
        if sign is not None:
            self.evidence.observe(gate, sign, weight)
        return outcome

    def truth(self, gate: str):
        return self.evidence.truth(gate)

    def decision(self, gate: str) -> float:
        return self.evidence.decision(gate)


if __name__ == "__main__":
    wl = WarningLedger()
    # a gate flags "LayerZero" in a draft; the next revision removes it -> applied (positive)
    wl.warn("conflict-detector", "draft.md", "LayerZero", "we should use LayerZero")
    print("outcome:", wl.resolve("draft.md", "we should use canonical messaging"))
    # a gate flags something that survives the rewrite -> ignored (weak negative)
    wl.warn("conflict-detector", "d2.md", "Uniswap", "integrate Uniswap now")
    print("outcome:", wl.resolve("d2.md", "integrate Uniswap now, per plan"))
    print("conflict-detector:", wl.truth("conflict-detector"), "decision=%.3f" % wl.decision("conflict-detector"))
