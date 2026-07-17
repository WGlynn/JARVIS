#!/usr/bin/env python3
"""_asp_fallback.py -- pure-Python semi-naive Datalog fixpoint over the memory-graph facts.

Independent second engine for {reachable, dead_link, unreferenced}. Two roles:
(1) FALLBACK if the clingo wheel ever breaks on a Python upgrade; (2) DIFFERENTIAL TEST ORACLE --
clingo and this engine agreeing on the same facts is a mechanical soundness/determinism proof the
build loop can check. All Phase-1 rules are stratified Datalog, so a plain fixpoint gives identical
answers.

Free to copy (JARVIS non-LLM intelligence architecture). Zero LLM calls, stdlib only.
"""
from __future__ import annotations

import re
from pathlib import Path

_PRIM = re.compile(r'^primitive\("([^"]*)"\)\.')
_LINK = re.compile(r'^links\("([^"]*)","([^"]*)"\)\.')
_FILE = re.compile(r'^file\("([^"]*)","([^"]*)"\)\.')


def parse_facts(facts_path: Path) -> tuple[set[str], list[tuple[str, str]]]:
    prims: set[str] = set()
    edges: list[tuple[str, str]] = []
    for line in Path(facts_path).read_text(encoding="utf-8").splitlines():
        m = _PRIM.match(line)
        if m:
            prims.add(m.group(1))
            continue
        m = _LINK.match(line)
        if m:
            edges.append((m.group(1), m.group(2)))
    return prims, edges


def parse_files(facts_path: Path) -> dict[str, list[str]]:
    """slug -> [filenames] from file/2 facts."""
    slug_files: dict[str, list[str]] = {}
    for line in Path(facts_path).read_text(encoding="utf-8").splitlines():
        m = _FILE.match(line)
        if m:
            slug_files.setdefault(m.group(1), []).append(m.group(2))
    return slug_files


def dup_slugs(slug_files: dict[str, list[str]]) -> set[tuple[str, str, str]]:
    """(slug, f1, f2) pairs where two files canonicalize to the same node id (f1 < f2)."""
    out: set[tuple[str, str, str]] = set()
    for slug, files in slug_files.items():
        s = sorted(files)
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                out.add((slug, s[i], s[j]))
    return out


def dead_links(prims: set[str], edges: list[tuple[str, str]]) -> set[tuple[str, str]]:
    return {(a, b) for (a, b) in edges if b not in prims}


def unreferenced(prims: set[str], edges: list[tuple[str, str]]) -> set[str]:
    referenced = {b for (_, b) in edges}
    return {p for p in prims if p not in referenced}


def reachable_from(edges: list[tuple[str, str]], start: str) -> set[str]:
    adj: dict[str, set[str]] = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
    seen: set[str] = set()
    stack = list(adj.get(start, ()))
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj.get(n, ()))
    return seen


if __name__ == "__main__":
    import sys

    facts = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).parent / "_system" / "asp" / "facts.lp"
    )
    p, e = parse_facts(facts)
    dl, ur = dead_links(p, e), unreferenced(p, e)
    print(f"fallback: {len(p)} nodes, {len(e)} edges, {len(dl)} dead, {len(ur)} unreferenced")
