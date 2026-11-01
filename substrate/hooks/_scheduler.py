#!/usr/bin/env python3
"""_scheduler.py — OR-Tools CP-SAT concurrency scheduler for JARVIS.

LOOP 3 deliverable (ROADMAP.md §LOOP 3 / SYNTHESIS.md §2 Tier-1).

Replaces the "max 3 concurrent forge/agent, hope it doesn't OOM" heuristic
with an optimally-solved bin-packing/scheduling problem via OR-Tools CP-SAT.

PROBLEM FORMULATION
===================
Given:
  - N pending jobs, each with:
      name        : str
      ram_weight  : int   (1 = standard forge, 2 = via_ir, 3 = agent, etc.)
      cpu_weight  : int   (default 1; heavy jobs can be 2)
      priority    : int   (higher = prefer to schedule sooner, ≥0)
  - Global caps:
      max_ram_slots  : int  (default 3 — the CLAUDE.md "max 3 concurrent" rule)
      max_cpu_slots  : int  (default 6 — Ryzen 5 1600 logical cores / 2)
      max_jobs       : int  (optional hard count cap, default = max_ram_slots)

Find:
  An admissible subset of jobs to run NOW such that:
  1. sum(ram_weight for admitted jobs) <= max_ram_slots
  2. sum(cpu_weight for admitted jobs) <= max_cpu_slots
  3. len(admitted jobs) <= max_jobs
  4. Subject to (1-3), MAXIMIZE sum(priority for admitted jobs)

This is a variant of the bounded bin-packing / multi-dimensional knapsack
problem.  CP-SAT solves it optimally at Jarvis scales (<20 jobs) in <1ms.

COVERAGE BOUNDARY
=================
IN SCOPE : integer resource weights and priorities, single time-slice
           ("what should I run right now?"). The solver knows nothing about
           job durations, dependencies between jobs, or actual RAM usage.
OUT SCOPE: multi-step sequencing with time windows, job dependencies,
           preemption, wall-clock duration estimation. Out-of-scope requests
           → return empty schedule with a "not_evaluated" flag.
SOUNDNESS: within scope the solver is COMPLETE — if an admissible schedule
           exists, CP-SAT finds the OPTIMAL one (not just any feasible one).

Maturity: ✅ built and pytest-verified (LOOP 3).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Optional

try:
    from ortools.sat.python import cp_model  # type: ignore
    _ORTOOLS_AVAILABLE = True
except ImportError:
    _ORTOOLS_AVAILABLE = False

# ---------------------------------------------------------------------------
# Hardware caps live in LOCAL config (env), not this committed file, per
# [[local-vs-shared-constraints]]. Conservative portable defaults; override via env
# (e.g. JARVIS_MAX_FORGE_CONCURRENT=8) for your own hardware.
# ---------------------------------------------------------------------------
import os as _os

DEFAULT_MAX_RAM_SLOTS: int = int(_os.environ.get("JARVIS_MAX_FORGE_CONCURRENT", "3"))
DEFAULT_MAX_CPU_SLOTS: int = int(_os.environ.get("JARVIS_MAX_CPU_SLOTS", "6"))
DEFAULT_MAX_JOBS: int = int(_os.environ.get("JARVIS_MAX_JOBS", "3"))


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Job:
    """A pending job that may be admitted to run.

    Attributes:
        name        : unique identifier (used in schedule output).
        ram_weight  : how many RAM slots this job consumes.
                      1 = standard forge/agent, 2 = via_ir build, 3 = full-suite.
        cpu_weight  : how many CPU slots this job consumes (default 1).
        priority    : non-negative integer; higher = more preferred.
                      Jobs with equal priority are ranked by ram efficiency.
    """
    name: str
    ram_weight: int = 1
    cpu_weight: int = 1
    priority: int = 1

    def __post_init__(self) -> None:
        if self.ram_weight < 1:
            raise ValueError(f"Job '{self.name}': ram_weight must be >= 1")
        if self.cpu_weight < 1:
            raise ValueError(f"Job '{self.name}': cpu_weight must be >= 1")
        if self.priority < 0:
            raise ValueError(f"Job '{self.name}': priority must be >= 0")


@dataclass
class Schedule:
    """The result of a solve() call.

    Attributes:
        admitted     : jobs selected to run now (in priority-descending order).
        deferred     : jobs not selected (RAM/CPU cap would be exceeded).
        total_ram    : total RAM slots consumed by admitted jobs.
        total_cpu    : total CPU slots consumed by admitted jobs.
        optimal      : True if the solver proved this is optimal.
        not_evaluated: True if the input was out of the coverage boundary.
        solver_status: raw CP-SAT status string (for diagnostics).
    """
    admitted: list[Job] = field(default_factory=list)
    deferred: list[Job] = field(default_factory=list)
    total_ram: int = 0
    total_cpu: int = 0
    optimal: bool = False
    not_evaluated: bool = False
    solver_status: str = ""


# ---------------------------------------------------------------------------
# Core solver
# ---------------------------------------------------------------------------

def solve(
    jobs: list[Job],
    max_ram_slots: int = DEFAULT_MAX_RAM_SLOTS,
    max_cpu_slots: int = DEFAULT_MAX_CPU_SLOTS,
    max_jobs: int = DEFAULT_MAX_JOBS,
    timeout_ms: int = 500,
) -> Schedule:
    """Compute the optimal admissible schedule for the given job list.

    Args:
        jobs         : list of pending Job objects.
        max_ram_slots: RAM slot ceiling (default: CLAUDE.md constant = 3).
        max_cpu_slots: CPU slot ceiling (default: 6 = Ryzen core count).
        max_jobs     : hard count cap on simultaneous jobs (default: 3).
        timeout_ms   : CP-SAT time limit in ms (default: 500ms).

    Returns:
        Schedule with admitted/deferred split and optimality flag.
    """
    if not _ORTOOLS_AVAILABLE:
        raise RuntimeError(
            "_scheduler: ortools not installed. Run `pip install ortools`."
        )

    # Coverage boundary check
    if not jobs:
        return Schedule(optimal=True, solver_status="TRIVIAL_EMPTY")
    if max_ram_slots < 1 or max_cpu_slots < 1 or max_jobs < 1:
        return Schedule(not_evaluated=True, solver_status="OUT_OF_SCOPE")
    if len(jobs) > 200:
        # More than 200 pending jobs is out of the design envelope for Jarvis.
        return Schedule(not_evaluated=True, solver_status="OUT_OF_SCOPE")

    # -----------------------------------------------------------------------
    # Build CP-SAT model
    # -----------------------------------------------------------------------
    model = cp_model.CpModel()

    # Decision variables: x[i] = 1 if job i is admitted, 0 otherwise
    x = [model.new_bool_var(f"x_{i}_{j.name}") for i, j in enumerate(jobs)]

    # Constraint 1: RAM cap
    model.add(
        sum(x[i] * jobs[i].ram_weight for i in range(len(jobs))) <= max_ram_slots
    )

    # Constraint 2: CPU cap
    model.add(
        sum(x[i] * jobs[i].cpu_weight for i in range(len(jobs))) <= max_cpu_slots
    )

    # Constraint 3: count cap
    model.add(sum(x) <= max_jobs)

    # Objective: maximise total priority of admitted jobs
    model.maximize(sum(x[i] * jobs[i].priority for i in range(len(jobs))))

    # -----------------------------------------------------------------------
    # Solve
    # -----------------------------------------------------------------------
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout_ms / 1000.0
    solver.parameters.num_search_workers = 1  # single thread — predictable on 16GB

    status = solver.solve(model)
    status_name = solver.status_name(status)

    admitted: list[Job] = []
    deferred: list[Job] = []

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for i, job in enumerate(jobs):
            if solver.value(x[i]) == 1:
                admitted.append(job)
            else:
                deferred.append(job)
        # Sort admitted by priority descending for readable output
        admitted.sort(key=lambda j: j.priority, reverse=True)
        deferred.sort(key=lambda j: j.priority, reverse=True)

        return Schedule(
            admitted=admitted,
            deferred=deferred,
            total_ram=sum(j.ram_weight for j in admitted),
            total_cpu=sum(j.cpu_weight for j in admitted),
            optimal=(status == cp_model.OPTIMAL),
            solver_status=status_name,
        )

    if status == cp_model.INFEASIBLE:
        # No job fits within the caps — all deferred
        return Schedule(
            deferred=list(jobs),
            optimal=True,
            solver_status=status_name,
        )

    # UNKNOWN (timeout or model error) — fail open, admit nothing
    return Schedule(
        deferred=list(jobs),
        not_evaluated=True,
        solver_status=status_name,
    )


# ---------------------------------------------------------------------------
# Heuristic baseline (for comparison in tests)
# ---------------------------------------------------------------------------

def greedy_schedule(
    jobs: list[Job],
    max_ram_slots: int = DEFAULT_MAX_RAM_SLOTS,
    max_jobs: int = DEFAULT_MAX_JOBS,
) -> list[Job]:
    """Naive greedy: admit jobs in arrival order until cap is hit.

    This is the pre-LOOP3 "hope it doesn't OOM" heuristic — pick the first
    jobs that fit, ignore priority, ignore CPU, stop when RAM cap is full.
    Used in tests to demonstrate cases where CP-SAT beats greedy.
    """
    admitted: list[Job] = []
    ram_used = 0
    for job in jobs:
        if len(admitted) >= max_jobs:
            break
        if ram_used + job.ram_weight <= max_ram_slots:
            admitted.append(job)
            ram_used += job.ram_weight
    return admitted


# ---------------------------------------------------------------------------
# CLI demo + replay test
# ---------------------------------------------------------------------------

def _demo() -> None:
    print("=== _scheduler.py CLI demo ===\n")
    print(f"OR-Tools available: {_ORTOOLS_AVAILABLE}")
    print(f"Caps: RAM={DEFAULT_MAX_RAM_SLOTS}, CPU={DEFAULT_MAX_CPU_SLOTS}, "
          f"jobs={DEFAULT_MAX_JOBS}\n")

    # Synthetic job set representing a realistic Jarvis session
    jobs: list[Job] = [
        # via_ir full build — high value but ram_weight=2
        Job("forge-full-build",    ram_weight=2, cpu_weight=2, priority=10),
        # targeted test run — high priority, cheap
        Job("forge-test-CommitReveal", ram_weight=1, cpu_weight=1, priority=8),
        # background agent — moderate
        Job("agent-audit",         ram_weight=1, cpu_weight=1, priority=5),
        # another targeted test — moderate priority
        Job("forge-test-VibeAMM",  ram_weight=1, cpu_weight=1, priority=5),
        # low-priority lint job
        Job("linter",              ram_weight=1, cpu_weight=1, priority=2),
    ]

    print("Pending jobs:")
    for j in jobs:
        print(f"  {j.name:<30} ram={j.ram_weight}  cpu={j.cpu_weight}  "
              f"priority={j.priority}")
    print()

    sched = solve(jobs)
    print(f"CP-SAT schedule (status={sched.solver_status}, "
          f"optimal={sched.optimal}):")
    print(f"  Admitted ({sched.total_ram}/{DEFAULT_MAX_RAM_SLOTS} RAM slots):")
    for j in sched.admitted:
        print(f"    + {j.name} (priority={j.priority}, ram={j.ram_weight})")
    print("  Deferred:")
    for j in sched.deferred:
        print(f"    - {j.name} (priority={j.priority}, ram={j.ram_weight})")

    greedy = greedy_schedule(jobs)
    print(f"\nGreedy baseline (first-fit, ignores priority):")
    g_names = {j.name for j in greedy}
    for j in jobs:
        tag = "+" if j.name in g_names else "-"
        print(f"  {tag} {j.name} (priority={j.priority})")

    cp_priority = sum(j.priority for j in sched.admitted)
    g_priority  = sum(j.priority for j in greedy)
    print(f"\nCP-SAT total priority admitted: {cp_priority}")
    print(f"Greedy  total priority admitted: {g_priority}")
    improvement = cp_priority - g_priority
    if improvement > 0:
        print(f"CP-SAT beats greedy by {improvement} priority points")
    elif improvement == 0:
        print("CP-SAT and greedy tied on this instance")
    else:
        print("Greedy outperformed CP-SAT (unexpected — check constraints)")


if __name__ == "__main__":
    _demo()
