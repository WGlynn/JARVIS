#!/usr/bin/env python3
"""
Boot witness for the memory index BOOT-LOAD BUDGET (in-system alarm).

The boot index MEMORY.md is hard-capped at BUDGET on-disk bytes. When it goes
over, corpus-cache-warmer.py silently TRUNCATES it at boot -- context is lost and
the only guard is a non-blocking augmentation warning (hooks/memory-budget-gate.py,
docstring: "Augmentation gate, NOT a block") that a direct Edit/Write can ride
past. That is exactly how MEMORY.md reached 26,282 bytes (1,882 over) and lost
context at boot -- the silent-failure class already fixed for crons, crash-recovery
and the autosave daemon.

There is a SECOND silent-drop channel on the index side. hooks/memory-preprocessor.py
injects every MEMORY_INDEX_*.md as boot context but caps the COMBINED payload at
PREPROCESSOR_CAP bytes (MAX_BYTES = 100_000, memory-preprocessor.py:65); when the sum
is over, it orders PREFLIGHT-first then smallest-first and greedily keeps files under
cap, SKIPPING (not break-dropping) any single file too big to fit
(memory-preprocessor.py:131-147) -- a SILENT whole-file drop of whatever does not fit.
So an index growing does not truncate one file, it can silently delete a large index
(e.g. ACTIVE) from boot entirely while smaller ones still load. Same silent-failure
class, different mechanism.

This hook, wired into SessionStart, surfaces LOUD on either breach:

  - MEMORY.md OVER BUDGET   -> MEMORY.md exceeds BUDGET; corpus-cache-warmer TRUNCATES
                              the boot index NOW (per-file cap, in-file truncation).
  - INDEX PAYLOAD OVER CAP  -> sum of all MEMORY_INDEX_*.md exceeds PREPROCESSOR_CAP;
                              the preprocessor SILENTLY DROPS whole later-alphabetical
                              indexes from boot. Reports which files survive vs are cut.
  - MISSING                 -> MEMORY.md itself is gone (surfaced loud).

Clean (MEMORY.md at/under BUDGET and index sum at/under PREPROCESSOR_CAP) -> SILENT
(a clean boot adds zero noise), except a single terse OK line is still appended to
the witness log so the log itself proves liveness (absence of recent log lines ==
this witness stopped running).

Byte measure MUST match the boot budget's measure. corpus-cache-warmer.py compares
the cache's n_bytes (raw on-disk size) to 24,400, so we read raw bytes off disk
(len of the byte content) -- NOT text-mode, which would normalize CRLF->LF and
undercount by one byte per line on the CRLF boot file.

Witness log: ~/.claude/.autosave/index-budget-witness.log (append-only, same dir as
the other liveness logs). Each boot appends one line; over-budget events are marked
OVER-BY-N so a grep of the log is a full history of every breach.

Warn-only: prints to stdout and always returns 0. It can NEVER block boot and NEVER
mutates any memory file. Relocating bullets back under budget is a separate,
human-decided action (see PROPOSALS.md / the relocate hint below).

Derived: corpus-health-2 hardening pass 2026-08-07 (theme = silent failure).
Composes [P.boot-hook-fail-loud] (loud version of a silent truncation),
[P.universal-coverage-hook] (a witness per self-improvement mechanism).
ASCII-only output (Windows cp1252 console).
"""

import glob
import os
import time
from datetime import datetime, timezone
from pathlib import Path

BUDGET = 24_400  # must match corpus-cache-warmer.py boot-load budget (MEMORY.md)
PREPROCESSOR_CAP = 100_000  # must match memory-preprocessor.py MAX_BYTES (index sum)
# must match memory-preprocessor.py PRIORITY_ORDER (injected first, size-exempt in ordering)
PRIORITY_ORDER = ("MEMORY_INDEX_PREFLIGHT.md",)

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
MEMORY_MD = MEMORY_DIR / "MEMORY.md"
INDEX_GLOB = str(MEMORY_DIR / "MEMORY_INDEX_*.md")

LOG = Path.home() / ".claude" / ".autosave" / "index-budget-witness.log"

RELOCATE_HINT = (
    "move ~2KB of MEMORY.md bullets into the matching MEMORY_INDEX_*.md / "
    "MEMORY_WARM_*.md (boot-injected losslessly) until on-disk MEMORY.md <= 24,400 B"
)


def disk_bytes(path):
    """Raw on-disk byte size, matching the boot budget's n_bytes measure.

    Reads bytes (not text mode) so CRLF is counted as two bytes -- the boot budget
    (corpus-cache-warmer) compares raw on-disk size, so this must too. Returns None
    if the file cannot be read.
    """
    try:
        return len(path.read_bytes())
    except Exception:
        return None


def utf8_bytes(path):
    """UTF-8 byte size after CRLF->LF normalization, matching the preprocessor's
    index-payload measure.

    memory-preprocessor.py reads each index in text mode (read_text) and sums
    len(content.encode('utf-8')) against MAX_BYTES. Text mode normalizes CRLF->LF,
    so we replicate that here so the index-sum comparison matches the real cap the
    preprocessor applies. Returns None if unreadable.
    """
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").encode("utf-8"))
    except Exception:
        return None


def preprocessor_survivors(index_paths):
    """Replay the preprocessor's keep/drop decision (memory-preprocessor.py:131-147).

    Mirrors the REAL ordering (PRIORITY_ORDER first, then smallest-first) and the
    greedy-fit: keep a file if the running UTF-8-byte sum stays <= PREPROCESSOR_CAP,
    otherwise SKIP that file and CONTINUE -- one oversized file never zeroes the rest
    (the 2026-08 regression fix). Returns (kept_names, dropped_names, total_utf8_bytes).
    """
    sized = []
    total = 0
    for p in index_paths:
        size = utf8_bytes(p)
        if size is None:
            continue
        sized.append((p, size))
        total += size

    # Same rank as the preprocessor: PRIORITY_ORDER index first, then size ascending.
    def _rank(item):
        p, size = item
        pri = PRIORITY_ORDER.index(p.name) if p.name in PRIORITY_ORDER else len(PRIORITY_ORDER)
        return (pri, size)
    sized.sort(key=_rank)

    if total <= PREPROCESSOR_CAP:
        return [p.name for p, _ in sized], [], total

    kept, dropped = [], []
    accumulated = 0
    for p, size in sized:
        if accumulated + size > PREPROCESSOR_CAP:
            dropped.append(p.name)   # skip-and-continue (NOT break) -- mirrors the fix
            continue
        kept.append(p.name)
        accumulated += size
    return kept, dropped, total


def _append_log(line):
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8", errors="replace") as f:
            f.write(line.rstrip("\n") + "\n")
    except Exception:
        # A witness that cannot write its log must still never break boot.
        pass


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- Channel 1: MEMORY.md per-file boot budget (in-file truncation). ---
    if not MEMORY_MD.exists():
        msg = "MEMORY.md is MISSING at " + str(MEMORY_MD)
        _append_log(f"{stamp} MISSING {msg}")
        print("=== INDEX-BUDGET WITNESS: MISSING ===")
        print(msg)
        print("The boot index is gone -- boot context load is degraded.")
        return

    mem_bytes = disk_bytes(MEMORY_MD)
    mem_over = None
    if mem_bytes is not None and mem_bytes > BUDGET:
        mem_over = mem_bytes - BUDGET

    # --- Channel 2: combined index payload vs preprocessor cap (whole-file drop). ---
    index_paths = [Path(p) for p in sorted(glob.glob(INDEX_GLOB))]
    kept, dropped, index_total = preprocessor_survivors(index_paths)
    index_over = index_total > PREPROCESSOR_CAP

    # --- Log: always append one line so the log itself proves liveness. ---
    log_parts = []
    if mem_over is not None:
        log_parts.append(f"MEMORY.md=+{mem_over}")
    if index_over:
        log_parts.append(
            f"INDEX_SUM={index_total}(cap={PREPROCESSOR_CAP},dropped={'|'.join(dropped) or 'none'})"
        )
    if log_parts:
        _append_log(f"{stamp} OVER-BY {' '.join(log_parts)}")
    else:
        _append_log(
            f"{stamp} OK MEMORY.md={mem_bytes}B/{BUDGET}B "
            f"INDEX_SUM={index_total}B/{PREPROCESSOR_CAP}B"
        )

    # --- Boot stdout: LOUD only on breach; silent on a clean boot. ---
    if mem_over is None and not index_over:
        return

    print("=== INDEX-BUDGET WITNESS: OVER BUDGET ===")
    if mem_over is not None:
        print(
            f"  MEMORY.md: {mem_bytes:,} bytes = {mem_over:,} OVER the "
            f"{BUDGET:,}-byte boot budget [TRUNCATED AT BOOT]"
        )
        print("  => corpus-cache-warmer SILENTLY truncates the boot index this session.")
        print(f"  relocate: {RELOCATE_HINT}")
    if index_over:
        print(
            f"  MEMORY_INDEX_* payload: {index_total:,} bytes = "
            f"{index_total - PREPROCESSOR_CAP:,} OVER the {PREPROCESSOR_CAP:,}-byte "
            "preprocessor cap [WHOLE FILES SILENTLY DROPPED AT BOOT]"
        )
        if dropped:
            print(f"  DROPPED from boot (later-alphabetical): {', '.join(dropped)}")
        print(f"  kept in boot: {', '.join(kept) if kept else 'NONE -- ZERO sub-indexes injected'}")
        if not kept:
            print(
                "  [!!] Every index individually exceeds the cap, so the preprocessor "
                "skips them all and injects NOTHING -- including PREFLIGHT. (Should be "
                "unreachable: PREFLIGHT is injected first and is far under the 100KB cap.)"
            )
        print(
            "  => memory-preprocessor.py drops the DROPPED indexes entirely; if PREFLIGHT "
            "or STATE_PROTOCOL is in that list, fail-closed boot rules are NOT loaded."
        )
    print(f"  witness log: {LOG}")


if __name__ == "__main__":
    main()
