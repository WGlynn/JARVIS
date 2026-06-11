#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Obsidian vault view — renders the JARVIS memory corpus as a live Obsidian
graph by mapping our [X·slug] shortcodes to [[wikilinks]] Obsidian can see.

Read-only: writes a parallel _obsidian-view/ dir of converted copies, NEVER
mutates the canonical corpus (the shortcode form stays the source of truth;
this is a projection). Makes the 'open it in Obsidian and the graph works'
claim literally true. Stdlib only.
"""
import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")
MEM = os.path.join(HOME, ".claude", "projects", "C--Users-Will", "memory")
OUT = os.path.join(MEM, "_obsidian-view")

# [X·slug] or [Label](X·slug) -> [[slug]] ; also bare [[name]] passes through.
# X is a tier letter (P/F/J/U/R/O/M). slug maps to a primitive file stem.
SHORTCODE = re.compile(r"\[([A-Z])·([a-z0-9][a-z0-9-]*)\]")
TIER_PREFIX = {"P": "primitive_", "F": "feedback_", "J": "project_",
               "U": "user_", "R": "reference_", "O": "protocol_", "M": ""}


def _stem_exists(slug: str, tier: str) -> str | None:
    cand = TIER_PREFIX.get(tier, "") + slug
    if os.path.exists(os.path.join(MEM, cand + ".md")):
        return cand
    # fall back: any file whose stem ends with the slug
    for fn in os.listdir(MEM):
        if fn.endswith(slug + ".md"):
            return fn[:-3]
    return None


def convert(text: str) -> tuple[str, int]:
    n = 0
    def repl(m):
        nonlocal n
        tier, slug = m.group(1), m.group(2)
        stem = _stem_exists(slug, tier) or (TIER_PREFIX.get(tier, "") + slug)
        n += 1
        return f"[[{stem}]]"
    return SHORTCODE.sub(repl, text), n


def main() -> int:
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    files = edges = 0
    for fn in sorted(os.listdir(MEM)):
        if not fn.endswith(".md"):
            continue
        try:
            t = open(os.path.join(MEM, fn), encoding="utf-8").read()
        except Exception:
            continue
        conv, n = convert(t)
        open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n").write(conv)
        files += 1
        edges += n
    # a .obsidian marker hint + readme so opening the dir is obvious
    open(os.path.join(OUT, "_README.md"), "w", encoding="utf-8", newline="\n").write(
        "# JARVIS memory — Obsidian view\n\n"
        "Open THIS folder as an Obsidian vault. Graph view, backlinks, and tags\n"
        "render natively. These are projected copies: [X·slug] shortcodes in the\n"
        "canonical corpus are mapped to [[wikilinks]] here. Source of truth stays\n"
        "the parent dir; regenerate with `python ~/.claude/hooks/obsidian-vault-view.py`.\n")
    print(f"obsidian-view: {files} notes, {edges} shortcode links -> wikilinks. "
          f"Open {OUT} as a vault.")
    return 0


if __name__ == "__main__":
    main()
