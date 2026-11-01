#!/usr/bin/env python3
"""voice-summary: speak a one-sentence summary of each finished turn, fully offline.

Stop hook. Reads the turn's transcript (path from the hook's stdin JSON), takes the opening sentence of the
last assistant text, strips markdown/code/links/paths, and speaks it with Windows' built-in
System.Speech voice in a detached process, so the hook returns at once. Nothing leaves the machine.

Off switch: create ~/.claude/voice-off (delete it to turn voice back on).
A new summary stops the previous one if it is still speaking. Never blocks, never fails the turn.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home() / ".claude"
OFF = HOME / "voice-off"
STATE = HOME / "hooks" / ".voice-summary.json"
MAX_CHARS = 220


def last_assistant_text(transcript: Path) -> tuple[str, str]:
    """Return (message id, text) of the last assistant message that contains text."""
    msg_id, text = "", ""
    with open(transcript, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if '"assistant"' not in line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") != "assistant":
                continue
            parts = [c.get("text", "") for c in rec.get("message", {}).get("content", [])
                     if isinstance(c, dict) and c.get("type") == "text"]
            joined = "\n".join(p for p in parts if p.strip())
            if joined.strip():
                msg_id, text = rec.get("uuid", ""), joined
    return msg_id, text


def summarize(text: str) -> str:
    t = re.sub(r"```.*?```", " ", text, flags=re.S)            # code blocks
    t = re.sub(r"`([^`]*)`", r"\1", t)                          # inline code -> plain
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)              # [label](url) -> label
    t = re.sub(r"https?://\S+", " ", t)                         # bare urls
    t = re.sub(r"(?:[A-Za-z]:)?[~./\\][\w.\-~/\\]+", " ", t)    # file paths
    t = re.sub(r"[*_#>|]+", " ", t)                             # markdown marks
    t = re.sub(r"\s+", " ", t).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", t)                        # first sentence
    s = m.group(1) if m else t
    if len(s) > MAX_CHARS:
        s = s[:MAX_CHARS].rsplit(" ", 1)[0] + "."
    return s


def stop_previous() -> None:
    try:
        pid = json.loads(STATE.read_text()).get("pid")
        if pid:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
    except (OSError, ValueError):
        pass


def speak(sentence: str) -> int:
    escaped = sentence.replace("'", "''")                       # single-quoted PowerShell string: no expansion
    ps = ("Add-Type -AssemblyName System.Speech; "
          "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.Rate = 1; $s.Speak('{escaped}')")
    flags = 0x00000008 | 0x08000000                              # DETACHED_PROCESS | CREATE_NO_WINDOW
    p = subprocess.Popen(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
    return p.pid


def main() -> None:
    try:
        if OFF.exists():
            return
        data = json.loads(sys.stdin.read() or "{}")
        path = data.get("transcript_path")
        if not path or not os.path.exists(path):
            return
        msg_id, text = last_assistant_text(Path(path))
        if not text:
            return
        prev = {}
        if STATE.exists():
            try:
                prev = json.loads(STATE.read_text())
            except ValueError:
                prev = {}
        if msg_id and prev.get("last_id") == msg_id:                # already spoken (repeat Stop firing)
            return
        sentence = summarize(text)
        if not sentence:
            return
        stop_previous()
        pid = speak(sentence)
        STATE.write_text(json.dumps({"last_id": msg_id, "pid": pid}))
    except Exception:                                               # never fail the turn
        return


if __name__ == "__main__":
    main()
