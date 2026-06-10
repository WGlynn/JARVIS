#!/usr/bin/env python3
"""Code-mode nudge — PostToolUse hook.

Detects repeated same-tool calls in a sliding window. When ≥THRESHOLD
identical-tool fires within WINDOW seconds, surfaces a nudge toward
one Python/Bash script over N tool round-trips.

Empirical motivation: Anthropic "Code execution with MCP" (Nov 2025)
reports 150,000 → 2,000 tokens (98.7%) on a multi-file aggregation
task by replacing 5 tool calls with one script that filtered
server-side. Cline / Composio community benches converge on 5-20x
for any multi-step aggregation.

This is augmentation only — model still makes the call. Hook just
adds "consider a single script next" to context once per cluster.

ASCII-only output (cp1252-safe for downstream pipes).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import time
from pathlib import Path

LOG = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'tool_call_log.jsonl'
NUDGE_LOG = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'code_mode_nudge_fires.jsonl'

WINDOW_SECONDS = 120
THRESHOLD = 4
COOLDOWN_SECONDS = 300

WATCH_TOOLS = {'Bash', 'Read', 'Grep', 'Glob'}


def load_recent_calls() -> list[dict]:
    if not LOG.exists():
        return []
    cutoff = time.time() - WINDOW_SECONDS
    out = []
    try:
        with LOG.open('r', encoding='utf-8') as f:
            tail = f.readlines()[-200:]
        for line in tail:
            try:
                rec = json.loads(line)
                if rec.get('ts', 0) >= cutoff:
                    out.append(rec)
            except Exception:
                continue
    except Exception:
        return []
    return out


def append_call(tool: str) -> None:
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': time.time(), 'tool': tool}) + '\n')
    except Exception:
        pass


def in_cooldown() -> bool:
    if not NUDGE_LOG.exists():
        return False
    try:
        with NUDGE_LOG.open('r', encoding='utf-8') as f:
            last = None
            for line in f:
                last = line
            if last:
                rec = json.loads(last)
                return time.time() - rec.get('ts', 0) < COOLDOWN_SECONDS
    except Exception:
        return False
    return False


def log_nudge(tool: str, count: int) -> None:
    try:
        NUDGE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with NUDGE_LOG.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': time.time(), 'tool': tool, 'count': count}) + '\n')
    except Exception:
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print('{}')
        return 0

    tool = payload.get('tool_name') or payload.get('toolName') or ''
    if tool not in WATCH_TOOLS:
        print('{}')
        return 0

    append_call(tool)

    recent = load_recent_calls()
    counts = {}
    for r in recent:
        t = r.get('tool', '')
        counts[t] = counts.get(t, 0) + 1

    over = [(t, c) for t, c in counts.items() if c >= THRESHOLD]
    if not over:
        print('{}')
        return 0

    if in_cooldown():
        print('{}')
        return 0

    worst_tool, worst_count = max(over, key=lambda x: x[1])
    log_nudge(worst_tool, worst_count)

    msg = (
        '[CODE-MODE NUDGE]\n'
        f'Detected {worst_count} consecutive {worst_tool} calls in last '
        f'{WINDOW_SECONDS}s (threshold {THRESHOLD}).\n'
        'Anthropic Nov-2025 customer trace: 150k -> 2k tokens (98.7%) by '
        'replacing N tool round-trips with one server-side Python script.\n'
        f'Consider: one Bash/Python script that does the {worst_tool} loop '
        'and returns the filtered result in a single tool result.\n'
        'Per [P·code-mode-orchestration]. Augmentation; proceed if a script '
        'is wrong-shape for this task (streaming UX, partial-failure recovery, '
        'human-approval-per-call, <2s latency).'
    )
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PostToolUse',
            'additionalContext': msg,
        }
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
