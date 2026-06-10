#!/usr/bin/env python3
"""
Anticipation Hook — Surface Before Tony Asks
=============================================

UserPromptSubmit hook. Anticipates what's waiting for attention BEFORE the
user has to remember to ask. Adjacent to (not duplicating) thread-resume-
detector.py: that hook reacts to prompt-token overlap; this one surfaces
items that are *waiting* regardless of what the prompt is about.

Frame: JARVIS surfaces before Tony asks.

Signals (any of them — top items merged, deduped, capped at 8 bullets):
  1. Date-anchored items coming due within +/- 3 days of today.
     Scans open_threads.md, decisions_log.md, MEMORY.md for YYYY-MM-DD
     strings. Surfaces matches with their surrounding context line.
  2. Stale PENDING items > 7 days old.
     Pulls from open_threads.md HIGH-urgency section where the (Nd)
     age marker exceeds 7.
  3. Recently surfaced but unactioned items.
     Scans the tail of protocol_telemetry.jsonl for deep-recall matches
     that have been surfaced N>=3 times in the last 50 events but
     haven't appeared in post-generation-recall (= weren't actioned).

Output: hookSpecificOutput.additionalContext, <=8 bullets, <=120 chars
each, headered "[ANTICIPATION — items waiting for attention]". If nothing
qualifies, no output (do not spam).

Constraints:
  - stdlib only
  - fail-quiet on missing inputs (augmentation, not load-bearing)
  - 3s budget
  - idempotent — does NOT write any files (telemetry log is read-only here)

Registration: NOT auto-registered. Will adds to settings.json manually:
  "UserPromptSubmit": [{
    "hooks": [{
      "type": "command",
      "command": "python ~/.claude/hooks/anticipation-hook.py"
    }]
  }]
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ============ Paths ============

HOME = Path.home()
MEMORY_DIR = HOME / ".claude" / "projects" / "C--Users-Will" / "memory"
SYSTEM_DIR = MEMORY_DIR / "_system"

OPEN_THREADS = SYSTEM_DIR / "open_threads.md"
DECISIONS_LOG = SYSTEM_DIR / "decisions_log.md"
MEMORY_MD = MEMORY_DIR / "MEMORY.md"
TELEMETRY_LOG = SYSTEM_DIR / "protocol_telemetry.jsonl"
SESSION_STATE = HOME / "vibeswap" / ".claude" / "SESSION_STATE.md"

# ============ Tunables ============

DATE_WINDOW_DAYS = 3       # +/- days from today for date-anchored items
STALE_THRESHOLD_DAYS = 7   # PENDING age threshold for "stale"
TELEMETRY_TAIL_EVENTS = 50 # how many recent telemetry events to scan
SURFACED_REPEAT_THRESHOLD = 3  # >=N surfacings = "we keep mentioning this"
MAX_BULLETS = 8
MAX_BULLET_LEN = 120

DATE_RE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")
AGE_RE = re.compile(r"\((\d+)d\)")  # matches (Nd) in open_threads
PENDING_LINE_RE = re.compile(
    r"^-\s+\*\*\[(pending|next-session|fixme|queued|section-pending|aa-candidate-pending)\]\*\*"
    r"\s*\((\d+)d?\)\s*(?:L(\d+))?\s*[-—]\s*(.+)$"
)
SOURCE_HEADER_RE = re.compile(r"^###\s+`(.+?)`\s*$")

# ============ Helpers ============

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _clip(s: str, n: int = MAX_BULLET_LEN) -> str:
    s = " ".join(s.split())
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"


def _today() -> date:
    return date.today()


# ============ Signal 1: date-anchored items in +/- 3 day window ============

def find_date_anchored_items(today: date) -> list[str]:
    """Scan open_threads, decisions_log, MEMORY.md for YYYY-MM-DD strings
    within +/- DATE_WINDOW_DAYS of today. Return clipped context lines."""
    lo = today - timedelta(days=DATE_WINDOW_DAYS)
    hi = today + timedelta(days=DATE_WINDOW_DAYS)

    sources = [
        ("open_threads", OPEN_THREADS),
        ("decisions", DECISIONS_LOG),
        ("MEMORY", MEMORY_MD),
    ]
    out: list[tuple[date, str]] = []
    seen: set[str] = set()

    for label, path in sources:
        if not path.exists():
            continue
        content = _read(path)
        if not content:
            continue
        for raw in content.splitlines():
            line = raw.strip()
            if not line:
                continue
            for m in DATE_RE.finditer(line):
                try:
                    d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                except ValueError:
                    continue
                if lo <= d <= hi and d != today:
                    key = f"{d.isoformat()}::{line[:80]}"
                    if key in seen:
                        continue
                    seen.add(key)
                    delta = (d - today).days
                    tag = (
                        f"DUE {d.isoformat()} (today)" if delta == 0
                        else f"DUE {d.isoformat()} (+{delta}d)" if delta > 0
                        else f"PAST {d.isoformat()} ({delta}d)"
                    )
                    bullet = f"[date/{label}] {tag} :: {line.lstrip('-* ').strip()}"
                    out.append((d, _clip(bullet)))
                    break  # one date hit per line
    # sort: today first, then nearest future, then most recent past
    def sort_key(item):
        d, _ = item
        delta = (d - today).days
        return (abs(delta), -delta)  # nearest, future-before-past
    out.sort(key=sort_key)
    return [b for _, b in out]


# ============ Signal 2: stale PENDING items > 7d ============

def find_stale_pending() -> list[str]:
    """From open_threads.md HIGH section, pull entries whose (Nd) age
    exceeds STALE_THRESHOLD_DAYS. Sort oldest first (most stale)."""
    if not OPEN_THREADS.exists():
        return []
    content = _read(OPEN_THREADS)
    if not content:
        return []

    in_high = False
    current_source = "?"
    rows: list[tuple[int, str]] = []
    for raw in content.splitlines():
        line = raw.rstrip()
        if line.startswith("## HIGH urgency"):
            in_high = True
            continue
        if in_high and line.startswith("## ") and "HIGH urgency" not in line:
            break
        if not in_high:
            continue
        m_src = SOURCE_HEADER_RE.match(line)
        if m_src:
            current_source = m_src.group(1)
            continue
        m = PENDING_LINE_RE.match(line)
        if not m:
            continue
        kind, age_s, _ln, text = m.groups()
        try:
            age = int(age_s)
        except ValueError:
            continue
        if age <= STALE_THRESHOLD_DAYS:
            continue
        # collapse source path to last 2 segments for readability
        src_short = "/".join(current_source.split("/")[-2:])
        bullet = f"[stale {age}d/{kind}] {src_short} :: {text}"
        rows.append((age, _clip(bullet)))

    rows.sort(key=lambda r: -r[0])  # oldest first
    return [b for _, b in rows]


# ============ Signal 3: deep-recall surfaced but not actioned ============

def find_unactioned_surfacings() -> list[str]:
    """Read tail of telemetry. Items appearing in deep-recall matches
    >= SURFACED_REPEAT_THRESHOLD times but absent from post-generation-recall
    matches = surfaced, never grabbed. Indicates a recurring relevance
    signal Will hasn't acted on."""
    if not TELEMETRY_LOG.exists():
        return []
    try:
        with TELEMETRY_LOG.open("r", encoding="utf-8", errors="replace") as f:
            # tail efficiently — read all then slice; file is JSONL, manageable
            lines = f.readlines()[-max(TELEMETRY_TAIL_EVENTS * 4, 200):]
    except Exception:
        return []

    surfaced: dict[str, int] = {}
    actioned: set[str] = set()
    events_seen = 0
    for raw in reversed(lines):
        if events_seen >= TELEMETRY_TAIL_EVENTS * 4:
            break
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        events_seen += 1
        hook = rec.get("hook", "")
        matches = rec.get("matches") or []
        if not isinstance(matches, list):
            continue
        if hook == "deep-recall":
            for item in matches:
                if isinstance(item, str):
                    surfaced[item] = surfaced.get(item, 0) + 1
        elif hook == "post-generation-recall":
            for item in matches:
                if isinstance(item, str):
                    actioned.add(item)

    candidates = [
        (cnt, name) for name, cnt in surfaced.items()
        if cnt >= SURFACED_REPEAT_THRESHOLD and name not in actioned
    ]
    candidates.sort(key=lambda r: -r[0])

    out = []
    for cnt, name in candidates:
        out.append(_clip(f"[surfaced x{cnt}, unactioned] {name}"))
    return out


# ============ Assembly ============

def assemble_bullets() -> list[str]:
    today = _today()
    bullets: list[str] = []

    # Order: most time-sensitive first
    date_items = find_date_anchored_items(today)
    stale_items = find_stale_pending()
    unactioned = find_unactioned_surfacings()

    # Round-robin-ish interleave to mix signal types, prioritized by signal 1
    quotas = {
        "date": min(4, len(date_items)),
        "stale": min(3, len(stale_items)),
        "unactioned": min(2, len(unactioned)),
    }
    # If we're under budget, fill with whatever's left
    total = sum(quotas.values())
    leftover_budget = MAX_BULLETS - total
    if leftover_budget > 0:
        for key, pool in (("date", date_items), ("stale", stale_items), ("unactioned", unactioned)):
            available = len(pool) - quotas[key]
            take = min(available, leftover_budget)
            quotas[key] += take
            leftover_budget -= take
            if leftover_budget <= 0:
                break

    bullets.extend(date_items[: quotas["date"]])
    bullets.extend(stale_items[: quotas["stale"]])
    bullets.extend(unactioned[: quotas["unactioned"]])

    # Dedupe by content prefix (defensive)
    seen: set[str] = set()
    uniq: list[str] = []
    for b in bullets:
        key = b[:80].lower()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(b)
    return uniq[:MAX_BULLETS]


# ============ Main ============

def main() -> int:
    try:
        payload = sys.stdin.read()
        _data = json.loads(payload) if payload.strip() else {}
        # We don't actually need the prompt text — anticipation is prompt-
        # agnostic by design. Parse only to fail-quiet on bad JSON.
    except Exception:
        return 0

    try:
        bullets = assemble_bullets()
    except Exception:
        return 0

    if not bullets:
        # Empty — emit nothing (per spec: do NOT spam)
        return 0

    lines = ["[ANTICIPATION — items waiting for attention]"]
    lines.extend(f"- {b}" for b in bullets)

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(lines),
        }
    }
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
