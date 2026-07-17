#!/usr/bin/env python3
"""_truthvalue_test.py -- pytest for _truthvalue.py (LOOP 5). Run: python -m pytest _truthvalue_test.py -q"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import _truthvalue as tv  # noqa: E402


def test_from_evidence_basics():
    t = tv.TruthValue.from_evidence(9, 10)          # k=1 → c = 10/11
    assert t.strength == pytest.approx(0.9)
    assert t.confidence == pytest.approx(10 / 11)


def test_no_evidence_is_ignorance():
    t = tv.TruthValue.from_evidence(0, 0)
    assert t.strength == 0.5 and t.confidence == 0.0
    assert t.expectation() == pytest.approx(0.5)     # no evidence → decision is a coin flip


def test_confidence_never_one():
    t = tv.TruthValue(0.9, 1.0)                       # would be infinite evidence
    assert t.confidence < 1.0


def test_expectation_bounds():
    assert tv.TruthValue(1.0, 1.0 - 1e-9).expectation() == pytest.approx(1.0, abs=1e-6)
    assert tv.TruthValue(0.0, 1.0 - 1e-9).expectation() == pytest.approx(0.0, abs=1e-6)


def test_revision_adds_evidence():
    a = tv.TruthValue.from_evidence(9, 10)
    b = tv.TruthValue.from_evidence(9, 10)
    r = tv.revise(a, b)
    # same strength, but MORE confidence than either alone (evidence accumulated)
    assert r.strength == pytest.approx(0.9)
    assert r.confidence > a.confidence


def test_revision_commutative():
    a = tv.TruthValue.from_evidence(8, 10)
    b = tv.TruthValue.from_evidence(2, 5)
    r1, r2 = tv.revise(a, b), tv.revise(b, a)
    assert r1.strength == pytest.approx(r2.strength)
    assert r1.confidence == pytest.approx(r2.confidence)


def test_revision_ignorance_is_noop():
    a = tv.TruthValue.from_evidence(7, 10)
    r = tv.revise(a, tv.TruthValue(0.5, 0.0))
    assert r.strength == pytest.approx(a.strength)
    assert r.confidence == pytest.approx(a.confidence)


def test_revision_matches_pooled_counts():
    # revising (s from 9/10) with (s from 1/10) == one ledger of 10/20
    a = tv.TruthValue.from_evidence(9, 10)
    b = tv.TruthValue.from_evidence(1, 10)
    r = tv.revise(a, b)
    pooled = tv.TruthValue.from_evidence(10, 20)
    assert r.strength == pytest.approx(pooled.strength)
    assert r.confidence == pytest.approx(pooled.confidence)


def test_deduction_weakens_confidence():
    ab = tv.TruthValue(0.9, 0.8)
    bc = tv.TruthValue(0.9, 0.8)
    d = tv.deduction(ab, bc)
    assert d.confidence < ab.confidence           # chaining only loses confidence
    assert 0.0 <= d.strength <= 1.0


def test_ledger_self_calibrates():
    g = tv.EvidenceLedger()
    for _ in range(8):
        g.observe("gate", True)
    for _ in range(2):
        g.observe("gate", False)
    t = g.truth("gate")
    assert t.strength == pytest.approx(0.8)
    assert 0.0 < g.decision("gate") < 1.0
    # more consistent evidence ⇒ decision rises toward strength
    for _ in range(90):
        g.observe("gate", True)
    assert g.decision("gate") > t.expectation()
