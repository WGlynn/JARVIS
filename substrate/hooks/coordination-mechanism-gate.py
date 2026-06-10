#!/usr/bin/env python3
"""Coordination-mechanism gate. Classify Agent spawn → recommend cheaper tier when applicable.
Cost-saving augmentation, not block. Per Rick TG 2026-06-10 + [P·apply-the-rule-you-just-wrote].
Signals: description + prompt body + subagent_type. Surfaces downgrade-only + Code-Mode hint.
Logs all fires to telemetry for future corpus-based tuning."""

import json
import re
import sys
import datetime as dt
from pathlib import Path

TIER_RANK = {'haiku': 0, 'sonnet': 1, 'opus': 2}

TELEMETRY = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'coordination_gate_fires.jsonl'

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
# Code-Mode pattern: deterministic multi-step suggests Python orchestrator
# would beat N tool calls. Per [P·code-mode-orchestration].
CODE_MODE_HINT = [
    r'\b(for each|loop over|iterate|batch process|across (all|N|every))\b',
    r'\b(N files|each (file|primitive|hook|entry))\b',
]

# Subagent-type defaults — Plan/Explore are inherently lighter than general-purpose
SUBAGENT_DEFAULTS = {
    'Explore': 'sonnet',   # reading, no synthesis
    'Plan': 'sonnet',      # reasoning, structured output
    'general-purpose': 'sonnet',  # default
    'statusline-setup': 'haiku',  # trivial
    'claude-code-guide': 'sonnet',  # research-shape
}


def classify(d: str, prompt: str, subagent_type: str) -> tuple[str, str]:
    combined = (d + ' ' + prompt).lower()
    for pat in SUBSTANTIVE:
        if re.search(pat, combined):
            return ('opus', pat)
    for pat in TRIVIAL:
        if re.search(pat, combined):
            return ('haiku', pat)
    if subagent_type == 'statusline-setup':
        return ('haiku', 'subagent_type=statusline-setup is trivial')
    if len(d) < 80 and len(prompt) < 400:
        return ('haiku', 'short description AND short prompt body')
    return ('sonnet', 'default mid-tier')


def code_mode_match(combined: str) -> str | None:
    for pat in CODE_MODE_HINT:
        if re.search(pat, combined):
            return pat
    return None


def log_fire(entry: dict) -> None:
    try:
        TELEMETRY.parent.mkdir(parents=True, exist_ok=True)
        with TELEMETRY.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except Exception:
        pass  # never block on telemetry failure


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print('{}')
        return 0
    ti = payload.get('tool_input') or payload.get('toolInput') or {}
    desc = ti.get('description', '')
    prompt = ti.get('prompt', '')
    subagent_type = ti.get('subagent_type', 'general-purpose')
    if not desc:
        print('{}')
        return 0
    rec, why = classify(desc, prompt, subagent_type)
    actual = (ti.get('model') or SUBAGENT_DEFAULTS.get(subagent_type, 'sonnet')).lower()
    combined_lower = (desc + ' ' + prompt).lower()
    cm_hint = code_mode_match(combined_lower)

    log_fire({
        'ts': dt.datetime.now().isoformat(timespec='seconds'),
        'desc': desc[:200],
        'prompt_len': len(prompt),
        'subagent_type': subagent_type,
        'actual_model': actual,
        'recommended': rec,
        'why': why,
        'code_mode_hint': bool(cm_hint),
    })

    # Build advisory output only if there is something to say
    hints = []
    if TIER_RANK[rec] < TIER_RANK[actual]:
        hints.append(f'Cost-saving opportunity: {actual} → {rec} ({why})')
    if cm_hint:
        hints.append(f'Code-Mode hint: prompt matches deterministic-multi-step pattern "{cm_hint}". Consider writing a single Python orchestrator (Bash-executed) instead of N tool calls. Per [P·code-mode-orchestration]. ~50% token reduction at agentic scale.')

    if not hints:
        print('{}')
        return 0

    msg = '[COORDINATION-MECHANISM GATE]\n' + f'Agent spawn: {desc[:120]}\n' + '\n'.join(hints) + '\nAugmentation only; proceed if classifier is wrong.'
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'additionalContext': msg,
        }
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
