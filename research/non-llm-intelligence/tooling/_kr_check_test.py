#!/usr/bin/env python3
"""_kr_check_test.py -- pytest suite for LOOP 6 (Typed Knowledge + Sound Inference).

Tests:
  1. Schema loads without error.
  2. Corpus graph builds (nodes extracted, closure runs deterministically).
  3. Each check returns structured results with required keys.
  4. Synthetic-inconsistency fixture: a fake Gate with no hook is caught by check_gate_missing_hook.
  5. Synthetic dead-link fixture: an unresolved wikilink is caught by check_wikilink_targets_resolve.
  6. Closure is deterministic: two independent graph builds produce the same triple count.
  7. Canon nodes (from _CANON_ files) are typed Canon in the graph.
  8. Feedback nodes (from feedback_ files) are typed Feedback in the graph.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure the memory dir is on the path
MEMORY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(MEMORY_DIR))

# ---------------------------------------------------------------------------
# Conditional skip if rdflib unavailable
# ---------------------------------------------------------------------------
try:
    from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
    RDFLIB_OK = True
except ImportError:
    RDFLIB_OK = False

rdflib_required = pytest.mark.skipif(not RDFLIB_OK, reason="rdflib not installed")

# ---------------------------------------------------------------------------
# Import module under test (after path setup)
# ---------------------------------------------------------------------------
if RDFLIB_OK:
    import _kr_check as kr


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def live_graph():
    """Build the real corpus graph once per test session."""
    return kr.build_graph()


@pytest.fixture
def minimal_graph():
    """A tiny synthetic graph with known structure for unit tests."""
    g = Graph()
    g.bind("j", Namespace("urn:jarvis:"))

    J = Namespace("urn:jarvis:")

    # Load real schema so class hierarchy is present
    schema_path = MEMORY_DIR / "_kr_schema.ttl"
    if schema_path.exists():
        g.parse(str(schema_path), format="turtle")

    # Node A: a real Gate with a real hook reference
    node_a = URIRef("urn:jarvis:node/test-gate-with-hook")
    g.add((node_a, RDF.type, J.Gate))
    g.add((node_a, J.gate_hasHook, Literal("em-dash-augmentation-gate.py")))
    g.add((node_a, J.isCorpusNode, Literal(True)))

    # Node B: a Gate with NO hook (synthetic inconsistency)
    node_b = URIRef("urn:jarvis:node/test-gate-no-hook")
    g.add((node_b, RDF.type, J.Gate))
    g.add((node_b, J.isCorpusNode, Literal(True)))

    # Node C: a Primitive (target of a valid link) — has corpus marker
    node_c = URIRef("urn:jarvis:node/test-primitive-exists")
    g.add((node_c, RDF.type, J.Primitive))
    g.add((node_c, J.isCorpusNode, Literal(True)))

    # Node D: a Feedback linking to node_c (valid)
    node_d = URIRef("urn:jarvis:node/test-feedback-linked")
    g.add((node_d, RDF.type, J.Feedback))
    g.add((node_d, J.isCorpusNode, Literal(True)))
    g.add((node_d, J.links_to, node_c))

    # Node E: a Feedback with a dead wikilink (synthetic inconsistency).
    # The dead_target has NO isCorpusNode marker — it never had a file.
    # RDFS range closure will give it rdf:type MemoryNode, but that does NOT
    # satisfy the isCorpusNode check, so it correctly surfaces as a dead link.
    node_e = URIRef("urn:jarvis:node/test-feedback-dead-link")
    g.add((node_e, RDF.type, J.Feedback))
    g.add((node_e, J.isCorpusNode, Literal(True)))
    dead_target = URIRef("urn:jarvis:node/this-node-does-not-exist-xyz")
    g.add((node_e, J.links_to, dead_target))
    # deliberately NO isCorpusNode on dead_target

    # Node F: Canon node (should never be deprecated)
    node_f = URIRef("urn:jarvis:node/test-canon-valid")
    g.add((node_f, RDF.type, J.Canon))
    g.add((node_f, J.isCorpusNode, Literal(True)))

    # Synthetic Canon+deprecated violation
    node_g = URIRef("urn:jarvis:node/test-canon-deprecated-BAD")
    g.add((node_g, RDF.type, J.Canon))
    g.add((node_g, J.isCorpusNode, Literal(True)))
    g.add((node_g, J.primitive_hasType, Literal("deprecated")))

    # Apply closure
    kr.rdfs_closure_fallback(g)

    # Attach metadata the checks expect
    g._hooks_on_disk = {"em-dash-augmentation-gate.py", "atomic-reflection-gate.py"}
    g._files_loaded = 7
    g._closure_method = "fallback-rdfs (test)"

    return g


# ---------------------------------------------------------------------------
# Test 1: Schema loads without error
# ---------------------------------------------------------------------------

@rdflib_required
def test_schema_loads():
    schema_path = MEMORY_DIR / "_kr_schema.ttl"
    assert schema_path.exists(), f"Schema file missing: {schema_path}"
    g = Graph()
    g.parse(str(schema_path), format="turtle")
    # Must contain the core classes
    J = Namespace("urn:jarvis:")
    assert (J.Gate, RDFS.subClassOf, J.Primitive) in g, "Gate subClassOf Primitive missing"
    assert (J.Canon, RDFS.subClassOf, J.Primitive) in g, "Canon subClassOf Primitive missing"
    assert (J.Primitive, RDFS.subClassOf, J.MemoryNode) in g, "Primitive subClassOf MemoryNode missing"
    assert (J.Feedback, RDFS.subClassOf, J.MemoryNode) in g, "Feedback subClassOf MemoryNode missing"


# ---------------------------------------------------------------------------
# Test 2: Corpus graph builds with non-zero nodes
# ---------------------------------------------------------------------------

@rdflib_required
def test_corpus_graph_builds(live_graph):
    assert live_graph._files_loaded > 0, "No files loaded from corpus"
    assert len(live_graph) > 100, "Graph suspiciously small — extraction likely broken"
    # Must have at least some typed nodes
    J = Namespace("urn:jarvis:")
    primitives = list(live_graph.triples((None, RDF.type, J.Primitive)))
    feedbacks   = list(live_graph.triples((None, RDF.type, J.Feedback)))
    assert len(primitives) > 0, "No Primitive nodes found"
    assert len(feedbacks) > 0, "No Feedback nodes found"


# ---------------------------------------------------------------------------
# Test 3: Each check returns structured results with required keys
# ---------------------------------------------------------------------------

@rdflib_required
def test_check_results_have_required_keys(live_graph):
    results = kr.run_checks(live_graph)
    required_keys = {"check", "description", "passed"}
    assert len(results) >= 3, "Fewer than 3 checks returned"
    for r in results:
        missing = required_keys - r.keys()
        assert not missing, f"Check '{r.get('check','?')}' missing keys: {missing}"
        assert isinstance(r["passed"], bool), f"'passed' must be bool in {r['check']}"


# ---------------------------------------------------------------------------
# Test 4: Synthetic Gate-no-hook inconsistency is caught
# ---------------------------------------------------------------------------

@rdflib_required
def test_synthetic_gate_no_hook_caught(minimal_graph):
    result = kr.check_gate_missing_hook(minimal_graph)
    assert not result["passed"], "Expected check to FAIL on gate-no-hook fixture"
    slugs = [v["node"] for v in result["violations"]]
    assert "test-gate-no-hook" in slugs, (
        f"test-gate-no-hook not in violations: {slugs}"
    )
    # The gate WITH a hook and real hook on disk should NOT be a violation
    assert "test-gate-with-hook" not in slugs, (
        "test-gate-with-hook should NOT be a violation (hook is on disk)"
    )


# ---------------------------------------------------------------------------
# Test 5: Synthetic dead-link is caught
# ---------------------------------------------------------------------------

@rdflib_required
def test_synthetic_dead_link_caught(minimal_graph):
    result = kr.check_wikilink_targets_resolve(minimal_graph)
    assert not result["passed"], "Expected check to FAIL on dead-link fixture"
    targets = [v["target"] for v in result["all_violations"]]
    assert "this-node-does-not-exist-xyz" in targets, (
        f"Dead link target not caught: {targets}"
    )


# ---------------------------------------------------------------------------
# Test 6: Canon + deprecated contradiction is caught
# ---------------------------------------------------------------------------

@rdflib_required
def test_synthetic_canon_deprecated_caught(minimal_graph):
    result = kr.check_canon_not_deprecated(minimal_graph)
    assert not result["passed"], "Expected check to FAIL on canon+deprecated fixture"
    nodes = [v["node"] for v in result["violations"]]
    assert "test-canon-deprecated-bad" in nodes or "test-canon-deprecated-BAD" in nodes, (
        f"Canon+deprecated node not caught: {nodes}"
    )
    # The valid canon should NOT appear
    bad = [n for n in nodes if "valid" in n]
    assert not bad, f"Valid canon incorrectly flagged: {bad}"


# ---------------------------------------------------------------------------
# Test 7: Closure is deterministic (two builds = same triple count)
# ---------------------------------------------------------------------------

@rdflib_required
def test_closure_is_deterministic():
    g1 = kr.build_graph()
    g2 = kr.build_graph()
    assert len(g1) == len(g2), (
        f"Non-deterministic closure: {len(g1)} vs {len(g2)} triples"
    )


# ---------------------------------------------------------------------------
# Test 8: Canon nodes from _CANON_ files are typed Canon in live graph
# ---------------------------------------------------------------------------

@rdflib_required
def test_canon_files_typed_canon(live_graph):
    J = Namespace("urn:jarvis:")
    canon_nodes = list(live_graph.triples((None, RDF.type, J.Canon)))
    assert len(canon_nodes) > 0, (
        "No Canon-typed nodes found — _CANON_ files not being typed correctly"
    )


# ---------------------------------------------------------------------------
# Test 9: Feedback files typed Feedback in live graph
# ---------------------------------------------------------------------------

@rdflib_required
def test_feedback_files_typed_feedback(live_graph):
    J = Namespace("urn:jarvis:")
    fb_nodes = list(live_graph.triples((None, RDF.type, J.Feedback)))
    # Should have many — corpus has hundreds of feedback_ files
    assert len(fb_nodes) > 50, (
        f"Only {len(fb_nodes)} Feedback nodes found — expected >> 50"
    )


# ---------------------------------------------------------------------------
# Test 10: Gate inference fires on feedback files that mention hook paths
# ---------------------------------------------------------------------------

@rdflib_required
def test_gate_inference_from_hook_body(live_graph):
    J = Namespace("urn:jarvis:")
    gate_nodes = list(live_graph.triples((None, RDF.type, J.Gate)))
    assert len(gate_nodes) > 0, (
        "No Gate nodes inferred — hook-body detection may be broken"
    )


# ---------------------------------------------------------------------------
# Entry point (allow running directly without pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
