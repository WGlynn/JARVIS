#!/usr/bin/env python3
"""
_wwwd_infer_test.py — LOOP 8: WWWD Inference Model Test Suite
==============================================================

pytest suite covering:
  1. Model fits from corpus deterministically (same corpus → same posterior).
  2. Seen/in-distribution pattern → low surprise + confident prediction.
  3. Unseen/OOD trigger → high epistemic uncertainty → escalate flag set.
  4. Revision (online update) shifts the posterior in the correct direction.
  5. Uncertainty-calibration: OOD > in-distribution uncertainty (the structural
     guarantee that must hold regardless of correction sparsity).
  6. Data-sparsity transparency: the model correctly reports N_corrections
     and does not fabricate a predictive-accuracy result when N < 5.

Run:
    cd ~/.claude/projects/<project>/memory
    python -m pytest _wwwd_infer_test.py -v

No LLM calls. No network. CPU only.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import numpy as np
import pytest

from _wwwd_infer import (
    ESCALATE_THRESHOLD,
    KNOWN_ACTIONS,
    KNOWN_TRIGGER_CLASSES,
    WWWDInferenceModel,
    ScoreResult,
    _parse_correction_action,
    extract_features,
    run_exit_test,
)

# ============ Fixtures ============

def _make_entry(
    decision_class: str = "severity-calibration",
    trigger: list[str] | None = None,
    tool_name: str = "Write",
    candidate_excerpt: str = "",
    correction: dict | None = None,
    gate_revision_occurred: bool = False,
) -> dict:
    return {
        "timestamp": "2026-07-01T00:00:00+00:00",
        "decision_class": decision_class,
        "trigger": trigger if trigger is not None else [decision_class],
        "tool_name": tool_name,
        "candidate_excerpt": candidate_excerpt,
        "projection": "test-projection",
        "executed": True,
        "gate_revision_occurred": gate_revision_occurred,
        "corpus_sources_used": [],
        "correction": correction,
    }


def _write_corpus(entries: list[dict], tmp_path: Path) -> Path:
    p = tmp_path / "wwwd_gate_fires.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps(e) + "\n")
    return p


# ============ Test 1: Deterministic fit ============

class TestDeterministicFit:
    """Model fitted twice from same corpus must produce identical posteriors."""

    def test_identical_posteriors(self, tmp_path):
        entries = [_make_entry("severity-calibration") for _ in range(20)]
        entries += [_make_entry("scope-decision") for _ in range(5)]
        corpus = _write_corpus(entries, tmp_path)

        m1 = WWWDInferenceModel().fit_from_jsonl(corpus)
        m2 = WWWDInferenceModel().fit_from_jsonl(corpus)

        s1 = m1.posterior_summary()
        s2 = m2.posterior_summary()

        for cls in KNOWN_TRIGGER_CLASSES:
            for action in KNOWN_ACTIONS:
                a1 = m1._alpha[cls][action]
                a2 = m2._alpha[cls][action]
                assert abs(a1 - a2) < 1e-9, (
                    f"Posterior mismatch for class={cls}, action={action}: {a1} vs {a2}"
                )

    def test_refit_resets_state(self, tmp_path):
        """Calling fit_from_jsonl a second time must reset and refit, not accumulate."""
        entries_a = [_make_entry("severity-calibration") for _ in range(10)]
        entries_b = [_make_entry("severity-calibration") for _ in range(20)]
        dir_a = tmp_path / "a"
        dir_a.mkdir()
        dir_b = tmp_path / "b"
        dir_b.mkdir()
        corpus_a = _write_corpus(entries_a, dir_a)
        corpus_b = _write_corpus(entries_b, dir_b)

        m = WWWDInferenceModel()
        m.fit_from_jsonl(corpus_a)
        n_after_a = m._n["severity-calibration"]
        m.fit_from_jsonl(corpus_b)
        n_after_b = m._n["severity-calibration"]

        # Second fit should reflect corpus_b count, not corpus_a + corpus_b.
        assert n_after_a == 10
        assert n_after_b == 20, (
            f"Expected 20 after refit on corpus_b, got {n_after_b}"
        )


# ============ Test 2: Seen pattern → low surprise + confident prediction ============

class TestInDistributionScoring:
    """High-count classes must yield low uncertainty and confident predictions."""

    def test_high_count_class_low_uncertainty(self, tmp_path):
        # 500 fires on severity-calibration, no corrections → posterior firmly on 'accepted'
        entries = [_make_entry("severity-calibration") for _ in range(500)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        candidate = {
            "decision_class": "severity-calibration",
            "trigger": ["severity-calibration"],
            "tool_name": "Write",
            "candidate_excerpt": "some content with severity",
        }
        result = m.score(candidate)

        assert result.predicted_action == "accepted", (
            f"Expected 'accepted' (no corrections), got '{result.predicted_action}'"
        )
        assert result.epistemic_uncertainty < ESCALATE_THRESHOLD, (
            f"Expected low uncertainty for 500-example class, "
            f"got {result.epistemic_uncertainty:.4f} > threshold {ESCALATE_THRESHOLD}"
        )
        assert not result.escalate, "High-support class should not trigger escalation"
        assert result.n_examples_seen == 500

    def test_surprise_is_low_for_confident_prediction(self, tmp_path):
        entries = [_make_entry("scope-decision") for _ in range(200)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        candidate = {"decision_class": "scope-decision", "trigger": ["scope-decision"], "tool_name": "Edit"}
        result = m.score(candidate)

        # EFE surprise should be well below 1.0 nat for a confident prediction
        # (P(accepted) ≈ 0.99+ → -log(0.99) ≈ 0.01)
        assert result.efe_surprise < 1.0, (
            f"Expected low EFE surprise for well-supported class, got {result.efe_surprise:.4f}"
        )

    def test_prediction_consistent_with_dominant_observation(self, tmp_path):
        """If 99% of observations are 'accepted', prediction must be 'accepted'."""
        entries = [_make_entry("artifact-template-resolution") for _ in range(99)]
        # 1 correction mapped to revise-severity
        correction_entry = _make_entry(
            "artifact-template-resolution",
            correction={"text_excerpt": "change that to medium severity", "matched_patterns": []},
            gate_revision_occurred=True,
        )
        entries.append(correction_entry)
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        candidate = {"decision_class": "artifact-template-resolution", "trigger": ["artifact-template-resolution"], "tool_name": "Write"}
        result = m.score(candidate)
        assert result.predicted_action == "accepted", (
            f"99:1 ratio should predict 'accepted', got '{result.predicted_action}'"
        )


# ============ Test 3: OOD trigger → high uncertainty + escalate ============

class TestOODEscalation:
    """Unknown trigger class must always escalate regardless of corpus size."""

    def test_ood_class_escalates(self, tmp_path):
        # Even with a huge corpus, an unknown class is OOD.
        entries = [_make_entry("severity-calibration") for _ in range(5000)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        ood_candidate = {
            "decision_class": "NOVEL_UNREGISTERED_TRIGGER_2026",
            "trigger": ["NOVEL_UNREGISTERED_TRIGGER_2026"],
            "tool_name": "Agent",
            "candidate_excerpt": "some future trigger pattern",
        }
        result = m.score(ood_candidate)

        assert result.is_ood is True
        assert result.escalate is True
        assert result.epistemic_uncertainty == 1.0
        assert result.predicted_action == "ESCALATE"
        assert result.n_examples_seen == 0

    def test_ood_uncertainty_exceeds_indistribution(self, tmp_path):
        """Core calibration guarantee: OOD uncertainty must exceed in-distribution."""
        entries = [_make_entry("severity-calibration") for _ in range(100)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        ood = m.score({"decision_class": "UNKNOWN_XYZ", "trigger": [], "tool_name": "Write"})
        indist = m.score({"decision_class": "severity-calibration", "trigger": ["severity-calibration"], "tool_name": "Write"})

        assert ood.epistemic_uncertainty > indist.epistemic_uncertainty, (
            f"OOD uncertainty {ood.epistemic_uncertainty:.4f} must exceed "
            f"in-dist {indist.epistemic_uncertainty:.4f}"
        )

    def test_empty_trigger_class_uncategorized_scores(self, tmp_path):
        """'uncategorized' is a known class (no-trigger-fired), not OOD."""
        entries = [_make_entry("uncategorized", trigger=[]) for _ in range(50)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        result = m.score({"decision_class": "uncategorized", "trigger": [], "tool_name": "Edit"})
        assert result.is_ood is False


# ============ Test 4: Revision updates posterior ============

class TestPosteriorRevision:
    """revise_from_correction() must shift posterior toward the corrected action."""

    def test_revision_increments_correct_action(self, tmp_path):
        entries = [_make_entry("tone-framing-marketing-register") for _ in range(10)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        alpha_before = m._alpha["tone-framing-marketing-register"]["revise-tone"]
        m.revise_from_correction("tone-framing-marketing-register", "no, drop the excited to share language")
        alpha_after = m._alpha["tone-framing-marketing-register"]["revise-tone"]

        assert alpha_after == alpha_before + 1.0, (
            f"Expected alpha to increment by 1.0: {alpha_before} → {alpha_after}"
        )

    def test_revision_shifts_prediction_after_many_corrections(self, tmp_path):
        """After enough revise-severity corrections, prediction must shift from 'accepted'."""
        entries = [_make_entry("partner-facing-publicly-visible") for _ in range(5)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        # Apply 20 severity-revision corrections online.
        for _ in range(20):
            m.revise_from_correction("partner-facing-publicly-visible", "change that to medium severity")

        candidate = {
            "decision_class": "partner-facing-publicly-visible",
            "trigger": ["partner-facing-publicly-visible"],
            "tool_name": "Write",
        }
        result = m.score(candidate)
        assert result.predicted_action == "revise-severity", (
            f"After 20 revise-severity corrections, expected 'revise-severity', "
            f"got '{result.predicted_action}'"
        )

    def test_revision_unknown_class_is_silent(self, tmp_path):
        """Revision on unknown class must not raise; posterior unchanged."""
        corpus = _write_corpus([], tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)
        m.revise_from_correction("COMPLETELY_UNKNOWN_CLASS_XYZ", "some correction text")
        # No exception → pass; unknown class silently ignored.

    def test_n_corrections_increments(self, tmp_path):
        corpus = _write_corpus([], tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)
        assert m.n_corrections == 0
        m.revise_from_correction("scope-decision", "actually, stop here don't continue")
        assert m.n_corrections == 1


# ============ Test 5: Uncertainty calibration (OOD > in-dist) ============

class TestUncertaintyCalibration:
    """Standalone calibration tests that must hold regardless of correction sparsity."""

    def test_uncertainty_decreases_with_more_data(self, tmp_path):
        """Classes with more observations must have lower epistemic uncertainty."""
        entries_small = [_make_entry("read-order-as-framing") for _ in range(5)]
        entries_large = [_make_entry("severity-calibration") for _ in range(500)]
        corpus = _write_corpus(entries_small + entries_large, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        small_result = m.score({"decision_class": "read-order-as-framing", "trigger": ["read-order-as-framing"], "tool_name": "Agent"})
        large_result = m.score({"decision_class": "severity-calibration", "trigger": ["severity-calibration"], "tool_name": "Write"})

        assert small_result.epistemic_uncertainty > large_result.epistemic_uncertainty, (
            f"5-example class ({small_result.epistemic_uncertainty:.4f}) should have "
            f"higher uncertainty than 500-example class ({large_result.epistemic_uncertainty:.4f})"
        )

    def test_pure_prior_class_escalates(self, tmp_path):
        """A class with zero observations (pure prior) must always trigger escalation."""
        # Use empty corpus — every class is at pure prior.
        corpus = _write_corpus([], tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)

        for cls in KNOWN_TRIGGER_CLASSES:
            result = m.score({"decision_class": cls, "trigger": [cls], "tool_name": "Write"})
            assert result.escalate, (
                f"Pure-prior class '{cls}' should escalate (unc={result.epistemic_uncertainty:.4f})"
            )

    def test_calibration_gap_is_positive(self, tmp_path):
        """run_exit_test must report calibration.pass=True when OOD > in-dist."""
        entries = [_make_entry("severity-calibration") for _ in range(200)]
        corpus = _write_corpus(entries, tmp_path)
        et = run_exit_test(corpus)
        assert et["calibration"]["pass"] is True, (
            f"Calibration test must pass (OOD uncertainty > in-dist). "
            f"gap={et['calibration']['gap']}"
        )


# ============ Test 6: Data-sparsity transparency ============

class TestDataSparsityTransparency:
    """Model must honestly report correction count and not fabricate accuracy."""

    def test_exit_test_reports_n_corrections(self, tmp_path):
        # Corpus with 1 correction (mirrors the real corpus).
        entries = [_make_entry("severity-calibration") for _ in range(100)]
        correction_entry = _make_entry(
            "partner-facing-publicly-visible",
            correction={
                "timestamp": "2026-05-24T17:12:39.942397+00:00",
                "text_excerpt": "no actually, lets change that to medium severity",
                "matched_patterns": [r"\bno,?\s+"],
            },
            gate_revision_occurred=True,
        )
        entries.append(correction_entry)
        corpus = _write_corpus(entries, tmp_path)

        et = run_exit_test(corpus)
        assert et["n_corrections_found"] == 1, (
            f"Expected 1 correction, got {et['n_corrections_found']}"
        )

    def test_exit_test_accuracy_withheld_when_sparse(self, tmp_path):
        """When N < 5, accuracy_test.status must be 'under-powered', not a number."""
        entries = [_make_entry("severity-calibration") for _ in range(50)]
        corpus = _write_corpus(entries, tmp_path)
        et = run_exit_test(corpus)
        assert et["accuracy_test"]["status"] == "under-powered", (
            f"Expected 'under-powered' with 0 corrections, got '{et['accuracy_test']['status']}'"
        )

    def test_verdict_contains_correction_count(self, tmp_path):
        """Verdict string must include the honest correction count."""
        corpus = _write_corpus([], tmp_path)
        et = run_exit_test(corpus)
        # Verdict must contain the N=0 signal.
        assert "0" in et["verdict"], (
            f"Verdict should mention correction count=0. Got: {et['verdict']}"
        )

    def test_accuracy_runs_when_sufficient_data(self, tmp_path):
        """With >= 5 corrections, accuracy test must run and return a numeric result."""
        entries = []
        # 5 correction entries — all map to revise-severity
        for _ in range(5):
            entries.append(
                _make_entry(
                    "partner-facing-publicly-visible",
                    correction={
                        "timestamp": "2026-07-01T00:00:00+00:00",
                        "text_excerpt": "change that to medium severity",
                        "matched_patterns": [],
                    },
                    gate_revision_occurred=True,
                )
            )
        # Bulk uncorrected entries to build the posterior.
        entries += [_make_entry("severity-calibration") for _ in range(50)]
        corpus = _write_corpus(entries, tmp_path)
        et = run_exit_test(corpus)
        assert et["accuracy_test"]["status"] == "ran", (
            f"Expected 'ran' with 5 corrections, got '{et['accuracy_test']['status']}'"
        )
        assert "accuracy" in et["accuracy_test"]
        assert 0.0 <= et["accuracy_test"]["accuracy"] <= 1.0


# ============ Test 7: Feature extraction edge cases ============

class TestFeatureExtraction:
    def test_empty_candidate(self):
        feats = extract_features({})
        assert feats["primary_class"] == "uncategorized"
        assert feats["is_ood"] is False  # 'uncategorized' is a known class

    def test_ood_class_detected(self):
        feats = extract_features({"decision_class": "FUTURE_UNKNOWN_CLASS"})
        assert feats["is_ood"] is True

    def test_trigger_set_populated(self):
        feats = extract_features({
            "decision_class": "scope-decision",
            "trigger": ["scope-decision", "severity-calibration"],
        })
        assert "scope-decision" in feats["trigger_set"]
        assert "severity-calibration" in feats["trigger_set"]
        assert feats["trigger_count"] == 2


# ============ Test 8: _parse_correction_action ============

class TestParseCorrection:
    def test_none_returns_accepted(self):
        assert _parse_correction_action(None) == "accepted"

    def test_severity_keyword(self):
        c = {"text_excerpt": "no actually, lets change that to medium severity"}
        assert _parse_correction_action(c) == "revise-severity"

    def test_tone_keyword(self):
        c = {"text_excerpt": "drop the excited to share tone please"}
        assert _parse_correction_action(c) == "revise-tone"

    def test_scope_keyword(self):
        c = {"text_excerpt": "actually stop, don't continue that"}
        assert _parse_correction_action(c) == "revise-scope"

    def test_generic_correction(self):
        c = {"text_excerpt": "nope, redo the whole thing"}
        assert _parse_correction_action(c) == "revise-other"

    def test_string_input(self):
        assert _parse_correction_action("change the severity to high") == "revise-severity"


# ============ Test 9: Posterior summary structure ============

class TestPosteriorSummary:
    def test_summary_covers_all_classes(self, tmp_path):
        corpus = _write_corpus([], tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)
        summary = m.posterior_summary()
        for cls in KNOWN_TRIGGER_CLASSES:
            assert cls in summary["classes"], f"Class '{cls}' missing from summary"

    def test_summary_probabilities_sum_to_one(self, tmp_path):
        entries = [_make_entry("severity-calibration") for _ in range(30)]
        corpus = _write_corpus(entries, tmp_path)
        m = WWWDInferenceModel().fit_from_jsonl(corpus)
        summary = m.posterior_summary()
        for cls, info in summary["classes"].items():
            # action_probs values are rounded to 4 decimal places in the summary,
            # so floating-point accumulation allows up to 5 * 1e-4 drift across 5 actions.
            total = sum(info["action_probs"].values())
            assert abs(total - 1.0) < 5e-4, (
                f"Probabilities for '{cls}' sum to {total:.6f}, not 1.0"
            )


# ============ Integration: live corpus smoke test ============

class TestLiveCorpusIntegration:
    """
    Smoke test against the real gate-fire log if it exists.
    Skipped gracefully if the corpus is absent (CI / other machines).

    Does NOT assert predictive accuracy (N_corrections too sparse).
    Asserts: model fits, calibration passes, sparsity is honestly reported.
    """

    LIVE_CORPUS = (
        Path.home()
        / ".claude"
        / "projects"
        / "<project>"
        / "memory"
        / "_system"
        / "wwwd_gate_fires.jsonl"
    )

    @pytest.mark.skipif(
        not (Path.home() / ".claude" / "projects" / "<project>" / "memory" / "_system" / "wwwd_gate_fires.jsonl").exists(),
        reason="Live corpus not found — skipping live integration test",
    )
    def test_live_corpus_fits_and_calibrates(self):
        m = WWWDInferenceModel().fit_from_jsonl(self.LIVE_CORPUS)
        summary = m.posterior_summary()

        # Must have processed thousands of entries.
        total_obs = sum(v for v in m._n.values())
        assert total_obs > 1000, f"Expected > 1000 total observations, got {total_obs}"

        # Calibration: OOD > best in-distribution class.
        ood = m.score({"decision_class": "UNDEFINED_OOD_CLASS", "trigger": [], "tool_name": "Write"})
        best_cls = max(m._n, key=lambda c: m._n.get(c, 0))
        indist = m.score({"decision_class": best_cls, "trigger": [best_cls], "tool_name": "Write"})
        assert ood.epistemic_uncertainty > indist.epistemic_uncertainty

        # Correction sparsity is honest.
        assert m.n_corrections <= 5, (
            f"Surprisingly many corrections ({m.n_corrections}) — verify corpus"
        )

        # Exit test runs without error.
        et = run_exit_test(self.LIVE_CORPUS)
        assert "verdict" in et
        assert et["n_corrections_found"] == m.n_corrections

        # Print for human inspection.
        print(f"\n[LIVE CORPUS] n_entries_total={total_obs}")
        print(f"[LIVE CORPUS] n_corrections={m.n_corrections}")
        print(f"[LIVE CORPUS] calibration_gap={et['calibration']['gap']:.4f}")
        print(f"[LIVE CORPUS] verdict: {et['verdict']}")
