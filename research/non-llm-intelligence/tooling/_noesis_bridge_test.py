#!/usr/bin/env python3
"""pytest for LOOP 10 (_noesis_bridge): the Noesis <-> JARVIS structural isomorphism."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _noesis_bridge as nb  # noqa: E402

Q16 = nb.Q16
CORPUS = nb._demo_corpus()
THETA = int(0.90 * Q16)


def test_noesis_v0_exact_duplicate_earns_zero():
    vals = nb.NoveltyOracleV0().cell_values(CORPUS, THETA)
    assert vals[1] == 0  # pom_dup is an exact duplicate of pom


def test_noesis_v0_deterministic():
    o = nb.NoveltyOracleV0()
    assert o.cell_values(CORPUS, THETA) == o.cell_values(CORPUS, THETA)


def test_jarvis_oracle_satisfies_seam_contract():
    jar = nb.JarvisAttentionOracle(
        centrality={"pom": 5, "pom_dup": 5, "amd": 3, "tempnov": 2, "pom_near": 4},
        recency_q16={"pom": Q16, "pom_dup": Q16, "amd": Q16 // 2, "tempnov": Q16, "pom_near": Q16 // 4},
    )
    c = nb.verify_contract(jar, CORPUS, THETA)
    assert c["valid_value_oracle"] is True
    assert c["deterministic"] and c["integer_output"] and c["one_value_per_cell"]


def test_shared_pipeline_runs_for_both_oracles():
    for oracle in (nb.NoveltyOracleV0(),
                   nb.JarvisAttentionOracle(centrality={c.slug: 1 for c in CORPUS})):
        st = nb.standing(oracle, CORPUS, THETA)
        alloc = nb.allocate(st, budget=100)
        assert sum(alloc.values()) in (0, 100)  # largest-remainder conserves the budget
        assert all(isinstance(v, int) for v in st.values())


def test_allocation_proportional_to_standing():
    st = {"a": 3, "b": 1}
    alloc = nb.allocate(st, 100)
    assert alloc["a"] > alloc["b"] and sum(alloc.values()) == 100


def test_grounding_pointers_present():
    # every structural claim carries a Noesis file:line (anti-hallucination discipline)
    assert nb.NOESIS_REF["ValueOracle_trait"].startswith("node/src/lib.rs")
    assert len(nb.NOESIS_REF) >= 5
