#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structural fire-witness for autonomous cron loops (UserPromptSubmit hook).

The gap this closes
-------------------
cron-keeper witnesses REGISTRATION (is the cron in scheduled_tasks.json).
cron-productivity-witness witnesses PRODUCTION (did the loop write its output log).
Nothing witnessed the middle axis: did the cron actually FIRE -- did its prompt
get injected on schedule? A cron can be registered yet never fire (machine asleep,
scheduler wedged), and for the 13 loops with no per-fire output log the whole thing
is invisible. This hook makes firing observable for EVERY cron, present and future,
with zero per-loop cooperation: it fires on the same UserPromptSubmit that carries
the cron's `type:` marker.

Honest boundary
---------------
A fire-heartbeat proves the prompt was INJECTED, not that the loop body did useful
work. It is deliberately a DIFFERENT signal from the productivity log -- the witness
reports the two axes separately (fired-but-no-output = loop-body-dead is the exact
silent-decay case we want loud). We never treat a fire-stamp as productivity.

False-positive guard
--------------------
A user prompt could contain the substring "type:". We only stamp when the extracted
marker resolves to a REAL canonical cron prompt file (cron-prompts/<marker>.md) or a
known heartbeat log already exists -- grounding the signal in a real cron, not prose.

Additive + fail-open: appends one line to _<marker>-heartbeat.log, never blocks,
prints nothing (no context pollution). Stdlib only, ASCII-only. Detection mirrors
the canonical cron-injection regex in story-mode-gate.py.

Derived: TRP2 round 2026-08-10 (silent cron fire-axis blind spot). Composes
[P.universal-coverage-hook] (O(1) hook x O(inf) loops) and [P.boot-hook-fail-loud].
"""
import json
import os
import re
import sys
import time

CLAUDE = os.path.join(os.path.expanduser("~"), ".claude")
CRON_PROMPTS = os.path.join(CLAUDE, "cron-prompts")
REGISTRY = os.path.join(CLAUDE, "scheduled_tasks.json")

# Marker at line-start or after a sentence break "<Title>. type: <marker>".
# Marker charset matches cron-prompt filenames (lowercase, digits, hyphen).
_MARKER_RE = re.compile(r"(?m)(?:^|\.\s+)type:\s*([a-z0-9][a-z0-9-]{2,})\b")
_TYPE_IN_PROMPT = re.compile(r"type:\s*([a-z0-9][a-z0-9-]{2,})")


def _registered_types():
    """Authoritative ground: the set of type: markers of live scheduled tasks.

    Covers both pointer->file crons and inline-logic crons (whose body lives in
    the prompt, so they have no cron-prompts/<marker>.md). Fail-open: on any read
    error returns None so the caller falls back to the file-existence proxy.
    """
    try:
        d = json.load(open(REGISTRY, encoding="utf-8"))
    except Exception:
        return None
    tasks = d if isinstance(d, list) else (
        d.get("tasks") or d.get("scheduled_tasks") or list(d.values()))
    types = set()
    for t in tasks if isinstance(tasks, list) else []:
        if not isinstance(t, dict):
            continue
        mm = _TYPE_IN_PROMPT.search(t.get("prompt", "") or "")
        if mm:
            types.add(mm.group(1))
    return types or None


def _resolve_marker(prompt: str):
    """Return a marker string iff it maps to a real registered cron, else None."""
    m = _MARKER_RE.search(prompt or "")
    if not m:
        return None
    marker = m.group(1)
    # Primary ground: the live task registry (covers inline-logic crons too).
    reg = _registered_types()
    if reg is not None:
        return marker if marker in reg else None
    # Fallback ground (registry unreadable): canonical prompt file / prior heartbeat.
    if os.path.isfile(os.path.join(CRON_PROMPTS, marker + ".md")):
        return marker
    if os.path.isfile(os.path.join(CRON_PROMPTS, "_" + marker + "-heartbeat.log")):
        return marker
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = payload.get("prompt", "") if isinstance(payload, dict) else ""
    marker = _resolve_marker(prompt)
    if not marker:
        return 0
    log = os.path.join(CRON_PROMPTS, "_" + marker + "-heartbeat.log")
    line = time.strftime("%Y-%m-%dT%H:%M:%S") + "  fired\n"
    try:
        # Append is atomic enough for a single short line on local fs; fail-open.
        with open(log, "a", encoding="utf-8", newline="\n") as f:
            f.write(line)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
