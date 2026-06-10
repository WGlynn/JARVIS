#!/usr/bin/env python3
"""
Fix the broken-link categories that are mechanically batchable.

Cat 1 (path-depth mistakes): for each broken link, try to find a matching file
elsewhere in the repo. If found at exactly one location, rewrite the link with
a correct relative path. If found at multiple, skip and report ambiguity. If not
found anywhere, mark as Cat 5.

Cat 4 (slug-only refs like `F·jul-is-primary-liquidity`): convert `[text](F·slug)`
to just `[text]` (drop the link). These were never real paths.

Cat 3 (out-of-repo refs to ~/.claude/projects/): convert `[text](path)` to just
`[text]` (drop the link). The target lives outside the repo.

Cat 2 (JARVIS scaffold dirs): defer — needs investigation of whether dirs
were renamed.

Cat 5 (truly missing): report only, no auto-fix.

Usage:
    python fix_broken_links.py <repo_root> --csv broken.csv [--dry-run]
"""

import sys
import io
import re
import csv
import argparse
from pathlib import Path
from collections import defaultdict
from urllib.parse import unquote

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def is_slug_ref(link: str) -> bool:
    """Cat 4: bare slug like 'F·jul-is-primary-liquidity' (no slash, no extension)."""
    return "/" not in link and "." not in link and (
        "·" in link or any(link.startswith(p) for p in ("P·", "F·", "J·", "U·", "R·", "O·", "M·"))
    )


def is_outside_repo(link: str) -> bool:
    """Cat 3: refs into user home / outside-repo paths."""
    return (
        ".claude/projects/" in link
        or "/Users-Will/memory" in link
        or link.count("../") >= 3 and ".claude" in link
    )


def is_jarvis_scaffold_dir(link: str, source: Path) -> bool:
    """Cat 2: jarvis-substrate scaffold subdirs (defer)."""
    if "jarvis-substrate" not in str(source):
        return False
    scaffold = ["01-hooks", "02-persistence", "03-anti-hallucination",
                "04-discipline", "05-meta-protocols", "06-agent-overlay",
                "07-stateful-applications", "08-filesystem-as-substrate",
                "/verify/", "/LICENSE"]
    return any(s in link for s in scaffold)


def find_matching_file(target_name: str, repo_root: Path) -> list:
    """Search for files matching the target basename across the repo. Returns relative paths."""
    matches = []
    # Index by basename for fast lookup
    target_path = target_name.replace("\\", "/")
    target_basename = Path(target_path).name

    for p in repo_root.rglob(target_basename):
        # Skip artifact dirs
        parts = set(p.parts)
        if any(skip in parts for skip in [".git", "node_modules", "out", "out-full", "out-ci", "out-deploy", "dist", "build", "__pycache__", ".cache", "target", "cache"]):
            continue
        matches.append(p)
    return matches


def relative_link(source: Path, target: Path) -> str:
    """Compute proper relative link from source file to target file."""
    rel = Path("/".join(["../"] * (len(source.parent.relative_to(source.parents[-1]).parts)) ))
    # Use os.path.relpath via pathlib equivalent
    import os
    rel = os.path.relpath(target, source.parent).replace("\\", "/")
    return rel


def apply_link_replacement(file_text: str, old_link: str, new_text: str) -> tuple:
    """Replace `(old_link)` with `(new_text)` inside markdown link patterns.
    If new_text is None or empty string, convert to bare bracket form by removing `(old_link)`.
    Returns (new_text, count_replaced).
    """
    # Match `](old_link)` or `](old_link "...")`
    escaped = re.escape(old_link)
    pattern = re.compile(r"\]\(" + escaped + r"(?:\s+\"[^\"]*\")?\)")
    if new_text is None or new_text == "":
        # Drop the parens entirely → leaves `[text]`
        new_pattern = "]"
    else:
        new_pattern = f"]({new_text})"
    new, count = pattern.subn(new_pattern, file_text)
    return new, count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root")
    parser.add_argument("--csv", required=True, help="Broken-links CSV from find_broken_links.py")
    parser.add_argument("--dry-run", action="store_true", help="Report fixes but don't write")
    parser.add_argument("--apply", choices=["cat1", "cat3", "cat4", "all"], default="all",
                        help="Which categories to apply (default: all batchable)")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()

    with open(args.csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded {len(rows)} broken links from {args.csv}")

    # Categorize
    cat_rows = defaultdict(list)
    for r in rows:
        link = r["broken_link"]
        src = repo_root / r["source_file"]
        if is_slug_ref(link):
            cat_rows["cat4"].append(r)
        elif is_outside_repo(link):
            cat_rows["cat3"].append(r)
        elif is_jarvis_scaffold_dir(link, src):
            cat_rows["cat2"].append(r)
        else:
            cat_rows["cat1_or_5"].append(r)

    print(f"  Cat1/5 (path or missing): {len(cat_rows['cat1_or_5'])}")
    print(f"  Cat2 (jarvis scaffold):   {len(cat_rows['cat2'])} [DEFERRED]")
    print(f"  Cat3 (out-of-repo):       {len(cat_rows['cat3'])}")
    print(f"  Cat4 (slug refs):         {len(cat_rows['cat4'])}")

    # Group edits by source file (so we read/write once)
    edits_by_file = defaultdict(list)  # {source_path: [(old_link, new_target_or_None), ...]}
    stats = {"cat1_fixed": 0, "cat1_ambiguous": 0, "cat3_dropped": 0, "cat4_dropped": 0, "cat5_truly_missing": 0}

    # Cat 4 — drop the link, keep bracket text
    if args.apply in ("cat4", "all"):
        for r in cat_rows["cat4"]:
            src = repo_root / r["source_file"]
            edits_by_file[src].append((r["broken_link"], None))
            stats["cat4_dropped"] += 1

    # Cat 3 — drop the link (target is outside repo)
    if args.apply in ("cat3", "all"):
        for r in cat_rows["cat3"]:
            src = repo_root / r["source_file"]
            edits_by_file[src].append((r["broken_link"], None))
            stats["cat3_dropped"] += 1

    # Cat 1 — find matching file by basename and rewrite path
    if args.apply in ("cat1", "all"):
        for r in cat_rows["cat1_or_5"]:
            src = repo_root / r["source_file"]
            link = r["broken_link"]
            # Strip anchor / query for basename match
            target_basename = unquote(link.split("#", 1)[0].split("?", 1)[0])
            # If link has no extension, skip (not a file ref)
            if "." not in Path(target_basename).name:
                stats["cat5_truly_missing"] += 1
                continue
            matches = find_matching_file(target_basename, repo_root)
            if len(matches) == 1:
                # Compute relative link
                new_rel = Path(matches[0]).relative_to(src.parent.resolve(), walk_up=True) if hasattr(Path, "is_relative_to") else None
                # Use os.path.relpath for compatibility
                import os
                new_rel = os.path.relpath(matches[0], src.parent).replace("\\", "/")
                # Preserve anchor if any
                anchor = ""
                if "#" in link:
                    anchor = "#" + link.split("#", 1)[1]
                edits_by_file[src].append((link, new_rel + anchor))
                stats["cat1_fixed"] += 1
            elif len(matches) > 1:
                stats["cat1_ambiguous"] += 1
            else:
                stats["cat5_truly_missing"] += 1

    # Apply edits
    files_modified = 0
    total_replacements = 0
    failed = []
    for src, edits in edits_by_file.items():
        try:
            text = src.read_text(encoding="utf-8")
        except Exception as e:
            failed.append((src, str(e)))
            continue
        new_text = text
        local_count = 0
        for old_link, new_link in edits:
            updated, n = apply_link_replacement(new_text, old_link, new_link)
            if n > 0:
                new_text = updated
                local_count += n
        if new_text != text and local_count > 0:
            files_modified += 1
            total_replacements += local_count
            if not args.dry_run:
                src.write_text(new_text, encoding="utf-8")

    print(f"\n=== Results ===")
    print(f"Cat1 path-rewrites: {stats['cat1_fixed']}")
    print(f"Cat1 ambiguous (multiple matches, skipped): {stats['cat1_ambiguous']}")
    print(f"Cat3 dropped (out-of-repo): {stats['cat3_dropped']}")
    print(f"Cat4 dropped (slug refs): {stats['cat4_dropped']}")
    print(f"Cat5 truly missing (no auto-fix): {stats['cat5_truly_missing']}")
    print(f"Files modified: {files_modified}")
    print(f"Total replacements: {total_replacements}")
    if failed:
        print(f"\nFailed reads:")
        for f, e in failed:
            print(f"  {f}: {e}")
    if args.dry_run:
        print("\n(DRY RUN — no files written)")


if __name__ == "__main__":
    main()
