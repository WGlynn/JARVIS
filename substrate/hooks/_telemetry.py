"""
Hook Telemetry Helper
=====================

Shared logging module for JARVIS protocol-overlay hooks. Each hook calls
`log_event()` with a structured record when it fires. The log is JSONL
under `_system/protocol_telemetry.jsonl` — append-only, parseable by
downstream analyzers.

Schema (per line, JSON):
  - ts: ISO8601 timestamp
  - hook: hook name (e.g. "entity-context-cross-reference")
  - event: "fire" | "match" | "noop" | "error"
  - matches: list of matched items (entity names, primitive ids, file paths)
    where applicable; omitted otherwise
  - meta: dict of free-form fields (input size, score, query token count, etc.)

The telemetry log:
  - Lives at `~/.claude/projects/C--Users-Will/memory/_system/protocol_telemetry.jsonl`
  - Is NOT committed to the memory repo by default (it grows and contains
    no AA-class material). Gitignore it after first commit if pruning is
    desired; for now we add to .gitignore when we ship the analyzer.
  - Is the substrate for `_protocol_telemetry_report.py` (in memory dir)
    which produces human-readable summaries.

Hooks that import this:
  - entity-context-cross-reference.py
  - deep-recall.py
  - post-generation-reflect.py

Design note: log_event MUST not raise. Any error inside the logger gets
swallowed silently. The hooks must remain robust to telemetry failure;
losing log lines is acceptable, breaking the hook's primary function is
not.

Origin: 2026-05-13 autopilot Round 2, Build (telemetry).
"""
import json
import os
import time
from pathlib import Path

_LOG_PATH = (
    Path.home()
    / ".claude"
    / "projects"
    / "C--Users-Will"
    / "memory"
    / "_system"
    / "protocol_telemetry.jsonl"
)


def log_event(hook: str, event: str, matches=None, meta=None) -> None:
    """Append a telemetry line. Silent on failure."""
    try:
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "hook": hook,
            "event": event,
        }
        if matches:
            record["matches"] = list(matches)[:20]  # cap noise
        if meta:
            record["meta"] = meta
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        # Telemetry must not break hooks. Silent on any error.
        pass
