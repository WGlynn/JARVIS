#!/usr/bin/env python3
"""Oversell gate — "am I overselling this?"

PreToolUse Write|Edit. Scans the content being written for HYPE / overclaimed
MATURITY / overclaimed CAPABILITY / unqualified STAT flourishes, and fires ONLY
when those positive claims are NOT balanced by honest-floor / deflation language.
That encodes the actual failure mode: a claim without its caveat is an oversell.

Origin: Will, 2026-09-29. After two oversells in one session (calling a Hodge
cycle-energy extract "the single most sellable" when it is off-the-shelf math that
cannot, by our own wash_sim 0%-separation result, tell a wash circle from a
legitimate one; and marking new-this-session code "SOLID / load-bearing" when
Noesis has no live network). Will: "I need a teammate/partner, not a salesman."

Complement of research-before-capability-claim-gate.py (AA#4): that gate guards
claims about EXTERNAL products in partner drafts; this one guards inflation of OUR
OWN work in any artifact. Augmentation, never a block — same contract as the
em-dash and AA#4 gates. Sibling primer on the conversational surface:
oversell-primer.py (UserPromptSubmit).

Design note (learned from AA#4 over-firing): threshold + balance, not raw presence.
'solid' or 'proven' alone is normal writing; the alarm is a one-sided-positive
artifact. Fire iff (hype+maturity+capability hits) >= 2 AND exceed deflation hits.
"""

import io
import json
import re
import sys
from pathlib import Path

TELEMETRY = (
    Path.home() / '.claude' / 'projects' / 'C--Users-Will' / 'memory'
    / '_system' / 'oversell_gate_fires.jsonl'
)

# ---- lexicons (word-boundary, case-insensitive) ----------------------------
HYPE = [
    r'impressive', r'sellable', r'revolutionary', r'breakthrough', r'game[- ]?chang\w*',
    r'best[- ]in[- ]class', r'world[- ]class', r'cutting[- ]edge', r'state[- ]of[- ]the[- ]art',
    r'unprecedented', r'groundbreaking', r'novel', r'killer\s+(feature|app)', r'magic\w*',
    r'seamless\w*', r'effortless\w*', r'blazing\w*', r'insanely', r'10x', r'100x',
    r'hugely', r'massively', r'the\s+single\s+most\s+\w+', r'most\s+sellable',
    r'highest[- ]leverage', r'no[- ]brainer',
]
MATURITY = [
    r'battle[- ]tested', r'production[- ]ready', r'bullet[- ]?proof', r'rock[- ]?solid',
    r'iron[- ]?clad', r'air[- ]?tight', r'\bproven\b', r'\bguaranteed\b',
    r'fully\s+(tested|working|complete|solved)', r'\bcomplete(ly)?\b', r'\brobust\b',
    r'maturity\s+SOLID', r'\bSOLID\b',
]
CAPABILITY = [
    r'\bsolves\b', r'\beliminates\b', r'\bensures\b', r'\bnever\s+fails\b',
    r'\balways\s+works\b', r'\bentirely\b', r'\bdetects\s+(fraud|wash|collusion)\b',
]
# unqualified numeric flourish: a big number with no baseline/null/vs nearby
STAT = re.compile(r'\b\d+(?:\.\d+)?\s*(?:x|σ|sigma|%)\b', re.IGNORECASE)
STAT_CONTEXT = re.compile(
    r'(null|baseline|vs\.?|versus|only|caveat|however|but\b|untested|sample|control|'
    r'degree[- ]preserv|not\s+yet|floor|limitation)', re.IGNORECASE)

# honest-floor / deflation language — presence of these means the writing is
# already self-balancing, so we damp the alarm.
DEFLATION = [
    r'off[- ]the[- ]shelf', r'not\s+yet', r'untested', r'thinly\s+tested', r'honest\s+(floor|baseline)',
    r'\bcaveat\b', r'\blimitation', r'\bhowever\b', r'\bbut\b', r'\bonly\b', r'\bbaseline\b',
    r'\bnull\b', r'\bunproven\b', r'\bdemo\b', r'\btheory\b', r'\bdowngrade', r'no\s+live',
    r'pre[- ]launch', r'not\s+battle[- ]tested', r'not\s+(?:a\s+)?proven', r'coupling',
    r'\bassum\w+', r'\bopen\s+(problem|question|gap)', r'does\s+not\s+(solve|close|detect)',
    r'cannot\b', r'can\'?t\b', r'not\s+(?:a\s+)?(?:detector|standalone)', r'\bmaturity\s+(DEMO|THEORY)\b',
    r'\btriage\b', r'leading\s+indicator', r'\bhedge\b', r'\bhonest\b',
]

HYPE_RE = [re.compile(p, re.IGNORECASE) for p in HYPE]
MAT_RE = [re.compile(p, re.IGNORECASE) for p in MATURITY]
CAP_RE = [re.compile(p, re.IGNORECASE) for p in CAPABILITY]
DEF_RE = [re.compile(p, re.IGNORECASE) for p in DEFLATION]


def get_content(payload):
    ti = payload.get('tool_input', {}) or {}
    path = ti.get('file_path', '') or ti.get('path', '') or ''
    # Write -> content ; Edit -> new_string ; (ignore old_string, that's being removed)
    content = ti.get('content', '')
    if not content:
        content = ti.get('new_string', '')
    return path, content or ''


def hits(res, text):
    out = []
    for r in res:
        m = r.search(text)
        if m:
            out.append(m.group(0))
    return out


def main():
    try:
        payload = json.load(io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace'))
    except Exception:
        print('{}')
        return 0

    path, text = get_content(payload)
    if not text or len(text) < 40:
        print('{}')
        return 0

    hype = hits(HYPE_RE, text)
    mat = hits(MAT_RE, text)
    cap = hits(CAP_RE, text)
    defl = hits(DEF_RE, text)

    # unqualified stat flourishes: a numeric claim with no baseline/caveat within 60 chars
    stat_hits = []
    for m in STAT.finditer(text):
        window = text[max(0, m.start() - 60): m.end() + 60]
        if not STAT_CONTEXT.search(window):
            stat_hits.append(m.group(0))

    positive = len(hype) + len(mat) + len(cap) + len(stat_hits)
    deflation = len(defl)

    # Fire only on one-sided-positive writing: >=2 positive claims that outweigh the floor.
    if positive < 2 or positive <= deflation:
        print('{}')
        return 0

    try:
        TELEMETRY.parent.mkdir(parents=True, exist_ok=True)
        with io.open(TELEMETRY, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'path': path[-80:], 'pos': positive, 'defl': deflation,
                                'hype': hype[:5], 'mat': mat[:5], 'stat': stat_hits[:5]}) + '\n')
    except Exception:
        pass

    samples = '; '.join((hype + mat + cap + stat_hits)[:5])
    msg = (
        '[OVERSELL CHECK — am I overselling this?]\n'
        f'{positive} positive claim(s), {deflation} honest-floor mention(s) in this artifact '
        f'(...{path[-50:]}).\n'
        f'Flagged: {samples[:220]}\n'
        'Will needs a teammate, not a salesman. Before saving, for EACH claim state the honest floor:\n'
        '  - Is it off-the-shelf / unoriginal? Say so.\n'
        '  - Tested in isolation vs proven in production? Do not round "green tests" up to "solid".\n'
        '  - What hidden assumption or known limitation is the claim rounding past?\n'
        'Pair every claim with its deflation, or cut it. Augmentation only; proceed if already balanced.'
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
