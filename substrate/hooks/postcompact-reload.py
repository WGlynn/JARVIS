#!/usr/bin/env python3
"""
PostCompact Reload
==================
Compaction-boundary layer of the layered-persistence-defense
([[feedback_layered-persistence-defense]]). Fires AFTER context compaction.

After the summary replaces the detailed context, the load-bearing threads written
earlier this session can silently fall out of working memory. This hook reads the
PreCompact snapshot and re-injects pointers to that fresh memory via
hookSpecificOutput.additionalContext (the sanctioned post-event injection seam),
so compaction cannot quietly drop what mattered.

Robustness: if `additionalContext` is not honored for PostCompact on this installed
version, the emitted JSON is simply ignored — never fatal. Returns 0 always.
(The StopSchema per-event gating could not be fully verified from the 2.1.172
binary; this hook is written so that an unsupported field degrades to a no-op
rather than an error.)
"""
import json
import sys
from pathlib import Path

SNAPSHOT = Path.home() / ".claude" / "hooks" / ".ctx-handoff" / "compaction-snapshot-LATEST.md"

_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass


def main() -> int:
    try:
        payload = sys.stdin.read()
        _ = json.loads(payload) if payload.strip() else {}
    except Exception:
        pass

    ctx = None
    try:
        if SNAPSHOT.exists():
            body = SNAPSHOT.read_text(encoding="utf-8", errors="replace")
            names = [l[2:].strip() for l in body.splitlines()
                     if l.startswith("- ") and l.strip().endswith(".md")]
            if names:
                ctx = ("Context was just compacted. Load-bearing memory written earlier this "
                       "session is below — re-read any still relevant before continuing; do not "
                       "treat these threads as dropped:\n"
                       + "\n".join(f"- {n}" for n in names[:30]))
    except Exception:
        ctx = None

    if ctx:
        try:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PostCompact",
                    "additionalContext": ctx,
                }
            }))
            log_event("postcompact-reload", "fire", meta={"reinjected": ctx.count("\n- ")})
        except Exception:
            pass
    else:
        log_event("postcompact-reload", "noop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
