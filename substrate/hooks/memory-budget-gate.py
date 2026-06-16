#!/usr/bin/env python3
"""
memory-budget-gate.py

Shift-left guard for the MEMORY.md boot-load budget.

The boot index MEMORY.md is hard-capped at BUDGET bytes; corpus-cache-warmer.py
reports the overage at BOOT (after the truncation already happened that session).
This hook moves that signal to AUTHOR time: when a Write/Edit would push MEMORY.md
over budget, it augments context with the overage + the established fix (relocate a
bullet to a sub-index, which is boot-injected losslessly).

Augmentation gate, NOT a block. The write proceeds; the warning rides along so the
relocation happens in the same pass instead of next boot.

Derived: TRP2 2026-06-16 (subject=jarvis substrate). Bottleneck = silent boot-time
truncation of the index. Convergent form = PreToolUse hook (same shift-left shape as
the author-generic leak gate). Composes [P.universal-coverage-hook],
[P.boot-hook-fail-loud] (this is the loud version of a silent truncation).

ASCII-only output (Windows cp1252 console; cf. _primitives-pending L237).
Fail-OPEN: any error emits {} so a guard bug can never block a memory write.
"""
import json
import os
import sys

BUDGET = 24400  # must match corpus-cache-warmer.py boot-load budget

# Only the boot-loaded index, not any other MEMORY.md (e.g. vibeswap/).
TARGET_SUFFIX = "projects/c--users-will/memory/memory.md"


def disk_bytes(text):
    """On-disk byte size matching the boot budget measure.

    The boot file is CRLF on disk, but Python text-mode reads normalize \\r\\n -> \\n,
    undercounting by one byte per line. The boot budget (corpus-cache-warmer n_bytes)
    measures on-disk size, so we add back one byte per newline. On a pure-LF file this
    over-counts by #lines (conservative: warns slightly early), which is correct for an
    augmentation gate -- a false-negative (missing an over-budget write) is the failure
    we must avoid; a false-positive only warns a hair early.
    """
    return len(text.encode("utf-8")) + text.count("\n")


def _emit(obj):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(json.dumps(obj))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _emit({})
        return

    if payload.get("hook_event_name", "") != "PreToolUse":
        _emit({})
        return

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        _emit({})
        return

    ti = payload.get("tool_input", {})
    path = (ti.get("file_path", "") or "").replace("\\", "/").lower()
    if not path.endswith(TARGET_SUFFIX):
        _emit({})
        return

    # Compute the resulting byte size after this write.
    try:
        if tool == "Write":
            result = ti.get("content", "") or ""
        else:  # Edit
            real_path = ti.get("file_path", "")
            with open(real_path, encoding="utf-8") as f:
                current = f.read()
            old = ti.get("old_string", "") or ""
            new = ti.get("new_string", "") or ""
            if ti.get("replace_all"):
                result = current.replace(old, new)
            else:
                result = current.replace(old, new, 1)
        size = disk_bytes(result)
    except Exception:
        _emit({})  # fail-open: can't compute -> never block
        return

    if size <= BUDGET:
        _emit({})
        return

    over = size - BUDGET
    msg = (
        "[MEMORY-BUDGET GATE] This write puts MEMORY.md at {size} bytes, "
        "{over} OVER the {budget}-byte boot-load budget. The boot hook TRUNCATES "
        "the index over budget (silent context loss next session). Fix in THIS pass: "
        "move a bullet from MEMORY.md into the matching sub-index "
        "(MEMORY_INDEX_*.md / MEMORY_WARM_*.md) -- those are boot-injected losslessly, "
        "so relocation costs nothing. Add new pointers to a sub-index, not MEMORY.md. "
        "Augmentation only; the write is NOT blocked."
    ).format(size=size, over=over, budget=BUDGET)

    _emit({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": msg,
        }
    })


if __name__ == "__main__":
    main()
