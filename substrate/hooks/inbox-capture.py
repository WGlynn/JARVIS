#!/usr/bin/env python3
"""
Inbox capture: UserPromptSubmit hook, the front door of the two-way protocol (Will 2026-11-01).

Runs the moment Will sends a message, while the model may still be busy:
  1. Secret gate, for him: a message carrying a key shape is blocked before the model sees it
     (exit 2 erases it), and he is told to rotate the key (Constitution 2.4: a secret pasted into
     a conversation counts as burned). "#allow-secret" in the message lets it through on purpose.
  2. Durable record: the message is written to ~/.claude/state/inbox/msgs/ the moment it is sent,
     so it survives even if the window dies before the model reads it.
  3. Starts inbox-prep.py detached, so the time the message waits in the queue becomes prep time.

Must stay fast and must never eat a message by accident: every error path exits 0.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _inbox  # noqa: E402

PREP_SCRIPT = Path(__file__).resolve().parent / "inbox-prep.py"

BLOCK_MSG = (
    "Blocked before it reached the model: this message contains a key shape ({kind}).\n"
    "Treat that key as burned and rotate it (Constitution 2.4). To use a key, put it straight into\n"
    "the .env or config file instead of the chat. To send this message anyway, add #allow-secret.\n"
)


def spawn_prep(msg_path):
    flags = 0
    if os.name == "nt":
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    args = [sys.executable, str(PREP_SCRIPT), str(msg_path)]
    kw = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
    try:
        # Leave the hook runner's job object if it has one, so the worker outlives this hook.
        subprocess.Popen(args, creationflags=flags | getattr(subprocess, "CREATE_BREAKAWAY_FROM_JOB", 0), **kw)
    except OSError:
        subprocess.Popen(args, creationflags=flags, **kw)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = data.get("prompt") or ""
    session = data.get("session_id") or ""

    kind = _inbox.find_secret(prompt)
    if kind and _inbox.ALLOW_SECRET not in prompt:
        _inbox.log({"event": "blocked", "kind": kind, "session": session[:8]})
        sys.stderr.write(BLOCK_MSG.format(kind=kind))
        return 2

    if _inbox.is_machine_prompt(prompt):
        return 0

    try:
        ts = _inbox.now_iso()
        mid = _inbox.msg_id(session, ts, prompt)
        _inbox.MSG_DIR.mkdir(parents=True, exist_ok=True)
        path = _inbox.MSG_DIR / f"{mid}.json"
        path.write_text(json.dumps({
            "id": mid, "ts": ts, "session": session, "cwd": data.get("cwd") or "",
            "prompt": _inbox.redact_secrets(prompt),
        }, ensure_ascii=False), encoding="utf-8")
        _inbox.log({"event": "captured", "id": mid, "session": session[:8], "chars": len(prompt)})
        spawn_prep(path)
    except Exception as e:
        _inbox.log({"event": "capture_error", "error": str(e)[:200]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
