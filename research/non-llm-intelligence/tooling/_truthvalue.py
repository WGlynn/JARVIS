#!/usr/bin/env python3
"""_truthvalue.py -- PLN/NARS-style (strength, confidence) truth-values. LOOP 5 belief layer.

Explicit uncertainty as two numbers instead of ad-hoc LLM judgment:
  strength   s ∈ [0,1]  -- the frequency/probability the statement holds (evidence ratio).
  confidence c ∈ [0,1)  -- how much evidence backs s; c = n/(n+k) for evidence count n, horizon k.

Two independent evidence sources for the same statement are combined by REVISION (evidence adds).
The decision value is the EXPECTATION: c*(s-0.5)+0.5 -- equals s at full confidence, 0.5 at none.

Jarvis use (feeds LOOP 7): a gate/primitive accumulates (s,c) from WAL fire outcomes. Routine
applicability scoring then comes from the truth-value; the LLM is reserved for genuinely novel cases.

CPU-only, stdlib, zero LLM calls. Free to copy (JARVIS non-LLM intelligence architecture).
"""
from __future__ import annotations

from dataclasses import dataclass

# Personal evidential horizon: how much evidence to reach confidence 0.5. NARS default 1.0.
DEFAULT_K: float = 1.0
_EPS = 1e-9


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


@dataclass(frozen=True)
class TruthValue:
    strength: float
    confidence: float

    def __post_init__(self) -> None:
        # frozen dataclass: clamp via object.__setattr__
        object.__setattr__(self, "strength", _clamp01(self.strength))
        # confidence must stay < 1 (c=1 ⇒ infinite evidence count)
        object.__setattr__(self, "confidence", min(_clamp01(self.confidence), 1.0 - _EPS))

    # ---- constructors ----
    @classmethod
    def from_evidence(cls, positive: float, total: float, k: float = DEFAULT_K) -> "TruthValue":
        """Build from raw counts: s = positive/total, c = total/(total+k)."""
        if total <= 0:
            return cls(0.5, 0.0)  # no evidence → maximal ignorance
        s = _clamp01(positive / total)
        c = total / (total + k)
        return cls(s, c)

    # ---- interpretation ----
    def count(self, k: float = DEFAULT_K) -> float:
        """Confidence → equivalent evidence count: n = k*c/(1-c)."""
        return k * self.confidence / (1.0 - self.confidence)

    def expectation(self) -> float:
        """Decision value in [0,1]: c*(s-0.5)+0.5. = s at c=1, = 0.5 at c=0."""
        return self.confidence * (self.strength - 0.5) + 0.5

    def __repr__(self) -> str:
        return f"TV(s={self.strength:.3f}, c={self.confidence:.3f})"


def revise(a: TruthValue, b: TruthValue, k: float = DEFAULT_K) -> TruthValue:
    """Combine two INDEPENDENT evidence sources for the same statement (evidence adds).

    Commutative and associative; revising with a zero-confidence TV is a no-op.
    """
    na, nb = a.count(k), b.count(k)
    n = na + nb
    if n <= 0:
        return TruthValue(0.5, 0.0)
    s = (na * a.strength + nb * b.strength) / n
    c = n / (n + k)
    return TruthValue(s, c)


def deduction(ab: TruthValue, bc: TruthValue) -> TruthValue:
    """Chained inference A→B, B→C ⇒ A→C (PLN independence-assumption form).

    strength = s_ab * s_bc + 0.5*(1 - s_ab)   (unknown-term default 0.5);
    confidence = c_ab * c_bc  (chaining only weakens confidence).
    """
    s = ab.strength * bc.strength + 0.5 * (1.0 - ab.strength)
    c = ab.confidence * bc.confidence
    return TruthValue(s, c)


class EvidenceLedger:
    """Accumulates positive/total evidence for named statements (e.g. gate reliability).

    A gate fire that led to a good outcome = positive evidence; a false positive = negative.
    `truth(name)` returns the current self-calibrated TruthValue; `decision(name)` its expectation.
    """

    def __init__(self, k: float = DEFAULT_K) -> None:
        self.k = k
        self._pos: dict[str, float] = {}
        self._tot: dict[str, float] = {}

    def observe(self, name: str, positive: bool, weight: float = 1.0) -> None:
        self._tot[name] = self._tot.get(name, 0.0) + weight
        if positive:
            self._pos[name] = self._pos.get(name, 0.0) + weight
        else:
            self._pos.setdefault(name, 0.0)

    def truth(self, name: str) -> TruthValue:
        return TruthValue.from_evidence(self._pos.get(name, 0.0), self._tot.get(name, 0.0), self.k)

    def decision(self, name: str) -> float:
        return self.truth(name).expectation()


if __name__ == "__main__":
    # tiny demo
    g = EvidenceLedger()
    for _ in range(8):
        g.observe("wwwd-gate", True)
    for _ in range(2):
        g.observe("wwwd-gate", False)
    print("wwwd-gate:", g.truth("wwwd-gate"), "decision=%.3f" % g.decision("wwwd-gate"))
    a = TruthValue.from_evidence(9, 10)
    b = TruthValue.from_evidence(1, 2)
    print("revise:", a, "+", b, "=", revise(a, b))
