#!/usr/bin/env python3
"""_asp_extract.py -- compile a markdown knowledge-graph into ASP facts.

LOOP increment 1 (non-LLM reasoning substrate for JARVIS). Walks TOP-LEVEL ``*.md`` only, so
``_obsidian-view/`` duplicate copies, ``nda-locked/``, ``_system/`` and every other subdir are
excluded by construction. Emits a sorted, byte-deterministic ``facts.lp`` plus ``provenance.json``.

Phase 2 adds **name-aliasing**: a ``[[wikilink]]`` often targets a primitive's short ``name:`` slug
(e.g. ``[[voluntary-noesis]]``) while the file is ``_CANON_voluntary-noesis-lived-economics.md``.
We alias a clean ``name:`` slug onto its canonical filename-slug so those links resolve instead of
showing as dead. Aliasing is conservative: only clean ``^[a-z0-9-]+$`` names, never one that
collides with a real node, never an ambiguous name claimed by two files.

Generic on purpose: point ``--root`` at any flat markdown graph whose edges are ``[[wikilinks]]``.
Part of the JARVIS non-LLM intelligence architecture -- free to copy (see repo LICENSE). Zero LLM calls.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

try:
    import yaml  # PyYAML; frontmatter parsing
except ImportError:  # pragma: no cover
    yaml = None

WIKILINK = re.compile(r"\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]")
# Bracket-tag refs `[P·slug]` (P∈PFRJOMU). Same node ids as wikilinks; the majority edge syntax
# in this corpus. Regex mirrors _index.py's PRIMITIVE_REF_PATTERN (AA#N audit refs excluded).
BRACKETTAG = re.compile(r"\[[PFRJOMU]·([a-zA-Z0-9_\-]+)\]")
CLEAN_SLUG = re.compile(r"^[a-z0-9][a-z0-9\-]*$")
TYPE_PREFIXES = ("primitive_", "feedback_", "reference_", "project_", "protocol_", "user_")
# Default to the directory this script lives in (correct wherever it's copied), env-overridable.
DEFAULT_ROOT = Path(os.environ["JARVIS_MEMORY_ROOT"]) if os.environ.get("JARVIS_MEMORY_ROOT") \
    else Path(__file__).resolve().parent


def _strip_type_prefix(stem_lower: str) -> str:
    """Strip a `_canon_`/`primitive_`/`feedback_`/... prefix from an already-lowercased stem.

    Shared by filename AND wikilink-target normalization so `[[primitive_foo]]`, `[[_canon_foo]]`
    and `[[foo]]` all resolve to the same canonical node `foo`.
    """
    if stem_lower.startswith("_canon_"):
        return stem_lower[len("_canon_"):]
    for pfx in TYPE_PREFIXES:  # TYPE_PREFIXES are already lowercase
        if stem_lower.startswith(pfx):
            return stem_lower[len(pfx):]
    return stem_lower


def slug_from_filename(name: str) -> str:
    """Canonical node id = filename-derived slug (the ``name:`` frontmatter is unreliable prose)."""
    stem = name[:-3] if name.endswith(".md") else name
    return _strip_type_prefix(stem.strip().lower())


def slug_from_link(target: str) -> str:
    return _strip_type_prefix(target.split("|")[0].strip().lower())


def name_slug(text: str) -> str | None:
    """Return a clean ``name:`` frontmatter slug, or None (prose / missing / dirty)."""
    if yaml is None or not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(text[3:end]) or {}
    except Exception:
        return None
    n = fm.get("name") if isinstance(fm, dict) else None
    if isinstance(n, str):
        n = n.strip().lower()
        if CLEAN_SLUG.match(n):
            return n
    return None


def _q(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def extract(root: Path) -> tuple[list[str], dict, dict]:
    files = sorted(p for p in root.glob("*.md") if p.is_file() and "nda-locked" not in p.parts)

    # pass 1: canonical slugs + candidate name-aliases
    texts: dict[Path, str] = {}
    canonical: set[str] = set()
    for path in files:
        texts[path] = path.read_text(encoding="utf-8", errors="replace")
        canonical.add(slug_from_filename(path.name))

    alias: dict[str, str | None] = {}
    for path in files:
        cslug = slug_from_filename(path.name)
        nm = name_slug(texts[path])
        if not nm or nm == cslug or nm in canonical:
            continue  # missing/self/would-shadow a real node
        if nm in alias and alias[nm] != cslug:
            alias[nm] = None  # ambiguous: two files claim the same name -> refuse to alias
        else:
            alias.setdefault(nm, cslug)
    alias = {k: v for k, v in alias.items() if v}  # drop ambiguous

    # pass 2: emit facts
    facts: set[str] = set()
    provenance: dict[str, list] = {}
    alias_hits = 0
    for path in files:
        cslug = slug_from_filename(path.name)
        facts.add(f'primitive("{_q(cslug)}").')
        facts.add(f'file("{_q(cslug)}","{_q(path.name)}").')
        for lineno, line in enumerate(texts[path].splitlines(), 1):
            for m in WIKILINK.finditer(line):
                raw = slug_from_link(m.group(1))
                if not raw:
                    continue
                tgt = alias.get(raw, raw)
                if tgt != raw:
                    alias_hits += 1
                facts.add(f'links("{_q(cslug)}","{_q(tgt)}").')
                provenance.setdefault(f"{cslug}->{tgt}", []).append(
                    {"file": path.name, "line": lineno, "syntax": "wikilink"}
                )
            for m in BRACKETTAG.finditer(line):
                raw = slug_from_link(m.group(1))
                if not raw:
                    continue
                tgt = alias.get(raw, raw)
                facts.add(f'links("{_q(cslug)}","{_q(tgt)}").')
                provenance.setdefault(f"{cslug}->{tgt}", []).append(
                    {"file": path.name, "line": lineno, "syntax": "brackettag"}
                )
    for a, c in sorted(alias.items()):
        facts.add(f'alias("{_q(a)}","{_q(c)}").')

    stats = {
        "files": len(files),
        "nodes": sum(1 for f in facts if f.startswith("primitive(")),
        "edges": sum(1 for f in facts if f.startswith("links(")),
        "aliases": len(alias),
        "alias_resolved_links": alias_hits,
    }
    return sorted(facts), provenance, stats


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(DEFAULT_ROOT), help="markdown graph root (flat *.md)")
    ap.add_argument("--out", default=None, help="output dir (default: <root>/_system/asp)")
    args = ap.parse_args()

    root = Path(args.root)
    out = Path(args.out) if args.out else root / "_system" / "asp"
    out.mkdir(parents=True, exist_ok=True)

    facts, provenance, stats = extract(root)
    (out / "facts.lp").write_text("\n".join(facts) + "\n", encoding="utf-8")
    (out / "provenance.json").write_text(
        json.dumps(provenance, indent=0, sort_keys=True), encoding="utf-8"
    )
    print(
        f"extracted {stats['files']} files -> {stats['nodes']} nodes, {stats['edges']} edges "
        f"({stats['aliases']} name-aliases resolving {stats['alias_resolved_links']} links) "
        f"-> {out / 'facts.lp'}"
    )


if __name__ == "__main__":
    main()
