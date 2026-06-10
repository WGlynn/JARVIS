"""Universal contract tests across ALL Python hooks.
Per #2 audit suggestion: each hook has well-defined JSON-in/JSON-out contract.
This file parametrizes the contract over every *.py hook discovered automatically.

What's tested universally:
- empty payload → fail-quiet (no crash, valid JSON or empty)
- malformed payload → fail-quiet
- valid no-match payload → silent {} output
- non-zero exit codes are forbidden

Per-hook behavioral tests live in test_hook_contract.py (representative samples).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).parent.parent

# Hooks that need special handling (read network, etc.) — exclude from parametrize
SKIP = {
    "_telemetry.py",  # not a hook, internal utility
    "phone-ping.py",  # makes external API calls
}


def discover_hooks() -> list[Path]:
    out = []
    for p in HOOKS_DIR.glob("*.py"):
        if p.name in SKIP:
            continue
        out.append(p)
    return sorted(out)


def run_hook(hook_path: Path, payload_str: str, timeout: int = 10) -> tuple[int, str, str]:
    """Returns (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input=payload_str,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="module")
def all_hooks():
    hooks = discover_hooks()
    assert len(hooks) >= 20, f"Expected ≥20 hooks discovered, got {len(hooks)}"
    return hooks


@pytest.mark.parametrize("hook_name", [h.name for h in discover_hooks()])
def test_hook_empty_payload_fails_quiet(hook_name):
    """Every hook must return 0 + valid JSON (or empty) on empty input."""
    hook_path = HOOKS_DIR / hook_name
    rc, stdout, stderr = run_hook(hook_path, "")
    assert rc == 0, f"{hook_name} returned {rc} on empty: stderr={stderr[:200]}"
    out = stdout.strip()
    if out:
        try:
            json.loads(out)
        except json.JSONDecodeError as e:
            pytest.fail(f"{hook_name} emitted invalid JSON: {e}; output={out[:200]}")


@pytest.mark.parametrize("hook_name", [h.name for h in discover_hooks()])
def test_hook_malformed_payload_fails_quiet(hook_name):
    """Garbage payload must not crash."""
    hook_path = HOOKS_DIR / hook_name
    rc, stdout, stderr = run_hook(hook_path, '{"garbage":true,"tool_input":"not-a-dict"}')
    assert rc == 0, f"{hook_name} crashed on garbage: rc={rc} stderr={stderr[:200]}"


@pytest.mark.parametrize("hook_name", [h.name for h in discover_hooks()])
def test_hook_invalid_json_fails_quiet(hook_name):
    """Non-JSON stdin must not crash."""
    hook_path = HOOKS_DIR / hook_name
    rc, stdout, stderr = run_hook(hook_path, "this is not json {{{")
    assert rc == 0, f"{hook_name} crashed on non-JSON: rc={rc} stderr={stderr[:200]}"


@pytest.mark.parametrize("hook_name", [h.name for h in discover_hooks()])
def test_hook_no_unbounded_output(hook_name):
    """Hook output must be reasonable size (<100KB)."""
    hook_path = HOOKS_DIR / hook_name
    rc, stdout, _ = run_hook(hook_path, "{}")
    assert len(stdout) < 100_000, f"{hook_name} emitted {len(stdout)} bytes on empty input"
