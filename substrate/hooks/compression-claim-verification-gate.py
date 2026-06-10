#!/usr/bin/env python3
"""AMD-style dissolution of the 4-gap measurement class.

Per [F·augmented-mechanism-design-paper]: don't patch each
observability/instrumentation gap individually. Augment the substrate with
a math-enforced invariant: every compression claim shipped through memory
or papers must declare its verification basis.

Fires PreToolUse on Write|Edit. Scans content for compression-claim
patterns (X% reduction, Y-token savings, Nx compression). When a claim
is detected, checks for a verification anchor near the claim:
  - measured-against: <source>
  - verified-by: <script>
  - benchmark: <file>
  - tokenizer: <name>
  - cache-telemetry: <file>
  - or a [unverified] / [proxy:<name>] tag

If no anchor is present within K lines of the claim, surfaces an
augmentation warning. Doesn't block — operator can ship unverified
claims with explicit [unverified] tag.

Closes the class of:
  Gap 1 (cache observability) — flags claims about cache hit-rate without telemetry
  Gap 2 (task-quality verification) — flags compression claims without round-trip benchmark
  Gap 3 (tokenizer mismatch) — flags token-count claims without naming the tokenizer
  Gap 4 (harness opacity) — flags multiplicative-cost claims without harness inspection

ASCII-only output (cp1252-safe).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import re
from pathlib import Path

TELEMETRY = Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory' / '_system' / 'compression_claim_gate_fires.jsonl'

# Targets memory + papers + substrate docs (anywhere compression claims could be shipped)
TARGET_PATH_PATTERNS = [
    r'memory[/\\].*\.md$',
    r'papers[/\\].*\.md$',
    r'jarvis-monorepo[/\\].*\.md$',
    r'docs[/\\]jarvis-substrate[/\\].*\.md$',
    r'ARCHITECTURE\.md$',
]

# Compression-claim patterns. Each must trigger an anchor check.
CLAIM_PATTERNS = [
    (r'\b\d+(?:\.\d+)?\s*%\s*(?:reduction|compression|smaller|cheaper|saved?|cut|less)', 'percent-reduction'),
    (r'\b\d+(?:\.\d+)?\s*x\s+(?:compression|smaller|cheaper|fewer|reduction|speedup)', 'multiplier'),
    (r'\b\d{2,}\s*(?:->|→|to)\s*\d{2,}\s*tokens?\b', 'before-after-token-count'),
    (r'\b(?:0\.\d+|1\.\d+)\s*x\s+(?:base\s+cost|cost|rate|input|read)', 'cost-multiplier-claim'),
    (r'\b(?:cache[- ]hit|cache[- ]read|cached?\s+tokens?)\b.*\b\d+(?:\.\d+)?\s*%', 'cache-hit-percentage'),
    (r'\border[- ]of[- ]magnitude\b', 'order-of-magnitude-claim'),
    (r'\bmultiplicative\b', 'multiplicative-compound-claim'),
]

# Verification anchors. Presence within ANCHOR_WINDOW lines of a claim passes the gate.
ANCHOR_PATTERNS = [
    r'\bmeasured(?:[- ]against)?[:\s]',
    r'\bverified(?:[- ]by)?[:\s]',
    r'\bbenchmark(?:ed|ing)?\s+(?:against|via|on|in|by)\b',
    # tokenizer anchors must be specific — bare "tokenizer" is too lax
    r'\bcl100k_base\b',
    r'\bo200k_base\b',
    r'\bClaude\s+BPE\b',
    r'\btiktoken\b',
    r'\bcount_tokens\b',
    r'\bcache[- ]telemetry[:\s]',
    r'\busage\.cache_read',
    r'\busage\.cache_creation',
    r'\bharness[- ]inspect',
    r'\[unverified\]',
    r'\[proxy:\s*\w+\]',
    r'\bgap[- ]flag(?:ged)?[:\s]',
    r'\bsource[:\s]+.*\.py',
    r'\bderived\s+(?:arithmetic|from)\b',
    r'\bAnthropic.*pricing\b',
    r'\bpublished.*pricing\b',
    r'\bempirically\s+measured\b',
]
ANCHOR_WINDOW = 8  # lines


def is_target_path(path: str) -> bool:
    norm = path.replace('\\', '/').lower()
    return any(re.search(p, norm, re.IGNORECASE) for p in TARGET_PATH_PATTERNS)


def get_content(payload: dict) -> tuple[str, str, str]:
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


def find_claims(text: str) -> list[tuple[int, str, str]]:
    """Return [(line_no, claim_type, match_text)] for each detected claim."""
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        for pat, kind in CLAIM_PATTERNS:
            m = re.search(pat, line, re.IGNORECASE)
            if m:
                out.append((i, kind, m.group(0)[:80]))
    return out


def has_anchor_nearby(text: str, line_no: int) -> bool:
    lines = text.splitlines()
    lo = max(0, line_no - ANCHOR_WINDOW)
    hi = min(len(lines), line_no + ANCHOR_WINDOW + 1)
    window = '\n'.join(lines[lo:hi])
    for pat in ANCHOR_PATTERNS:
        if re.search(pat, window, re.IGNORECASE):
            return True
    return False


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

    path, content, tool_name = get_content(payload)
    if not path or not content or tool_name not in ('Write', 'Edit'):
        print('{}')
        return 0

    if not is_target_path(path):
        print('{}')
        return 0

    claims = find_claims(content)
    if not claims:
        print('{}')
        return 0

    unanchored = []
    for line_no, kind, match in claims:
        if not has_anchor_nearby(content, line_no):
            unanchored.append((line_no, kind, match))

    if not unanchored:
        print('{}')
        return 0

    log_fire({
        'path': path[-80:],
        'tool': tool_name,
        'unanchored_claims': len(unanchored),
        'total_claims': len(claims),
        'samples': [(ln, k, m) for ln, k, m in unanchored[:3]],
    })

    samples = '\n  '.join(f"L{ln+1} [{kind}] {match}" for ln, kind, match in unanchored[:3])
    msg = (
        '[COMPRESSION-CLAIM VERIFICATION GATE — AMD class-dissolver]\n'
        f'File: ...{path[-60:]}\n'
        f'Detected {len(claims)} compression-style claim(s); {len(unanchored)} lack a '
        f'verification anchor within {ANCHOR_WINDOW} lines.\n'
        f'Sample(s):\n  {samples}\n'
        'Per [F·augmented-mechanism-design-paper] applied to measurement-gap class:\n'
        '  add an anchor near each claim: measured-against / verified-by / tokenizer /\n'
        '  cache-telemetry / [unverified] / [proxy:cl100k_base] / derived arithmetic from <source>.\n'
        'Augmentation only. Mark [unverified] to ship explicitly-unverified claims.'
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
