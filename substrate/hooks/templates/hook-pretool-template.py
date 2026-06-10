#!/usr/bin/env python3
"""TEMPLATE — copy this to add a new PreToolUse hook.

5-step adoption (10 minutes):
  1. cp templates/hook-pretool-template.py hooks/<your-hook-name>.py
  2. fill in DETECT_PATTERNS for whatever you want to catch
  3. fill in the MESSAGE that fires when patterns match
  4. add to ~/.claude/settings.json under PreToolUse with the right matcher
  5. add a payload sample to tests/test_hook_contract.py

Contract (must preserve):
  - stdin JSON → stdout JSON or empty
  - silent ('{}') when no signal
  - emit {hookSpecificOutput:{hookEventName,additionalContext}} when surfacing
  - never crash, never raise — wrap everything in try/except with fail-quiet
  - never block the main thread > 5 seconds
"""

import json
import re
import sys
import datetime as dt
from pathlib import Path

# === Configure these for your hook =========================================

# Optional telemetry log path
TELEMETRY = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'YOUR_HOOK_fires.jsonl'

# Patterns that this hook detects
DETECT_PATTERNS = [
    r'\bexample-pattern\b',
    # add more
]

# Message surfaced when a pattern matches
ADVISORY_MESSAGE = '[YOUR HOOK NAME]\nDescribe what was detected and what to do about it.'

# Optional: restrict to specific paths
PARTNER_PREFIXES = ['Desktop/', 'Desktop\\']

# === End configuration =====================================================


def hits(text: str) -> list[str]:
    out = []
    for pat in DETECT_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            out.append(m.group(0))
    return out


def is_partner_facing(path: str) -> bool:
    norm = path.replace('\\', '/').lower()
    return any(p.lower().replace('\\', '/') in norm for p in PARTNER_PREFIXES)


def log_fire(entry: dict) -> None:
    try:
        TELEMETRY.parent.mkdir(parents=True, exist_ok=True)
        with TELEMETRY.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except Exception:
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print('{}')
        return 0

    ti = payload.get('tool_input') or payload.get('toolInput') or {}
    tool_name = payload.get('tool_name') or payload.get('toolName') or ''

    # Read the field you care about (file_path / description / prompt / content / etc.)
    path = ti.get('file_path', '') or ti.get('filePath', '')
    if tool_name == 'Write':
        content = ti.get('content', '')
    elif tool_name == 'Edit':
        content = ti.get('new_string', '') or ti.get('newString', '')
    else:
        content = ''

    if not is_partner_facing(path):
        print('{}')
        return 0

    matches = hits(content)
    if not matches:
        print('{}')
        return 0

    log_fire({
        'ts': dt.datetime.now().isoformat(timespec='seconds'),
        'path': path[-80:],
        'matches': matches[:5],
    })

    msg = f'{ADVISORY_MESSAGE}\nDetected: {"; ".join(matches[:3])}\nAugmentation only; proceed if claims verified.'
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'additionalContext': msg,
        }
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
