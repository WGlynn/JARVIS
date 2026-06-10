#!/usr/bin/env python3
"""Coordination-mechanism gate. Classify Agent spawn → recommend cheaper tier when applicable.
Cost-saving augmentation, not block. Per Rick TG 2026-06-10 + [P·apply-the-rule-you-just-wrote].
Initial conservative version: surface downgrade-only recommendations (haiku ⇐ sonnet/opus, sonnet ⇐ opus).
Upgrade-recommendations deferred — model decides when it needs more capacity."""

import json
import re
import sys

TIER_RANK = {'haiku': 0, 'sonnet': 1, 'opus': 2}

TRIVIAL = [
    r'\b(list|count|show|print|read|fetch|get|check)\s+\w+\b',
    r'\b(weather|date|time|status|version)\b',
    r'\b(rename|move|copy|delete) (a |the )?file\b',
]
SUBSTANTIVE = [
    r'\b(design|architecture|spec|implement|build|refactor|migrate)\b',
    r'\b(security|audit|verification|formal)\b',
    r'\b(multi-step|cross-?cut|plan|strategy|roadmap)\b',
    r'\b(comparison|side-by-side|landscape|survey)\b',
]


def classify(d: str) -> tuple[str, str]:
    dl = d.lower()
    for pat in SUBSTANTIVE:
        if re.search(pat, dl):
            return ('opus', pat)
    for pat in TRIVIAL:
        if re.search(pat, dl):
            return ('haiku', pat)
    if len(d) < 80:
        return ('haiku', 'short description (<80 char)')
    return ('sonnet', 'default mid-tier')


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print('{}')
        return 0
    ti = payload.get('tool_input') or payload.get('toolInput') or {}
    desc = ti.get('description', '')
    if not desc:
        print('{}')
        return 0
    rec, why = classify(desc)
    actual = (ti.get('model') or 'sonnet').lower()
    if actual == rec:
        print('{}')
        return 0
    if TIER_RANK[rec] >= TIER_RANK[actual]:
        print('{}')
        return 0
    msg = (
        f'[COORDINATION-MECHANISM GATE]\n'
        f'Agent spawn: {desc[:120]}\n'
        f'Cost-saving opportunity: {actual} → {rec} ({why})\n'
        f'Set model={rec} if task is genuinely this trivial. Augmentation only; proceed if classifier is wrong.'
    )
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'additionalContext': msg,
        }
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
