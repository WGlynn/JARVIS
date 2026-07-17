#!/usr/bin/env python3
"""_asp_test.py -- pytest for the ASP memory-graph tooling (LOOP 1, Phase 1-2).

Verifies: extraction correctness (prefix-normalization + name-aliasing), byte-determinism, and the
clingo-vs-fallback DIFFERENTIAL -- two independent engines must agree on {dead_link, unreferenced}.

Run: python -m pytest _asp_test.py -q
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


_extract = _load("_asp_extract")
_fb = _load("_asp_fallback")
_query = _load("_asp_query")

# Synthetic corpus exercising: wikilink, prefix-in-link, name-alias, alias-syntax link,
# dead link, prose-noise dead link, orphan node.
CORPUS = {
    "primitive_alpha.md": "body [[beta]] and [[primitive_gamma]] and [[nonexistent-thing]]\n",
    "primitive_beta.md": "---\nname: b-alias\n---\nbody [[alpha]]\n",
    "primitive_gamma.md": "no links here\n",
    "feedback_delta.md": "orphan node, links nothing inbound or out\n",
    "project_epsilon.md": "body [[b-alias]]\n",
    "_CANON_zeta.md": "body [[alpha]]\n",
    "user_eta.md": "body [[wikilinks]] and [[gamma]]\n",
    "reference_theta.md": "body [[alpha|display text]] and [P·gamma] via bracket-tag\n",
    # slug collision: both canonicalize to "dup"
    "primitive_dup.md": "body, collides with feedback_dup\n",
    "feedback_dup.md": "body, collides with primitive_dup\n",
}


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    for name, body in CORPUS.items():
        (tmp_path / name).write_text(body, encoding="utf-8")
    return tmp_path


def _facts_file(corpus: Path) -> Path:
    facts, _prov, _stats = _extract.extract(corpus)
    out = corpus / "facts.lp"
    out.write_text("\n".join(facts) + "\n", encoding="utf-8")
    return out


def test_node_count_and_alias(corpus: Path):
    facts, _prov, stats = _extract.extract(corpus)
    # 10 files, but primitive_dup + feedback_dup collide into 1 node "dup" => 9 nodes
    assert stats["nodes"] == 9
    assert 'alias("b-alias","beta").' in facts


def test_dup_slug_detected(corpus: Path):
    slug_files = _fb.parse_files(_facts_file(corpus))
    dups = _fb.dup_slugs(slug_files)
    assert ("dup", "feedback_dup.md", "primitive_dup.md") in dups


def test_prefix_and_alias_resolve(corpus: Path):
    facts, _prov, _stats = _extract.extract(corpus)
    assert 'links("alpha","gamma").' in facts       # [[primitive_gamma]] -> gamma
    assert 'links("epsilon","beta").' in facts       # [[b-alias]] -> beta via name-alias
    assert 'links("theta","alpha").' in facts        # [[alpha|display]] alias syntax


def test_brackettag_edge(corpus: Path):
    facts, _prov, _stats = _extract.extract(corpus)
    assert 'links("theta","gamma").' in facts        # [P·gamma] bracket-tag -> gamma


def test_determinism(corpus: Path):
    f1, _p1, _s1 = _extract.extract(corpus)
    f2, _p2, _s2 = _extract.extract(corpus)
    assert f1 == f2


def test_dead_links_expected(corpus: Path):
    prims, edges = _fb.parse_facts(_facts_file(corpus))
    dead_targets = {b for _a, b in _fb.dead_links(prims, edges)}
    assert "nonexistent-thing" in dead_targets   # genuine dead link
    assert "wikilinks" in dead_targets           # prose false-positive (a real class in the corpus)
    assert "gamma" not in dead_targets           # prefix-normalized, resolves
    assert "beta" not in dead_targets            # name-aliased, resolves


def test_orphan_detected(corpus: Path):
    prims, edges = _fb.parse_facts(_facts_file(corpus))
    assert "delta" in _fb.unreferenced(prims, edges)


def test_clingo_matches_fallback(corpus: Path):
    """The differential: clingo and the pure-Python fixpoint must agree exactly."""
    facts_path = _facts_file(corpus)
    prims, edges = _fb.parse_facts(facts_path)
    fb_dead = _fb.dead_links(prims, edges)
    fb_unref = _fb.unreferenced(prims, edges)

    fb_dup = _fb.dup_slugs(_fb.parse_files(facts_path))

    atoms = _query._solve([facts_path, _query.RULES])
    cl_dead = {
        tuple(m.groups())
        for a in atoms
        if (m := re.match(r'dead_link\("([^"]*)","([^"]*)"\)', a))
    }
    cl_unref = {
        m.group(1) for a in atoms if (m := re.match(r'unreferenced\("([^"]*)"\)', a))
    }
    cl_dup = {
        tuple(m.groups())
        for a in atoms
        if (m := re.match(r'dup_slug\("([^"]*)","([^"]*)","([^"]*)"\)', a))
    }

    assert cl_dead == fb_dead, f"dead_link mismatch: clingo={cl_dead} fallback={fb_dead}"
    assert cl_unref == fb_unref, f"unreferenced mismatch: clingo={cl_unref} fallback={fb_unref}"
    assert cl_dup == fb_dup, f"dup_slug mismatch: clingo={cl_dup} fallback={fb_dup}"
