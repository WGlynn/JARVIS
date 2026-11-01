#!/usr/bin/env python3
"""_solver_gate_hook.py -- LIVE WIRING 2 of the JARVIS non-LLM intelligence architecture.

PreToolUse(Bash) wrapper around _solver_gate.check_concurrency (LOOP 3, Z3-backed sound concurrency
invariant). Where the existing resource-cgroup-gate is a pattern-match heuristic ("count forge pids <
cap"), this adds a PROVABLY SOUND check on the cap arithmetic -- including the via_ir RAM double-weight
on a proposed build, which the naive pid-count misses (see _solver_gate.adversarial_fixture).

Doctrine (LIVE-WIRING-SPEC W2): AUGMENTATION ONLY. Emits the solver's suggested_reformulation via
additionalContext on a would-be violation; it NEVER exit-2 / permissionDecision:deny -- the concurrency
rule is advisory, and the heuristic resource-cgroup-gate remains the hard enforcer. Fail-silent: if z3
is missing or anything raises, emit {} and get out of the way (never block a Bash call).

Coverage boundary (honest): running via_ir builds are NOT distinguished from plain forge at the process
level (tasklist/ps give no cmdline cheaply), so via_ir_running is measured as 0; a PROPOSED via_ir build
IS detected (FOUNDRY_PROFILE=full|deploy / --via-ir) and weighted. So the sound gain is on the proposed
side; the running-via_ir adversarial case defers to the heuristic gate. Documented, not hidden.

Origin: 2026-07-17, LIVE-WIRING-SPEC W2 (Will-approved). Free to copy (build-in-the-open).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from _solver_gate import SolverState, check_concurrency
except Exception:
    SolverState = None
    check_concurrency = None

try:
    from _telemetry import log_event
except Exception:  # telemetry optional
    def log_event(*a, **k):  # type: ignore
        pass

# Mirror resource-cgroup-gate's classifiers (kept in sync deliberately; independent gate, same rule).
FORGE = re.compile(r"\bforge\s+(test|build|coverage|snapshot)\b", re.I)
HEAVY = re.compile(
    r"\b(forge\s+(test|build|coverage|snapshot)|npm\s+run\s+build|vite\s+build|"
    r"cargo\s+(build|test)|pytest)\b",
    re.I,
)
VIA_IR = re.compile(r"(FOUNDRY_PROFILE\s*=\s*(full|deploy)|--via[-_]ir|via_ir\s*=\s*true)", re.I)


def _live_counts() -> tuple[int, int]:
    """(forge_procs, heavy_total) currently running. Mirrors resource-cgroup-gate._live_counts."""
    forge = heavy = 0
    try:
        out = subprocess.run(
            ["tasklist", "/v", "/fo", "csv"], capture_output=True, text=True, timeout=6
        ).stdout
        forge = out.count("forge.exe")
        heavy = forge + out.count("node.exe")
    except Exception:
        try:
            out = subprocess.run(
                ["ps", "-eo", "comm"], capture_output=True, text=True, timeout=6
            ).stdout
            forge = out.count("forge")
            heavy = forge + out.count("vite") + out.count("pytest")
        except Exception:
            return 0, 0
    return forge, heavy


def _emit(obj: dict) -> None:
    print(json.dumps(obj))


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _emit({})
        return
    if payload.get("tool_name") not in (None, "Bash"):
        _emit({})
        return
    cmd = (payload.get("tool_input") or {}).get("command", "")
    if not cmd or not HEAVY.search(cmd):
        _emit({})  # not a heavy/forge spawn -> zero-cost passthrough
        return
    if check_concurrency is None:  # z3/solver unavailable -> defer silently
        _emit({})
        return

    is_forge = bool(FORGE.search(cmd))
    is_via_ir = bool(VIA_IR.search(cmd))
    propose_via_ir = is_forge and is_via_ir
    propose_forge = is_forge and not is_via_ir
    propose_heavy = (not is_forge) and bool(HEAVY.search(cmd))

    forge, heavy = _live_counts()
    state = SolverState(
        forge_running=min(forge, 100),
        via_ir_running=0,  # coverage boundary: running via_ir not distinguished
        heavy_running=max(0, min(heavy - forge, 100)),
    )
    try:
        ok, cex = check_concurrency(
            state,
            propose_forge=propose_forge,
            propose_via_ir=propose_via_ir,
            propose_heavy=propose_heavy,
        )
    except Exception:
        _emit({})  # z3 not installed / solver raised -> never block
        return

    if ok or cex is None:
        _emit({})
        return

    log_event(
        "solver-gate",
        "block-advisory",
        matches=[cex.violated_constraint[:80]],
        meta={"forge": forge, "heavy": heavy, "cmd": cmd[:100]},
    )
    ctx = (
        "[SOLVER-GATE / concurrency invariant (Z3, advisory)]\n\n"
        f"Constraint violated: {cex.violated_constraint}\n"
        f"Suggested reformulation: {cex.suggested_reformulation}\n\n"
        "This is a SOUND check (augmentation, not a block). The heuristic resource gate is the hard "
        "enforcer; proceed only if you have measured headroom."
    )
    _emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": ctx}})


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # A PreToolUse advisory must never break a Bash call.
        try:
            _emit({})
        except Exception:
            pass
    sys.exit(0)
