#!/usr/bin/env python3
"""Memory exporter: dump indexed memories to canonical JSON.

Format-obsolescence hedge. If markdown parsing drifts, the JSON export preserves
every memory's name/type/description/body/refs in a structure any future parser
can read.

Not a replacement for the markdown files — a PARALLEL backup in a more-universal
format. Run periodically (manual or scheduled); output at:
    memory/MEMORY_EXPORT.json

Covers: every *.md file in the memory directory that has YAML frontmatter.
Skips: index files (MEMORY.md, MEMORY_WARM_*.md, MEMORY_V*.md, *_BACKUP.md),
       format-spec, registry.json, non-memory dirs.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

MEMORY_DIR = os.path.expanduser("~/.claude/projects/C--Users-Will/memory")

# Matches YAML frontmatter block at start of file
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
# Matches simple YAML key-value lines (flat dicts only — no nested)
YAML_LINE_RE = re.compile(r"^([a-zA-Z_][\w-]*):\s*(.*)$")
# Matches inline refs inside memory bodies: T·stem or memory/foo.md
TYPE_REF_RE = re.compile(r"(?:^|[^\w·])([PFJUROM])·([a-z0-9][a-z0-9\-]+)")
EXPLICIT_PATH_RE = re.compile(r"memory/([a-zA-Z0-9_\-]+\.md)")
BARE_LINK_RE = re.compile(r"\]\(([a-zA-Z0-9_\-]+\.md)\)")

TYPE_PREFIX = {
    "P": "primitive_",
    "F": "feedback_",
    "J": "project_",
    "U": "user_",
    "R": "reference_",
    "O": "protocol_",
    "M": "",
}

INDEX_FILE_PATTERNS = ("MEMORY.md", "MEMORY_WARM_", "MEMORY_V", "_BACKUP.md",
                       "MEMORY_FORMAT_SPEC.md", "MEMORY_EXPORT.json")


def is_index_file(fname: str) -> bool:
    if fname == "MEMORY.md":
        return True
    for p in INDEX_FILE_PATTERNS:
        if fname.startswith(p) or fname.endswith(p):
            return True
    return False


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Empty dict if no frontmatter."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    block = m.group(1)
    body = text[m.end():]
    fm: dict[str, str] = {}
    for line in block.splitlines():
        km = YAML_LINE_RE.match(line)
        if km:
            k = km.group(1).strip()
            v = km.group(2).strip()
            # Strip surrounding quotes if present
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            fm[k] = v
    return fm, body


def extract_refs(body: str) -> list[str]:
    """Extract all memory-file references from a body."""
    refs: set[str] = set()
    for m in TYPE_REF_RE.finditer(body):
        code, stem = m.group(1), m.group(2)
        refs.add(f"{TYPE_PREFIX[code]}{stem}.md")
    for m in EXPLICIT_PATH_RE.finditer(body):
        refs.add(m.group(1))
    for m in BARE_LINK_RE.finditer(body):
        refs.add(m.group(1))
    return sorted(refs)


def infer_type_from_filename(fname: str) -> str:
    """Fallback if frontmatter is missing: infer from filename prefix."""
    for prefix, tname in (
        ("primitive_", "primitive"),
        ("feedback_", "feedback"),
        ("project_", "project"),
        ("user_", "user"),
        ("reference_", "reference"),
        ("protocol_", "protocol"),
    ):
        if fname.startswith(prefix):
            return tname
    return "legacy"


def export() -> dict:
    memories: list[dict] = []
    skipped: list[str] = []
    for fname in sorted(os.listdir(MEMORY_DIR)):
        if not fname.endswith(".md"):
            continue
        if is_index_file(fname):
            continue
        path = os.path.join(MEMORY_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            skipped.append(f"{fname}: read error {e}")
            continue
        fm, body = parse_frontmatter(text)
        entry = {
            "filename": fname,
            "name": fm.get("name", fname[:-3]),
            "type": fm.get("type", infer_type_from_filename(fname)),
            "description": fm.get("description", ""),
            "body": body.strip(),
            "refs": extract_refs(body),
        }
        if "originSessionId" in fm:
            entry["originSessionId"] = fm["originSessionId"]
        memories.append(entry)

    return {
        "format_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "session-chain/memory-exporter.py",
        "memory_count": len(memories),
        "skipped_count": len(skipped),
        "skipped": skipped,
        "memories": memories,
    }


def main() -> int:
    out_path = os.path.join(MEMORY_DIR, "MEMORY_EXPORT.json")
    data = export()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[memory-exporter] wrote {out_path}")
    print(f"[memory-exporter] {data['memory_count']} memories, {data['skipped_count']} skipped")
    # summary by type
    by_type: dict[str, int] = {}
    for m in data["memories"]:
        by_type[m["type"]] = by_type.get(m["type"], 0) + 1
    for t, n in sorted(by_type.items(), key=lambda kv: -kv[1]):
        print(f"  {t:12s} {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
