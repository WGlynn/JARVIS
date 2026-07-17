# Non-LLM Intelligence — Tooling (copyable)

Deterministic, CPU-only, **zero-LLM** reasoning components for an agent substrate. Built as LOOP 1 + LOOP 3
of the roadmap in `../ROADMAP.md`. Free to copy and adapt (see repo LICENSE). No GPU, no data center — the
whole point is that the *reasoning* runs local and deterministic while the LLM stays an occasional, fallible
peripheral.

## What's here

### LOOP 1 — memory-graph deduction (ASP / clingo)
Compile a flat markdown knowledge-graph (files with YAML frontmatter + `[[wikilink]]` and/or `[X·slug]`
bracket-tag edges) into Answer-Set-Programming facts and **deduce over it** — transitive reachability, dead
links, orphans, slug collisions — with zero model calls.

- `_asp_extract.py` — markdown → `facts.lp` (+ `provenance.json`). Non-recursive top-level walk; prefix
  normalization; `name:`-aliasing; both link syntaxes. Point `--root` at any graph (or set
  `JARVIS_MEMORY_ROOT`); defaults to its own directory.
- `_asp_rules.lp` — the stratified Datalog/ASP rules (reachability, `dead_link`, `unreferenced`, `dup_slug`).
- `_asp_query.py` — `report` (writes a classified `graph_report.md`) and `reachable <slug>`. Requires
  `pip install clingo`.
- `_asp_fallback.py` — an independent pure-Python semi-naive fixpoint. Doubles as the **differential test
  oracle**: clingo and this engine agreeing on the same facts is a mechanical soundness proof.
- `_asp_test.py` — `pytest` (8 tests) incl. the clingo≡fallback differential and byte-determinism.

### LOOP 3 — sound solver gates (Z3 + OR-Tools)
- `_solver_gate.py` — Z3-backed **sound** concurrency-invariant check with an explicit coverage boundary
  and an adversarial fixture where Z3 blocks a state a naive count-heuristic waves through.
- `_scheduler.py` — OR-Tools CP-SAT optimal admission scheduler (a bin-packing that beats greedy).
- `test_loop3_solvers.py` — `pytest` (25 tests).

Hardware caps are env-configurable (`JARVIS_MAX_FORGE_CONCURRENT`, …) with conservative defaults — never
hard-coded, so a copier sets their own machine's limits.

## Run
```
pip install clingo z3-solver ortools
python _asp_extract.py --root /path/to/your/markdown/graph
python _asp_query.py report --root /path/to/your/markdown/graph
python -m pytest _asp_test.py test_loop3_solvers.py -q      # 33 tests
```

## Design discipline
Read-only (never auto-edits your notes). Honest coverage boundaries (out-of-scope → "not evaluated", not a
false pass). Two independent engines cross-check the graph. It found a real slug collision and a bug in its
own extractor on first contact — that's the point: the substrate audits itself, deterministically, for free.
