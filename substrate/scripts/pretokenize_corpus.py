#!/usr/bin/env python3
"""L4 — Z-token corpus cache.
Pre-tokenize MEMORY.md + sub-indexes + WWWD corpus into BPE token-ID jsonl.
Consumers load token-IDs directly, skipping the encode pass at boot.

Uses cl100k_base (GPT-4 family) as proxy for Claude tokenizer — close
enough for the tokens-per-byte ratio. The exact ID space differs but
the relative compression and the encode-pass-skipped property hold.

Output: _system/corpus.tokens.jsonl
  one record per source file:
  {"path": str, "sha256": str, "n_bytes": int, "n_tokens": int,
   "tokens": [int,...], "mtime": float}

Re-run is idempotent — skips files whose sha256 matches the cache.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import hashlib
import json
import time
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("pip install tiktoken", file=sys.stderr)
    sys.exit(1)

MEMORY_ROOT = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory'
CACHE_PATH = MEMORY_ROOT / '_system' / 'corpus.tokens.jsonl'

SOURCES = [
    MEMORY_ROOT / 'MEMORY.md',
    MEMORY_ROOT / 'MEMORY_INDEX_PREFLIGHT.md',
    MEMORY_ROOT / 'MEMORY_INDEX_CODE.md',
    MEMORY_ROOT / 'MEMORY_INDEX_COMM.md',
    MEMORY_ROOT / 'MEMORY_INDEX_SOCIAL_SHIP.md',
    MEMORY_ROOT / 'MEMORY_INDEX_STATE_PROTOCOL.md',
    MEMORY_ROOT / 'MEMORY_AUDIT_ARSENAL.md',
    MEMORY_ROOT / '_system' / 'wwwd_corpus_priority.json',
]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_cache() -> dict:
    """Return {path: record} for incremental skip."""
    cache = {}
    if not CACHE_PATH.exists():
        return cache
    try:
        with CACHE_PATH.open('r', encoding='utf-8') as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    cache[rec['path']] = rec
                except Exception:
                    continue
    except Exception:
        return {}
    return cache


def main() -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    cache = load_cache()
    new_records = []
    skipped = 0
    re_encoded = 0
    fresh = 0
    total_bytes_in = 0
    total_tokens = 0

    for src in SOURCES:
        if not src.exists():
            print(f"  miss: {src.name}", file=sys.stderr)
            continue
        raw = src.read_bytes()
        digest = sha256_bytes(raw)
        rel = str(src.relative_to(MEMORY_ROOT))
        prior = cache.get(rel)
        total_bytes_in += len(raw)

        if prior and prior.get('sha256') == digest:
            new_records.append(prior)
            total_tokens += prior['n_tokens']
            skipped += 1
            continue

        text = raw.decode('utf-8', errors='replace')
        ids = enc.encode(text)
        rec = {
            'path': rel,
            'sha256': digest,
            'n_bytes': len(raw),
            'n_tokens': len(ids),
            'tokens': ids,
            'mtime': src.stat().st_mtime,
            'encoded_at': time.time(),
        }
        new_records.append(rec)
        total_tokens += len(ids)
        if prior:
            re_encoded += 1
        else:
            fresh += 1

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE_PATH.with_suffix('.jsonl.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        for rec in new_records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    tmp.replace(CACHE_PATH)

    print(f"L4 corpus cache -> {CACHE_PATH.name}")
    print(f"  files       : {len(new_records)}  (fresh {fresh}, re-encoded {re_encoded}, skipped {skipped})")
    print(f"  bytes in    : {total_bytes_in:,}")
    print(f"  tokens cache: {total_tokens:,}")
    print(f"  ratio       : {total_tokens / max(total_bytes_in, 1):.4f} tok/byte")
    return 0


if __name__ == '__main__':
    sys.exit(main())
