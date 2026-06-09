#!/usr/bin/env python3
"""
API Death Shield v1 — Conversation state persistence independent of AI liveness.

Problem: When Anthropic's API throws 500s, the AI can't write state. All existing
crash recovery (WAL, SSL Gate, auto-checkpoint) requires the AI to be alive to write.
This script runs CLIENT-SIDE via hooks — it fires even when the API is dead.

Events handled:
  stop-failure   → StopFailure hook: API error killed the turn. Auto-commit dirty
                   files, write crash marker, finalize chain. THE CRITICAL PATH.
  user-prompt    → UserPromptSubmit hook: Log every user message. Preserves the
                   human side of conversation when API dies mid-response.
  stop           → Stop hook: Heartbeat after each successful response. Tracks
                   last-known-good state.
  pre-compact    → PreCompact hook: Sync chain before context compression.

Usage in settings.json:
  "StopFailure":       [{"hooks": [{"type": "command", "command": "python .../api-death-shield.py stop-failure"}]}]
  "UserPromptSubmit":  [{"hooks": [{"type": "command", "command": "python .../api-death-shield.py user-prompt"}]}]
  "Stop":              [{"hooks": [{"type": "command", "command": "python .../api-death-shield.py stop"}]}]
  "PreCompact":        [{"hooks": [{"type": "command", "command": "python .../api-death-shield.py pre-compact"}]}]
"""

import sys
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

CHAIN_DIR = Path(__file__).parent
VIBESWAP_DIR = Path("~/vibeswap")
SHIELD_DIR = CHAIN_DIR / "shield"
CONVERSATION_LOG = SHIELD_DIR / "conversation.log"
HEARTBEAT_FILE = SHIELD_DIR / "heartbeat.json"
CRASH_MARKERS_DIR = SHIELD_DIR / "crashes"
LOG_FILE = SHIELD_DIR / "shield.log"

# Max conversation log size before rotation (500KB)
MAX_LOG_SIZE = 500_000

# SHIELD-PERSIST-LEAK defense (2026-04-21): mirror of the NDA keyword list
# in ~/.claude/bin/nda-[REDACTED-NDA]-gate.py. SOURCE OF TRUTH lives there;
# this copy is defense-in-depth so SHIELD never commits NDA material even when
# the PreToolUse gate isn't invoked (SHIELD writes run via the hook pipeline,
# not through tool-use). Keep these two lists in sync.
_NDA_KEYWORDS = [
    "[REDACTED-NDA]",
    r"M4\.1\.2",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
    "[REDACTED-NDA]",
]
_NDA_RE = re.compile("|".join(_NDA_KEYWORDS), re.IGNORECASE)


def ensure_dirs():
    SHIELD_DIR.mkdir(exist_ok=True)
    CRASH_MARKERS_DIR.mkdir(exist_ok=True)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def log(msg):
    """Append to shield log. Never crash."""
    try:
        ensure_dirs()
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{now_iso()}] {msg}\n")
    except Exception:
        pass


def read_stdin():
    """Read hook context from stdin. Returns dict or empty dict."""
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except Exception:
        pass
    return {}


def rotate_log_if_needed():
    """Rotate conversation log if it exceeds MAX_LOG_SIZE."""
    try:
        if CONVERSATION_LOG.exists() and CONVERSATION_LOG.stat().st_size > MAX_LOG_SIZE:
            archive = SHIELD_DIR / f"conversation-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.log"
            CONVERSATION_LOG.rename(archive)
            log(f"Rotated conversation log → {archive.name}")
    except Exception as e:
        log(f"Log rotation error: {e}")


def git_auto_commit(reason):
    """
    Auto-commit any dirty files in vibeswap repo.
    Returns True if a commit was made.
    """
    try:
        def run_git(*args):
            return subprocess.run(
                ["git"] + list(args),
                cwd=str(VIBESWAP_DIR),
                capture_output=True,
                text=True,
                timeout=15,
            )

        # Check for dirty files
        status = run_git("status", "--porcelain")
        if not status.stdout.strip():
            return False

        # Stage everything that's tracked + modified (not untracked)
        run_git("add", "-u")

        # Also stage known state files
        for f in [".claude/SESSION_STATE.md", ".claude/WAL.md", ".session-chain"]:
            run_git("add", f)

        # SHIELD-PERSIST-LEAK defense: scan staged diff for NDA keywords BEFORE
        # committing. Conversation-state files can absorb protected topics; if
        # any landed in the diff, abort the auto-commit, unstage, and record
        # the incident. Next-session recovery still has the heartbeat + crash
        # marker + conversation log — just not a git commit.
        staged_diff = run_git("diff", "--cached", "--no-color").stdout
        if _NDA_RE.search(staged_diff or ""):
            # Find offending files for the log
            name_status = run_git("diff", "--cached", "--name-only").stdout
            hit_lines = []
            for line in (staged_diff or "").splitlines():
                if _NDA_RE.search(line):
                    hit_lines.append(line.strip()[:160])
                    if len(hit_lines) >= 3:
                        break
            run_git("reset")  # unstage everything
            log(
                "NDA-ABORT: staged diff contained protected keywords, auto-commit aborted. "
                f"Files in staged set: {name_status.strip().replace(chr(10), ', ')[:400]}. "
                f"Sample lines: {' | '.join(hit_lines)}"
            )
            return False

        # Commit
        msg = f"[SHIELD] {reason}\n\nAuto-committed by API Death Shield on {now_iso()}"
        result = run_git("commit", "-m", msg)

        if result.returncode == 0:
            # Try to push (don't block on failure)
            run_git("push", "origin", "master")
            log(f"Auto-committed: {reason}")
            return True
        else:
            log(f"Commit failed: {result.stderr.strip()[:100]}")
            return False

    except subprocess.TimeoutExpired:
        log("Git auto-commit timed out")
        return False
    except Exception as e:
        log(f"Git auto-commit error: {e}")
        return False


def write_crash_marker(error_info):
    """Write a crash marker file for the next session to find."""
    try:
        ensure_dirs()
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        marker = CRASH_MARKERS_DIR / f"crash-{ts}.json"
        marker.write_text(json.dumps({
            "timestamp": now_iso(),
            "error": error_info,
            "last_heartbeat": read_heartbeat(),
            "git_status": get_git_status(),
        }, indent=2))
        log(f"Crash marker written: {marker.name}")
        return marker
    except Exception as e:
        log(f"Crash marker error: {e}")
        return None


def read_heartbeat():
    """Read last heartbeat data."""
    try:
        if HEARTBEAT_FILE.exists():
            return json.loads(HEARTBEAT_FILE.read_text())
    except Exception:
        pass
    return None


def get_git_status():
    """Quick git status summary."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(VIBESWAP_DIR),
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        return {
            "dirty_files": len(lines),
            "files": lines[:10],  # First 10 for context
        }
    except Exception:
        return {"dirty_files": -1, "files": []}


# ============ Event Handlers ============

def handle_stop_failure(ctx):
    """
    THE CRITICAL PATH.
    API error killed the turn. Save everything we can.
    """
    log("=== STOP FAILURE DETECTED ===")

    error_info = ctx.get("error", ctx.get("message", "Unknown API error"))
    log(f"Error: {error_info}")

    # 1. Write crash marker FIRST (cheapest operation)
    write_crash_marker(str(error_info)[:500])

    # 2. Finalize any pending chain checkpoints
    try:
        sys.path.insert(0, str(CHAIN_DIR))
        from chain import finalize, git_sync
        finalize(tag="API-DEATH")
        log("Chain finalized with API-DEATH tag")
    except Exception as e:
        log(f"Chain finalize error: {e}")

    # 3. Auto-commit dirty files
    committed = git_auto_commit(f"API error recovery — {str(error_info)[:80]}")

    # 4. Append to conversation log
    try:
        ensure_dirs()
        with open(CONVERSATION_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n--- API ERROR at {now_iso()} ---\n")
            f.write(f"Error: {error_info}\n")
            f.write(f"Auto-committed: {committed}\n")
            f.write(f"---\n")
    except Exception:
        pass

    log("=== STOP FAILURE HANDLED ===")


def handle_user_prompt(ctx):
    """
    Log every user message. This is the conversation recovery backbone.
    Even if the API dies on the response, we have the user's intent.
    """
    ensure_dirs()
    rotate_log_if_needed()

    # Extract user message from hook context
    prompt = ctx.get("prompt", ctx.get("message", ctx.get("content", "")))
    if not prompt:
        # Try to extract from nested structure
        for key in ctx:
            if isinstance(ctx[key], str) and len(ctx[key]) > 5:
                prompt = ctx[key]
                break

    if not prompt:
        return

    try:
        with open(CONVERSATION_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n[{now_iso()}] USER:\n{prompt[:2000]}\n")
    except Exception as e:
        log(f"Conversation log error: {e}")


def handle_stop(ctx):
    """
    Heartbeat after each successful response.
    If StopFailure fires next, we know the last good state.
    """
    ensure_dirs()
    try:
        heartbeat = {
            "timestamp": now_iso(),
            "turn_count": (read_heartbeat() or {}).get("turn_count", 0) + 1,
            "git_head": get_git_head(),
        }
        HEARTBEAT_FILE.write_text(json.dumps(heartbeat, indent=2))
    except Exception as e:
        log(f"Heartbeat error: {e}")


def handle_pre_compact(ctx):
    """
    Context is about to be compressed. Sync everything now.
    """
    log("PreCompact: syncing chain before compression")
    try:
        sys.path.insert(0, str(CHAIN_DIR))
        from chain import finalize, git_sync
        pending = __import__('chain').collect_pending()
        if pending:
            finalize(tag="PRE-COMPACT")
        git_sync(quiet=True)
        log("PreCompact: chain synced")
    except Exception as e:
        log(f"PreCompact error: {e}")


def get_git_head():
    """Get current git HEAD hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(VIBESWAP_DIR),
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


# ============ Recovery (called on next session boot) ============

def check_crashes():
    """
    Check for crash markers from previous sessions.
    Called by SessionStart hook or manually.
    Returns list of unprocessed crash markers.
    """
    ensure_dirs()
    crashes = []
    for f in sorted(CRASH_MARKERS_DIR.glob("crash-*.json")):
        try:
            data = json.loads(f.read_text())
            data["_file"] = str(f)
            crashes.append(data)
        except Exception:
            pass
    return crashes


def clear_crashes():
    """Mark all crash markers as processed."""
    for f in CRASH_MARKERS_DIR.glob("crash-*.json"):
        try:
            processed = f.with_suffix(".processed")
            f.rename(processed)
        except Exception:
            pass


def recovery_report():
    """Generate a recovery report for the AI to read on boot."""
    crashes = check_crashes()
    if not crashes:
        return None

    report = f"# API Death Shield Recovery Report\n\n"
    report += f"**{len(crashes)} crash(es) detected since last clean session.**\n\n"

    for i, crash in enumerate(crashes, 1):
        report += f"## Crash {i}: {crash.get('timestamp', '?')}\n"
        report += f"- Error: {crash.get('error', 'unknown')}\n"
        hb = crash.get("last_heartbeat")
        if hb:
            report += f"- Last heartbeat: {hb.get('timestamp', '?')} (turn {hb.get('turn_count', '?')})\n"
        gs = crash.get("git_status", {})
        if gs.get("dirty_files", 0) > 0:
            report += f"- Dirty files at crash: {gs['dirty_files']}\n"
            for f in gs.get("files", []):
                report += f"  - `{f}`\n"
        report += "\n"

    # Check conversation log for recent entries
    if CONVERSATION_LOG.exists():
        try:
            lines = CONVERSATION_LOG.read_text(encoding="utf-8").strip().split("\n")
            recent = lines[-20:] if len(lines) > 20 else lines
            report += "## Recent Conversation Log\n```\n"
            report += "\n".join(recent)
            report += "\n```\n"
        except Exception:
            pass

    return report


# ============ Main ============

def main():
    if len(sys.argv) < 2:
        print("Usage: api-death-shield.py <event>")
        print("Events: stop-failure, user-prompt, stop, pre-compact, check-crashes, clear-crashes, report")
        return

    event = sys.argv[1]
    ctx = read_stdin()

    handlers = {
        "stop-failure": handle_stop_failure,
        "user-prompt": handle_user_prompt,
        "stop": handle_stop,
        "pre-compact": handle_pre_compact,
    }

    if event in handlers:
        try:
            handlers[event](ctx)
        except Exception as e:
            log(f"FATAL: {event} handler crashed: {type(e).__name__}: {e}")
    elif event == "check-crashes":
        crashes = check_crashes()
        if crashes:
            print(f"{len(crashes)} unprocessed crash marker(s)")
            for c in crashes:
                print(f"  {c.get('timestamp', '?')}: {c.get('error', '?')[:60]}")
        else:
            print("No crash markers found.")
    elif event == "clear-crashes":
        clear_crashes()
        print("Crash markers cleared.")
    elif event == "report":
        report = recovery_report()
        if report:
            print(report)
        else:
            print("No crashes to report.")
    else:
        print(f"Unknown event: {event}")


if __name__ == "__main__":
    main()
