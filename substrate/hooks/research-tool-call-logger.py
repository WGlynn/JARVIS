#!/usr/bin/env python3
"""Companion to AA#4 gate. Logs WebSearch / WebFetch / gh tool calls to jsonl.
PostToolUse on WebSearch|WebFetch|Bash. Filters Bash for gh-commands. Fail-quiet."""

import json
import sys
import datetime as dt
from pathlib import Path

LOG = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'research_tool_calls.jsonl'


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print('{}')
        return 0

    tool_name = payload.get('tool_name') or payload.get('toolName') or ''
    ti = payload.get('tool_input') or payload.get('toolInput') or {}

    if tool_name in ('WebSearch', 'WebFetch'):
        kind = tool_name.lower()
    elif tool_name == 'Bash':
        cmd = ti.get('command', '')
        # Round-4 class-fix: any gh subcommand counts (api/repo/issue/pr/release/search/workflow/auth/...).
        # Simpler regex eliminates 'new gh subcommand added by GitHub silently misses logging.'
        if re.search(r'(?:^|[\s;|&])gh\s+\w+', cmd):
            kind = 'gh'
        else:
            print('{}')
            return 0
    else:
        print('{}')
        return 0

    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open('a', encoding='utf-8') as f:
            f.write(json.dumps({
                'ts': dt.datetime.now().isoformat(timespec='seconds'),
                'kind': kind,
            }) + '\n')
    except Exception:
        pass

    print('{}')
    return 0


import re
if __name__ == '__main__':
    sys.exit(main())
