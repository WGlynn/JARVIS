#!/usr/bin/env python3
"""
Memory Preprocessor — L2→L1 Burst at Boot
=========================================

SessionStart hook. Reads all `MEMORY_INDEX_*.md` sub-index files in the
memory directory and injects their concatenated content as
additionalContext.

The Economics
-------------
MEMORY.md has a hard load-budget (~24.4KB) past which the Claude Code
boot hook truncates. Sub-index files (MEMORY_INDEX_PREFLIGHT.md,
MEMORY_INDEX_COMM.md, etc.) are NOT auto-loaded — they're referenced
from MEMORY.md but their bodies live separately and are otherwise
fetched on-demand.

This preprocessor pushes the L2 sub-indexes into the boot context via
additionalContext, which is a separate budget. Result: Claude sees the
full expanded memory at every session start, while MEMORY.md proper
stays compact and pointer-only.

ETM framing: MEMORY.md is L1 (always-loaded, scarce blockspace).
Sub-indexes are L2 (rollup state, normally off-chain). This hook is
the data-availability layer that posts L2 state back to L1 at boot,
trustlessly reconstructible from disk.

Fail-Closed Contract
--------------------
If the preprocessor fails for any reason, MEMORY.md proper still has
the FAIL-CLOSED set: NDA, HIERO, PCP Gate, Anti-Stale, Always=Gate,
BootHookFailLoud, identity. Those rules survive even with this hook
dead.

Performance
-----------
Files are concatenated, no parsing or transformation. ~50ms typical.
Fits comfortably in the 25s SessionStart budget alongside other hooks.

Origin: 2026-05-14 autopilot. The "overlooked move" Will named: hook
preprocesses MEMORY at boot, gives Claude expanded view without paying
MEMORY.md hard-budget cost. ETM-principled L2-to-L1 burst.
"""
import json
import os
import sys
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"

# Telemetry
_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass


# Hard cap on injected payload to avoid swamping additionalContext.
# Sub-indexes combined currently ~30-40KB; cap at 60KB for headroom.
MAX_BYTES = 60_000


def collect_sub_indexes() -> tuple[list[tuple[str, str]], int]:
    """Return list of (filename, content) tuples + total bytes."""
    if not MEMORY_DIR.exists():
        return [], 0
    files = sorted(MEMORY_DIR.glob("MEMORY_INDEX_*.md"))
    out = []
    total = 0
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        out.append((f.name, content))
        total += len(content.encode("utf-8"))
    return out, total


def render(sub_indexes: list[tuple[str, str]], total_bytes: int) -> str:
    """Render the injected payload. Each sub-index gets a clear header
    so Claude can locate-by-section."""
    lines = [
        "[MEMORY PREPROCESSOR — L2 sub-indexes injected as L1-equivalent boot context]",
        "",
        "MEMORY.md proper contains the FAIL-CLOSED set (NDA, HIERO, PCP Gate, etc.).",
        "The bulk of the memory index lives in MEMORY_INDEX_*.md sub-indexes, normally",
        "fetched on-demand. This hook injects them at boot so Claude sees the full",
        "expanded view without consuming MEMORY.md's hard load budget.",
        "",
        f"Total injected: {total_bytes:,} bytes across {len(sub_indexes)} sub-index(es).",
        "",
        "---",
        "",
    ]
    for name, content in sub_indexes:
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(content.rstrip())
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    sub_indexes, total = collect_sub_indexes()
    if not sub_indexes:
        log_event("memory-preprocessor", "noop",
                  meta={"reason": "no_sub_indexes"})
        return 0

    if total > MAX_BYTES:
        # Trim from the end (alphabetical order) until under cap
        accumulated = 0
        kept = []
        for name, content in sub_indexes:
            size = len(content.encode("utf-8"))
            if accumulated + size > MAX_BYTES:
                break
            kept.append((name, content))
            accumulated += size
        sub_indexes = kept
        total = accumulated

    payload_text = render(sub_indexes, total)
    log_event("memory-preprocessor", "fire",
              meta={"sub_indexes": [n for n, _ in sub_indexes],
                    "total_bytes": total})

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": payload_text,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
