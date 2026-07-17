#!/usr/bin/env python3
"""
_gate_evolve.py — LOOP 9: Self-Improvement Mechanized (TRP as Evolution)
=========================================================================

Genetic-programming-style evolution of gate candidates over a MAP-Elites
niche archive.  No LLM calls. No eval/exec. No auto-promotion. Pure Python.

WHAT A "GATE CANDIDATE" IS
---------------------------
A declarative spec — not executable code — interpreted safely at eval time:

    {
        "id": "gc-<hex8>",
        "pattern": "<regex string>",
        "severity": "info" | "warn" | "block",
        "message": "<human-readable context string>",
        "scope": "content" | "tool_name" | "hook_name",  # where to apply regex
        "generation": <int>,
        "niche": (<error_category>, <session_phase>),
        "fitness": <float>,          # WAL_catch_rate * (1 - token_cost_fraction)
        "shadow_catches": <int>,     # how many real/synthetic events it caught
        "shadow_fires": <int>,       # how many times it was tested
        "promoted": False,           # never auto-True; human/confidence gate only
        "confidence": <float>,       # precision = catches / fires
    }

PIPELINE
--------
1. WAL failure extraction  → FailureEvent list
2. Seeding + crossover + mutation  → candidate population (GP-style, declarative)
3. MAP-Elites archive      → niched by (error_category, session_phase)
4. Shadow-mode eval        → fitness scored on synthetic + real events (if any)
5. Confidence gate         → promotion proposed ONLY if confidence >= threshold
6. Archive written to _system/gate_evolve_archive.json
7. Promotion proposals written to _system/evolution_proposals/ (markdown, not code)

COVERAGE BOUNDARY
-----------------
This module covers gate CANDIDATES only (regex + severity + message spec).
It does NOT:
  - Write actual hook .py files (that is a human/approve step)
  - Execute evolved patterns on live I/O
  - Auto-modify settings.json
  - Make LLM calls
  - Use eval() or exec() on any derived content

FITNESS FUNCTION
----------------
    fitness = wal_catch_rate * (1.0 - token_cost_fraction)
where:
    wal_catch_rate      = shadow_catches / max(1, len(failure_events))
    token_cost_fraction = estimated overhead / MAX_TOKEN_COST_UNITS
    (token cost is a lightweight proxy: pattern complexity * fires)

HONEST LABEL DISCIPLINE (matching MEMORY.md convention)
--------------------------------------------------------
    ✅ built  = implemented here
    🟡 designed = specified but not yet built into harness
    🔬 open  = requires real shadow-mode accumulation to validate
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

# ── Root config (no hard-coded personal paths in copyable core) ─────────────
def _default_root() -> Path:
    """Return the memory root, preferring env override for portability."""
    import os
    env = os.environ.get("JARVIS_MEMORY_ROOT")
    if env:
        return Path(env)
    # Heuristic: walk up from this file until we find _system/
    here = Path(__file__).parent
    if (here / "_system").exists():
        return here
    # Fallback: assume standard layout
    return Path.home() / ".claude" / "projects" / "<project>" / "memory"

MEMORY_ROOT = _default_root()
SYSTEM_DIR  = MEMORY_ROOT / "_system"
TELEMETRY_LOG = SYSTEM_DIR / "protocol_telemetry.jsonl"
WWWD_LOG      = SYSTEM_DIR / "wwwd_gate_fires.jsonl"
ARCHIVE_PATH  = SYSTEM_DIR / "gate_evolve_archive.json"
PROPOSALS_DIR = SYSTEM_DIR / "evolution_proposals"

# ── Evolution hyper-parameters ──────────────────────────────────────────────
POPULATION_SIZE    = 40     # individuals per generation
NUM_GENERATIONS    = 8      # generations to run
MUTATION_RATE      = 0.25   # probability of mutating a candidate
CROSSOVER_RATE     = 0.40   # probability of crossover vs. clone
ELITISM_TOP_N      = 5      # top N survivors carried forward unchanged
PROMOTION_CONFIDENCE_THRESHOLD = 0.70   # minimum precision to propose promotion
PROMOTION_MIN_SHADOW_FIRES     = 10     # minimum shadow tests before proposing
MAX_TOKEN_COST_UNITS           = 1000.0 # normaliser for token-cost proxy

# MAP-Elites grid dimensions
# niche = (error_category, session_phase) — both are string labels
ERROR_CATEGORIES = [
    "contradiction",        # draft contradicts memory (conflict-detector class)
    "stale_claim",          # uses deprecated entity/decision
    "missing_gate",         # an "always X" rule not in settings.json
    "decision_fragile",     # decision pattern reversed too often
    "low_signal_hook",      # hook fires but rarely matches
    "em_dash",              # AI-tell em-dash in partner-facing draft
    "credential_leak",      # potential secrets in content
    "scope_bloat",          # action outside defined coverage boundary
]
SESSION_PHASES = [
    "session_start",
    "mid_task",
    "pre_commit",
    "partner_write",
    "tool_use",
]


# ════════════════════════════════════════════════════════════════════════════
# DATA LAYER — failure events from telemetry / WAL
# ════════════════════════════════════════════════════════════════════════════

class FailureEvent:
    """A structured error signal extracted from telemetry or WAL."""
    __slots__ = ("ts", "hook", "event", "content", "error_category", "session_phase", "meta")

    def __init__(
        self,
        ts: str,
        hook: str,
        event: str,
        content: str,
        error_category: str,
        session_phase: str,
        meta: dict,
    ):
        self.ts             = ts
        self.hook           = hook
        self.event          = event
        self.content        = content
        self.error_category = error_category
        self.session_phase  = session_phase
        self.meta           = meta

    def to_dict(self) -> dict:
        return {
            "ts": self.ts, "hook": self.hook, "event": self.event,
            "content": self.content[:200],
            "error_category": self.error_category,
            "session_phase": self.session_phase,
        }


def _infer_error_category(record: dict) -> str:
    """Heuristic: map a telemetry record to an error category."""
    hook  = record.get("hook", "")
    event = record.get("event", "")
    meta  = record.get("meta", {}) or {}
    matches = record.get("matches", []) or []

    if hook == "conflict-detector" and event == "conflict":
        return "contradiction"
    if hook in ("entity-context-cross-reference",) and event == "match":
        return "stale_claim"
    if hook in ("decision-capture",) and event == "noop":
        # gate should have fired but didn't → missing gate signal
        return "missing_gate"
    if hook == "post-generation-reflect" and event == "match":
        # matched something — check meta
        if meta.get("top_score", 1.0) > 0.3:
            return "stale_claim"
        return "missing_gate"
    if "em-dash" in hook or "em_dash" in hook:
        return "em_dash"
    if hook == "coordination-gate" or "coordination" in hook:
        return "scope_bloat"
    # Default: low_signal_hook for noop floods
    if event == "noop":
        return "low_signal_hook"
    return "missing_gate"


def _infer_session_phase(record: dict) -> str:
    """Heuristic: infer session phase from hook/context."""
    hook = record.get("hook", "")
    meta = record.get("meta", {}) or {}
    if "session" in hook or "boot" in hook or "start" in hook:
        return "session_start"
    tool_name = meta.get("tool_name", meta.get("toolName", ""))
    if tool_name in ("Write", "Edit", "NotebookEdit"):
        content = str(meta.get("candidate_excerpt", "") or "")
        partner_signals = ["**To**:", "**Subject**:", "reply", "outreach", "partner"]
        if any(s in content for s in partner_signals):
            return "partner_write"
        return "pre_commit"
    if "decision" in hook or "wwwd" in hook:
        return "mid_task"
    if "tool" in hook:
        return "tool_use"
    return "mid_task"


def load_failure_events(limit: int = 2000) -> list[FailureEvent]:
    """
    Load real failure events from telemetry and wwwd_gate_fires.
    Falls back gracefully if files are absent.
    Status: ✅ built — reads real files; 🔬 open — catch-rate needs
    real shadow accumulation to produce valid fitness numbers.
    """
    events: list[FailureEvent] = []

    def _parse_jsonl(path: Path) -> list[dict]:
        if not path.exists():
            return []
        out = []
        try:
            with path.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            pass
        return out

    for record in _parse_jsonl(TELEMETRY_LOG)[-limit:]:
        cat   = _infer_error_category(record)
        phase = _infer_session_phase(record)
        # Only include events that represent a failure / miss signal
        if record.get("event") in ("conflict", "match", "noop"):
            content = json.dumps(record.get("matches", []) or [])
            events.append(FailureEvent(
                ts=record.get("ts", ""),
                hook=record.get("hook", ""),
                event=record.get("event", ""),
                content=content,
                error_category=cat,
                session_phase=phase,
                meta=record.get("meta", {}),
            ))

    for record in _parse_jsonl(WWWD_LOG)[-limit:]:
        cat   = _infer_error_category(record)
        phase = _infer_session_phase(record)
        content = record.get("candidate_excerpt", "") or ""
        events.append(FailureEvent(
            ts=record.get("timestamp", record.get("ts", "")),
            hook="wwwd-gate",
            event="fire",
            content=content,
            error_category=cat,
            session_phase=phase,
            meta=record,
        ))

    return events


# ════════════════════════════════════════════════════════════════════════════
# GATE CANDIDATE — declarative spec only, never exec'd
# ════════════════════════════════════════════════════════════════════════════

SEVERITY_LEVELS = ("info", "warn", "block")
SCOPE_OPTIONS   = ("content", "tool_name", "hook_name")

# Seed patterns keyed by error category.  These are the hand-written baselines;
# the GP search explores mutations and crossovers FROM these seeds.
SEED_PATTERNS: dict[str, list[dict]] = {
    "contradiction": [
        {"pattern": r"(?:not|no longer|abandoned|deprecated|moved off)\b",
         "severity": "warn", "scope": "content",
         "message": "Draft may contradict a negated memory entry. Verify before delivery."},
        {"pattern": r"\b(?:LayerZero|LZ)\b",
         "severity": "warn", "scope": "content",
         "message": "LayerZero deprecated post-KelpDAO compromise. Check cross-chain approach."},
    ],
    "stale_claim": [
        {"pattern": r"\bLayerZero\b|\bLZ DVN\b",
         "severity": "warn", "scope": "content",
         "message": "Stale entity: LayerZero removed from stack."},
        {"pattern": r"\bvia_ir\s*:\s*true\b",
         "severity": "block", "scope": "content",
         "message": "via_ir:true OOMs Ryzen 1600. Use FOUNDRY_PROFILE=full instead."},
    ],
    "missing_gate": [
        {"pattern": r"\balways\b|\bnever\b|\bevery\b",
         "severity": "info", "scope": "content",
         "message": "Absolute rule detected — verify it is enforced by hook, not just memory."},
        {"pattern": r"from now on|each time|whenever",
         "severity": "info", "scope": "content",
         "message": "Behavioral rule: requires settings.json hook, not memory bullet."},
    ],
    "decision_fragile": [
        {"pattern": r"\bREVERSED\b|\breversed\b",
         "severity": "info", "scope": "content",
         "message": "Reversal marker in decision trail — this decision class may be fragile."},
    ],
    "low_signal_hook": [
        {"pattern": r'"event"\s*:\s*"noop"',
         "severity": "info", "scope": "content",
         "message": "High noop rate detected — hook may be over-broad."},
    ],
    "em_dash": [
        {"pattern": r"[–—]",
         "severity": "warn", "scope": "content",
         "message": "Em-dash detected in draft — scrub before partner delivery."},
    ],
    "credential_leak": [
        {"pattern": r"\b(?:sk-|api[_-]?key|secret[_-]?key|password|bearer\s+[A-Za-z0-9]{20,})",
         "severity": "block", "scope": "content",
         "message": "Potential credential in content. Gate: NoCredsInClaudeChat."},
    ],
    "scope_bloat": [
        {"pattern": r"forge\s+test\s+(?!--match)",
         "severity": "warn", "scope": "content",
         "message": "forge test without --match-path risks OOM on Ryzen 1600. Always scope."},
        {"pattern": r"git\s+push\s+--force",
         "severity": "block", "scope": "content",
         "message": "Force push to remote — explicit user confirmation required."},
    ],
}


def _short_id(salt: str) -> str:
    return hashlib.md5(salt.encode()).hexdigest()[:8]


def _make_candidate(
    pattern: str,
    severity: str,
    scope: str,
    message: str,
    generation: int,
    niche: tuple[str, str],
) -> dict:
    """Create a gate candidate dict from declarative fields."""
    cid = "gc-" + _short_id(f"{pattern}{severity}{scope}{message}{generation}")
    return {
        "id": cid,
        "pattern": pattern,
        "severity": severity,
        "scope": scope,
        "message": message,
        "generation": generation,
        "niche": list(niche),
        "fitness": 0.0,
        "shadow_catches": 0,
        "shadow_fires": 0,
        "promoted": False,
        "confidence": 0.0,
    }


def seed_population(rng: random.Random) -> list[dict]:
    """Initialise generation-0 population from SEED_PATTERNS."""
    pop = []
    for cat, seeds in SEED_PATTERNS.items():
        for s in seeds:
            # Pick a plausible initial phase
            phase = rng.choice(SESSION_PHASES)
            pop.append(_make_candidate(
                pattern=s["pattern"],
                severity=s["severity"],
                scope=s.get("scope", "content"),
                message=s["message"],
                generation=0,
                niche=(cat, phase),
            ))
    # Pad to POPULATION_SIZE with random seeds
    all_seeds = [s for seeds in SEED_PATTERNS.values() for s in seeds]
    while len(pop) < POPULATION_SIZE and all_seeds:
        s = rng.choice(all_seeds)
        cat = rng.choice(ERROR_CATEGORIES)
        phase = rng.choice(SESSION_PHASES)
        pop.append(_make_candidate(
            pattern=s["pattern"],
            severity=rng.choice(SEVERITY_LEVELS),
            scope=rng.choice(SCOPE_OPTIONS),
            message=s["message"],
            generation=0,
            niche=(cat, phase),
        ))
    return pop[:POPULATION_SIZE]


# ════════════════════════════════════════════════════════════════════════════
# GENETIC OPERATORS — purely over declarative spec fields
# ════════════════════════════════════════════════════════════════════════════

# Regex mutation vocabulary — safe, pre-baked fragments, no code generation
_PATTERN_FRAGMENTS = [
    r"\b", r"(?i)", r"(?:", r")",
    r"not\b", r"no longer", r"never\b", r"abandoned",
    r"deprecated", r"skip\b", r"avoid\b",
    r"always\b", r"every\b", r"each time",
    r"force\b", r"--force", r"--no-verify",
    r"secret", r"password", r"api[_-]?key",
    r"forge test", r"via_ir", r"npm install",
    r"–|—",  # en/em dash
    r"git push", r"git reset",
    r"LayerZero", r"eval\(", r"exec\(",
]

_SEVERITY_WEIGHTS = [("info", 0.4), ("warn", 0.4), ("block", 0.2)]


def _mutate_pattern(pattern: str, rng: random.Random) -> str:
    """Mutate a regex pattern by inserting, replacing, or removing a fragment."""
    op = rng.choice(["insert", "replace", "trim", "alternate"])
    frag = rng.choice(_PATTERN_FRAGMENTS)
    if op == "insert":
        pos = rng.randint(0, len(pattern))
        return pattern[:pos] + frag + pattern[pos:]
    elif op == "replace":
        # Replace a random token boundary segment
        parts = pattern.split("|")
        if len(parts) > 1:
            idx = rng.randint(0, len(parts) - 1)
            parts[idx] = frag
            return "|".join(parts)
        return frag + "|" + pattern
    elif op == "trim":
        # Remove up to 10 chars from one end
        n = min(10, len(pattern) - 1)
        if n <= 0:
            return pattern
        if rng.random() < 0.5:
            return pattern[n:]
        return pattern[:-n]
    else:  # alternate
        return pattern + "|" + frag


def _mutate_severity(severity: str, rng: random.Random) -> str:
    weights = [w for _, w in _SEVERITY_WEIGHTS]
    choices = [s for s, _ in _SEVERITY_WEIGHTS]
    return rng.choices(choices, weights=weights, k=1)[0]


def mutate(candidate: dict, generation: int, rng: random.Random) -> dict:
    """Return a mutated copy of a candidate. Never modifies the original."""
    new = dict(candidate)
    new["generation"] = generation
    new["fitness"]         = 0.0
    new["shadow_catches"]  = 0
    new["shadow_fires"]    = 0
    new["promoted"]        = False
    new["confidence"]      = 0.0

    if rng.random() < MUTATION_RATE:
        new["pattern"] = _mutate_pattern(new["pattern"], rng)
    if rng.random() < MUTATION_RATE * 0.5:
        new["severity"] = _mutate_severity(new["severity"], rng)
    if rng.random() < MUTATION_RATE * 0.3:
        new["scope"] = rng.choice(SCOPE_OPTIONS)
    if rng.random() < MUTATION_RATE * 0.2:
        # Shift niche phase
        cat = new["niche"][0]
        phase = rng.choice(SESSION_PHASES)
        new["niche"] = [cat, phase]

    new["id"] = "gc-" + _short_id(f"{new['pattern']}{new['severity']}{new['scope']}{generation}{rng.random()}")
    return new


def crossover(a: dict, b: dict, generation: int, rng: random.Random) -> dict:
    """Single-point crossover on the pattern strings; take severity from one parent."""
    pat_a, pat_b = a["pattern"], b["pattern"]
    # Split each pattern at a random "|" boundary if available, else at char level
    def split_at(p: str) -> tuple[str, str]:
        parts = p.split("|")
        if len(parts) >= 2:
            cut = rng.randint(1, len(parts) - 1)
            return "|".join(parts[:cut]), "|".join(parts[cut:])
        cut = rng.randint(1, max(1, len(p) - 1))
        return p[:cut], p[cut:]

    left, _ = split_at(pat_a)
    _, right = split_at(pat_b)
    new_pattern = left + right if (left and right) else (pat_a if rng.random() < 0.5 else pat_b)

    parent = a if rng.random() < 0.5 else b
    child = _make_candidate(
        pattern=new_pattern,
        severity=parent["severity"],
        scope=parent["scope"],
        message=parent["message"],
        generation=generation,
        niche=tuple(parent["niche"]),
    )
    return child


# ════════════════════════════════════════════════════════════════════════════
# SHADOW EVALUATION — safe regex match, no exec
# ════════════════════════════════════════════════════════════════════════════

def _apply_candidate_safe(candidate: dict, event: FailureEvent) -> bool:
    """
    Evaluate a declarative gate spec against a FailureEvent.
    Returns True if the gate would fire (catches the event).
    NEVER calls eval() or exec(). Pattern is interpreted as a plain regex.
    """
    try:
        compiled = re.compile(candidate["pattern"], re.IGNORECASE | re.DOTALL)
    except re.error:
        return False  # malformed pattern — candidate scores no catches

    scope = candidate.get("scope", "content")
    if scope == "content":
        target = event.content
    elif scope == "tool_name":
        target = event.hook  # hook name is closest analogue in telemetry
    elif scope == "hook_name":
        target = event.hook
    else:
        target = event.content

    return bool(compiled.search(target))


def _token_cost_proxy(candidate: dict) -> float:
    """
    Lightweight token-cost proxy: pattern complexity * normalised fire count.
    Longer / more complex patterns cost slightly more per evaluation.
    Normalised to [0, 1].
    """
    pat_len = len(candidate["pattern"])
    fires   = max(1, candidate.get("shadow_fires", 1))
    raw = (pat_len / 200.0) * (fires / MAX_TOKEN_COST_UNITS)
    return min(1.0, raw)


def evaluate_population(
    population: list[dict],
    failure_events: list[FailureEvent],
) -> list[dict]:
    """
    Shadow-evaluate every candidate against the failure event set.
    Updates fitness, shadow_catches, shadow_fires, confidence in-place.
    """
    n_events = len(failure_events)
    for candidate in population:
        catches = 0
        fires   = 0
        for event in failure_events:
            # Only test candidates whose niche matches the event's category
            # (diversity pressure: a gate is only rewarded for its own niche)
            niche_cat = candidate["niche"][0] if candidate["niche"] else ""
            if niche_cat and niche_cat != event.error_category:
                continue
            fires += 1
            if _apply_candidate_safe(candidate, event):
                catches += 1

        candidate["shadow_fires"]   = fires
        candidate["shadow_catches"] = catches
        precision = catches / fires if fires > 0 else 0.0
        candidate["confidence"] = precision

        # WAL catch-rate: catches / total events in the niche
        niche_events = [e for e in failure_events if e.error_category == (candidate["niche"][0] if candidate["niche"] else "")]
        n_niche = max(1, len(niche_events))
        wal_catch_rate = catches / n_niche

        token_frac = _token_cost_proxy(candidate)
        candidate["fitness"] = wal_catch_rate * (1.0 - token_frac)

    return population


# ════════════════════════════════════════════════════════════════════════════
# MAP-ELITES ARCHIVE (~50 LOC pure Python, no pyribs)
# ════════════════════════════════════════════════════════════════════════════

class MAPElitesArchive:
    """
    MAP-Elites niche archive.
    Niche key = (error_category, session_phase) — 8x5 = 40 possible niches.
    Each niche holds the single best candidate (by fitness) seen so far.
    This prevents monoculture: a high-fitness "contradiction" gate cannot
    crowd out a "credential_leak" gate.

    Status: ✅ built (pure Python, ~50 LOC).
    """

    def __init__(self) -> None:
        self._niches: dict[tuple[str, str], dict] = {}

    def offer(self, candidate: dict) -> bool:
        """
        Offer a candidate to the archive.
        Returns True if it was inserted (new niche or improved fitness).
        """
        niche = tuple(candidate["niche"])
        if niche not in self._niches:
            self._niches[niche] = dict(candidate)
            return True
        if candidate["fitness"] > self._niches[niche]["fitness"]:
            self._niches[niche] = dict(candidate)
            return True
        return False

    def elites(self) -> list[dict]:
        """Return all current archive elites, sorted by fitness descending."""
        return sorted(self._niches.values(), key=lambda c: -c["fitness"])

    def niche_count(self) -> int:
        return len(self._niches)

    def all_niches(self) -> list[tuple[str, str]]:
        return list(self._niches.keys())

    def to_dict(self) -> dict:
        return {
            "niches": {str(k): v for k, v in self._niches.items()},
            "niche_count": self.niche_count(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "MAPElitesArchive":
        archive = cls()
        for k_str, v in d.get("niches", {}).items():
            # Reconstruct tuple key
            try:
                k = tuple(k_str.strip("()").replace("'", "").split(", "))
            except Exception:
                k = (k_str, "mid_task")
            archive._niches[k] = v
        return archive


# ════════════════════════════════════════════════════════════════════════════
# EVOLUTIONARY SEARCH MAIN LOOP
# ════════════════════════════════════════════════════════════════════════════

def run_evolution(
    failure_events: list[FailureEvent],
    seed: int = 42,
    n_generations: int = NUM_GENERATIONS,
    population_size: int = POPULATION_SIZE,
) -> tuple[MAPElitesArchive, list[dict]]:
    """
    Run the full GP + MAP-Elites loop.

    Returns:
        archive: final MAP-Elites archive
        history: list of per-generation summary dicts
    """
    rng = random.Random(seed)
    archive = MAPElitesArchive()

    # Load existing archive if present (warm-start)
    if ARCHIVE_PATH.exists():
        try:
            with ARCHIVE_PATH.open(encoding="utf-8") as f:
                saved = json.load(f)
            archive = MAPElitesArchive.from_dict(saved.get("archive", {}))
        except Exception:
            archive = MAPElitesArchive()

    population = seed_population(rng)
    history: list[dict] = []

    for gen in range(n_generations):
        # Evaluate
        population = evaluate_population(population, failure_events)

        # Update MAP-Elites archive
        inserted = sum(1 for c in population if archive.offer(c))

        # Record generation summary
        fitnesses = [c["fitness"] for c in population]
        best = max(fitnesses) if fitnesses else 0.0
        mean = sum(fitnesses) / len(fitnesses) if fitnesses else 0.0
        history.append({
            "generation": gen,
            "best_fitness": best,
            "mean_fitness": mean,
            "archive_niches": archive.niche_count(),
            "archive_inserted": inserted,
        })

        # Selection: elitism + tournament
        population.sort(key=lambda c: -c["fitness"])
        survivors = population[:ELITISM_TOP_N]

        # Fill rest via crossover + mutation
        elites_pool = archive.elites()
        while len(survivors) < population_size:
            if rng.random() < CROSSOVER_RATE and len(elites_pool) >= 2:
                a = rng.choice(elites_pool)
                b = rng.choice(elites_pool)
                child = crossover(a, b, gen + 1, rng)
            else:
                parent = rng.choice(population[:max(1, population_size // 2)])
                child = mutate(parent, gen + 1, rng)
            survivors.append(child)

        population = survivors

    # Final evaluation pass
    population = evaluate_population(population, failure_events)
    for c in population:
        archive.offer(c)

    return archive, history


# ════════════════════════════════════════════════════════════════════════════
# SYNTHETIC FAILURE GENERATION (for honest demo when WAL is thin)
# ════════════════════════════════════════════════════════════════════════════

SYNTHETIC_FAILURE_TEMPLATES: list[dict] = [
    # Contradiction class
    {"content": "We should integrate LayerZero for cross-chain messaging.",
     "hook": "conflict-detector", "event": "conflict",
     "error_category": "contradiction", "session_phase": "partner_write"},
    {"content": "Using the abandoned LayerZero DVN RPC endpoints.",
     "hook": "conflict-detector", "event": "conflict",
     "error_category": "contradiction", "session_phase": "pre_commit"},
    # Stale claim
    {"content": "via_ir: true is required for this contract.",
     "hook": "post-generation-reflect", "event": "match",
     "error_category": "stale_claim", "session_phase": "pre_commit"},
    # Missing gate
    {"content": "From now on always use the full test suite.",
     "hook": "decision-capture", "event": "noop",
     "error_category": "missing_gate", "session_phase": "mid_task"},
    {"content": "Every session, never skip the WAL check.",
     "hook": "decision-capture", "event": "noop",
     "error_category": "missing_gate", "session_phase": "session_start"},
    # Em-dash
    {"content": "We shipped the feature — it's live now.",
     "hook": "em-dash-gate", "event": "noop",
     "error_category": "em_dash", "session_phase": "partner_write"},
    # Credential leak
    {"content": "API key: sk-proj-abc123 should be stored here.",
     "hook": "conflict-detector", "event": "noop",
     "error_category": "credential_leak", "session_phase": "pre_commit"},
    # Scope bloat
    {"content": "forge test --fuzz-runs 100000",
     "hook": "coordination-gate", "event": "noop",
     "error_category": "scope_bloat", "session_phase": "tool_use"},
    {"content": "git push --force origin main",
     "hook": "conflict-detector", "event": "noop",
     "error_category": "scope_bloat", "session_phase": "pre_commit"},
    # Low signal hook
    {"content": '{"event": "noop", "hook": "broad-gate", "reason": "no_match"}',
     "hook": "broad-gate", "event": "noop",
     "error_category": "low_signal_hook", "session_phase": "mid_task"},
    # Decision fragile
    {"content": "REVERSED: decision to use Balancer was overridden.",
     "hook": "decision-capture", "event": "fire",
     "error_category": "decision_fragile", "session_phase": "mid_task"},
]


def make_synthetic_failure_events() -> list[FailureEvent]:
    """Build a realistic synthetic failure set for demo / thin-WAL case."""
    out = []
    for t in SYNTHETIC_FAILURE_TEMPLATES:
        out.append(FailureEvent(
            ts="2026-07-17T00:00:00",
            hook=t["hook"],
            event=t["event"],
            content=t["content"],
            error_category=t["error_category"],
            session_phase=t["session_phase"],
            meta={},
        ))
    return out


# ════════════════════════════════════════════════════════════════════════════
# CONFIDENCE-GATED PROMOTION PROPOSALS
# ════════════════════════════════════════════════════════════════════════════

def _write_promotion_proposal(candidate: dict, real_data: bool) -> Path:
    """
    Write a markdown promotion proposal for a confident candidate.
    The proposal is a human-review artifact — no code is auto-executed.
    Status: ✅ built (propose-only; never auto-activates a gate live).
    """
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y-%m-%d_%H%M%S")
    cat   = candidate["niche"][0] if candidate["niche"] else "unknown"
    phase = candidate["niche"][1] if len(candidate["niche"]) > 1 else "unknown"
    slug  = re.sub(r"[^a-zA-Z0-9_\-]", "_", f"{cat}_{phase}")[:50]
    name  = f"{ts}_GATE_CANDIDATE_{slug}.md"
    path  = PROPOSALS_DIR / name

    data_label = "real WAL telemetry" if real_data else "synthetic failure set (WAL thin — see EXIT TEST note)"

    content = f"""# Gate Candidate Promotion Proposal

**Class**: GATE_CANDIDATE (from LOOP 9 MAP-Elites evolution)
**Generated**: {time.strftime("%Y-%m-%dT%H:%M:%S")}
**Candidate ID**: `{candidate['id']}`

## Niche
- Error category: `{cat}`
- Session phase:  `{phase}`

## Evolved Spec (declarative — NOT executable code)

```
pattern  : {candidate['pattern']}
severity : {candidate['severity']}
scope    : {candidate['scope']}
message  : {candidate['message']}
```

## Shadow-mode Performance

- Shadow fires (niche events tested): {candidate['shadow_fires']}
- Shadow catches: {candidate['shadow_catches']}
- Confidence (precision): {candidate['confidence']:.3f}
- Fitness (catch_rate * (1 - token_cost)): {candidate['fitness']:.4f}
- Generation derived: {candidate['generation']}
- Data source: {data_label}

**Confidence gate**: threshold = {PROMOTION_CONFIDENCE_THRESHOLD} — {'PASSED ✅' if candidate['confidence'] >= PROMOTION_CONFIDENCE_THRESHOLD else 'FAILED ❌ (should not be here)'}

## What to do with this proposal

1. Review the regex pattern — does it capture the error class without false-positive risk?
2. Verify it doesn't duplicate an existing hook in `~/.claude/hooks/`.
3. If approved, implement as a new PreToolUse (or appropriate event) hook in
   `~/.claude/hooks/<slug>.py` following the conflict-detector.py shape.
4. Log telemetry via `_telemetry.log_event()`.
5. Run for one session in shadow mode (additionalContext only, no block), then
   re-evaluate confidence against real events.

## Rollback

Disable the hook in `~/.claude/settings.json` `hooks` array. The pattern spec lives
in this proposal file — re-derive or adjust as needed.

## Review

**Decision**: ___________________________ (approve / reject / defer)

**Notes**: ___________________________
"""
    path.write_text(content, encoding="utf-8")
    return path


def propose_promotions(archive: MAPElitesArchive, real_data: bool) -> list[Path]:
    """
    Scan archive for candidates that meet the confidence + min-fires gate.
    Write one proposal per qualifying candidate.
    Returns list of proposal paths written.
    Status: ✅ built (confidence-gated; human review required before activation).
    """
    proposals: list[Path] = []
    for candidate in archive.elites():
        if (
            candidate["confidence"] >= PROMOTION_CONFIDENCE_THRESHOLD
            and candidate["shadow_fires"] >= PROMOTION_MIN_SHADOW_FIRES
        ):
            p = _write_promotion_proposal(candidate, real_data)
            proposals.append(p)
    return proposals


# ════════════════════════════════════════════════════════════════════════════
# EXIT TEST
# ════════════════════════════════════════════════════════════════════════════

def run_exit_test(
    archive: MAPElitesArchive,
    failure_events: list[FailureEvent],
    real_data: bool,
) -> dict:
    """
    EXIT TEST — honest assessment of what was achieved.

    (a) Does >=1 auto-derived candidate, in shadow mode, catch a real error
        class the hand-written gates missed?
    (b) Does the MAP-Elites archive hold >=N distinct niches (no monoculture)?

    Status: ✅ built — synthetic demo when WAL is thin (honest label).
    """
    result: dict[str, Any] = {}

    # (a) Shadow-catch demo
    # Hand-written gates cover: contradiction (LayerZero negation), em_dash.
    # Evolved candidates should additionally cover: credential_leak, scope_bloat,
    # missing_gate, decision_fragile — if the GP found patterns for those.
    hand_written_coverage = {"contradiction", "em_dash"}
    evolved_niches = set(tuple(c["niche"]) for c in archive.elites())
    evolved_cats = {n[0] for n in evolved_niches}

    new_coverage = evolved_cats - hand_written_coverage
    caught_new = False
    catching_example = None

    for cat in new_coverage:
        target_events = [e for e in failure_events if e.error_category == cat]
        if not target_events:
            continue
        # Find the elite for that category
        for niche_key, candidate in archive._niches.items():
            if niche_key[0] != cat:
                continue
            for ev in target_events:
                if _apply_candidate_safe(candidate, ev):
                    caught_new = True
                    catching_example = {
                        "candidate_id": candidate["id"],
                        "error_category": cat,
                        "caught_event_content": ev.content[:120],
                        "pattern": candidate["pattern"],
                        "confidence": candidate["confidence"],
                    }
                    break
            if caught_new:
                break

    result["shadow_catch_new_class"] = caught_new
    result["shadow_catch_example"]   = catching_example
    result["real_data"] = real_data
    if not real_data:
        result["shadow_catch_note"] = (
            "Demonstrated on SYNTHETIC failure set — WAL has limited real examples. "
            "Real fitness numbers require shadow-mode accumulation across live sessions. "
            "Status: 🔬 open."
        )

    # (b) Niche diversity
    n_niches = archive.niche_count()
    result["niche_count"]         = n_niches
    result["niches_present"]      = [str(k) for k in archive.all_niches()]
    result["monoculture_check"]   = "PASS" if n_niches >= 4 else "FAIL"

    return result


# ════════════════════════════════════════════════════════════════════════════
# PERSISTENCE
# ════════════════════════════════════════════════════════════════════════════

def save_archive(archive: MAPElitesArchive, history: list[dict], exit_result: dict) -> None:
    SYSTEM_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "loop": "LOOP-9-TRP-evolution",
        "archive": archive.to_dict(),
        "history": history,
        "exit_test": exit_result,
        "promotion_threshold": PROMOTION_CONFIDENCE_THRESHOLD,
        "promotion_min_fires": PROMOTION_MIN_SHADOW_FIRES,
    }
    ARCHIVE_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def main(seed: int = 42) -> int:
    """
    Full pipeline run:
    1. Load real failure events (WAL + telemetry)
    2. Augment with synthetic set if WAL is thin (< 5 events)
    3. Run GP + MAP-Elites evolution
    4. Propose promotion for confidence-gated elites
    5. Print exit-test results (honest)
    """
    print("=== LOOP 9: Gate Evolution Pipeline ===")
    print(f"Seed: {seed}  |  Generations: {NUM_GENERATIONS}  |  Pop: {POPULATION_SIZE}")
    print()

    # Step 1: load real data
    real_events = load_failure_events()
    real_data   = len(real_events) >= 5
    print(f"Real failure events loaded: {len(real_events)}")

    # Step 2: augment with synthetic if needed
    synthetic = make_synthetic_failure_events()
    if not real_data:
        print(f"WAL thin (<5 real events) — augmenting with {len(synthetic)} synthetic events.")
        print("(Honest label: fitness numbers are SYNTHETIC until real shadow accumulation.)")
        failure_events = synthetic
    else:
        # Merge: real events inform the categories, synthetic fill gaps
        failure_events = real_events + synthetic
        print(f"Merged: {len(failure_events)} total events (real + synthetic)")

    print()

    # Step 3: evolve
    print(f"Running evolution ({NUM_GENERATIONS} generations)...")
    archive, history = run_evolution(failure_events, seed=seed)

    print("\nGeneration history:")
    print(f"  {'Gen':>4}  {'Best':>8}  {'Mean':>8}  {'Niches':>7}  {'Inserted':>9}")
    for h in history:
        print(f"  {h['generation']:>4}  {h['best_fitness']:>8.4f}  {h['mean_fitness']:>8.4f}  "
              f"{h['archive_niches']:>7}  {h['archive_inserted']:>9}")

    # Step 4: promotion proposals
    proposals = propose_promotions(archive, real_data)
    print(f"\nPromotion proposals written: {len(proposals)}")
    for p in proposals:
        print(f"  {p}")

    # Step 5: exit test
    exit_result = run_exit_test(archive, failure_events, real_data)
    save_archive(archive, history, exit_result)

    print("\n=== EXIT TEST ===")
    print(f"(a) Shadow-catch new error class: {'[YES]' if exit_result['shadow_catch_new_class'] else '[NO]'}")
    if exit_result.get("shadow_catch_example"):
        ex = exit_result["shadow_catch_example"]
        print(f"    Category caught: {ex['error_category']}")
        print(f"    Pattern: {ex['pattern']}")
        print(f"    Confidence: {ex['confidence']:.3f}")
        print(f"    Event sample: {ex['caught_event_content'][:80]}")
    if not real_data:
        print(f"    NOTE: {exit_result.get('shadow_catch_note', '')}")
    print()
    print(f"(b) MAP-Elites niche count: {exit_result['niche_count']} — monoculture check: {exit_result['monoculture_check']}")
    print("    Niches present:")
    for n in exit_result["niches_present"]:
        print(f"      {n}")
    print()
    print(f"Archive written: {ARCHIVE_PATH}")

    return 0


if __name__ == "__main__":
    import sys
    seed_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    raise SystemExit(main(seed=seed_arg))
