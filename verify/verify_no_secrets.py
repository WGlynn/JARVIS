#!/usr/bin/env python3
"""verify_no_secrets.py — fresh-clone-runnable check.

Walks the repo and scans for credential patterns that should never appear in a
public substrate: AWS keys, OpenAI/Anthropic-style API keys, private keys, JWT
tokens, generic high-entropy `token=` / `password=` assignments.

Exits 0 if no matches; exits 1 with file:line for each hit.

No deps. Run from repo root:

    python verify/verify_no_secrets.py
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".github",
    "node_modules",
    ".venv",
    "venv",
    "_archive",
    "backups",
}

SKIP_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".zip", ".tar", ".gz"}

# Pattern -> human label. Tuned for low false-positive rate; favors specificity.
PATTERNS = [
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\baws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+]{30,}['\"]", re.I), "AWS secret"),
    (re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"), "OpenAI-style secret key"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{32,}\b"), "Anthropic API key"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"), "GitHub token"),
    (re.compile(r"\bxox[baprs]-[0-9A-Za-z\-]{10,}\b"), "Slack token"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{20,}\.eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\b"), "JWT"),
    (re.compile(r"\b(?:password|passwd|pwd)\s*=\s*['\"][^'\"\s]{8,}['\"]", re.I), "password assignment"),
    (re.compile(r"\bbot[0-9]{8,}:AA[A-Za-z0-9_-]{32,}\b"), "Telegram bot token"),
]


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return True
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    if path.name == "verify_no_secrets.py":
        return True  # don't flag our own patterns
    try:
        if path.stat().st_size > 1_500_000:
            return True
    except OSError:
        return True
    return False


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, start=1):
                for pat, label in PATTERNS:
                    if pat.search(line):
                        hits.append((lineno, label, line.strip()[:120]))
    except Exception:
        pass
    return hits


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    scanned = 0
    all_hits: list[tuple[str, int, str, str]] = []

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            rel = fpath.relative_to(REPO_ROOT)
            if should_skip(rel):
                continue
            scanned += 1
            for lineno, label, snippet in scan_file(fpath):
                all_hits.append((str(rel).replace("\\", "/"), lineno, label, snippet))

    print(f"secrets scan: {scanned} files scanned")
    if all_hits:
        print(f"  HITS: {len(all_hits)}")
        for relpath, lineno, label, snippet in all_hits[:30]:
            print(f"    {relpath}:{lineno} [{label}] {snippet}")
        if len(all_hits) > 30:
            print(f"    ... and {len(all_hits) - 30} more")
        print("FAIL")
        return 1
    print("  HITS: 0")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
