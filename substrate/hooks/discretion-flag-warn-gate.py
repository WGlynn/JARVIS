#!/usr/bin/env python3
"""Discretion-flag warning gate.
PreToolUse Write|Edit on memory paths. When a memory write carries `discretion: nda`
| `partner-private` | `internal` frontmatter, surface a reminder that:
  (a) the file will be excluded from public substrate sync (good)
  (b) if a previous public mirror exists, it will be deleted on next sync
  (c) git history on the public remote still retains pre-flag content
Class-eliminates 'set discretion flag but forget about history-leakage class.'
Per [F·no-bullshit-do-the-research] AA#4 + [P·class-elimination-not-instance-patch].
"""

import json
import re
import sys
from pathlib import Path

MEMORY_PREFIXES = [
    '.claude/projects/C--Users-Will/memory/',
    '.claude\\projects\\C--Users-Will\\memory\\',
]

DISCRETION_LINE = re.compile(r'^\s*discretion:\s*(nda|partner-private|internal|private)\b', re.MULTILINE | re.IGNORECASE)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print('{}')
        return 0

    ti = payload.get('tool_input') or payload.get('toolInput') or {}
    if not isinstance(ti, dict):  # malformed payload (non-dict tool_input) must fail-quiet
        ti = {}
    tool_name = payload.get('tool_name') or payload.get('toolName') or ''
    if tool_name not in ('Write', 'Edit'):
        print('{}')
        return 0

    path = ti.get('file_path', '') or ti.get('filePath', '')
    norm = path.replace('\\', '/').lower()
    if not any(pre.lower().replace('\\', '/') in norm for pre in MEMORY_PREFIXES):
        print('{}')
        return 0

    if tool_name == 'Write':
        content = ti.get('content', '')
    else:
        content = ti.get('new_string', '') or ti.get('newString', '')

    # Read first 4KB to find frontmatter (covers very long descriptions)
    head = content[:4096]
    m = DISCRETION_LINE.search(head)
    if not m:
        print('{}')
        return 0

    val = m.group(1).lower()
    file_name = Path(path).name if path else '<unknown>'
    mirror_path = (Path.home() / 'jarvis-monorepo' / 'substrate' / 'memory' / file_name)
    mirror_existed = mirror_path.exists()

    msg = (
        '[DISCRETION-FLAG GATE]\n'
        f'Memory write with discretion={val}.\n'
        f'File: {file_name}\n'
        f'• Sync will SKIP this file going forward (correct).\n'
    )
    if mirror_existed:
        msg += f'• A public-mirror copy already exists at substrate/memory/{file_name}; next sync will DELETE it (good).\n'
        msg += '• ⚠ Git history on the public remote still retains pre-flag content. If full removal is required, see substrate/ADOPTION.md "git-history leakage class" for filter-repo + force-push instructions.\n'
    else:
        msg += '• No pre-existing public mirror; clean from the start.\n'
    msg += 'Augmentation only; proceed.'

    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'additionalContext': msg,
        }
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
