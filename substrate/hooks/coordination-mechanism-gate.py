#!/usr/bin/env python3
"""Coordination-mechanism gate. Score-based classifier with confidence + ambiguity-flag.
PreToolUse Agent. Augmentation, not block. Per Rick TG 2026-06-10 + 2026-06-10 fix
after Rick exposed "nothing's doing the assessment, just regex."

Fix shape:
  - count ALL substantive + ALL trivial matches (no first-match-wins)
  - length-as-signal (combined > 800 ⇒ substantive bias; < 80 ⇒ trivial bias)
  - confidence score returned alongside tier
  - low-confidence ⇒ defer to /classify (LLM-based) instead of guessing
  - upgrade-rec surfaced when substantive signals clearly exceed default tier
"""

import json
import re
import sys
import datetime as dt
from pathlib import Path

TIER_RANK = {'haiku': 0, 'sonnet': 1, 'opus': 2}
TELEMETRY = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'coordination_gate_fires.jsonl'
CONF_THRESHOLD = 0.5  # below ⇒ ambiguity-flag, recommend /classify

TRIVIAL = [
    r'\b(list|count|show|print|read|fetch|get|check|inspect|view)\s+\w+\b',
    r'\b(weather|date|time|status|version|exists?|present)\b',
    r'\b(rename|move|copy|delete) (a |the )?file\b',
]
SUBSTANTIVE = [
    r'\b(design|architecture|spec|specify|implement|build|refactor|migrate|port)\b',
    r'\b(security|audit|verification|formal|review)\b',
    r'\b(multi-step|cross-?cut|plan|strategy|roadmap|orchestrat)\b',
    r'\b(comparison|side-by-side|landscape|survey|benchmark|optimize)\b',
    r'\b(prototype|scaffold|propose) (a |the |new )?\w+\b',
]
CODE_MODE_HINT = [
    r'\b(for each|loop over|iterate|batch process|across (all|N|every))\b',
    r'\b(N files|each (file|primitive|hook|entry))\b',
]
SUBAGENT_PRIOR = {
    'Explore': ('sonnet', 0.7),
    'Plan': ('sonnet', 0.7),
    'statusline-setup': ('haiku', 0.95),
    'claude-code-guide': ('sonnet', 0.6),
}


def classify(d: str, prompt: str, subagent_type: str) -> tuple[str, str, float]:
    """Return (tier, why, confidence ∈ [0,1])."""
    combined = (d + ' ' + prompt).lower()

    if subagent_type == 'statusline-setup':
        return ('haiku', 'subagent_type strong prior', 0.95)

    s_count = sum(1 for pat in SUBSTANTIVE if re.search(pat, combined))
    t_count = sum(1 for pat in TRIVIAL if re.search(pat, combined))
    total_len = len(d) + len(prompt)

    # length-as-signal (caught false-haiku 2026-06-10: short desc + long prompt = substantive)
    if total_len > 800:
        s_count += 1
    elif total_len < 80:
        t_count += 1

    prior = SUBAGENT_PRIOR.get(subagent_type)

    if s_count == 0 and t_count == 0:
        if prior:
            return (prior[0], 'no-keyword + subagent prior', prior[1])
        return ('sonnet', 'no-keyword + length-neutral', 0.3)

    if s_count > t_count:
        margin = s_count - t_count
        conf = min(0.95, 0.5 + margin * 0.12)
        return ('opus', f's={s_count} t={t_count}', conf)

    if t_count > s_count:
        margin = t_count - s_count
        conf = min(0.95, 0.5 + margin * 0.12)
        return ('haiku', f't={t_count} s={s_count}', conf)

    return ('sonnet', f's=t={s_count}, ambiguous', 0.35)


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
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print('{}')
        return 0
    ti = payload.get('tool_input') or payload.get('toolInput') or {}
    if not isinstance(ti, dict):  # malformed payload (e.g. tool_input as string) must fail-quiet
        ti = {}
    desc = ti.get('description', '')
    prompt = ti.get('prompt', '')
    subagent_type = ti.get('subagent_type', 'general-purpose')
    if not desc:
        print('{}')
        return 0

    rec, why, conf = classify(desc, prompt, subagent_type)
    actual = (ti.get('model') or 'sonnet').lower()
    combined_lower = (desc + ' ' + prompt).lower()
    cm_hint = code_mode_match(combined_lower)

    log_fire({
        'ts': dt.datetime.now().isoformat(timespec='seconds'),
        'desc': desc[:200],
        'prompt_len': len(prompt),
        'subagent_type': subagent_type,
        'actual_model': actual,
        'recommended': rec,
        'confidence': round(conf, 2),
        'why': why,
        'code_mode_hint': bool(cm_hint),
    })

    hints = []

    # downgrade — cost saving
    if TIER_RANK[rec] < TIER_RANK[actual] and conf >= CONF_THRESHOLD:
        hints.append(f'Cost-saving: {actual} → {rec} (conf={conf:.2f}; {why})')

    # upgrade — quality protection
    if TIER_RANK[rec] > TIER_RANK[actual] and conf >= 0.7:
        hints.append(f'Quality upgrade: {actual} → {rec} (conf={conf:.2f}; {why}). Substantive signals exceed default tier.')

    # ambiguity — defer to LLM-based /classify
    if conf < CONF_THRESHOLD and actual == 'sonnet':
        hints.append(f'Classifier uncertain (conf={conf:.2f}; {why}). Consider /classify for LLM-based assessment before spawning.')

    if cm_hint:
        hints.append(f'Code-Mode hint: matches "{cm_hint}". Python orchestrator > N tool calls per [P·code-mode-orchestration]. ~50% token reduction at agentic scale.')

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
