#!/usr/bin/env python3
"""Telemetry log rotation utility for JARVIS hooks.
Per #3 audit suggestion: rotate daily, compact monthly.
Runnable as cron or standalone. Idempotent. Per [P·class-elimination-not-instance-patch]:
class-eliminates 'log will grow unbounded and grep becomes slow' for ALL telemetry files.

Strategy:
- Daily rotation: if today's date in last 7 days, leave alone; else move to YYYY-MM/ subdir
- Monthly compaction: any YYYY-MM/ subdir > 1 month old → tar.gz the contents

Usage:
    python _telemetry_rotate.py              # rotate stale files
    python _telemetry_rotate.py --compact    # also tar.gz old monthly dirs
    python _telemetry_rotate.py --dry-run    # show what would happen
"""

import argparse
import datetime as dt
import gzip
import json
import shutil
import sys
import tarfile
from pathlib import Path

TELEMETRY_DIR = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system'
ROTATE_PATTERNS = ['*.jsonl', 'wwwd_gate_fires.jsonl', 'coordination_gate_fires.jsonl',
                   'aa4_research_gate_fires.jsonl', 'research_tool_calls.jsonl',
                   'protocol_telemetry.jsonl', 'decisions_live.jsonl', 'post_gen_reflections.jsonl']

ROTATE_AGE_DAYS = 7          # files older than this get moved to monthly bucket
COMPACT_AGE_MONTHS = 1       # monthly buckets older than this get tar.gz'd


def now() -> dt.datetime:
    return dt.datetime.now()


def file_mtime(p: Path) -> dt.datetime:
    return dt.datetime.fromtimestamp(p.stat().st_mtime)


def rotate(dry_run: bool = False) -> dict:
    """Move stale jsonl files into YYYY-MM/ subdirs by mtime."""
    stats = {'rotated': 0, 'skipped_fresh': 0, 'errors': 0}
    if not TELEMETRY_DIR.exists():
        return stats
    cutoff = now() - dt.timedelta(days=ROTATE_AGE_DAYS)
    for p in TELEMETRY_DIR.glob('*.jsonl'):
        if not p.is_file():
            continue
        try:
            mt = file_mtime(p)
            if mt > cutoff:
                stats['skipped_fresh'] += 1
                continue
            bucket = TELEMETRY_DIR / mt.strftime('%Y-%m')
            if not dry_run:
                bucket.mkdir(parents=True, exist_ok=True)
                target = bucket / p.name
                if target.exists():
                    target = bucket / f"{p.stem}.{mt.strftime('%Y%m%d-%H%M%S')}{p.suffix}"
                shutil.move(str(p), str(target))
            stats['rotated'] += 1
            print(f"  rotated: {p.name} -> {bucket.name}/")
        except Exception as e:
            stats['errors'] += 1
            print(f"  error rotating {p.name}: {e}", file=sys.stderr)
    return stats


def compact(dry_run: bool = False) -> dict:
    """Compress monthly buckets older than COMPACT_AGE_MONTHS into tar.gz."""
    stats = {'compacted': 0, 'skipped_recent': 0, 'errors': 0}
    cutoff = now() - dt.timedelta(days=30 * COMPACT_AGE_MONTHS)
    for bucket in TELEMETRY_DIR.glob('????-??'):
        if not bucket.is_dir():
            continue
        try:
            year, month = bucket.name.split('-')
            bucket_date = dt.datetime(int(year), int(month), 1)
            if bucket_date > cutoff:
                stats['skipped_recent'] += 1
                continue
            archive = TELEMETRY_DIR / f"{bucket.name}.tar.gz"
            if archive.exists():
                continue
            if not dry_run:
                with tarfile.open(archive, 'w:gz') as t:
                    t.add(str(bucket), arcname=bucket.name)
                shutil.rmtree(bucket)
            stats['compacted'] += 1
            print(f"  compacted: {bucket.name} -> {archive.name}")
        except Exception as e:
            stats['errors'] += 1
            print(f"  error compacting {bucket.name}: {e}", file=sys.stderr)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compact', action='store_true', help='also compact old monthly buckets')
    parser.add_argument('--dry-run', action='store_true', help='preview without changes')
    args = parser.parse_args()

    print(f"telemetry-rotate (dir={TELEMETRY_DIR})")
    if args.dry_run:
        print("DRY RUN — no changes will be made")

    print("rotating stale jsonl files (>7d)...")
    r = rotate(dry_run=args.dry_run)
    print(f"  total: rotated={r['rotated']}, fresh-skipped={r['skipped_fresh']}, errors={r['errors']}")

    if args.compact:
        print("compacting old monthly buckets (>1mo)...")
        c = compact(dry_run=args.dry_run)
        print(f"  total: compacted={c['compacted']}, recent-skipped={c['skipped_recent']}, errors={c['errors']}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
