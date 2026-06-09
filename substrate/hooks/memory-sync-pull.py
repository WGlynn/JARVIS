#!/usr/bin/env python
"""
SessionStart hook — pull memory repo before other loaders read it.

Goal: machine reads LIVE GitHub state on boot, never a stale clone.
Best-effort: never blocks boot. Logs status as additionalContext.

Behavior:
  - locate memory dir (env CLAUDE_MEMORY_DIR > ~/.claude/projects/*/memory/ that has origin)
  - git fetch origin
  - if working tree clean AND local strictly behind remote → ff-only pull
  - if dirty or diverged → skip pull, warn loud
"""
import json
import os
import subprocess
import sys
from glob import glob
from pathlib import Path


def find_memory_dir() -> Path | None:
    env = os.environ.get("CLAUDE_MEMORY_DIR")
    if env and Path(env).is_dir():
        return Path(env)
    home = Path.home()
    candidates = list((home / ".claude" / "projects").glob("*/memory"))
    for c in candidates:
        if not (c / ".git").exists():
            continue
        try:
            r = subprocess.run(
                ["git", "-C", str(c), "remote", "get-url", "origin"],
                capture_output=True, text=True, timeout=5,
            )
            if "claude-memory" in r.stdout:
                return c
        except Exception:
            pass
    return candidates[0] if candidates else None


def run(args, cwd):
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, timeout=20)


def main():
    mem = find_memory_dir()
    if not mem:
        print("[memory-sync-pull] no memory dir found, skipping", file=sys.stderr)
        return 0

    fetch = run(["git", "fetch", "--quiet", "origin"], mem)
    if fetch.returncode != 0:
        msg = f"[memory-sync-pull] fetch failed: {fetch.stderr.strip()[:200]}"
        print(msg, file=sys.stderr)
        emit_context(f"WARN: memory-sync fetch failed — running on possibly-stale local clone. {fetch.stderr.strip()[:150]}")
        return 0

    status = run(["git", "status", "--porcelain"], mem)
    dirty = bool(status.stdout.strip())

    counts = run(["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"], mem)
    if counts.returncode != 0:
        emit_context("WARN: memory-sync could not compare HEAD vs origin/main.")
        return 0
    try:
        ahead, behind = (int(x) for x in counts.stdout.split())
    except ValueError:
        return 0

    if behind == 0 and ahead == 0:
        emit_context(f"memory-sync: in sync with origin/main ({mem})")
        return 0

    if dirty:
        emit_context(
            f"WARN: memory dir dirty — skipping pull. behind={behind} ahead={ahead}. "
            f"Resolve manually before next boot to read live state."
        )
        return 0

    if ahead > 0:
        emit_context(
            f"WARN: local has {ahead} commits not on origin (behind={behind}). "
            f"Skipping ff-only pull. Push or rebase manually."
        )
        return 0

    pull = run(["git", "pull", "--ff-only", "--quiet", "origin", "main"], mem)
    if pull.returncode == 0:
        emit_context(f"memory-sync: pulled {behind} commits from origin/main ({mem})")
    else:
        emit_context(f"WARN: ff pull failed: {pull.stderr.strip()[:200]}")
    return 0


def emit_context(msg: str):
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": f"[memory-sync-pull] {msg}",
        }
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    sys.exit(main())
