#!/usr/bin/env python3
"""
_critic.py — Shared structured-critic helper for JARVIS PreToolUse hooks.
===========================================================================

LOOP 2 of the JARVIS non-LLM intelligence roadmap (ROADMAP.md).

Background
----------
Kambhampati et al. "LLM-Modulo" (dossier 02): a symbolic critic that returns
{violated_constraint, suggested_reformulation} instead of flat prose lets the
LLM iterate to correctness — 82 % success in ≤15 rounds where baseline LLM
planning fails. Zero added inference cost. This module supplies that schema
to every PreToolUse hook that imports it, so the harness-wide upgrade is a
one-line change per gate.

Coverage boundary (GOFAI guardrail 09-rule-1)
----------------------------------------------
COVERED:
  - Structuring an existing advisory message into the {violated_constraint,
    suggested_reformulation, severity, evidence} schema.
  - Rendering that struct back into the hookSpecificOutput.additionalContext
    string (schema unchanged — structure rides INSIDE the existing channel).
  - Providing a COVERAGE_BOUNDARY field on every critic output so any
    consumer can see what was / was not evaluated.

NOT EVALUATED by this module:
  - Whether the underlying constraint is correct (that is the gate's job).
  - Whether the LLM will actually accept the reformulation (empirical; measured
    per LOOP 2 exit test over ≥1 week of live fires).
  - Semantic similarity between the proposed reformulation and the original
    content (no LLM call here — zero inference cost preserved).
  - Any gate that uses exit-code-2 blocking (e.g., foundry-test-gate): the
    critic schema is for advisory/augmentation hooks only.

Usage (in a gate)
-----------------
    from _critic import critic_output, format_for_hook

    # 1. Build the structured feedback record
    feedback = critic_output(
        violated_constraint="[CONFLICT DETECTOR] entity X contradicts memory",
        suggested_reformulation="Verify entity X against memory before writing",
        severity="high",            # "high" | "medium" | "low" | "info"
        evidence=["file.md line 42: 'we moved off X post-incident'"],
    )

    # 2. Render it into the additionalContext string (schema unchanged)
    context_str = format_for_hook(feedback)

    # 3. Emit the standard hook output
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": context_str,
        }
    }))

Global rules (from ROADMAP.md)
-------------------------------
- Generic (no hard-coded paths in the copyable core).
- CPU-only, stdlib. No LLM calls.
- Honest labels: this module is BUILT (not designed, not open).
- Laptop test: Ryzen 5 1600 / 16 GB / no GPU. All code here is O(1).
"""

from __future__ import annotations

import json
from typing import Optional

# ── Schema version ──────────────────────────────────────────────────────────
# Increment when the critic dict shape changes so consumers can guard.
CRITIC_SCHEMA_VERSION = "1.0"

# ── Severity levels (ordered) ────────────────────────────────────────────────
SEVERITY_LEVELS = ("high", "medium", "low", "info")

# ── Coverage boundary declaration (GOFAI guardrail 09-rule-1) ───────────────
COVERAGE_BOUNDARY = {
    "covers": [
        "structuring_advisory_messages_into_critic_schema",
        "rendering_critic_schema_into_additionalContext_channel",
        "severity_labeling_for_constraint_violations",
        "evidence_list_attachment_for_provenance",
    ],
    "does_not_cover": [
        "correctness_of_the_underlying_constraint",
        "semantic_similarity_of_reformulation_to_original",
        "llm_acceptance_rate_of_reformulation",
        "exit_code_2_blocking_gates",
        "any_inference_call",
    ],
    "out_of_scope_handling": "explicit_not_evaluated",
}


# ── Core factory ─────────────────────────────────────────────────────────────

def critic_output(
    violated_constraint: str,
    suggested_reformulation: str,
    severity: str = "medium",
    evidence: Optional[list[str]] = None,
) -> dict:
    """
    Return the canonical structured critic dict.

    Parameters
    ----------
    violated_constraint : str
        Human-readable description of the constraint that was violated.
        Should be specific enough that the LLM can understand exactly
        what rule was broken.

    suggested_reformulation : str
        A concrete suggestion for how to fix the violation.  Should be
        actionable (not "think harder") and specific to the content.

    severity : str
        One of "high" | "medium" | "low" | "info".
        - high   : clear violation; LLM should revise before proceeding.
        - medium : likely violation; LLM should verify then decide.
        - low    : possible violation; LLM may proceed with awareness.
        - info   : informational; no revision implied.

    evidence : list[str] | None
        Optional list of provenance snippets (file:line, memory excerpt,
        regex match, etc.) that ground the claim.  Kept here to satisfy
        GOFAI guardrail 09-rule-2: verify every extracted fact before it
        enters the symbolic layer — the gate puts its receipts here.

    Returns
    -------
    dict with keys:
        schema_version, violated_constraint, suggested_reformulation,
        severity, evidence, coverage_boundary
    """
    if severity not in SEVERITY_LEVELS:
        severity = "medium"  # fail-safe, never raise

    return {
        "schema_version": CRITIC_SCHEMA_VERSION,
        "violated_constraint": str(violated_constraint),
        "suggested_reformulation": str(suggested_reformulation),
        "severity": severity,
        "evidence": list(evidence) if evidence else [],
        "coverage_boundary": COVERAGE_BOUNDARY,
    }


# ── Renderer ─────────────────────────────────────────────────────────────────

def format_for_hook(
    feedback: dict,
    gate_name: str = "",
    noop_if_no_violation: bool = False,
) -> str:
    """
    Render a critic dict into the additionalContext string.

    The string schema is UNCHANGED from the existing hooks — the structure
    lives INSIDE the existing channel.  A machine-readable CRITIC-JSON block
    is appended at the end so automated tools can parse it; human readers
    see the prose section first.

    Parameters
    ----------
    feedback : dict
        Output of critic_output().

    gate_name : str
        Optional gate identifier inserted into the header line (e.g.
        "conflict-detector").  Used for traceability.

    noop_if_no_violation : bool
        If True and violated_constraint is empty, return "" (caller should
        then emit {}).  Convenience for gates that conditionally build
        feedback.

    Returns
    -------
    str suitable for hookSpecificOutput.additionalContext.
    """
    if noop_if_no_violation and not feedback.get("violated_constraint", "").strip():
        return ""

    sev = feedback.get("severity", "medium").upper()
    header_tag = f"[CRITIC:{sev}]"
    if gate_name:
        header_tag = f"[CRITIC:{sev} / {gate_name}]"

    lines: list[str] = [
        header_tag,
        "",
        f"Constraint violated: {feedback['violated_constraint']}",
        "",
        f"Suggested reformulation: {feedback['suggested_reformulation']}",
    ]

    evidence = feedback.get("evidence", [])
    if evidence:
        lines.append("")
        lines.append("Evidence:")
        for e in evidence[:5]:  # cap at 5 to control context budget
            lines.append(f"  - {e}")

    # Append the machine-readable block at the end (after human-readable prose).
    # Format: a single JSON line prefixed with CRITIC-JSON: so a grep can find it.
    machine = {
        "schema_version": feedback.get("schema_version", CRITIC_SCHEMA_VERSION),
        "violated_constraint": feedback["violated_constraint"],
        "suggested_reformulation": feedback["suggested_reformulation"],
        "severity": feedback.get("severity", "medium"),
        "evidence_count": len(evidence),
        "coverage_boundary": feedback.get("coverage_boundary", COVERAGE_BOUNDARY),
    }
    lines.append("")
    lines.append(f"CRITIC-JSON: {json.dumps(machine, separators=(',', ':'))}")

    return "\n".join(lines)


# ── Convenience: build + format in one call ──────────────────────────────────

def emit_critic(
    violated_constraint: str,
    suggested_reformulation: str,
    severity: str = "medium",
    evidence: Optional[list[str]] = None,
    gate_name: str = "",
) -> str:
    """
    Build a critic_output dict and immediately format it.
    Single-call shorthand for the common case.

    Returns str for additionalContext.
    """
    fb = critic_output(
        violated_constraint=violated_constraint,
        suggested_reformulation=suggested_reformulation,
        severity=severity,
        evidence=evidence,
    )
    return format_for_hook(fb, gate_name=gate_name)


# ── Self-test (run directly: python _critic.py) ──────────────────────────────

def _self_test() -> None:
    """
    Lightweight self-test.  Run with: python _critic.py
    Tests: schema shape, severity clamp, evidence cap, renderer output,
    coverage boundary presence, machine-readable JSON parseable.
    No external dependencies.
    """
    import sys

    failures: list[str] = []

    # T1: basic shape
    fb = critic_output(
        violated_constraint="test constraint",
        suggested_reformulation="test fix",
        severity="high",
        evidence=["file.md:42: snippet"],
    )
    for key in ("schema_version", "violated_constraint", "suggested_reformulation",
                "severity", "evidence", "coverage_boundary"):
        if key not in fb:
            failures.append(f"T1: missing key '{key}'")

    # T2: severity clamp on unknown value
    fb2 = critic_output("c", "r", severity="INVALID")
    if fb2["severity"] != "medium":
        failures.append(f"T2: severity not clamped to medium, got {fb2['severity']!r}")

    # T3: evidence defaults to empty list
    fb3 = critic_output("c", "r")
    if fb3["evidence"] != []:
        failures.append("T3: evidence not empty list on None input")

    # T4: renderer produces non-empty string
    rendered = format_for_hook(fb, gate_name="test-gate")
    if not rendered:
        failures.append("T4: format_for_hook returned empty string")

    # T5: machine-readable CRITIC-JSON line is present and parseable
    critic_json_line = next(
        (l for l in rendered.splitlines() if l.startswith("CRITIC-JSON:")), None
    )
    if critic_json_line is None:
        failures.append("T5: no CRITIC-JSON line in output")
    else:
        try:
            parsed = json.loads(critic_json_line[len("CRITIC-JSON:"):].strip())
            for key in ("schema_version", "violated_constraint", "suggested_reformulation",
                        "severity", "evidence_count", "coverage_boundary"):
                if key not in parsed:
                    failures.append(f"T5: CRITIC-JSON missing key '{key}'")
        except json.JSONDecodeError as exc:
            failures.append(f"T5: CRITIC-JSON not parseable: {exc}")

    # T6: coverage_boundary declares does_not_cover
    cb = fb["coverage_boundary"]
    if "does_not_cover" not in cb:
        failures.append("T6: coverage_boundary missing does_not_cover")
    if "any_inference_call" not in cb.get("does_not_cover", []):
        failures.append("T6: coverage_boundary does not declare any_inference_call as out-of-scope")

    # T7: noop_if_no_violation
    empty_fb = critic_output("", "")
    result = format_for_hook(empty_fb, noop_if_no_violation=True)
    if result != "":
        failures.append("T7: noop_if_no_violation did not return empty string")

    # T8: emit_critic convenience wrapper
    s = emit_critic("some constraint", "some fix", severity="low",
                    evidence=["e1", "e2"], gate_name="mygate")
    if "CRITIC:LOW / mygate" not in s:
        failures.append("T8: emit_critic header not found in output")

    # T9: evidence capped at 5 in renderer
    many_evidence = [f"e{i}" for i in range(10)]
    fb_many = critic_output("c", "r", evidence=many_evidence)
    rendered_many = format_for_hook(fb_many)
    # count "  - e" lines
    evidence_lines = [l for l in rendered_many.splitlines() if l.startswith("  - ")]
    if len(evidence_lines) > 5:
        failures.append(f"T9: evidence not capped at 5, got {len(evidence_lines)}")

    # Report
    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  FAIL: {f}")
        sys.exit(1)
    else:
        print(f"SELF-TEST PASSED: 9/9 checks (schema_version={CRITIC_SCHEMA_VERSION})")
        sys.exit(0)


if __name__ == "__main__":
    _self_test()
