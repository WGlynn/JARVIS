#!/usr/bin/env python3
"""
Session Chain v3 — Hash-linked cognitive state persistence.

DESIGN (learned from v1+v2 failure):
- Blocks are JSON files, not in-memory
- Each block references parent hash → tamper-evident chain
- Sub-blocks (checkpoints) survive crashes
- Index file for fast lookup without loading entire chain
- Auto-sync to git after finalization (both remotes)
- Session boundary detection — stale checkpoints auto-finalize on new session

Usage:
    python chain.py append "prompt summary" "response summary"
    python chain.py checkpoint "work in progress description"
    python chain.py finalize                    # merge sub-blocks into main block
    python chain.py pending                     # view in-progress checkpoints
    python chain.py status                      # chain stats
    python chain.py last [n]                    # last N blocks
    python chain.py sync                        # commit + push to both remotes
    python chain.py heal                        # finalize stale + sync
"""

import sys

# Force UTF-8 stdout/stderr on Windows: the usage text (__doc__) and log lines
# contain non-cp1252 chars; without this `python chain.py` tracebacks on
# UnicodeEncodeError instead of printing usage.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

import json
import hashlib
import os
import subprocess
import time
import signal
from datetime import datetime, timezone
from pathlib import Path

CHAIN_DIR = Path(__file__).parent
BLOCKS_DIR = CHAIN_DIR / "blocks"
PENDING_DIR = CHAIN_DIR / "pending"
INDEX_FILE = CHAIN_DIR / "index.json"
SESSION_FILE = CHAIN_DIR / ".current_session"

# Git repo root — session-chain is symlinked into vibeswap as .session-chain/
# This means git operations work directly through the vibeswap repo
VIBESWAP_DIR = Path("~/vibeswap")
SYMLINK_PATH = VIBESWAP_DIR / ".session-chain"


def ensure_dirs():
    BLOCKS_DIR.mkdir(exist_ok=True)
    PENDING_DIR.mkdir(exist_ok=True)


def load_index():
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {"blocks": [], "head": None, "created": now_iso()}


def save_index(index):
    INDEX_FILE.write_text(json.dumps(index, indent=2))


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def now_date():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def compute_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]


# ============ Session Tracking ============

def get_session_id():
    """Generate a session ID from PID + date. Different session = different ID."""
    # Use CLAUDE_SESSION env var if set, otherwise PID + date
    env_session = os.environ.get("CLAUDE_SESSION_ID", "")
    if env_session:
        return env_session
    # Fallback: parent PID (Claude Code process) + date
    ppid = os.getppid()
    return f"{ppid}-{now_date()}"


def get_current_session():
    """Read the stored session ID."""
    if SESSION_FILE.exists():
        try:
            data = json.loads(SESSION_FILE.read_text())
            return data.get("session_id"), data.get("started")
        except (json.JSONDecodeError, KeyError):
            pass
    return None, None


def set_current_session(session_id):
    """Write the current session ID."""
    SESSION_FILE.write_text(json.dumps({
        "session_id": session_id,
        "started": now_iso(),
    }))


def is_new_session():
    """Check if we're in a different session than the last checkpoint."""
    current = get_session_id()
    stored, _ = get_current_session()
    return stored is not None and stored != current


# ============ Core Chain Operations ============

def append_block(prompt_summary, response_summary):
    ensure_dirs()
    index = load_index()

    block = {
        "id": len(index["blocks"]),
        "parent": index["head"],
        "timestamp": now_iso(),
        "prompt": prompt_summary,
        "response": response_summary,
        "checkpoints": collect_pending(),
    }
    block["hash"] = compute_hash(block)

    # Write block file
    block_file = BLOCKS_DIR / f"block-{block['id']:04d}.json"
    block_file.write_text(json.dumps(block, indent=2))

    # Update index
    index["blocks"].append({
        "id": block["id"],
        "hash": block["hash"],
        "timestamp": block["timestamp"],
        "prompt": prompt_summary[:80],
    })
    index["head"] = block["hash"]
    save_index(index)

    # Clear pending
    clear_pending()

    print(f"Block #{block['id']} committed: {block['hash']}")
    return block


def add_checkpoint(description):
    ensure_dirs()
    cp = {
        "timestamp": now_iso(),
        "description": description,
        "hash": compute_hash({"ts": now_iso(), "desc": description}),
    }
    cp_file = PENDING_DIR / f"cp-{datetime.now(timezone.utc).strftime('%H%M%S%f')}.json"
    cp_file.write_text(json.dumps(cp, indent=2))
    print(f"Checkpoint: {cp['hash'][:8]} — {description[:60]}")
    return cp


def collect_pending():
    cps = []
    if PENDING_DIR.exists():
        for f in sorted(PENDING_DIR.glob("cp-*.json")):
            try:
                cps.append(json.loads(f.read_text()))
            except Exception:
                pass
    return cps


def clear_pending():
    if PENDING_DIR.exists():
        for f in PENDING_DIR.glob("cp-*.json"):
            f.unlink()


def finalize(tag="WIP"):
    """Merge pending checkpoints into a block."""
    cps = collect_pending()
    if not cps:
        print("Nothing to finalize.")
        return None
    desc = "; ".join(cp["description"][:40] for cp in cps)
    block = append_block(f"[{tag}] {desc[:80]}", f"{len(cps)} checkpoints finalized")
    return block


# ============ Git Sync ============

def git_sync(quiet=False):
    """Commit session-chain changes and push to both remotes via symlink."""
    if not SYMLINK_PATH.exists():
        if not quiet:
            print("Warning: .session-chain symlink not found in vibeswap, skipping git sync")
        return False

    try:
        def run_git(*args, **kwargs):
            return subprocess.run(
                ["git"] + list(args),
                cwd=str(VIBESWAP_DIR),
                capture_output=True,
                text=True,
                timeout=30,
                **kwargs,
            )

        # Check if session-chain files have changes (use symlink path)
        status = run_git("status", "--porcelain", ".session-chain")
        if not status.stdout.strip():
            if not quiet:
                print("Session chain: nothing to sync (clean)")
            return True

        # Stage session-chain files only (through the symlink)
        run_git("add", ".session-chain")

        # Commit
        index = load_index()
        head = index.get("head", "???")[:8]
        n_blocks = len(index.get("blocks", []))
        msg = f"session-chain: sync {n_blocks} blocks (head: {head})"
        result = run_git("commit", "-m", msg)

        if result.returncode != 0:
            if not quiet:
                print(f"Git commit failed: {result.stderr.strip()}")
            return False

        # Push to origin (stealth remote retired 2026-03-25)
        for remote in ["origin"]:
            push = run_git("push", remote, "master")
            if push.returncode != 0 and not quiet:
                print(f"Push to {remote} failed: {push.stderr.strip()[:80]}")

        if not quiet:
            print(f"Session chain synced: {msg}")
        return True

    except subprocess.TimeoutExpired:
        if not quiet:
            print("Git sync timed out")
        return False
    except Exception as e:
        if not quiet:
            print(f"Git sync error: {e}")
        return False


# ============ Heal (stale recovery) ============

def heal(quiet=False):
    """Finalize any stale pending checkpoints and sync to git."""
    cps = collect_pending()
    if cps:
        block = finalize(tag="RECOVERED")
        if block and not quiet:
            print(f"Healed: finalized {len(cps)} stale checkpoints into block #{block['id']}")
    git_sync(quiet=quiet)


# ============ Display ============

def show_pending():
    cps = collect_pending()
    if not cps:
        print("No pending checkpoints.")
        return
    print(f"{len(cps)} pending checkpoint(s):")
    for cp in cps:
        print(f"  [{cp['hash'][:8]}] {cp['timestamp']} — {cp['description']}")


def show_status():
    index = load_index()
    cps = collect_pending()
    sid, started = get_current_session()
    print(f"Session Chain v3")
    print(f"  Blocks: {len(index['blocks'])}")
    print(f"  Head:   {index['head'] or '(genesis)'}")
    print(f"  Pending checkpoints: {len(cps)}")
    print(f"  Created: {index.get('created', 'unknown')}")
    print(f"  Session: {sid or 'none'} (started: {started or 'unknown'})")


def show_last(n=5):
    index = load_index()
    blocks = index["blocks"][-n:]
    if not blocks:
        print("No blocks yet.")
        return
    for b in blocks:
        print(f"  #{b['id']} [{b['hash'][:8]}] {b['timestamp']} — {b['prompt']}")


# ============ Daemon Mode (Autonomous Background Service) ============

DAEMON_PID_FILE = CHAIN_DIR / ".daemon.pid"
DAEMON_LOG_FILE = CHAIN_DIR / "daemon.log"
DAEMON_INTERVAL = 300  # 5 minutes between heal cycles
AUTO_FINALIZE_THRESHOLD = 5  # Finalize pending checkpoints after this many

def daemon_log(msg):
    """Append a log line to the daemon log file."""
    ts = now_iso()
    line = f"[{ts}] {msg}\n"
    with open(DAEMON_LOG_FILE, "a") as f:
        f.write(line)


def daemon_loop():
    """
    Autonomous background service for session chain maintenance.

    Runs every DAEMON_INTERVAL seconds:
    1. Auto-finalize if pending checkpoints exceed threshold
    2. Heal stale checkpoints from dead sessions
    3. Sync to git (both remotes)

    This ensures the chain NEVER goes stale, even if no Claude session is active.
    """
    daemon_log(f"Daemon started (PID {os.getpid()}, interval {DAEMON_INTERVAL}s)")
    print(f"Session chain daemon started (PID {os.getpid()})")
    print(f"  Heal interval: {DAEMON_INTERVAL}s")
    print(f"  Auto-finalize threshold: {AUTO_FINALIZE_THRESHOLD} checkpoints")
    print(f"  Log: {DAEMON_LOG_FILE}")

    # Write PID file for management
    DAEMON_PID_FILE.write_text(json.dumps({
        "pid": os.getpid(),
        "started": now_iso(),
        "interval": DAEMON_INTERVAL,
    }))

    # Graceful shutdown
    running = [True]
    def handle_signal(sig, frame):
        daemon_log(f"Received signal {sig}, shutting down")
        running[0] = False
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    # Initial heal on startup
    daemon_heal_cycle()

    while running[0]:
        try:
            time.sleep(DAEMON_INTERVAL)
            if running[0]:
                daemon_heal_cycle()
        except KeyboardInterrupt:
            break
        except Exception as e:
            daemon_log(f"ERROR in daemon loop: {type(e).__name__}: {e}")
            time.sleep(60)  # Back off on error

    daemon_log("Daemon stopped")
    if DAEMON_PID_FILE.exists():
        DAEMON_PID_FILE.unlink()
    print("Session chain daemon stopped.")


def daemon_heal_cycle():
    """One cycle of the daemon: finalize, heal, sync."""
    try:
        pending = collect_pending()
        healed = False

        # Auto-finalize if enough checkpoints accumulated
        if len(pending) >= AUTO_FINALIZE_THRESHOLD:
            block = finalize(tag="AUTO-DAEMON")
            if block:
                daemon_log(f"Auto-finalized {len(pending)} checkpoints → block #{block['id']}")
                healed = True

        # Heal any stale checkpoints (from dead sessions)
        remaining = collect_pending()
        if remaining:
            # Check if the current session is stale (no activity for 10+ minutes)
            stored_sid, started = get_current_session()
            if stored_sid and started:
                try:
                    from datetime import datetime as dt
                    started_dt = dt.fromisoformat(started)
                    age_minutes = (datetime.now(timezone.utc) - started_dt).total_seconds() / 60
                    # If no session boundary change in 30+ minutes, consider it stale
                    if age_minutes > 30 and len(remaining) > 0:
                        block = finalize(tag="STALE-DAEMON")
                        if block:
                            daemon_log(f"Stale-finalized {len(remaining)} checkpoints → block #{block['id']} (session age: {age_minutes:.0f}min)")
                            healed = True
                except Exception:
                    pass

        # Sync to git
        synced = git_sync(quiet=True)

        index = load_index()
        daemon_log(f"Heal cycle: {len(index['blocks'])} blocks, {len(collect_pending())} pending, sync={'ok' if synced else 'skip'}")

    except Exception as e:
        daemon_log(f"Heal cycle error: {type(e).__name__}: {e}")


def daemon_start():
    """Start the daemon in the background (detached)."""
    # Check if already running
    if DAEMON_PID_FILE.exists():
        try:
            data = json.loads(DAEMON_PID_FILE.read_text())
            pid = data.get("pid")
            # Check if process is alive (Windows-compatible)
            if pid:
                try:
                    os.kill(pid, 0)  # Signal 0 = check existence
                    print(f"Daemon already running (PID {pid}, started {data.get('started', '?')})")
                    return
                except OSError:
                    daemon_log(f"Stale PID file found (PID {pid} dead), restarting")
        except Exception:
            pass

    # Start as background process (Windows-compatible detach)
    import subprocess as sp
    kwargs = {}
    if sys.platform == 'win32':
        # Windows: CREATE_NEW_PROCESS_GROUP + DETACHED_PROCESS = fully detached
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        kwargs['creationflags'] = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    else:
        kwargs['start_new_session'] = True

    log_handle = open(DAEMON_LOG_FILE, "a")
    proc = sp.Popen(
        [sys.executable, __file__, "_daemon_run"],
        stdout=log_handle,
        stderr=log_handle,
        stdin=sp.DEVNULL,
        **kwargs,
    )
    print(f"Session chain daemon started in background (PID {proc.pid})")
    print(f"  Log: {DAEMON_LOG_FILE}")
    print(f"  Stop: python chain.py daemon-stop")


def daemon_stop():
    """Stop the running daemon."""
    if not DAEMON_PID_FILE.exists():
        print("No daemon running (no PID file)")
        return

    try:
        data = json.loads(DAEMON_PID_FILE.read_text())
        pid = data.get("pid")
        if pid:
            os.kill(pid, signal.SIGTERM)
            print(f"Sent SIGTERM to daemon (PID {pid})")
            # Wait briefly for clean shutdown
            time.sleep(1)
            try:
                os.kill(pid, 0)
                # Still alive, force kill
                os.kill(pid, signal.SIGKILL if hasattr(signal, 'SIGKILL') else signal.SIGTERM)
                print(f"Force-killed daemon (PID {pid})")
            except OSError:
                print("Daemon stopped cleanly")
        DAEMON_PID_FILE.unlink(missing_ok=True)
    except Exception as e:
        print(f"Error stopping daemon: {e}")
        DAEMON_PID_FILE.unlink(missing_ok=True)


def daemon_status():
    """Show daemon status."""
    if not DAEMON_PID_FILE.exists():
        print("Daemon: NOT RUNNING")
        return

    try:
        data = json.loads(DAEMON_PID_FILE.read_text())
        pid = data.get("pid")
        started = data.get("started", "?")
        try:
            os.kill(pid, 0)
            print(f"Daemon: RUNNING (PID {pid}, started {started})")
        except OSError:
            print(f"Daemon: DEAD (stale PID {pid}, started {started})")
            DAEMON_PID_FILE.unlink(missing_ok=True)
    except Exception as e:
        print(f"Daemon: ERROR reading PID file: {e}")

    # Show recent log lines
    if DAEMON_LOG_FILE.exists():
        lines = DAEMON_LOG_FILE.read_text().strip().split("\n")
        recent = lines[-5:] if len(lines) > 5 else lines
        print(f"\nRecent log ({DAEMON_LOG_FILE}):")
        for line in recent:
            print(f"  {line}")


# ============ CLI ============

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "append":
        if len(sys.argv) < 4:
            print("Usage: chain.py append <prompt> <response>")
            return
        append_block(sys.argv[2], sys.argv[3])
    elif cmd == "checkpoint":
        if len(sys.argv) < 3:
            print("Usage: chain.py checkpoint <description>")
            return
        add_checkpoint(sys.argv[2])
    elif cmd == "finalize":
        finalize()
    elif cmd == "pending":
        show_pending()
    elif cmd == "status":
        show_status()
        print()
        daemon_status()
    elif cmd == "last":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        show_last(n)
    elif cmd == "sync":
        git_sync()
    elif cmd == "heal":
        heal()
    elif cmd == "daemon":
        daemon_start()
    elif cmd == "daemon-stop":
        daemon_stop()
    elif cmd == "daemon-status":
        daemon_status()
    elif cmd == "_daemon_run":
        # Internal: called by daemon_start() in subprocess
        daemon_loop()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
