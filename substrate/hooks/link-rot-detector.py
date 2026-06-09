#!/usr/bin/env python3
"""Link-rot detector: scan MEMORY.md + MEMORY_WARM_*.md for path refs, verify backing files exist.

Called as SessionStart hook (surfaces rot at boot), or standalone for audit.

Resolves path references in three formats:
  1. T·stem         — prefix-code form (P·foo → memory/primitive_foo.md, etc.)
  2. memory/...md   — explicit path
  3. T_stem.md      — bare filename in a markdown link (legacy)

Emits a report listing orphan refs (ref exists, file doesn't) and orphan files
(file exists, no ref). Orphan refs = rot that breaks recall. Orphan files =
memory-garbage that drifted out of the index.
"""
import json
import os
import re
import sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

MEMORY_DIR = os.path.expanduser("~/.claude/projects/C--Users-Will/memory")
SETTINGS_PATH = os.path.expanduser("~/.claude/settings.json")
CLAUDE_MD_PATHS = [
    os.path.expanduser("~/.claude/CLAUDE.md"),
    os.path.expanduser("~/vibeswap/CLAUDE.md"),
]
# Anchor paths CLAUDE.md protocol chain declares as load-bearing
PROTOCOL_CHAIN_FILES = [
    os.path.expanduser("~/vibeswap/.claude/SESSION_STATE.md"),
    os.path.expanduser("~/vibeswap/.claude/WAL.md"),
    os.path.expanduser("~/vibeswap/.claude/JarvisxWill_SKB.md"),
    os.path.expanduser("~/vibeswap/.claude/JarvisxWill_GKB.md"),
]

PREFIX_MAP = {
    "P": "primitive_",
    "F": "feedback_",
    "J": "project_",
    "U": "user_",
    "R": "reference_",
    "O": "protocol_",
    "M": "",  # prefix-less
}

# Matches T·stem where T is one of the prefix codes and stem is kebab-case.
# Must be preceded by non-word or start so we don't match mid-identifier.
PREFIX_REF_RE = re.compile(r"(?:^|[^\w·])([PFJUROM])·([a-z0-9][a-z0-9\-]+)")
# Matches memory/foo.md in MEMORY.md explicit paths
EXPLICIT_PATH_RE = re.compile(r"memory/([a-zA-Z0-9_\-]+\.md)")
# Matches bare `filename.md` inside markdown link `](filename.md)` — warm files
# reference siblings without `memory/` prefix since they live in the same dir.
BARE_LINK_RE = re.compile(r"\]\(([a-zA-Z0-9_\-]+\.md)\)")


def collect_refs(text: str) -> set[str]:
    """Return set of resolved filenames referenced by text."""
    refs: set[str] = set()
    for m in PREFIX_REF_RE.finditer(text):
        code, stem = m.group(1), m.group(2)
        prefix = PREFIX_MAP[code]
        refs.add(f"{prefix}{stem}.md")
    for m in EXPLICIT_PATH_RE.finditer(text):
        refs.add(m.group(1))
    for m in BARE_LINK_RE.finditer(text):
        fname = m.group(1)
        # Skip files outside memory/ (e.g. cross-dir links like vibeswap/docs/...)
        # — BARE_LINK_RE already excludes those since they have '/' which isn't in the charset
        refs.add(fname)
    return refs


def scan_index_files(mem_dir: str) -> tuple[dict[str, set[str]], set[str]]:
    """Scan MEMORY.md + MEMORY_WARM_*.md. Return (file→refs, all_refs_union)."""
    index_files = ["MEMORY.md"] + sorted(
        f for f in os.listdir(mem_dir) if f.startswith("MEMORY_WARM_") and f.endswith(".md")
    )
    per_file: dict[str, set[str]] = {}
    all_refs: set[str] = set()
    for fname in index_files:
        path = os.path.join(mem_dir, fname)
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        refs = collect_refs(text)
        per_file[fname] = refs
        all_refs |= refs
    return per_file, all_refs


def scan_settings_hook_paths(settings_path: str) -> list[tuple[str, str]]:
    """Return list of (ref_path, context) for files referenced by hook commands in settings.json.

    Catches the failure class that broke 2026-04-21: a SessionStart hook cmd
    referenced a file at a path that no longer existed; the 2>/dev/null swallow
    + empty-stdin combo silently emitted "0 loops pending". Path-drift in hook
    command strings is exactly the surface this scan covers.
    """
    if not os.path.exists(settings_path):
        return []
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except Exception:
        return []

    missing: list[tuple[str, str]] = []
    hooks_config = settings.get("hooks", {})

    # Regex for C:/... or ~/... style paths inside hook command strings.
    # Matches .py .md .json .sh .bat .vbs .ps1 file references.
    path_re = re.compile(
        r"([A-Za-z]:[\\/][^\s\"';|]+\.(?:py|md|json|sh|bat|vbs|ps1))"
    )

    for event, event_hooks in hooks_config.items():
        if not isinstance(event_hooks, list):
            continue
        for block in event_hooks:
            for h in block.get("hooks", []):
                cmd = h.get("command", "")
                for m in path_re.finditer(cmd):
                    ref = m.group(1).replace("\\", "/")
                    # Strip trailing punctuation that regex may have captured
                    ref = ref.rstrip(",;)'\"")
                    if not os.path.exists(ref):
                        missing.append((ref, f"settings.json:{event}"))
    return missing


def scan_protocol_chain() -> list[tuple[str, str]]:
    """Verify CLAUDE.md protocol-chain declared files exist."""
    missing: list[tuple[str, str]] = []
    for p in PROTOCOL_CHAIN_FILES:
        if not os.path.exists(p):
            missing.append((p, "CLAUDE.md protocol chain"))
    return missing


def main() -> int:
    # Detect mode: hook (stdin JSON) vs standalone
    hook_mode = not sys.stdin.isatty()
    payload: dict = {}
    if hook_mode:
        try:
            payload = json.load(sys.stdin)
        except Exception:
            payload = {}

    per_file, all_refs = scan_index_files(MEMORY_DIR)
    hook_path_rot = scan_settings_hook_paths(SETTINGS_PATH)
    protocol_chain_rot = scan_protocol_chain()

    # Orphan refs: referenced but file missing
    orphan_refs: dict[str, list[str]] = defaultdict(list)
    for fname, refs in per_file.items():
        for ref in refs:
            target = os.path.join(MEMORY_DIR, ref)
            if not os.path.exists(target):
                orphan_refs[ref].append(fname)

    # Orphan files: file exists, no index references it. Excludes index files themselves
    # and known non-ref files (MEMORY_V*.md candidates, backups, registry.json, dirs).
    all_md = set()
    for f in os.listdir(MEMORY_DIR):
        if not f.endswith(".md"):
            continue
        if f == "MEMORY.md" or f.startswith("MEMORY_WARM_") or f.startswith("MEMORY_V"):
            continue
        if f.endswith("_BACKUP.md"):
            continue
        all_md.add(f)
    orphan_files = sorted(all_md - all_refs)

    # Build report
    lines = []
    if orphan_refs:
        lines.append(f"[MISS] {len(orphan_refs)} orphan refs (index points to missing files):")
        for ref, where in sorted(orphan_refs.items()):
            lines.append(f"  - {ref}  <- {', '.join(where)}")
    if hook_path_rot:
        lines.append(
            f"[HOOK-ROT] {len(hook_path_rot)} hook command paths point at missing files:"
        )
        for ref, where in hook_path_rot:
            lines.append(f"  - {ref}  <- {where}")
        lines.append(
            "  (This is the failure class that broke SessionStart 2026-04-21. "
            "Update settings.json or restore the file.)"
        )
    if protocol_chain_rot:
        lines.append(
            f"[PROTOCOL-ROT] {len(protocol_chain_rot)} CLAUDE.md protocol-chain files missing:"
        )
        for ref, where in protocol_chain_rot:
            lines.append(f"  - {ref}  <- {where}")
    if orphan_files:
        lines.append(f"[ORPH] {len(orphan_files)} orphan files (exist but no index ref):")
        for f in orphan_files[:20]:  # cap output
            lines.append(f"  - {f}")
        if len(orphan_files) > 20:
            lines.append(f"  ... and {len(orphan_files) - 20} more")
    if not (orphan_refs or hook_path_rot or protocol_chain_rot or orphan_files):
        lines.append("[OK] link-rot clean: all refs resolve, all files indexed, all hook paths live")

    report = "\n".join(lines)

    if hook_mode:
        # Surface to Claude on any breaking class (orphan_refs, hook-rot, protocol-rot).
        # Orphan files alone = memory-garbage, don't surface at boot.
        breaking = orphan_refs or hook_path_rot or protocol_chain_rot
        if breaking:
            out = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": (
                        f"[link-rot-detector]\n{report}\n\n"
                        "Surface to Will on first response if relevant."
                    ),
                }
            }
            print(json.dumps(out))
        # Always log to stderr for observability
        print(f"[link-rot-detector] {report}", file=sys.stderr)
    else:
        # Standalone: print report to stdout
        print(report)

    # Exit 0 always — informational only, don't block anything
    return 0


if __name__ == "__main__":
    sys.exit(main())
