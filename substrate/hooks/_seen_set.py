#!/usr/bin/env python3
"""
Session Seen-Set + Deep-Context detector  (Deep Context Mode)
=============================================================

A session-scoped record of which memory files have ALREADY been injected into a
given session's context, plus a cheap detector for whether the session has
entered DEEP CONTEXT MODE (>= C1 / 500k tokens).

Why
---
Context loaders (memory-warm-loader, deep-recall) re-inject the same warm shards
on every matching turn. Below ~500k tokens that redundancy is cheap. Past the
"context cliff" (~50-70% of the effective window) every re-injected byte competes
with load-bearing content for a degrading attention budget. This utility lets a
loader SUPPRESS a shard it already injected THIS session -- but only once the
session is actually in deep context.

Design invariant  (load-bearing -- keeps normal sessions byte-identical)
-----------------
  TRACK always   (mark_seen is cheap; just records filenames)
  SUPPRESS only   when is_deep_context() is True
Below 500k, is_deep_context() is False, so a caller that guards suppression on it
behaves exactly as before. Fully inert until the C1 sentinel exists.

Signal source
-------------
is_deep_context(session_id) == the .ctx-handoff/{session_id}.c1 sentinel exists.
That sentinel is written by tools/token-audit/context-rotation-hook.py (a Stop
hook) at the first Stop after the session crosses C1 (default 500k, env
CTX_TIER_C1). Reading it here means the activator and the loaders share ONE tier
signal and never disagree.

Copyable: no private paths or slugs. Root overridable via $CTX_HANDOFF_DIR.
Fail-open everywhere: any error -> "not seen" / "not deep context" -> the caller
does its normal thing. This utility can never block or crash a hook.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

__all__ = [
    "handoff_dir", "is_deep_context", "load_seen", "has_seen",
    "mark_seen", "clear", "prune",
]


def handoff_dir() -> Path:
    return Path(os.environ.get(
        "CTX_HANDOFF_DIR",
        str(Path.home() / ".claude" / "hooks" / ".ctx-handoff"),
    ))


def _seen_path(session_id: str, hd: Path | None = None) -> Path:
    hd = hd or handoff_dir()
    sid = session_id or "unknown-session"
    return Path(hd) / f"{sid}.seen-set.json"


def is_deep_context(session_id: str, hd: Path | None = None) -> bool:
    """True iff the session has crossed C1 (>=500k tokens). Fail-safe -> False."""
    try:
        if not session_id:
            return False
        hd = Path(hd) if hd else handoff_dir()
        return (hd / f"{session_id}.c1").exists()
    except Exception:
        return False


def load_seen(session_id: str, hd: Path | None = None) -> set[str]:
    try:
        p = _seen_path(session_id, hd)
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            seen = data.get("seen") if isinstance(data, dict) else None
            if isinstance(seen, list):
                return {str(x) for x in seen}
    except Exception:
        pass
    return set()


def has_seen(session_id: str, filename: str, hd: Path | None = None) -> bool:
    return filename in load_seen(session_id, hd)


def mark_seen(session_id, filenames, hd: Path | None = None) -> set[str]:
    """Add filename(s) to the session seen-set; persist atomically. Returns the
    updated set (best-effort; fail-open)."""
    if isinstance(filenames, str):
        filenames = [filenames]
    filenames = [f for f in (filenames or []) if f]
    seen = load_seen(session_id, hd)
    if not filenames or set(filenames) <= seen:
        return seen
    seen.update(filenames)
    try:
        d = Path(hd) if hd else handoff_dir()
        d.mkdir(parents=True, exist_ok=True)
        p = _seen_path(session_id, d)
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_text(
            json.dumps({"seen": sorted(seen), "updated": time.time()}),
            encoding="utf-8",
        )
        os.replace(tmp, p)
    except Exception:
        pass
    return seen


def clear(session_id: str, hd: Path | None = None) -> None:
    """Drop the session seen-set. Called post-compaction: context detail was
    summarized away, so 'already injected' guarantees no longer hold -> allow
    loaders to re-inject."""
    try:
        p = _seen_path(session_id, hd)
        if p.exists():
            p.unlink()
    except Exception:
        pass


def prune(days: int = 7, hd: Path | None = None) -> int:
    """Delete seen-set files older than `days`. Cheap housekeeping. Returns count."""
    n = 0
    try:
        d = Path(hd) if hd else handoff_dir()
        cutoff = time.time() - days * 86400
        for p in d.glob("*.seen-set.json"):
            try:
                if p.stat().st_mtime < cutoff:
                    p.unlink()
                    n += 1
            except Exception:
                continue
    except Exception:
        pass
    return n
