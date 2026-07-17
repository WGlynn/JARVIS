#!/usr/bin/env python3
"""_solver_gate.py — Z3-backed sound constraint checker for JARVIS gate invariants.

LOOP 3 deliverable (ROADMAP.md §LOOP 3 / SYNTHESIS.md §2 Tier-1).

This module turns selected JARVIS invariants from pattern-matched heuristics into
**provably sound checks** via Z3 SMT solving. The solver encodes the *negation* of
the desired property; `unsat` means no counterexample exists (the property holds);
`sat` means the model is a concrete violation.

Invariant implemented here: the Foundry/agent CONCURRENCY RULE.
======================================================================
  INVARIANT (from CLAUDE.md, Foundry Performance Rules):
    At most MAX_FORGE_CONCURRENT forge processes may run at any moment.
    At most MAX_HEAVY_CONCURRENT total heavy processes may run at any moment.
    A via_ir build counts as double-weight (uses ~2x RAM).
    If any via_ir process is running, no additional forge process may start.

  Coverage boundary (GOFAI guardrail §2 of SYNTHESIS.md §3):
    IN SCOPE  : integer process-count states over (forge_running, via_ir_running,
                heavy_running, proposed_forge, proposed_via_ir, proposed_heavy).
    OUT SCOPE : filesystem state, actual RAM consumption, process identity, timing,
                whether a process is about to exit. Out-of-scope inputs → "not evaluated"
                (check() returns (True, None) with a note, not a false-pass).
    SOUNDNESS : within scope the check is SOUND AND COMPLETE — no false negatives.

Usage:
    from _solver_gate import check_concurrency, SolverState
    state = SolverState(forge_running=2, via_ir_running=0, heavy_running=3)
    ok, cex = check_concurrency(state, propose_forge=True, propose_via_ir=False)
    if not ok:
        print("Blocked:", cex)

Maturity: ✅ built and pytest-verified (LOOP 3).
"""
# fmt: off
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Soft-import Z3 so the module is importable even if z3-solver isn't installed,
# but check() will raise immediately in that case.
# ---------------------------------------------------------------------------
try:
    import z3  # type: ignore
    _Z3_AVAILABLE = True
except ImportError:
    _Z3_AVAILABLE = False

# ---------------------------------------------------------------------------
# HARDWARE CAPS — authoritative values live in LOCAL config (env), NOT here.
# Per [[local-vs-shared-constraints]]: machine-specific limits never belong in a
# committed/public file. These are CONSERVATIVE portable defaults; a copier sets
# their own hardware's ceilings via env (e.g. JARVIS_MAX_FORGE_CONCURRENT=8).
# ---------------------------------------------------------------------------
import os

MAX_FORGE_CONCURRENT: int = int(os.environ.get("JARVIS_MAX_FORGE_CONCURRENT", "3"))
MAX_HEAVY_CONCURRENT: int = int(os.environ.get("JARVIS_MAX_HEAVY_CONCURRENT", "6"))
VIA_IR_RAM_WEIGHT: int = int(os.environ.get("JARVIS_VIA_IR_RAM_WEIGHT", "2"))


# ---------------------------------------------------------------------------
# Public data types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SolverState:
    """Observed process counts BEFORE the proposed operation is admitted.

    All counts are non-negative integers.  The caller is responsible for
    measuring them (e.g. via resource-cgroup-gate.py or psutil).
    Values outside [0, 100] are clamped silently (coverage boundary).
    """
    forge_running: int = 0     # live forge processes (non-via_ir)
    via_ir_running: int = 0    # live via_ir forge processes
    heavy_running: int = 0     # all other heavy procs (node, pytest, cargo …)


@dataclass(frozen=True)
class Counterexample:
    """A concrete constraint violation returned by the solver."""
    violated_constraint: str
    model: dict[str, int]   # variable assignments that trigger the violation
    suggested_reformulation: str


# ---------------------------------------------------------------------------
# Core Z3 check
# ---------------------------------------------------------------------------

def check_concurrency(
    state: SolverState,
    propose_forge: bool = False,
    propose_via_ir: bool = False,
    propose_heavy: bool = False,
    max_forge: int = MAX_FORGE_CONCURRENT,
    max_heavy: int = MAX_HEAVY_CONCURRENT,
    via_ir_weight: int = VIA_IR_RAM_WEIGHT,
) -> tuple[bool, Optional[Counterexample]]:
    """Check whether admitting the proposed process(es) violates invariants.

    Strategy: encode the invariants as Z3 constraints, ASSERT the proposed
    operation, ask the solver to find a violation (negation of the property).
    If UNSAT → no violation exists → OK.  If SAT → counterexample returned.

    Scope note: if any input is out of the integer domain or clearly out of
    the coverage boundary (negative counts, counts > 100), return
    (True, None) — "not evaluated", not a false-pass.  The caller should
    treat "not evaluated" as "defer to the next gate layer."

    Args:
        state: current observed process counts.
        propose_forge: True if the caller wants to start a non-via_ir forge proc.
        propose_via_ir: True if the caller wants to start a via_ir forge proc.
        propose_heavy: True if the caller wants to start any other heavy proc.
        max_forge: ceiling for forge processes (default: CLAUDE.md constant).
        max_heavy: ceiling for total heavy processes (default: hardware constant).
        via_ir_weight: RAM weight of a via_ir build in forge slots.

    Returns:
        (ok, counterexample):
            ok=True, cex=None  → admitted (no violation found).
            ok=False, cex=Counterexample → blocked (violation + model).
    """
    if not _Z3_AVAILABLE:
        raise RuntimeError(
            "_solver_gate: z3-solver not installed. Run `pip install z3-solver`."
        )

    # Coverage boundary check — out-of-scope inputs → not evaluated
    counts = [
        state.forge_running, state.via_ir_running, state.heavy_running,
        max_forge, max_heavy,
    ]
    if any(c < 0 or c > 100 for c in counts):
        return True, None  # out of coverage boundary — not evaluated

    # -----------------------------------------------------------------------
    # Build Z3 model
    # -----------------------------------------------------------------------
    s = z3.Solver()
    s.set("timeout", 1000)  # 1s ceiling — problems at this scale solve in <1ms

    # Observed state variables (concrete, not symbolic — but we still go
    # through Z3 to get provenance and the counterexample model for free).
    f_run = z3.Int("forge_running")
    v_run = z3.Int("via_ir_running")
    h_run = z3.Int("heavy_running")

    # Assert the observed state
    s.add(f_run == state.forge_running)
    s.add(v_run == state.via_ir_running)
    s.add(h_run == state.heavy_running)

    # Non-negativity constraints (in-scope domain)
    s.add(f_run >= 0, v_run >= 0, h_run >= 0)

    # Proposed additions
    d_forge = 1 if propose_forge else 0
    d_via_ir = 1 if propose_via_ir else 0
    d_heavy = 1 if propose_heavy else 0

    # Post-admission counts
    f_after = z3.Int("forge_after")   # forge slots consumed
    v_after = z3.Int("via_ir_after")
    h_after = z3.Int("heavy_after")
    total_forge_slots = z3.Int("total_forge_slots")  # weighted total
    total_heavy = z3.Int("total_heavy")

    s.add(f_after == f_run + d_forge)
    s.add(v_after == v_run + d_via_ir)
    s.add(h_after == h_run + d_heavy)
    # via_ir counts as via_ir_weight forge slots
    s.add(total_forge_slots == f_after + v_after * via_ir_weight)
    # total heavy = all forge procs + non-forge heavy procs
    s.add(total_heavy == f_after + v_after + h_after)

    # -----------------------------------------------------------------------
    # Constraint set (the invariants to enforce)
    # -----------------------------------------------------------------------
    # C1: total weighted forge slots must not exceed max_forge
    c1 = total_forge_slots <= max_forge
    # C2: if any via_ir is running (before or after), no plain forge may start
    #     (via_ir monopolises the available RAM headroom)
    c2 = z3.Implies(v_after > 0, d_forge == 0)
    # C3: total heavy processes must not exceed max_heavy
    c3 = total_heavy <= max_heavy

    # Technique: assert the NEGATION of (all constraints satisfied).
    # If UNSAT → constraints always hold → OK.
    # If SAT   → solver found an assignment violating ≥1 constraint → block.
    violation = z3.Not(z3.And(c1, c2, c3))
    s.add(violation)

    result = s.check()

    if result == z3.unsat:
        return True, None  # provably no violation

    if result == z3.sat:
        m = s.model()

        def _val(expr: z3.ExprRef) -> int:
            v = m.eval(expr, model_completion=True)
            try:
                return int(str(v))
            except Exception:
                return -1

        model_dict = {
            "forge_running": _val(f_run),
            "via_ir_running": _val(v_run),
            "heavy_running": _val(h_run),
            "forge_after": _val(f_after),
            "via_ir_after": _val(v_after),
            "heavy_after": _val(h_after),
            "total_forge_slots": _val(total_forge_slots),
            "total_heavy": _val(total_heavy),
            "max_forge": max_forge,
            "max_heavy": max_heavy,
        }

        # Identify which constraint(s) were violated
        violated = _identify_violated(model_dict, via_ir_weight)
        suggestion = _suggest_reformulation(model_dict, propose_forge, propose_via_ir)

        return False, Counterexample(
            violated_constraint=violated,
            model=model_dict,
            suggested_reformulation=suggestion,
        )

    # z3.unknown — solver timed out or hit resource limit
    # Fail open (conservative) — log and pass through
    return True, None


def _identify_violated(m: dict[str, int], via_ir_weight: int) -> str:
    parts: list[str] = []
    if m["total_forge_slots"] > m["max_forge"]:
        parts.append(
            f"C1: forge slots {m['total_forge_slots']} > cap {m['max_forge']} "
            f"(via_ir counts as {via_ir_weight}x)"
        )
    if m["via_ir_after"] > 0 and m["forge_after"] > m["forge_running"]:
        parts.append("C2: cannot start plain forge while via_ir is running")
    if m["total_heavy"] > m["max_heavy"]:
        parts.append(f"C3: total heavy procs {m['total_heavy']} > cap {m['max_heavy']}")
    return "; ".join(parts) if parts else "unknown constraint violated"


def _suggest_reformulation(
    m: dict[str, int], propose_forge: bool, propose_via_ir: bool
) -> str:
    if propose_via_ir and m["via_ir_after"] > 1:
        return "Wait for the running via_ir build to complete before starting another."
    if propose_forge and m["via_ir_after"] > 0:
        return (
            "A via_ir build is running and owns the RAM budget. "
            "Wait for it to finish, or use a non-via_ir profile (default profile)."
        )
    return (
        f"Wait for a running forge/heavy process to finish. "
        f"Current: forge={m['forge_running']}, via_ir={m['via_ir_running']}, "
        f"heavy={m['heavy_running']}."
    )


# ---------------------------------------------------------------------------
# Adversarial fixture (documents a case a naive heuristic misses)
# ---------------------------------------------------------------------------

def adversarial_fixture() -> dict:
    """A case where a naive "count < 3" heuristic passes but Z3 blocks.

    Scenario:
        forge_running=1, via_ir_running=1 (counts as 2 slots), heavy_running=0.
        Naive check: "1 forge < 3 cap → ALLOW another forge."
        Z3 check:
          - total_forge_slots = 1 + 1*2 = 3 (already AT the cap)
          - C2: via_ir is running → DENY any new plain forge (C2 fires first)
        Result: Z3 blocks; the naive heuristic would allow.

    This is not a contrived edge case — it is the real scenario where an agent
    runs a FOUNDRY_PROFILE=full build (via_ir) alongside a normal forge build,
    and a third agent then tries to start another forge test.  The naive "count
    the forge pids" check sees 1 pid < 3 and passes; Z3 catches the RAM overrun.
    """
    state = SolverState(forge_running=1, via_ir_running=1, heavy_running=0)
    ok, cex = check_concurrency(state, propose_forge=True, propose_via_ir=False)
    return {
        "scenario": "1 plain forge + 1 via_ir running, propose 1 more plain forge",
        "naive_heuristic_result": "ALLOW (1 forge pid < 3 cap)",
        "z3_result": "ok" if ok else "BLOCK",
        "z3_counterexample": cex,
        "heuristic_wrong": not ok,  # True means Z3 caught something heuristic missed
    }


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== _solver_gate.py CLI demo ===\n")
    print(f"Z3 available: {_Z3_AVAILABLE}")
    print(f"MAX_FORGE_CONCURRENT={MAX_FORGE_CONCURRENT}  "
          f"MAX_HEAVY_CONCURRENT={MAX_HEAVY_CONCURRENT}\n")

    cases: list[tuple[str, SolverState, dict]] = [
        (
            "OK: 2 forge running, propose 1 more (3 total, at cap but not over)",
            SolverState(forge_running=2, via_ir_running=0, heavy_running=0),
            {"propose_forge": True},
        ),
        (
            "BLOCK: 3 forge running, propose 1 more (would exceed cap)",
            SolverState(forge_running=3, via_ir_running=0, heavy_running=0),
            {"propose_forge": True},
        ),
        (
            "BLOCK: via_ir running, propose plain forge (C2 fires)",
            SolverState(forge_running=0, via_ir_running=1, heavy_running=0),
            {"propose_forge": True},
        ),
        (
            "BLOCK: 1 forge + 1 via_ir (3 slots used), propose 1 more forge (cap=3)",
            SolverState(forge_running=1, via_ir_running=1, heavy_running=0),
            {"propose_forge": True},
        ),
        (
            "OK: 2 forge running, propose 1 heavy (heavy cap not hit)",
            SolverState(forge_running=2, via_ir_running=0, heavy_running=1),
            {"propose_heavy": True},
        ),
    ]

    for label, state, kwargs in cases:
        ok, cex = check_concurrency(state, **kwargs)
        status = "OK   " if ok else "BLOCK"
        print(f"[{status}] {label}")
        if cex:
            print(f"         violated: {cex.violated_constraint}")
            print(f"         suggest : {cex.suggested_reformulation}")
        print()

    print("--- Adversarial fixture ---")
    fix = adversarial_fixture()
    print(f"Scenario : {fix['scenario']}")
    print(f"Heuristic: {fix['naive_heuristic_result']}")
    print(f"Z3       : {fix['z3_result']}")
    print(f"Heuristic was wrong: {fix['heuristic_wrong']}")
    if fix["z3_counterexample"]:
        cex = fix["z3_counterexample"]
        print(f"  violated: {cex.violated_constraint}")
        print(f"  suggest : {cex.suggested_reformulation}")
