#!/usr/bin/env python3
"""_outcome_probe_test.py -- pytest for _outcome_probe.py. Run: python -m pytest _outcome_probe_test.py -q"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _outcome_probe as op  # noqa: E402


def test_applied():
    assert op.classify_outcome("Xyz", "use Xyz now", "use the other thing") == "applied"


def test_ignored():
    assert op.classify_outcome("Xyz", "use Xyz", "use Xyz, per plan") == "ignored"


def test_no_rewrite():
    assert op.classify_outcome("Xyz", "use Xyz", "use Xyz") == "no-rewrite"


def test_unrelated_change():
    assert op.classify_outcome("Xyz", "hello world", "goodbye world") == "unrelated-change"


def test_empty_flag_is_no_signal():
    assert op.classify_outcome("", "a", "b") == "no-signal"


def test_evidence_mapping():
    assert op.outcome_to_evidence("applied") == (True, 1.0)
    assert op.outcome_to_evidence("ignored")[0] is False
    assert op.outcome_to_evidence("no-rewrite")[0] is None


def test_ledger_resolves_and_calibrates():
    wl = op.WarningLedger()
    # three warnings that get applied (positive), one ignored (weak neg)
    for i in range(3):
        wl.warn("g", f"f{i}", "flag", "has flag here")
        assert wl.resolve(f"f{i}", "fixed, no more") == "applied"
    wl.warn("g", "f9", "flag", "has flag here")
    assert wl.resolve("f9", "has flag here still, plus more") == "ignored"
    t = wl.truth("g")
    assert 0.5 < t.strength <= 1.0        # mostly applied ⇒ strength high
    assert t.confidence > 0.0             # evidence accumulated
    assert 0.5 < wl.decision("g") < 1.0


def test_unmatched_resolve_is_none():
    wl = op.WarningLedger()
    assert wl.resolve("never-warned", "whatever") is None


def test_no_rewrite_gives_no_evidence():
    wl = op.WarningLedger()
    wl.warn("g", "f", "flag", "has flag")
    wl.resolve("f", "has flag")            # no-rewrite ⇒ no evidence fed
    assert wl.truth("g").confidence == 0.0  # ledger stayed empty for g
