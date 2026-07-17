#!/usr/bin/env python3
"""_outcome_recorder.py -- LIVE WIRING 1 of the JARVIS non-LLM intelligence architecture.

Turns gate warnings into real (strength, confidence) evidence per gate, by tagging the OUTCOME of
each warning: did the next edit to the same target act on it, or ignore it? This is the convergent
unlock for LOOP 2 (exit test), LOOP 5 (calibration) and LOOP 7 (attention allocator). The offline
classification logic lives in memory/_outcome_probe.py + _truthvalue.py; THIS file is the live hook
that feeds it real data.

Design (why PostToolUse, not PreToolUse as the spec first sketched)
------------------------------------------------------------------
A PreToolUse hook cannot see whether SIBLING PreToolUse gates warned on the same write -- hooks run
independently and don't receive each other's stdout. So we take the producer signal from the one
place gates already record their fires synchronously: the telemetry log
(_system/protocol_telemetry.jsonl, written by _telemetry.log_event). PostToolUse runs strictly AFTER
all PreToolUse gates for a tool call have flushed telemetry, so "which gates warned on THIS write" is
knowable and race-free. Resolution latency is unchanged (a warning is resolved by the NEXT write to
the same target, exactly as a PreToolUse design would give).

Two responsibilities, every Write|Edit (both fail-silent -- this hook NEVER blocks or raises):
  1. RESOLVE: if an earlier turn recorded an open warning for this target, classify it against the
     content just written (applied / ignored / no-signal) and append the outcome to
     _system/gate_reliability.jsonl, feeding per-gate TruthValue.
  2. RECORD: read telemetry fires that occurred since the last checkpoint, attribute them to this
     target, and stash them in _system/outcome_pending.json for the next write to resolve.

Cross-event state is a file (outcome_pending.json), keyed by absolute target path -- never memory.
Copyable: root = $JARVIS_MEMORY_ROOT else the default memory dir.

Origin: 2026-07-17, LIVE-WIRING-SPEC W1 (Will-approved 2026-07-17 "approve then next loop").
Free to copy (JARVIS non-LLM intelligence architecture, build-in-the-open).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# ── Roots (copyable: env override else default single-user path) ─────────────
# NOTE: a Path object is ALWAYS truthy, so `Path(env or "") or default` would silently pick
# Path("")==cwd when the env var is unset. Guard on the string, not the Path.
_env_root = os.environ.get("JARVIS_MEMORY_ROOT", "").strip()
_MEM = Path(_env_root) if _env_root else (
    Path.home() / ".claude" / "projects" / "<project>" / "memory"
)
_SYS = _MEM / "_system"
_TELEMETRY = _SYS / "protocol_telemetry.jsonl"
_PENDING = _SYS / "outcome_pending.json"
_RELIABILITY = _SYS / "gate_reliability.jsonl"

# Attribute telemetry fires to a write only if they are recent (guards against a stale checkpoint
# sweeping in a huge backlog on first run) and newer than the last checkpoint we processed.
_FIRE_WINDOW_SEC = 30
# Telemetry events that count as "a warning was emitted". "noop"/"error" do not.
_NON_FIRE_EVENTS = {"noop", "error", "match"}

# Make the offline logic importable (memory/_outcome_probe.py, _truthvalue.py).
sys.path.insert(0, str(_MEM))
try:
    from _outcome_probe import classify_outcome, outcome_to_evidence  # noqa: E402
except Exception:  # no-cover: if logic missing, degrade to no-op
    classify_outcome = None
    outcome_to_evidence = None


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _target_of(tool_input: dict) -> str | None:
    fp = tool_input.get("file_path") or tool_input.get("filePath") or tool_input.get("path")
    if not fp:
        return None
    try:
        return str(Path(fp).resolve())
    except Exception:
        return str(fp)


def _content_of(tool_input: dict) -> str:
    # Write -> content ; Edit -> new_string (the text now present at the target)
    return str(
        tool_input.get("content")
        or tool_input.get("new_string")
        or tool_input.get("newString")
        or ""
    )


def _flagged_tokens(matches) -> list[str]:
    """Extract candidate flagged snippets from a telemetry fire's `matches`.

    conflict-detector logs matches as "Entity:file.md" -> the entity token is the flagged content
    (typically a substring of the draft). Generic rule: take the part before the first ':' if any,
    else the whole match. Dedup, keep order.
    """
    out: list[str] = []
    for m in (matches or []):
        tok = str(m).split(":", 1)[0].strip()
        if tok and tok not in out:
            out.append(tok)
    return out[:20]


_MAX_SCAN = 400  # bound the work: never parse more than this many trailing telemetry lines


def _recent_fires(last_count: int) -> tuple[dict[str, list[str]], int]:
    """Return {gate -> flagged_tokens} for telemetry fires appended since the last checkpoint, plus
    the new line-count checkpoint.

    Checkpoint is a LINE COUNT, not a timestamp: telemetry is append-only, so its length is
    monotonic, and this correctly distinguishes several fires that share one wall-clock second (a
    write burst). Guards: a recency window drops anything older than _FIRE_WINDOW_SEC (so a fresh
    checkpoint on a large pre-existing log, or a post-rotation reset, never sweeps in ancient fires),
    and work is bounded to the last _MAX_SCAN lines.
    """
    fires: dict[str, list[str]] = {}
    if not _TELEMETRY.exists():
        return fires, last_count
    try:
        lines = _TELEMETRY.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return fires, last_count
    total = len(lines)
    if last_count < 0 or last_count > total:
        # first run, or the log rotated/shrank -> start from a bounded recent tail
        start = max(0, total - _MAX_SCAN)
    else:
        start = max(last_count, total - _MAX_SCAN)  # never scan more than _MAX_SCAN even after a gap
    cutoff = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - _FIRE_WINDOW_SEC))
    for ln in lines[start:total]:
        try:
            rec = json.loads(ln)
        except Exception:
            continue
        ts = rec.get("ts", "")
        if ts and ts < cutoff:  # recency guard against sweep-in
            continue
        if rec.get("event") in _NON_FIRE_EVENTS:
            continue
        gate = rec.get("hook", "")
        if not gate or gate == "outcome-recorder":
            continue
        toks = _flagged_tokens(rec.get("matches"))
        if toks:
            fires.setdefault(gate, [])
            for t in toks:
                if t not in fires[gate]:
                    fires[gate].append(t)
    return fires, total


def _classify_multi(tokens: list[str], prior: str, new: str) -> str:
    """Collapse per-token outcomes into one gate-level outcome (applied dominates ignored)."""
    if prior == new:
        return "no-rewrite"
    outcomes = [classify_outcome(t, prior, new) for t in tokens] if classify_outcome else []
    if "applied" in outcomes:
        return "applied"
    if "ignored" in outcomes:
        return "ignored"
    return "no-signal"


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return
    tool_input = data.get("tool_input") or data.get("toolInput") or {}
    if not isinstance(tool_input, dict):
        return
    target = _target_of(tool_input)
    if not target:
        return
    content = _content_of(tool_input)

    store = _read_json(_PENDING, {})
    if not isinstance(store, dict):
        store = {}
    meta = store.setdefault("_meta", {})
    last_count = meta.get("last_line_count", 0)
    if not isinstance(last_count, int):
        last_count = 0

    # ── 1. RESOLVE any open warning recorded on a PRIOR turn for this target ──
    rec = store.get(target)
    if rec and classify_outcome is not None:
        for gate, info in list(rec.get("gates", {}).items()):
            prior = info.get("content", "")
            tokens = info.get("flagged", [])
            outcome = _classify_multi(tokens, prior, content)
            sign, weight = outcome_to_evidence(outcome)
            row = {
                "ts": _now_iso(),
                "gate": gate,
                "target": target,
                "flagged": tokens,
                "outcome": outcome,
                "evidence_sign": sign,
                "evidence_weight": weight,
            }
            try:
                _RELIABILITY.parent.mkdir(parents=True, exist_ok=True)
                with _RELIABILITY.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
            except Exception:
                pass
        store.pop(target, None)

    # ── 2. RECORD new gate fires (since checkpoint) against this target ──
    fires, new_count = _recent_fires(last_count)
    if fires:
        gates = {
            gate: {"flagged": toks, "content": content, "ts": _now_iso()}
            for gate, toks in fires.items()
        }
        store[target] = {"gates": gates, "recorded_ts": _now_iso()}
    meta["last_line_count"] = new_count
    store["_meta"] = meta

    try:
        _PENDING.parent.mkdir(parents=True, exist_ok=True)
        _PENDING.write_text(json.dumps(store, ensure_ascii=False, indent=0), encoding="utf-8")
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # A telemetry-side hook must NEVER break a write. Swallow everything.
        pass
    # Explicit clean exit; emit nothing (no additionalContext, never blocks).
    sys.exit(0)
