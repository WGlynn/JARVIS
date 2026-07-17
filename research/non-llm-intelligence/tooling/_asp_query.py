#!/usr/bin/env python3
"""_asp_query.py -- deduce over the ASP memory-graph with clingo. Zero LLM calls.

Commands:
  report            ground facts + rules, assert a single stable model, write graph_report.md
  reachable <slug>  transitive closure from <slug> (added inline; kept out of report for speed)

Exit codes: 0 healthy / 1 findings / 2 engine or determinism failure.
Part of the JARVIS non-LLM intelligence architecture -- free to copy (see repo LICENSE).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import clingo

# Default to the directory this script lives in (correct wherever it's copied), env-overridable.
DEFAULT_ROOT = Path(os.environ["JARVIS_MEMORY_ROOT"]) if os.environ.get("JARVIS_MEMORY_ROOT") \
    else Path(__file__).resolve().parent
RULES = Path(__file__).parent / "_asp_rules.lp"


def _solve(load_files: list[Path], inline: str = "") -> list[str]:
    ctl = clingo.Control(["--warn=none"])
    for f in load_files:
        ctl.load(str(f))
    parts = [("base", [])]
    if inline:
        ctl.add("q", [], inline)
        parts.append(("q", []))
    ctl.ground(parts)
    models: list[list[str]] = []
    ctl.solve(on_model=lambda m: models.append([str(s) for s in m.symbols(shown=True)]))
    if len(models) != 1:  # stratified program must have exactly one stable model
        print(f"FAIL: expected exactly 1 stable model, got {len(models)}", file=sys.stderr)
        sys.exit(2)
    return models[0]


def _classify_dead(target: str) -> str:
    """Heuristic bucket for a dead-link target (honest, coarse -- no fuzzy matching).

    file_ref   : starts with '_' -> points at a non-primitive file (handoff/boot/index), not a typo.
    concept_ref: contains '-' -> a multi-word slug; likely an intentional forward-ref (CLAUDE.md says
                 a [[name]] with no match yet is a valid "write this later" marker) or an alias miss.
    bare_word  : single token, no '-'/'_' -> likely prose false-positive or a proper noun.
    """
    if target.startswith("_"):
        return "file_ref"
    if "-" in target:
        return "concept_ref"
    return "bare_word"


def report(asp_dir: Path) -> int:
    atoms = _solve([asp_dir / "facts.lp", RULES])
    dead = sorted(a for a in atoms if a.startswith("dead_link("))
    unref = sorted(a for a in atoms if a.startswith("unreferenced("))
    dup = sorted(a for a in atoms if a.startswith("dup_slug("))

    buckets: dict[str, list[str]] = {"bare_word": [], "concept_ref": [], "file_ref": []}
    for a in dead:
        m = re.match(r'dead_link\("[^"]*","([^"]*)"\)', a)
        if m:
            buckets[_classify_dead(m.group(1))].append(a)

    lines = [
        "# ASP Memory-Graph Report (Phase 1-2)",
        "",
        "> Deduced by clingo over the wikilink graph. Zero LLM calls. Read-only (no auto-fix).",
        "> Verified: clingo == pure-Python fallback (differential), byte-deterministic extraction.",
        "> Phase scope: wikilinks + primitives + name-aliasing. Index/warm/canon files appear as",
        "> `unreferenced` until Phase 3 adds `index_entry`/`canon` facts -- expected noise.",
        "",
        f"- ⚠ slug collisions: **{len(dup)}**  (HIGH severity: ambiguous node id)",
        f"- dead links: **{len(dead)}**  "
        f"(bare_word {len(buckets['bare_word'])} · concept_ref {len(buckets['concept_ref'])} · "
        f"file_ref {len(buckets['file_ref'])})",
        f"- unreferenced nodes: **{len(unref)}**",
        "",
        "## ⚠ Slug collisions (two files → one node id → ambiguous [[links]])",
        *([f"- {a}" for a in dup] or ["- none"]),
        "",
        "## Dead links -- `bare_word` (single token: likely prose false-positive or proper noun)",
        *([f"- {a}" for a in buckets["bare_word"]] or ["- none"]),
        "",
        "## Dead links -- `concept_ref` (hyphenated slug: likely intentional forward-ref or alias miss)",
        *([f"- {a}" for a in buckets["concept_ref"]] or ["- none"]),
        "",
        "## Dead links -- `file_ref` (leading `_`: points at a non-primitive file, not a typo)",
        *([f"- {a}" for a in buckets["file_ref"]] or ["- none"]),
        "",
        "## Unreferenced nodes",
        *([f"- {a}" for a in unref] or ["- none"]),
    ]
    out = asp_dir / "graph_report.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"report -> {out}  ({len(dead)} dead: "
        f"{len(buckets['bare_word'])} bare / {len(buckets['concept_ref'])} concept / "
        f"{len(buckets['file_ref'])} file; {len(unref)} unreferenced)"
    )
    return 1 if (dead or unref) else 0


def reachable(asp_dir: Path, slug: str) -> int:
    slug = slug.strip().lower()
    inline = (
        "reachable(X,Y) :- links(X,Y). "
        "reachable(X,Z) :- reachable(X,Y), links(Y,Z). "
        f'q(Y) :- reachable("{slug}",Y). '
        "#show q/1."
    )
    atoms = _solve([asp_dir / "facts.lp"], inline=inline)
    tgts = sorted(a[len("q("):-1].strip('"') for a in atoms if a.startswith("q("))
    print(f"{slug} reaches {len(tgts)} nodes:")
    for t in tgts:
        print(f"  {t}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["report", "reachable"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    a = ap.parse_args()
    asp_dir = Path(a.root) / "_system" / "asp"
    if a.cmd == "report":
        sys.exit(report(asp_dir))
    if not a.arg:
        ap.error("reachable needs a slug")
    sys.exit(reachable(asp_dir, a.arg))


if __name__ == "__main__":
    main()
