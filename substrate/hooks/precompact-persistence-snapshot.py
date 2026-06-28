#!/usr/bin/env python3
"""
PreCompact Persistence Snapshot
===============================
Compaction-boundary layer of the layered-persistence-defense
([[feedback_layered-persistence-defense]]). Fires BEFORE context compaction.

Compaction summarizes the LIVE context (lossy), but the on-disk .jsonl transcript
survives. The real risk is losing AWARENESS of un-persisted load-bearing threads
once the summary replaces the detail. This hook:
  1. Snapshots the session's freshly-written memory file names to a durable file
     (`.ctx-handoff/compaction-snapshot-LATEST.md`), which the PostCompact hook
     re-injects after the summary lands.
  2. Flags the persistence-sweep cron to mine THIS session's full transcript with
     priority (the transcript outlives the compacted context).

Composes additively with the existing PreCompact hook (api-death-shield chain-sync);
different concern, same event. PASSIVE: writes files, returns 0, emits nothing
(so no hook-output-schema dependency, and it can never block compaction).
"""
import datetime as dt
import json
import sys
import time
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
HANDOFF_DIR = Path.home() / ".claude" / "hooks" / ".ctx-handoff"
SNAPSHOT = HANDOFF_DIR / "compaction-snapshot-LATEST.md"
SWEEP_LOG = Path.home() / ".claude" / "cron-prompts" / "_persistence-sweep-log.md"

_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass


def recent_memory(days: int = 2):
    cutoff = time.time() - days * 86400
    out = []
    try:
        for p in MEMORY_DIR.glob("*.md"):
            try:
                mt = p.stat().st_mtime
                if mt >= cutoff:
                    out.append((mt, p.name))
            except Exception:
                continue
    except Exception:
        pass
    out.sort(reverse=True)
    return [n for _, n in out]


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        data = {}

    sid = data.get("session_id") or data.get("sessionId") or "?"
    trigger = data.get("trigger") or data.get("custom_instructions") or "?"
    now = dt.datetime.now().isoformat(timespec="seconds")
    fresh = recent_memory()

    try:
        HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Compaction snapshot (pre-compact)",
            f"- when: {now}",
            f"- session: {sid}",
            f"- trigger: {trigger}",
            "",
            "## Fresh memory written recently (do NOT drop post-compaction):",
        ]
        lines += [f"- {n}" for n in fresh[:40]] or ["- (none in window)"]
        SNAPSHOT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except Exception:
        pass

    try:
        SWEEP_LOG.parent.mkdir(parents=True, exist_ok=True)
        with SWEEP_LOG.open("a", encoding="utf-8") as f:
            f.write(f"compaction | {now} | session {sid} | sweep-priority "
                    f"(context compacted; mine full transcript; {len(fresh)} fresh memories)\n")
    except Exception:
        pass

    log_event("precompact-persistence-snapshot", "fire",
              meta={"fresh_count": len(fresh), "trigger": str(trigger)[:40]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
