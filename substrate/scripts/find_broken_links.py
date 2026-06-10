#!/usr/bin/env python3
"""
Find broken markdown / HTML links in a repo.

For each .md / .mdx / .html file:
  - extract [text](path) and ![alt](path) markdown links
  - extract href="path" / src="path" HTML attrs
  - skip http://, https://, mailto:, tel:, #anchor-only, file://
  - resolve the path relative to the containing file
  - report any path that doesn't exist on disk

Usage:
    python find_broken_links.py <repo_root> [--csv broken.csv] [--ext .md,.html]
"""

import sys
import io
import re
import argparse
from pathlib import Path
from urllib.parse import unquote
from collections import defaultdict

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Markdown: [text](path) and ![alt](path)
# Captures group 1 = the path inside the parens
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")

# HTML href / src — captures path
HTML_HREF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)

# Skip patterns (links we don't validate)
SKIP_PREFIXES = (
    "http://", "https://", "mailto:", "tel:", "ftp://", "file://",
    "data:", "javascript:", "//",
)


def extract_links(text: str) -> list:
    """Return list of raw link strings found in text."""
    links = []
    links.extend(MD_LINK_RE.findall(text))
    links.extend(HTML_HREF_RE.findall(text))
    return links


def should_check(link: str) -> bool:
    """Skip external / scheme / anchor-only links."""
    link = link.strip()
    if not link:
        return False
    if link.startswith(SKIP_PREFIXES):
        return False
    if link.startswith("#"):
        return False  # bare anchor — refers to same file, skip
    return True


def resolve_link(link: str, source_file: Path, repo_root: Path) -> Path:
    """Resolve a link to an absolute path on disk.

    - Strip anchor fragment (#section)
    - Strip query string (?foo=bar)
    - URL-decode
    - Absolute (/) is relative to repo_root
    - Relative is relative to source_file's parent
    """
    # Strip anchor + query
    link = link.split("#", 1)[0]
    link = link.split("?", 1)[0]
    if not link:
        return None  # was anchor-only
    link = unquote(link)

    if link.startswith("/"):
        # Absolute path within the repo
        return (repo_root / link.lstrip("/")).resolve()
    else:
        return (source_file.parent / link).resolve()


def check_file(source: Path, repo_root: Path) -> list:
    """Return list of (link, resolved_path) tuples for broken links in this file."""
    try:
        text = source.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [(f"<read error: {e}>", None)]

    broken = []
    seen = set()
    for raw_link in extract_links(text):
        if not should_check(raw_link):
            continue
        if raw_link in seen:
            continue
        seen.add(raw_link)
        resolved = resolve_link(raw_link, source, repo_root)
        if resolved is None:
            continue
        if not resolved.exists():
            broken.append((raw_link, resolved))
    return broken


def scan_repo(repo_root: Path, extensions: list) -> dict:
    """Return {source_file: [(link, resolved), ...]} for files with broken links."""
    results = defaultdict(list)
    files_scanned = 0
    total_files = 0

    for ext in extensions:
        for source in repo_root.rglob(f"*{ext}"):
            # Skip node_modules, .git, build artifacts
            parts_set = set(source.parts)
            if any(skip in parts_set for skip in [".git", "node_modules", "out", "out-full", "out-ci", "out-deploy", "dist", "build", "__pycache__", ".cache", "cache", "target"]):
                continue
            total_files += 1
            broken = check_file(source, repo_root)
            files_scanned += 1
            if broken:
                results[source] = broken

    return results, files_scanned, total_files


def main():
    parser = argparse.ArgumentParser(description="Find broken links in a repo")
    parser.add_argument("repo_root")
    parser.add_argument("--ext", default=".md,.mdx,.html,.htm",
                        help="Comma-separated extensions to scan")
    parser.add_argument("--csv", help="Write results to CSV")
    parser.add_argument("--limit", type=int, default=200,
                        help="Max broken-link entries to print to stdout")
    parser.add_argument("--filter", help="Only show broken links matching substring")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    extensions = [e.strip() for e in args.ext.split(",")]

    print(f"Scanning {repo_root} for extensions: {extensions}", file=sys.stderr)
    results, files_scanned, _ = scan_repo(repo_root, extensions)

    total_broken = sum(len(v) for v in results.values())
    print(f"\nScanned {files_scanned} files. Files with broken links: {len(results)}. Total broken links: {total_broken}\n")

    # Group by source file, sorted by broken-count desc
    sorted_files = sorted(results.items(), key=lambda kv: -len(kv[1]))

    printed = 0
    for source, broken in sorted_files:
        if printed >= args.limit:
            print(f"\n... ({total_broken - printed} more broken links not shown; use --limit to see more or --csv to export)")
            break
        rel_source = source.relative_to(repo_root)
        if args.filter:
            broken_filtered = [(l, r) for l, r in broken if args.filter.lower() in l.lower() or (r and args.filter.lower() in str(r).lower())]
            if not broken_filtered:
                continue
            broken = broken_filtered
        print(f"\n📄 {rel_source}  ({len(broken)} broken)")
        for link, resolved in broken[:20]:
            print(f"    ✗ {link}")
            if resolved:
                rel_resolved = resolved.relative_to(repo_root) if resolved.is_absolute() and str(resolved).startswith(str(repo_root)) else resolved
                print(f"      → {rel_resolved}")
            printed += 1
            if printed >= args.limit:
                break

    if args.csv:
        import csv
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["source_file", "broken_link", "resolved_path"])
            for source, broken in sorted_files:
                rel_source = source.relative_to(repo_root)
                for link, resolved in broken:
                    rel_resolved = ""
                    if resolved:
                        try:
                            rel_resolved = str(resolved.relative_to(repo_root))
                        except ValueError:
                            rel_resolved = str(resolved)
                    w.writerow([str(rel_source), link, rel_resolved])
        print(f"\nCSV written: {args.csv}")


if __name__ == "__main__":
    main()
