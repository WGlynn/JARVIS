#!/usr/bin/env python3
"""L4 consumer — corpus-cache warmer.
SessionStart hook. Reads _system/corpus.tokens.jsonl, detects stale
entries (sha256 drift since last pretokenize), auto-refreshes the cache,
and emits per-file token budget visibility into boot context.

This is the hook that flips L4 from CACHE-BUILT to actually deployed.
Value:
  1. Boot-time token budget visibility (how many tokens MEMORY.md is, etc.)
  2. Staleness self-healing (auto re-run pretokenize on drift)
  3. Foundation for future tokenizer-aware consumers
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import hashlib
import json
import subprocess
from pathlib import Path

MEMORY_ROOT = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory'
CACHE_PATH = MEMORY_ROOT / '_system' / 'corpus.tokens.jsonl'
PRETOKENIZER = Path.home() / 'jarvis-monorepo' / 'substrate' / 'scripts' / 'pretokenize_corpus.py'


def sha256_path(p: Path) -> str | None:
    if not p.exists():
        return None
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except Exception:
        return None


def load_cache() -> list[dict]:
    if not CACHE_PATH.exists():
        return []
    recs = []
    try:
        with CACHE_PATH.open('r', encoding='utf-8') as f:
            for line in f:
                try:
                    recs.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []
    return recs


def detect_stale(recs: list[dict]) -> list[str]:
    stale = []
    for rec in recs:
        src = MEMORY_ROOT / rec['path']
        cur = sha256_path(src)
        if cur is None:
            continue  # file missing now; surface separately
        if cur != rec.get('sha256'):
            stale.append(rec['path'])
    return stale


def refresh_cache() -> bool:
    if not PRETOKENIZER.exists():
        return False
    try:
        subprocess.run(
            [sys.executable, str(PRETOKENIZER)],
            capture_output=True, text=True, timeout=30, check=False,
        )
        return True
    except Exception:
        return False


def main() -> int:
    try:
        json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        pass

    recs = load_cache()
    if not recs:
        # No cache yet — try to build it
        if refresh_cache():
            recs = load_cache()
        if not recs:
            print(json.dumps({
                'hookSpecificOutput': {
                    'hookEventName': 'SessionStart',
                    'additionalContext': '[L4 corpus-cache] not built. Run: python ~/jarvis-monorepo/substrate/scripts/pretokenize_corpus.py',
                }
            }))
            return 0

    stale = detect_stale(recs)
    refreshed = False
    if stale:
        refreshed = refresh_cache()
        if refreshed:
            recs = load_cache()
            stale = detect_stale(recs)

    total_tokens = sum(r.get('n_tokens', 0) for r in recs)
    total_bytes = sum(r.get('n_bytes', 0) for r in recs)
    ratio = total_tokens / max(total_bytes, 1)

    lines = [
        '[L4 corpus-cache | BPE-pre-encoded memory index]',
        f'  files: {len(recs)} | tokens: {total_tokens:,} | bytes: {total_bytes:,} | ratio: {ratio:.3f} tok/B',
    ]
    if refreshed:
        lines.append(f'  drift-detected: {len(stale)} file(s) re-encoded just now')
    elif stale:
        lines.append(f'  STALE: {len(stale)} file(s) (auto-refresh failed)')
    else:
        lines.append('  state: clean (all sha256 match)')

    # Per-file budget summary (top-5 by token cost)
    top = sorted(recs, key=lambda r: -r.get('n_tokens', 0))[:5]
    lines.append('  top-5 by token cost:')
    for r in top:
        name = Path(r['path']).name
        lines.append(f"    {r['n_tokens']:>5,} tok  {name}")

    # Boot-load budget warning (MEMORY.md > 24,400 B per system_self_report)
    # ASCII-only — hook output must be cp1252-safe for non-UTF8 stdout consumers.
    mem_rec = next((r for r in recs if r['path'].endswith('MEMORY.md')), None)
    if mem_rec and mem_rec.get('n_bytes', 0) > 24400:
        over = mem_rec['n_bytes'] - 24400
        lines.append(f'  [!] MEMORY.md is {over} bytes over the 24,400-byte boot-load budget ({mem_rec["n_tokens"]:,} tokens).')

    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'SessionStart',
            'additionalContext': '\n'.join(lines),
        }
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
