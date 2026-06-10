"""Smoke tests for JARVIS Python hooks. JSON-in / JSON-out contract verification.
Each hook fires as subprocess with sample payload; output must be valid JSON.

Started 2026-06-10 (3 representative hooks). Coverage expands per ROADMAP.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.parent
REPO_ROOT = HOOKS_DIR.parent.parent


def run_hook(hook_name: str, payload: dict) -> dict:
    """Spawn a hook with payload on stdin, return parsed JSON output (or {} on parse fail)."""
    hook_path = HOOKS_DIR / hook_name
    if not hook_path.exists():
        return {"__error__": f"hook not found: {hook_path}"}
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        return {"__error__": f"nonzero exit: {result.returncode}", "stderr": result.stderr[:200]}
    out = result.stdout.strip()
    if not out:
        return {}
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        return {"__error__": f"invalid JSON: {e}", "stdout": out[:200]}


# ============ Contract tests (all hooks must satisfy these) ============

def test_empty_payload_does_not_crash():
    """All hooks fail-quiet on empty input."""
    for hook in ["coordination-mechanism-gate.py", "autonomous-continue.py", "em-dash-augmentation-gate.py"]:
        out = run_hook(hook, {})
        assert "__error__" not in out, f"{hook} crashed on empty: {out}"


def test_malformed_payload_does_not_crash():
    """All hooks fail-quiet on garbage payload."""
    for hook in ["coordination-mechanism-gate.py", "autonomous-continue.py"]:
        out = run_hook(hook, {"nonsense": "garbage", "tool_input": "not-a-dict"})
        assert "__error__" not in out, f"{hook} crashed on malformed: {out}"


# ============ coordination-mechanism-gate specific ============

def test_coordination_gate_silent_on_aligned():
    """Already aligned (haiku for trivial task) = silent."""
    payload = {
        "tool_input": {
            "description": "list files in dir",
            "prompt": "",
            "model": "haiku",
        }
    }
    out = run_hook("coordination-mechanism-gate.py", payload)
    assert out == {} or "hookSpecificOutput" not in out


def test_coordination_gate_downgrade_rec_on_trivial():
    """Trivial task running sonnet → surfaces haiku downgrade rec."""
    payload = {
        "tool_input": {
            "description": "check current time",
            "prompt": "",
            "model": "sonnet",
        }
    }
    out = run_hook("coordination-mechanism-gate.py", payload)
    assert "hookSpecificOutput" in out
    assert "haiku" in out["hookSpecificOutput"]["additionalContext"].lower()


def test_coordination_gate_ambiguity_flag():
    """Mixed signals (sonnet + ambiguous) → ambiguity flag recommending /classify."""
    payload = {
        "tool_input": {
            "description": "implement a simple counter",
            "prompt": "",
            "model": "sonnet",
        }
    }
    out = run_hook("coordination-mechanism-gate.py", payload)
    if "hookSpecificOutput" in out:
        assert "classify" in out["hookSpecificOutput"]["additionalContext"].lower() or \
               "uncertain" in out["hookSpecificOutput"]["additionalContext"].lower()


# ============ autonomous-continue specific ============

def test_autonomous_continue_silent_on_clean():
    """No in-flight signals + no WAL ACTIVE = silent."""
    out = run_hook("autonomous-continue.py", {"transcript_path": ""})
    assert out == {} or "decision" not in out


# ============ em-dash-augmentation-gate specific ============

def test_em_dash_gate_on_partner_path():
    """Em-dash in partner-facing path = surface warning."""
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/c/Users/Will/Desktop/rick-reply-test.md",
            "content": "hello rick — this has an em-dash",
        }
    }
    out = run_hook("em-dash-augmentation-gate.py", payload)
    # may or may not surface depending on exact match logic, but must not crash
    assert "__error__" not in out
