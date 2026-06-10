#!/usr/bin/env python3
"""AA#4 — Research-Before-Capability-Claim gate.
PreToolUse Write|Edit. Scans partner-facing draft content for capability-assertion
patterns. If ≥2 hits AND no WebSearch/WebFetch/gh in last 30 min telemetry, surfaces
advisory. Augmentation, not block. Per [F·no-bullshit-do-the-research]. Will 2026-06-10."""

import json
import re
import sys
import datetime as dt
from pathlib import Path

TELEMETRY = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'aa4_research_gate_fires.jsonl'
RESEARCH_LOG = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'research_tool_calls.jsonl'
RESEARCH_WINDOW_SECONDS = 30 * 60

PARTNER_PREFIXES = ['Desktop/', 'Desktop\\', 'desktop/', 'desktop\\']

CAPABILITY_PATTERNS = [
    r'\b(does|doesn\'?t|supports|works with|runs on|only does|never does|always does)\s+\w+\b',
    r'\b(has|lacks|added|removed|shipped|will ship)\s+\w+\s+(feature|support|capability|integration|api)\b',
    r'\b(tier|version|v\d+)\s+\d+\s+of\s+\w+\b',
    r'\b(claude code|hermes|openai|codex|inworld|bifrost|gpt-?\d+|gemini|grok|llama|qwen|deepseek|portkey|litellm)\s+(can|cannot|does|supports|lacks|has|works|runs|ships)\b',
    r'\b(no|without)\s+\w+\s+(subscription|api|key|account)\s+\w+\b',
    r'\b\w+\s+(is|are)\s+(substrate-agnostic|llm-agnostic|vendor-agnostic|portable|locked|coupled|bound)\b',
    r'\b(anthropic|openai|google|meta|nous)\s*-?\s*(only|specific|locked|bound)\b',
]


def get_path_and_content(payload: dict) -> tuple[str, str, str]:
    ti = payload.get('tool_input') or payload.get('toolInput') or {}
    tool_name = payload.get('tool_name') or payload.get('toolName') or ''
    path = ti.get('file_path', '') or ti.get('filePath', '')
    if tool_name == 'Write':
        content = ti.get('content', '')
    elif tool_name == 'Edit':
        content = ti.get('new_string', '') or ti.get('newString', '')
    else:
        content = ''
    return path, content, tool_name


def is_partner_facing(path: str) -> bool:
    norm = path.replace('\\', '/').lower()
    return any(pre.lower().replace('\\', '/') in norm for pre in PARTNER_PREFIXES)


def capability_hits(text: str) -> list[str]:
    hits = []
    for pat in CAPABILITY_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            hits.append(m.group(0))
    return hits


def recent_research_count() -> int:
    if not RESEARCH_LOG.exists():
        return 0
    cutoff = dt.datetime.now().timestamp() - RESEARCH_WINDOW_SECONDS
    count = 0
    try:
        with RESEARCH_LOG.open('r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    ts = dt.datetime.fromisoformat(entry.get('ts', '')).timestamp()
                    if ts >= cutoff:
                        count += 1
                except Exception:
                    continue
    except Exception:
        return 0
    return count


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

    path, content, tool_name = get_path_and_content(payload)
    if not path or not content or tool_name not in ('Write', 'Edit'):
        print('{}')
        return 0

    if not is_partner_facing(path):
        print('{}')
        return 0

    hits = capability_hits(content)
    if len(hits) < 2:
        print('{}')
        return 0

    research_count = recent_research_count()

    log_fire({
        'ts': dt.datetime.now().isoformat(timespec='seconds'),
        'path': path[-80:],
        'tool': tool_name,
        'hit_count': len(hits),
        'sample_hits': hits[:3],
        'recent_research': research_count,
    })

    if research_count > 0:
        print('{}')
        return 0

    sample = '; '.join(hits[:3])
    msg = (
        '[AA#4 — RESEARCH-BEFORE-CAPABILITY-CLAIM GATE]\n'
        f'Partner-facing draft at ...{path[-60:]} contains {len(hits)} capability-assertion patterns.\n'
        f'Samples: {sample[:200]}\n'
        'No WebSearch / WebFetch / gh in last 30 min (per telemetry).\n'
        'Per [F·no-bullshit-do-the-research]: verify before assert. Run research before saving.\n'
        'Augmentation only; proceed if claims are already verified by other means.'
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
