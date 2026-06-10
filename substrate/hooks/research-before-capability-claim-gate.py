#!/usr/bin/env python3
"""AA#4 — Research-Before-Capability-Claim gate.
PreToolUse Write|Edit. Scans partner-facing draft content for capability-assertion
patterns. If ≥2 hits AND no WebSearch/WebFetch/gh in last 30 min telemetry, surfaces
advisory. Augmentation, not block. Per [F·no-bullshit-do-the-research]. Will 2026-06-10.

Credit: Rick Beato (usd8.fi / OpenZeppelin), TG 2026-06-10. His question
'how does this work? who is doing the default prompt assessment?' exposed
the regex-only weakness in coordination-mechanism-gate.py; 3 speculative
drafts collapsed when actual research returned the opposite answer.
The AA#4 gate exists because Rick poked at it.

⚠ COUPLING DEPENDENCY: this gate reads from research_tool_calls.jsonl
which is populated by sibling hook ~/.claude/hooks/research-tool-call-logger.py
(PostToolUse on WebSearch|WebFetch|Bash). If the logger is removed or
disabled, this gate falls back to 'no recent research' and over-fires.
The two hooks are coupled via filesystem at:
  ~/.claude/projects/C--Users-Will/memory/_system/research_tool_calls.jsonl
Both files reference this path. Removing one breaks the other's signal."""

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

# Data-driven class-fix from telemetry analysis 2026-06-10: false-positive on partner
# drafts where the author describes their own just-shipped code. Pattern: draft references
# "the gate" / "the classifier" / "the hook" / "the regex" etc. with first-person ownership.
# Such drafts don't need external research; the writer wrote the code.
SELF_REFERENCE_PATTERNS = [
    r'\b(the|my|this)\s+(gate|classifier|hook|regex|script|tool|harness|skill|primitive)\b',
    r'\b(i wrote|i shipped|i built|i made|i added)\s+(this|the|a)\b',
    r'\b(pushed an upgrade|patched the|updated the)\b',
]


def is_self_reference(text: str) -> bool:
    """Return True if the text describes the writer's own code (not external products)."""
    matches = sum(1 for pat in SELF_REFERENCE_PATTERNS if re.search(pat, text, re.IGNORECASE))
    return matches >= 2  # require ≥2 self-reference hits to flip; one is too weak


def get_path_and_content(payload: dict) -> tuple[str, str, str]:
    ti = payload.get('tool_input') or payload.get('toolInput') or {}
    if not isinstance(ti, dict):  # malformed payload (e.g. tool_input as string) must fail-quiet
        ti = {}
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
    # L3 hot-path: terse-ops rewrite. Source-tok ~50% reduction vs verbose form.
    # See ~/.claude/hooks/_terse_ops.py (recent/c/f).
    if not RESEARCH_LOG.exists():
        return 0
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from _terse_ops import recent
    except Exception:
        return 0
    try:
        with RESEARCH_LOG.open('r', encoding='utf-8') as fh:
            ts_list = []
            for line in fh:
                try:
                    ts_list.append(dt.datetime.fromisoformat(json.loads(line).get('ts', '')).timestamp())
                except Exception:
                    continue
        return recent(ts_list, RESEARCH_WINDOW_SECONDS)
    except Exception:
        return 0


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

    # Data-driven false-positive suppression: if draft is self-referential
    # (writer describing their own code), skip — the writer doesn't need
    # external research for code they just wrote.
    if is_self_reference(content):
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
