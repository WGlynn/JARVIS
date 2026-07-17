#!/usr/bin/env python3
"""_hopfield_recall_test.py -- pytest suite for LOOP 4 Hopfield associative memory.

Tests are grounded in empirically verified behavior on the real dataset (855 primitives,
_system/semantic_index.json, Ryzen 5 1600 / 16GB / no GPU).

All tests are deterministic (fixed seeds). Zero LLM calls. stdlib + numpy only.

Run: pytest _hopfield_recall_test.py -v
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

# ── module under test ──────────────────────────────────────────────────────────
import importlib.util, sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("_hopfield_recall", HERE / "_hopfield_recall.py")
hr = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(hr)                 # type: ignore[union-attr]


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def small_patterns() -> tuple[list[str], np.ndarray]:
    """10 synthetic orthonormal patterns (d=64). No disk access."""
    rng = np.random.default_rng(0)
    n, d = 10, 64
    X = rng.standard_normal((n, d)).astype(np.float32)
    # orthogonalise to make patterns well-separated
    X, _ = np.linalg.qr(X.T)
    X = X.T[:n].astype(np.float32)
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    X /= norms
    keys = [f"pattern_{i:02d}" for i in range(n)]
    return keys, X


@pytest.fixture(scope="module")
def mem_small(small_patterns) -> hr.HopfieldMemory:
    keys, X = small_patterns
    return hr.HopfieldMemory(beta=64.0).fit(keys, X)


@pytest.fixture(scope="module")
def real_mem_and_X():
    """Loaded from _system/semantic_index.json if present; skipped otherwise."""
    idx = HERE / "_system" / "semantic_index.json"
    if not idx.exists():
        pytest.skip("semantic_index.json not present")
    mem = hr.load(HERE)
    # also need raw X for cosine baseline calls
    keys, X, _vocab, _proj = hr._load_from_semantic_index(HERE)
    return mem, keys, X


# ── 1. exact recall ────────────────────────────────────────────────────────────

class TestExactRecall:
    """Querying a stored pattern exactly must return it as rank-0."""

    def test_exact_recall_all_patterns(self, mem_small, small_patterns):
        keys, X = small_patterns
        for i, key in enumerate(keys):
            results = mem_small.retrieve(X[i], k=1)
            assert results[0][0] == key, (
                f"Exact recall failed for {key}: got {results[0][0]}"
            )

    def test_exact_recall_returns_sim_near_one(self, mem_small, small_patterns):
        _, X = small_patterns
        results = mem_small.retrieve(X[0], k=1)
        assert results[0][1] > 0.99, (
            f"Similarity for exact recall should be ~1.0, got {results[0][1]:.4f}"
        )

    def test_topk_length(self, mem_small, small_patterns):
        _, X = small_patterns
        for k in [1, 3, 5, 10]:
            results = mem_small.retrieve(X[0], k=k)
            assert len(results) == k


# ── 2. partial-cue completion ─────────────────────────────────────────────────

class TestPartialCue:
    """Pattern completion: zeroing half the dimensions must still recall correctly."""

    def test_half_mask_recalls_correct(self, mem_small, small_patterns):
        """50% of dims zeroed -- Hopfield must recover the correct pattern."""
        keys, X = small_patterns
        rng = np.random.default_rng(1)
        for i in range(len(keys)):
            cue = X[i].copy()
            mask = rng.random(cue.shape[0]) < 0.50
            cue[mask] = 0.0
            norm = np.linalg.norm(cue)
            if norm < 1e-9:
                continue
            cue /= norm
            results = mem_small.retrieve(cue, k=1)
            assert results[0][0] == keys[i], (
                f"Partial-cue recall failed for {keys[i]}: got {results[0][0]}"
            )

    def test_top5_contains_target_at_70pct_mask(self, mem_small, small_patterns):
        """70% masked -- target should appear in top-5 for orthonormal patterns."""
        keys, X = small_patterns
        rng = np.random.default_rng(42)
        hits = 0
        for i in range(len(keys)):
            cue = X[i].copy()
            mask = rng.random(cue.shape[0]) < 0.70
            cue[mask] = 0.0
            norm = np.linalg.norm(cue)
            if norm < 1e-9:
                continue
            cue /= norm
            top5 = [r[0] for r in mem_small.retrieve(cue, k=5)]
            if keys[i] in top5:
                hits += 1
        # Orthonormal patterns: should hit nearly all
        assert hits >= 8, f"Expected >=8/10 hits at 70% mask, got {hits}"


# ── 3. noise robustness ────────────────────────────────────────────────────────

class TestNoiseRobustness:
    """Additive Gaussian noise at moderate sigma must not collapse recall."""

    @pytest.mark.parametrize("sigma", [0.05, 0.10, 0.20])
    def test_noise_top5_accuracy(self, mem_small, small_patterns, sigma):
        """Low-noise regime: target must appear in top-5."""
        keys, X = small_patterns
        rng = np.random.default_rng(7)
        hits = 0
        for i in range(len(keys)):
            noise = rng.standard_normal(X[i].shape).astype(np.float32) * sigma
            cue = X[i] + noise
            norm = np.linalg.norm(cue)
            if norm < 1e-9:
                continue
            cue /= norm
            top5 = [r[0] for r in mem_small.retrieve(cue, k=5)]
            if keys[i] in top5:
                hits += 1
        # At sigma<=0.20 on orthonormal 64-dim patterns, expect high accuracy
        threshold = {0.05: 10, 0.10: 9, 0.20: 7}[sigma]
        assert hits >= threshold, (
            f"sigma={sigma}: expected >={threshold}/10 hits, got {hits}"
        )


# ── 4. determinism ─────────────────────────────────────────────────────────────

class TestDeterminism:
    """Same cue must always return same result -- no randomness in retrieval."""

    def test_retrieve_is_deterministic(self, mem_small, small_patterns):
        _, X = small_patterns
        cue = X[3].copy()
        cue[:32] = 0.0       # partial cue
        cue /= np.linalg.norm(cue)
        results_a = mem_small.retrieve(cue, k=5)
        results_b = mem_small.retrieve(cue, k=5)
        assert results_a == results_b

    def test_load_is_deterministic(self):
        """Two load() calls must produce identical stored matrices."""
        idx = HERE / "_system" / "semantic_index.json"
        if not idx.exists():
            pytest.skip("semantic_index.json not present")
        mem_a = hr.load(HERE)
        mem_b = hr.load(HERE)
        assert mem_a.keys == mem_b.keys
        assert np.allclose(mem_a.X, mem_b.X, atol=1e-6), (
            "load() produced different matrices on two calls"
        )

    def test_retrieve_from_text_deterministic(self):
        idx = HERE / "_system" / "semantic_index.json"
        if not idx.exists():
            pytest.skip("semantic_index.json not present")
        mem = hr.load(HERE)
        r1 = mem.retrieve_from_text("primitive pattern completion hopfield", k=5)
        r2 = mem.retrieve_from_text("primitive pattern completion hopfield", k=5)
        assert r1 == r2


# ── 5. exit-test contract ──────────────────────────────────────────────────────

class TestExitTest:
    """The exit_test() function must return an honest result dict and meet spec."""

    def test_exit_test_returns_dict(self, real_mem_and_X):
        result = hr.exit_test(HERE, n_held_out=20, k=5, seed=42)
        assert isinstance(result, dict)
        assert "verdict" in result
        assert "status" in result

    def test_exit_test_status_is_valid_label(self, real_mem_and_X):
        result = hr.exit_test(HERE, n_held_out=20, k=5, seed=42)
        assert result["status"] in ("built", "designed", "open"), (
            f"status must be one of built/designed/open, got: {result['status']}"
        )

    def test_exit_test_never_rounds_up_to_open(self, real_mem_and_X):
        """'open' is for unverified claims. Exit test is a measurement, not a claim."""
        result = hr.exit_test(HERE, n_held_out=20, k=5, seed=99)
        assert result["status"] != "open", (
            "exit_test() produced status='open'; only built or designed are valid"
        )

    def test_exit_test_hopfield_wins_exist_on_real_data(self, real_mem_and_X):
        """On real dataset (seed=7, n=50): spec requires >=1 partial-cue case
        where Hopfield recalls and cosine does not. Verified empirically."""
        result = hr.exit_test(HERE, n_held_out=50, k=5, seed=7)
        total_wins = sum(
            result[r].get("hop_only_wins", 0)
            for r in result
            if isinstance(result[r], dict)
        )
        # As measured: 2 hop-only wins in short_text_5words regime
        assert total_wins >= 1, (
            f"Spec requires >=1 partial-cue Hopfield-only win. Got {total_wins}. "
            f"Full result: {result}"
        )

    def test_accuracy_values_are_in_range(self, real_mem_and_X):
        result = hr.exit_test(HERE, n_held_out=20, k=5, seed=42)
        for rname in ("kept_entry_5pct", "short_text_5words", "mask_85pct"):
            if rname not in result:
                continue
            r = result[rname]
            if r.get("total", 0) == 0:
                continue
            assert 0.0 <= r["hop_acc"] <= 1.0
            assert 0.0 <= r["cos_acc"] <= 1.0


# ── 6. coverage boundary ───────────────────────────────────────────────────────

class TestCoverageBoundary:
    """COVERAGE_BOUNDARY must be present, machine-readable, and honest."""

    def test_coverage_boundary_exists(self):
        assert hasattr(hr, "COVERAGE_BOUNDARY")
        cb = hr.COVERAGE_BOUNDARY
        assert isinstance(cb, dict)

    def test_coverage_boundary_has_required_keys(self):
        cb = hr.COVERAGE_BOUNDARY
        assert "does" in cb
        assert "does_not" in cb
        assert "honest_status" in cb

    def test_coverage_boundary_honest_status_matches_exit_test(self):
        """COVERAGE_BOUNDARY.honest_status must not be 'built' if exit test says 'designed'."""
        idx = HERE / "_system" / "semantic_index.json"
        if not idx.exists():
            pytest.skip("semantic_index.json not present")
        result = hr.exit_test(HERE, n_held_out=30, k=5, seed=7)
        cb_status = hr.COVERAGE_BOUNDARY.get("honest_status", "")
        exit_status = result.get("status", "")
        # Both must agree: if exit says designed, CB must not claim built
        if exit_status == "designed":
            assert cb_status != "built", (
                f"COVERAGE_BOUNDARY.honest_status='{cb_status}' but "
                f"exit_test reports status='{exit_status}'"
            )

    def test_no_llm_calls_claimed(self):
        cb = hr.COVERAGE_BOUNDARY
        does_not = " ".join(str(x) for x in cb.get("does_not", []))
        assert "LLM" in does_not or "llm" in does_not.lower(), (
            "COVERAGE_BOUNDARY.does_not must explicitly disclaim LLM calls"
        )


# ── 7. fit/load API ────────────────────────────────────────────────────────────

class TestFitLoadAPI:
    def test_fit_requires_keys_and_X(self):
        mem = hr.HopfieldMemory()
        with pytest.raises(RuntimeError):
            mem.retrieve(np.zeros(64, dtype=np.float32), k=1)

    def test_fit_normalises_rows(self):
        """fit() must L2-normalise stored patterns."""
        keys = ["a", "b"]
        X = np.array([[2.0, 0.0], [0.0, 3.0]], dtype=np.float32)
        mem = hr.HopfieldMemory().fit(keys, X)
        norms = np.linalg.norm(mem.X, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-6)

    def test_retrieve_output_sorted_descending(self, mem_small, small_patterns):
        _, X = small_patterns
        results = mem_small.retrieve(X[0], k=5)
        sims = [r[1] for r in results]
        assert sims == sorted(sims, reverse=True), (
            "retrieve() results must be sorted by similarity descending"
        )

    def test_bow_hash_vector_deterministic(self):
        v1 = hr._bow_hash_vector("hello world pattern recall", dim=128)
        v2 = hr._bow_hash_vector("hello world pattern recall", dim=128)
        assert np.allclose(v1, v2)

    def test_bow_hash_vector_normalised(self):
        v = hr._bow_hash_vector("hello world", dim=64)
        assert abs(np.linalg.norm(v) - 1.0) < 1e-6

    def test_cosine_topk_returns_k_indices(self, small_patterns):
        keys, X = small_patterns
        idxs = hr.cosine_topk(X, X[0], k=5)
        assert len(idxs) == 5
        assert all(0 <= i < len(keys) for i in idxs)

    def test_load_returns_fitted_memory(self):
        idx = HERE / "_system" / "semantic_index.json"
        if not idx.exists():
            pytest.skip("semantic_index.json not present")
        mem = hr.load(HERE)
        assert mem.X is not None
        assert len(mem.keys) > 0
        assert mem.X.shape[0] == len(mem.keys)
