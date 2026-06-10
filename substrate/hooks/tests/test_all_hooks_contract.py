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

# Network-touching hooks excluded by name
SKIP = {
    "phone-ping.py",  # makes external API calls
}

# CLI utilities that live in the hooks dir but are NOT stdin-JSON hooks.
# They are argv-driven (and some have side effects or make API calls), so the
# universal JSON-in/JSON-out contract does not apply to them.
CLI_TOOLS = {
    "chain.py",  # session-chain CLI: `chain.py append|checkpoint|finalize|...`
    "replay-proposal.py",  # argparse CLI, requires session_id, replays via LLM API
    "memory-exporter.py",  # manual/scheduled exporter; running it writes MEMORY_EXPORT.json
}


def discover_hooks() -> list[Path]:
    """Discover hooks by convention.
    - Files starting with `_` are utility/helper modules (e.g., `_telemetry.py`, `_telemetry_rotate.py`), not hooks.
    - Files ending `.test.py` are self-test scripts (e.g., `proposal-scraper.test.py`), not hooks.
    - Explicit SKIP set for network-touching hooks; CLI_TOOLS for argv-driven utilities.
    Class-eliminates 'new utility file accidentally tested as a hook' regression."""
    out = []
    for p in HOOKS_DIR.glob("*.py"):
        if p.name.startswith("_"):
            continue
        if p.name.endswith(".test.py"):
            continue
        if p.name in SKIP or p.name in CLI_TOOLS:
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
        encoding="utf-8",  # hooks emit UTF-8; Windows default cp1252 kills the reader thread
        errors="replace",
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


# ============ Schema-shape validation (class-eliminates emit-mismatch) ============

PRETOOL_SHAPE_HOOKS = {
    "coordination-mechanism-gate.py", "wwwd-gate.py", "hiero-gate.py",
    "research-before-capability-claim-gate.py", "em-dash-augmentation-gate.py",
    "time-logic-gate.py", "directive-verb-action-class-gate.py",
    "jarvis-design-goal-gate.py", "entity-context-cross-reference.py",
    "conflict-detector.py", "partner-draft-formalize-gate.py",
    "partner-architecture-load-gate.py", "post-generation-recall.py",
    "thread-resume-detector.py", "atomic-reflection-gate.py",
}

STOP_SHAPE_HOOKS = {
    "autonomous-continue.py", "wwwd-correction-detector.py",
    "post-generation-reflect.py", "decision-capture.py",
    "self-review-gate.py",
}


def _emits_pretool_shape(payload_str: str, hook_name: str) -> bool:
    """When a hook surfaces, must use {hookSpecificOutput:{hookEventName,additionalContext}}
    NOT {decision:'block',reason:...}. PRETOOL_SHAPE_HOOKS must satisfy this."""
    hook_path = HOOKS_DIR / hook_name
    rc, stdout, _ = run_hook(hook_path, payload_str)
    if not stdout.strip() or stdout.strip() == "{}":
        return True  # silent is always valid
    try:
        out = json.loads(stdout)
    except Exception:
        return False
    if "decision" in out and out.get("decision") == "block":
        return False  # Stop-shape emitted from a PreTool hook
    return True


def _emits_stop_shape(payload_str: str, hook_name: str) -> bool:
    """Stop-event hooks may emit `{}` (silent) or `{decision:'block',reason:...}`.
    Must NOT use `hookSpecificOutput.additionalContext` (schema rejects per [P·stop-event-schema-restriction])."""
    hook_path = HOOKS_DIR / hook_name
    rc, stdout, _ = run_hook(hook_path, payload_str)
    if not stdout.strip() or stdout.strip() == "{}":
        return True
    try:
        out = json.loads(stdout)
    except Exception:
        return False
    if "hookSpecificOutput" in out:
        return False  # PreTool-shape emitted from a Stop hook
    return True


@pytest.mark.parametrize("hook_name", sorted(PRETOOL_SHAPE_HOOKS))
def test_pretool_hooks_emit_pretool_shape(hook_name):
    if not (HOOKS_DIR / hook_name).exists():
        pytest.skip(f"{hook_name} not present in this checkout")
    assert _emits_pretool_shape("{}", hook_name), \
        f"{hook_name} emitted Stop-shape from a PreToolUse hook"


@pytest.mark.parametrize("hook_name", sorted(STOP_SHAPE_HOOKS))
def test_stop_hooks_emit_stop_shape(hook_name):
    if not (HOOKS_DIR / hook_name).exists():
        pytest.skip(f"{hook_name} not present in this checkout")
    assert _emits_stop_shape("{}", hook_name), \
        f"{hook_name} emitted PreTool-shape from a Stop hook (forbidden per [P·stop-event-schema-restriction])"
