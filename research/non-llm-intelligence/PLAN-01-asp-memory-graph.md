# PLAN-01 — Compile the Memory Graph into ASP (clingo)

**LOOP increment 1** of the non-LLM-intelligence build. Target: the memory directory
(`~/.claude/projects/<host>/memory/`) becomes a **Datalog/ASP program** that
deduces graph facts on CPU with **zero LLM calls** — transitive closure, dead links, orphans,
conflict candidates, parent/child hierarchy, load-bearing support cones.

Status legend per house discipline: ✅ built · 🟡 designed · 🔬 open. Everything below is 🟡 until a
phase's verify step passes.

---

## 0. Ground truth (measured 2026-07-16, do not trust after corpus churn — re-measure)

- ~946 top-level .md files (memories + indexes) + `_*.py` tooling + `_system/`.
- **⚠ `_obsidian-view/` contains 558 DUPLICATE copies of memory files.** Any recursive walk
  double-counts every node and edge. The extractor walks **top-level `*.md` only** — memory files
  live flat; every subdir (`_obsidian-view/`, `_archive/`, `_system/`, `correspondence/`,
  `nda-locked/`, `__pycache__/`, `aa_candidates/`) is excluded by construction.
- **1,883 `[[wikilink]]` occurrences across 406 files** (duplicates excluded) — primary edge syntax.
- **2,668 bracket-tag refs `[T·slug]`** (T ∈ P F R J O M U, plus `AA#N`) — second edge syntax.
  `_index.py` already has the canonical regexes: `PRIMITIVE_REF_PATTERN =
  r"\[((?:[PFRJOMU]·[a-zA-Z0-9_\-]+)|(?:AA#\d+))\]"` and the filename→prefix map
  (`primitive_→P·`, `feedback_→F·`, `reference_→R·`, `project_→J·`, `protocol_→O·`, `user_→U·`).
  **Reuse these, do not re-derive.**
- Frontmatter comes in **two shapes** (both live in corpus):
  - flat: `type: feedback` (older files, e.g. `feedback_advocate-with-receipts.md`)
  - nested: `metadata: {node_type: memory, type: project, originSessionId: ...}` (newer)
- `name:` frontmatter is **NOT a reliable slug** — sometimes prose ("Advocate For Our Work — Cite
  Our Receipts…"). **Canonical node ID = filename-derived slug** (strip `{type}_` prefix + `.md`).
- Special files: `MEMORY.md` + `MEMORY_INDEX_*.md` + `MEMORY_WARM_*.md` = indexes (markdown links
  `[Title](file.md)`), `_CANON_*.md` = exalted capstones, `_archive/` = excluded, `_system/` =
  build outputs, `memory/nda-locked/` = **NEVER read** (PreToolUse hook enforces; extractor must
  hard-skip the path).
- Existing overlapping tooling (COMPLEMENT, then subsume with parity proof):
  - `memory/_index.py` → `_system/primitive_link_index.json` (bracket-tag graph only)
  - `memory/_link_enforcer.py` → orphans / dead-ends / asymmetric links / hubs, heuristic, report
    at `_system/link_health_report.md`
  - `~/.claude/hooks/conflict-detector.py` → PreToolUse Write|Edit; regex negation-window near
    entity mentions using `_system/entity_index.json`. Fires on *drafts*, not on the graph itself.
- Environment: Python 3.12.10, PyYAML 6.0.3 ✅ installed, clingo ❌ not installed but **wheel
  5.8.0 available on pip for this platform** (verified via `pip index versions clingo`).
  Hardware: Ryzen 5 1600 / 16GB, CPU-only. Graph is ~1k nodes / ~6k edges — clingo grounds+solves
  this in well under a second; hardware is a non-issue.

---

## 1. Engine decision: **clingo** (Potassco ASP, official Python bindings)

| Candidate | Verdict | Why |
|---|---|---|
| **clingo** | **CHOSEN** | `pip install clingo` = binary wheel, no compiler. Embeds in-process (`clingo.Control`). Datalog is a strict subset of ASP, so all pure-Datalog rules run as-is; ASP adds negation-as-failure (dead_link/orphan are one-liners), aggregates (`#count` for hubs), and — for later loop increments — choice rules + optimization (repair suggestions, minimal support sets). One runtime covers this loop and the next three. |
| souffle | rejected | Compiled C++, no first-class Windows wheel; toolchain cost > benefit at 1k nodes. Reconsider only if corpus grows 100× (it won't on this box). |
| pyDatalog | rejected | Effectively unmaintained; metaclass magic; no aggregates worth having. |
| hand-rolled fixpoint | **kept as fallback + oracle** | All Phase-1/2 rules are stratified Datalog; a ~80-LOC semi-naive fixpoint gives identical answers. Ship it as `_asp_fallback.py`: (a) insurance if the clingo wheel ever breaks on a Python upgrade, (b) **differential test oracle** — two independent engines agreeing on the same facts is a determinism proof the build loop can check mechanically. |

Pin: `clingo>=5.8,<6`.

---

## 2. Fact schema (extractor output → `_system/asp/facts.lp`)

All constants are quoted strings (slugs contain `-`). Facts are **sorted before emit** so
`facts.lp` is byte-deterministic for a given corpus state.

```prolog
% ---- nodes ----
primitive("slug").                          % a .md file exists defining this node
ptype("slug", feedback).                    % type ∈ user|feedback|project|reference|primitive|protocol|canon|index
file("slug", "feedback_foo.md").            % provenance for every report line
canon("slug").                              % _CANON_* files
index_file("MEMORY.md").                    % the index/warm/boot files themselves

% ---- edges (every edge carries provenance via the extractor's line map, kept in a
% ---- sidecar JSON, not in ASP — ASP reasons over the pure graph) ----
links("a","b").                             % union of all body reference syntaxes, deduped
link_syntax("a","b",wikilink).              % [[b]] or [[b|alias]]
link_syntax("a","b",brackettag).            % [T·b] — tag stripped to slug
index_entry("slug").                        % slug is linked from MEMORY.md / MEMORY_INDEX_* / MEMORY_WARM_*
                                            % (markdown [Title](file.md) links)

% ---- declared structure (regex-extracted from authoring conventions; see §5 honesty) ----
declares_parent("child","parent").          % "parent:", "parent of" (inverted), "Child:", "child of",
                                            % "parent-frame", "capstone of"
declares_sibling("a","b").                  % "sibling", "sibling-lens", "companion:"
declares_inverse("a","b").                  % "Inverse of", "inverse:", "Inverse=", "⊥"
declares_supersedes("a","b").               % "supersedes", "replaces", "overrides", "deprecat"
deprecated("slug").                         % body contains deprecation/superseded-by marker about ITSELF

% ---- query-time injected facts (not in facts.lp; added per invocation) ----
claim_root("slug").                         % the X in "what is load-bearing for claim X"
```

**Slug normalization** (single function, unit-tested, shared by every fact emitter):
lowercase; wikilink target used verbatim minus alias; bracket-tag `T·slug` → `slug`; file
`primitive_foo-bar.md` → `foo-bar`; `_CANON_foo.md` → `foo` + `canon` fact. A wikilink resolves to
a node iff its normalized form equals some file-derived slug — anything else is a `dead_link`
by rule, which is exactly the diagnostic we want (typos surface, they don't get fuzzy-matched away).

---

## 3. Rule set (`_asp_rules.lp`, static, checked into git)

```prolog
% ===== reachability (transitive closure) =====
reachable(X,Y) :- links(X,Y).
reachable(X,Z) :- reachable(X,Y), links(Y,Z).

% ===== dead links: reference to a node no file defines =====
dead_link(A,B) :- links(A,B), not primitive(B).

% ===== orphans =====
referenced(B) :- links(A,B), primitive(A).
unreferenced(P) :- primitive(P), not referenced(P), not index_entry(P), not canon(P).
% hard orphan: additionally links to nothing (fully disconnected)
orphan(P) :- unreferenced(P), not has_outlink(P).
has_outlink(P) :- links(P,_).

% ===== hierarchy =====
parent(P,C)   :- declares_parent(C,P).
ancestor(P,C) :- parent(P,C).
ancestor(P,C) :- parent(P,M), ancestor(M,C).
hierarchy_cycle(P) :- ancestor(P,P).                      % should be EMPTY; report loudly if not
sibling(A,B)  :- parent(P,A), parent(P,B), A < B.
sibling(A,B)  :- declares_sibling(A,B), A < B.
sibling(A,B)  :- declares_sibling(B,A), A < B.

% ===== conflict candidates (structural signals ONLY — see §5) =====
conflict_candidate(A,B,inverse)     :- declares_inverse(A,B).
conflict_candidate(A,B,superseded)  :- declares_supersedes(A,B), links(C,B), C != A, not deprecated(C).
                                       % B was superseded but live nodes still link it
conflict_candidate(A,B,dup_name)    :- primitive(A), primitive(B), A < B, same_name(A,B).
                                       % extractor emits same_name/2 when two files' name: collide
zombie(B)                           :- deprecated(B), links(_,B).   % deprecated but still cited

% ===== load-bearing for a claim =====
% claim_root(X) injected at query time; the support cone is everything X transitively cites.
load_bearing(P)        :- claim_root(X), reachable(X,P), primitive(P).
load_bearing_broken(P) :- claim_root(X), reachable(X,Y), dead_link(Y,P).
                          % the claim rests on a link that resolves to NOTHING — highest-value alert

% ===== structural health extras (subsumes _link_enforcer categories) =====
asym(A,B) :- links(A,B), primitive(B), not links(B,A).
hub(P,N)  :- primitive(P), N = #count { A : links(A,P) }, N >= 8.

#show dead_link/2.  #show orphan/1.  #show unreferenced/1.
#show conflict_candidate/3.  #show zombie/1.  #show hierarchy_cycle/1.
```

The program is **stratified** (negation only over facts or lower strata) ⇒ exactly one stable
model ⇒ fully deterministic; assert `models == 1` in the driver and fail loud otherwise
per [P·boot-hook-fail-loud].

---

## 4. Components — file by file

All new code lives beside the existing tooling in
`~/.claude/projects/<host>/memory/` (house convention: `_name.py`), outputs in
`_system/asp/`. Python: black, 100-char, type hints, stdlib+pyyaml+clingo only.

| File | Role | LOC est. |
|---|---|---|
| `memory/_asp_extract.py` | Walk **top-level `*.md` only** (no recursion ⇒ `_obsidian-view/` dupes, `_archive/`, `_system/`, `nda-locked/`, `correspondence/` all excluded by construction; additionally hard-assert the resolved path parent == memory dir per NDA invariant). Parse frontmatter with PyYAML handling BOTH flat `type:` and nested `metadata.type`. Extract wikilinks (`\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]`), bracket-tags (reuse `_index.py` regex verbatim), index markdown links, declared-structure markers. Emit sorted `_system/asp/facts.lp` + `_system/asp/provenance.json` (edge → file:line for report rendering). | ~230 |
| `memory/_asp_rules.lp` | §3 verbatim. Pure data, no codegen. | ~70 |
| `memory/_asp_query.py` | CLI driver. `report` → ground facts+rules via `clingo.Control`, assert single model, render `_system/asp/graph_report.md` (sections: dead links w/ provenance · zombies · conflict candidates · orphans · hierarchy cycles · hubs · stats). `reachable <slug>`, `supports <slug>` (injects `claim_root`), `deadlinks`, `parity` (diff vs `_link_enforcer` categories). Exit code 0 = healthy, 1 = findings, 2 = engine/extract failure. | ~170 |
| `memory/_asp_fallback.py` | Semi-naive stratified-Datalog fixpoint over the same facts for {reachable, dead_link, unreferenced, orphan}. Used by `--engine=fallback` and by the differential test. | ~90 |
| `memory/_asp_test.py` | pytest. Fixture mini-corpus of 8 synthetic .md files under `tests/fixture_corpus/` exercising: both frontmatter shapes, wikilink+alias, bracket-tag, dead link, orphan, parent chain w/ 3 levels, declared inverse, deprecated-but-linked, NDA-path skip. Golden `facts.lp` diff + expected-atoms assertions + clingo-vs-fallback differential. | ~140 |

Total new code: **~700 LOC**. One new dep: `clingo` (pinned). No services, no daemons.

### Surfacing (how results reach Will / the harness)
1. **CLI first** (Phase 1–2): `python _asp_query.py report` — runnable by hand, by autopilot, by cron.
2. **Report file**: `_system/asp/graph_report.md` — same pattern as `link_health_report.md`,
   human-review-applies per `_link_enforcer` doctrine (read-only, no auto-fix).
3. **Hook complement** (Phase 3, additive — does NOT modify conflict-detector's own logic):
   `conflict-detector.py` gains an optional consult: after its regex pass, if
   `_system/asp/graph_report.md` is fresh (<24h), append any `conflict_candidate`/`zombie` rows
   whose slugs appear in the draft to its `additionalContext` warning. Division of labor:
   conflict-detector = *draft vs memory* (prose, heuristic); ASP = *memory vs memory* (graph,
   sound). Neither replaces the other; together they cover both surfaces.
4. **Freshness**: a `SessionStart`-adjacent cron or the existing autopilot loop runs
   `_asp_extract.py && _asp_query.py report` (total runtime target <5s). No PreToolUse latency
   is added anywhere.

---

## 5. What ASP does NOT buy us — honest limits (do not oversell)

1. **No semantic contradiction detection.** `conflict_candidate` fires only on *structural*
   signals (declared inverses, supersession, duplicate names, zombie citations). Two primitives
   that contradict in prose meaning without any marker are invisible to this layer. Judging a
   candidate = still LLM/Will. ASP narrows the haystack; it does not find the needle's meaning.
2. **Extraction bounds soundness.** Inference is sound *over the facts*; the facts come from
   regex over authoring conventions. A "parent of" phrase used rhetorically becomes a bogus
   `declares_parent` fact and every downstream `ancestor` inherits the error. Mitigation:
   provenance on every fact + report shows the source line; but garbage-in remains possible.
3. **"Load-bearing" = citation cone, not logical entailment.** `load_bearing(P)` means the claim
   *transitively cites* P — necessary-context, not proved-premise. Real entailment would need the
   claims themselves formalized, which is a different (much larger) loop increment.
4. **No relevance ranking, no retrieval.** Which memory matters for the current prompt stays with
   the existing semantic index + LLM. ASP answers structure questions, not salience questions.
5. **No natural language.** Writing memories, compressing them, HIERO-encoding — all still LLM.
6. **Corpus scale ceiling is a non-concern here** (1k nodes), but the naive `reachable/2` is
   O(V·E) grounded atoms; at ~100k nodes this design would need magic-sets/souffle. Flagged, not
   fixed — YAGNI per ponytail.

Net honest claim: this makes the substrate's *graph integrity* self-auditing and its *dependency
structure* queryable at zero marginal LLM cost. It does not make the substrate "reason about
meaning."

---

## 6. Phased build plan (each phase = one autonomous-loop increment, green before next)

### Phase 0 — engine smoke (15 min)
- `pip install "clingo>=5.8,<6"`.
- Verify: `python -c "import clingo; ctl=clingo.Control(); ctl.add('base',[],'a. b :- a.'); ctl.ground([('base',[])]); ctl.solve(on_model=print)"` prints a model containing `a b`.
- Failure branch: if wheel import fails on this box, flip default engine to `_asp_fallback.py`
  and demote clingo to optional — Phases 1–2 lose nothing (they're pure stratified Datalog);
  Phase 3 aggregates (`hub`) get a 5-line Python count instead. Record outcome in this file.

### Phase 1 — smallest end-to-end slice (target: one session)
- Build `_asp_extract.py` **wikilinks + primitives only** (no bracket-tags, no declared
  structure), `_asp_rules.lp` with only `reachable/dead_link/unreferenced`, `_asp_query.py`
  with `report` + `reachable <slug>`, fixture corpus + tests for exactly this slice.
- **Deterministic verification:**
  a. `pytest memory/_asp_test.py` green.
  b. Run extractor twice → `fd -x sha256sum` on `facts.lp` identical (sorted-emit proof).
  c. Spot-truth 3 known edges: `christian-mechanism-design → augmented-mechanism-design-paper`,
     `ponytail-lazy-senior-dev → structure-does-the-work`, `ponytail-lazy-senior-dev →
     apply-the-rule-you-just-wrote` (all confirmed present in corpus 2026-07-16).
  d. `reachable christian-mechanism-design` output is non-empty and every listed slug has a
     `primitive` fact or appears in dead-link section.
  e. Solver reports exactly 1 model; runtime <5s wall on full corpus.

### Phase 2 — full schema + link_enforcer parity
- Add bracket-tag edges, `ptype`, `index_entry`, `canon`, orphan/asym/hub rules,
  declared-structure extraction (`parent/ancestor/sibling/cycle`), `_asp_fallback.py` +
  differential test.
- **Verification:** pytest green incl. differential (clingo == fallback on shared predicates);
  `_asp_query.py parity` compares orphan/dead-end/asym sets vs `_link_enforcer.py` output —
  every *disagreement* must be explained in the report (expected: ASP finds strictly more, since
  it resolves both syntaxes; a case _link_enforcer finds that ASP misses = bug, fix before green).
  `hierarchy_cycle` section empty or each cycle hand-confirmed real.

### Phase 3 — conflicts, load-bearing, surfacing
- Add `declares_inverse/supersedes/deprecated/same_name` extraction; `conflict_candidate`,
  `zombie`, `load_bearing`, `load_bearing_broken`; `supports <slug>` CLI; the additive
  conflict-detector consult (guarded by report-freshness check, fail-open to current behavior);
  wire refresh into autopilot/cron.
- **Verification:** fixture cases for each conflict signal; inject `claim_root` on a real capstone
  (`triple-intersection-provenance-of-mind`) and hand-audit its printed support cone once;
  conflict-detector hook regression: run its existing test/manual invocation with the ASP file
  absent, stale, and fresh — identical behavior in first two cases.
- **Deprecation decision point (Will-gated):** if parity has held for 2 weeks of autopilot runs,
  retire `_link_enforcer.py` analysis (keep `_index.py`, which feeds other consumers).

### Phase 4 — explicitly OUT of this loop increment (backlog for LOOP 2+)
Incremental grounding on file-watch; formalizing claim content (real entailment); repair
suggestions via ASP optimization (`#minimize` over edit sets); WAL/SESSION_STATE as facts; VSA
retrieval layer. Listed so the build loop doesn't scope-creep into them.

---

## 7. Invariants for the autonomous build loop
- Never read/glob `memory/nda-locked/` (hook-enforced anyway; extractor must also hard-skip).
- Outputs only under `_system/asp/`; source files only the five named in §4; no other memory
  files touched.
- Read-only analysis — no auto-fix of memory files, ever (matches `_link_enforcer` doctrine).
- Every phase ends: pytest green + report regenerated + one-paragraph increment note appended to
  this file's changelog section below.

## Changelog
- 2026-07-16 — PLAN-01 authored (plan only; no phase executed). Engine probe: clingo 5.8.0 wheel
  confirmed available via pip index; PyYAML 6.0.3 present; clingo not yet installed.
- 2026-07-16 — Severity-calibration pass: initial link counts (3,163 / 572) were inflated by
  `_obsidian-view/` duplicate copies; corrected to 1,883 wikilinks / 406 files and switched
  extractor spec to non-recursive top-level walk. Credit: conflict-detector hook surfacing the
  duplicate path.
