#!/usr/bin/env python3
"""cron_health_check.py — fail-loud guard against orphaned cron references.

Bottleneck dissolved: a durable cron whose prompt references a script/file that
was renamed or moved fails SILENTLY every fire (FileNotFound -> no-op), which is
invisible drift. Surfaced by the afk-corpus-reweight regression (cron pointed at a
renamed script for days). Per [F.persistent-engagement-backlog] / [P.boot-hook-fail-loud]
applied to the cron layer, and [F.primitives-are-bottleneck-dissolutions].

Recursive build-off-existing: reads the same ~/.claude/scheduled_tasks.json the cron
runtime uses; no new state. Extracts every filesystem path referenced in each task's
prompt, resolves ~, checks existence, and reports the missing ones.

Usage:
    python cron_health_check.py            # human summary; exit 1 if any missing
    python cron_health_check.py --json     # machine-readable delta
"""
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
TASKS = os.path.join(HOME, ".claude", "scheduled_tasks.json")

# Paths we care about: .claude-rooted refs ending in a known executable/doc ext.
# Covers ~/.claude/..., C:/Users/<u>/.claude/..., and bare .claude/... forms.
PATH_RE = re.compile(
    r"(?:~|[A-Za-z]:[\\/](?:Users[\\/][^\s/\\]+[\\/])?|(?<![\w./\\]))"
    r"\.claude[\\/][^\s`'\"()]+?\.(?:py|md|sh|json|js|ts)",
    re.IGNORECASE,
)


def resolve(p: str) -> str:
    p = p.strip().strip("`'\"")
    if p.startswith("~"):
        p = HOME + p[1:]
    # bare ".claude/..." -> home-rooted
    if p.startswith(".claude"):
        p = os.path.join(HOME, p)
    return os.path.normpath(p)


def main() -> int:
    as_json = "--json" in sys.argv
    if not os.path.exists(TASKS):
        print(f"[cron-health] FATAL: {TASKS} not found", file=sys.stderr)
        return 2

    with open(TASKS, encoding="utf-8") as fh:
        data = json.load(fh)

    missing = []
    checked = 0
    for task in data.get("tasks", []):
        prompt = task.get("prompt", "")
        seen = set()
        for m in PATH_RE.findall(prompt):
            real = resolve(m)
            if real in seen:
                continue
            seen.add(real)
            checked += 1
            if not os.path.exists(real):
                missing.append({
                    "id": task.get("id"),
                    "cron": task.get("cron"),
                    "ref": m,
                    "resolved": real,
                })

    if as_json:
        print(json.dumps({"checked": checked, "missing": missing}, indent=2))
    else:
        print(f"[cron-health] {checked} path-refs checked across "
              f"{len(data.get('tasks', []))} tasks; {len(missing)} missing.")
        for x in missing:
            print(f"  MISSING  cron {x['id']} ({x['cron']})")
            print(f"           ref: {x['ref']}")
            print(f"           ->  {x['resolved']}")
        if missing:
            print("\nACTION: a durable cron references a missing file -> it is "
                  "silently no-op'ing every fire. Fix the path or recreate the cron.")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
