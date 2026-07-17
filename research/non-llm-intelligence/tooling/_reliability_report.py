#!/usr/bin/env python3
"""_reliability_report.py -- per-gate TruthValue from real warning outcomes (LIVE WIRING 1 readout).

Replays _system/gate_reliability.jsonl (written by ~/.claude/hooks/_outcome_recorder.py) through the
same evidence -> (strength, confidence) logic used offline (_outcome_probe + _truthvalue), and prints
one calibrated TruthValue per gate: how often, when a gate warns, the warning is actually acted on.

This is the human-legible readout of "which gates earn their firing budget", and the data source
LOOP 5 / LOOP 7 consume for attention weighting. Deterministic, CPU-only, zero LLM calls.

Usage:  python _reliability_report.py
"""
from __future__ import annotations

import json
import os
from pathlib import Path

_env_root = os.environ.get("JARVIS_MEMORY_ROOT", "").strip()  # Path("") is truthy -> guard on the string
_MEM = Path(_env_root) if _env_root else Path(__file__).resolve().parent
_RELIABILITY = _MEM / "_system" / "gate_reliability.jsonl"

import sys  # noqa: E402
sys.path.insert(0, str(_MEM))
from _outcome_probe import outcome_to_evidence  # noqa: E402
import _truthvalue as _tv  # noqa: E402


def build() -> "tuple[_tv.EvidenceLedger, dict[str, dict[str, int]]]":
    ledger = _tv.EvidenceLedger()
    counts: dict[str, dict[str, int]] = {}
    if not _RELIABILITY.exists():
        return ledger, counts
    for ln in _RELIABILITY.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(ln)
        except Exception:
            continue
        gate = row.get("gate", "?")
        outcome = row.get("outcome", "no-signal")
        counts.setdefault(gate, {}).setdefault(outcome, 0)
        counts[gate][outcome] += 1
        sign, weight = outcome_to_evidence(outcome)
        if sign is not None:
            ledger.observe(gate, sign, weight)
    return ledger, counts


def main() -> None:
    ledger, counts = build()
    if not counts:
        print("no gate_reliability.jsonl yet -- no warnings have been resolved.")
        print(f"(expected at: {_RELIABILITY})")
        return
    print("PER-GATE RELIABILITY (strength = fraction of warnings acted on; confidence = evidence mass)")
    print("=" * 84)
    rows = []
    for gate in sorted(counts):
        tv = ledger.truth(gate)
        dec = ledger.decision(gate)
        rows.append((gate, tv, dec, counts[gate]))
    rows.sort(key=lambda r: (r[2]), reverse=True)
    for gate, tv, dec, c in rows:
        s = getattr(tv, "strength", None)
        conf = getattr(tv, "confidence", None)
        breakdown = " ".join(f"{k}={v}" for k, v in sorted(c.items()))
        s_str = f"{s:.3f}" if s is not None else "  n/a"
        c_str = f"{conf:.3f}" if conf is not None else "  n/a"
        print(f"  {gate:<38} strength={s_str} confidence={c_str} decision={dec:+.3f}")
        print(f"      {breakdown}")


if __name__ == "__main__":
    main()
