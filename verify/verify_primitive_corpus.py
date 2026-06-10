#!/usr/bin/env python3
"""verify_primitive_corpus.py — fresh-clone-runnable check.

Walks substrate/memory/ and verifies every markdown primitive has well-formed
YAML frontmatter with the required fields: name, description, type. Exits 0 on
clean, 1 on any malformed file.

No deps. Run from repo root:

    python verify/verify_primitive_corpus.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = REPO_ROOT / "substrate" / "memory"

REQUIRED_FIELDS = {"name", "description", "type"}
ALLOWED_TYPES = {"primitive", "feedback", "project", "reference", "user", "other"}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def parse_frontmatter(text: str) -> dict | None:
    """Return parsed frontmatter dict, or None if absent / malformed."""
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if len(lines) < 3:
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    out: dict = {}
    for line in lines[1:end]:
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        out[key.strip()] = val.strip()
    return out


def main() -> int:
    if not MEMORY_DIR.exists():
        print(f"FAIL: memory dir missing at {MEMORY_DIR}")
        return 1

    md_files = sorted(MEMORY_DIR.glob("*.md"))
    parsed = 0
    skipped_index = 0
    skipped_no_frontmatter = 0
    errors: list[tuple[str, str]] = []

    for fpath in md_files:
        name = fpath.name
        if name.startswith("MEMORY") or name.startswith("_") or name == "README.md":
            skipped_index += 1
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            errors.append((name, f"read error: {e}"))
            continue
        if not text.startswith("---"):
            # Legacy protocol docs without frontmatter — not primitives.
            skipped_no_frontmatter += 1
            continue
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append((name, "malformed frontmatter"))
            continue
        missing = REQUIRED_FIELDS - set(fm.keys())
        if missing:
            errors.append((name, f"missing fields: {sorted(missing)}"))
            continue
        if fm["type"] not in ALLOWED_TYPES:
            errors.append((name, f"unknown type: {fm['type']!r}"))
            continue
        parsed += 1

    total = parsed + len(errors)
    print(f"primitive corpus: {parsed}/{total} parsed clean")
    print(f"  skipped index/system files: {skipped_index}")
    print(f"  skipped no-frontmatter (legacy docs): {skipped_no_frontmatter}")
    if errors:
        print(f"  errors: {len(errors)}")
        for name, msg in errors[:20]:
            print(f"    {name}: {msg}")
        if len(errors) > 20:
            print(f"    ... and {len(errors) - 20} more")
        return 1
    print("  errors: 0")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
