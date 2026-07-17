#!/usr/bin/env python3
"""_kr_check.py -- LOOP 6: Typed Knowledge + Sound Inference over the JARVIS memory graph.

Loads the corpus into an RDF graph, applies RDFS closure (subClassOf/subPropertyOf/domain/range),
then runs >=3 SPARQL consistency checks. Zero LLM calls. Pure Python (rdflib + owlrl or fallback).

COVERAGE_BOUNDARY
-----------------
COVERS:
  - Top-level *.md files in JARVIS_MEMORY_ROOT (excluding nda-locked/, _obsidian-view/, _archive/,
    _system/, __pycache__, and any subdirectory file)
  - Frontmatter fields: name, type, metadata.type, metadata.status, description
  - Body-text evidence: wikilinks [[...]], bracket-tags [X·slug], hook-path mentions (~/.claude/hooks/*.py)
  - Filename-prefix typing (primitive_, feedback_, reference_, project_, _CANON_, user_)
  - Registered hook files on disk: ~/.claude/hooks/ directory listing

DOES NOT COVER:
  - Archived, NDA-locked, or _obsidian-view/ files (excluded by construction)
  - Semantic meaning of node content beyond structured extraction
  - Any inference requiring language understanding (no LLM calls)
  - Subdirectory *.md files (MEMORY_WARM_*, MEMORY_INDEX_*, etc. are indexed but typed via prefix only)
  - settings.json hook registration (checks hook FILE existence, not registration)

GOFAI GUARDRAIL: every extracted fact carries its provenance (file:line or filename) — no fact is
asserted without a verifiable source in the raw file content or filesystem.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Dependency availability
# ---------------------------------------------------------------------------
try:
    from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD
    from rdflib.namespace import NamespaceManager
    RDFLIB_OK = True
except ImportError:
    RDFLIB_OK = False

try:
    import owlrl
    OWLRL_OK = True
except ImportError:
    OWLRL_OK = False

try:
    import yaml
    YAML_OK = True
except ImportError:
    YAML_OK = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ["JARVIS_MEMORY_ROOT"]) if os.environ.get("JARVIS_MEMORY_ROOT") else SCRIPT_DIR
HOOKS_DIR = Path.home() / ".claude" / "hooks"
SCHEMA_TTL = SCRIPT_DIR / "_kr_schema.ttl"

# ---------------------------------------------------------------------------
# Namespaces
# ---------------------------------------------------------------------------
if RDFLIB_OK:
    J = Namespace("urn:jarvis:")
    SCHEMA_BASE = "urn:jarvis:"

# ---------------------------------------------------------------------------
# Regex patterns (provenance-verified extraction)
# ---------------------------------------------------------------------------
WIKILINK = re.compile(r"\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]")
BRACKETTAG = re.compile(r"\[[PFRJOMU]·([a-zA-Z0-9_\-]+)\]")
HOOK_REF = re.compile(r"~/.claude/hooks/([a-z0-9_\-]+\.py)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

TYPE_PREFIXES = ("primitive_", "feedback_", "reference_", "project_", "user_")

# Map from filename prefix / frontmatter type -> KR class URI (string suffix)
PREFIX_TO_CLASS = {
    "primitive_": "Primitive",
    "feedback_": "Feedback",
    "reference_": "Reference",
    "project_": "Project",
    "user_": "UserContext",
    "_canon_": "Canon",
}
FMTYPE_TO_CLASS = {
    "primitive": "Primitive",
    "feedback": "Feedback",
    "reference": "Reference",
    "project": "Project",
    "user": "UserContext",
    "protocol": "Protocol",
}

# ---------------------------------------------------------------------------
# Slugging (mirrors _asp_extract.py to keep node IDs consistent)
# ---------------------------------------------------------------------------

def _strip_type_prefix(s: str) -> str:
    if s.startswith("_canon_"):
        return s[len("_canon_"):]
    for pfx in TYPE_PREFIXES:
        if s.startswith(pfx):
            return s[len(pfx):]
    return s


def slug_from_filename(name: str) -> str:
    stem = name[:-3] if name.endswith(".md") else name
    return _strip_type_prefix(stem.strip().lower())


def slug_from_link(target: str) -> str:
    return _strip_type_prefix(target.split("|")[0].strip().lower())


def node_uri(slug: str) -> "URIRef":
    return URIRef(f"urn:jarvis:node/{slug}")


# ---------------------------------------------------------------------------
# Frontmatter parsing (provenance: file:line 1-N of the YAML block)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str, filename: str) -> dict[str, Any]:
    """Extract frontmatter dict. Returns {} if absent or unparseable (never raises)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    if YAML_OK:
        try:
            fm = yaml.safe_load(raw) or {}
            if not isinstance(fm, dict):
                return {}
            # Normalise nested metadata: block
            meta = fm.get("metadata") or {}
            if isinstance(meta, dict):
                for k, v in meta.items():
                    if k not in fm:
                        fm[k] = v
            return fm
        except Exception:
            return {}
    # Minimal fallback: key: value on each line
    result: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    return result


# ---------------------------------------------------------------------------
# Class inference: filename prefix wins; frontmatter breaks ties; body upgrades to Gate/Canon
# ---------------------------------------------------------------------------

def infer_class(path: Path, fm: dict, body: str) -> str:
    """Return KR class name (string suffix of urn:jarvis:) for a file.
    Provenance: filename prefix (load-bearing) > frontmatter type > body evidence.
    """
    name_lower = path.name.lower()

    # Canon: _CANON_ prefix is unambiguous
    if name_lower.startswith("_canon_"):
        return "Canon"

    # Filename prefix detection
    for pfx, cls in PREFIX_TO_CLASS.items():
        if pfx != "_canon_" and name_lower.startswith(pfx):
            base_class = cls
            break
    else:
        # Fall back to frontmatter
        fm_type = (fm.get("type") or "").lower().strip()
        base_class = FMTYPE_TO_CLASS.get(fm_type, "MemoryNode")

    # Upgrade Feedback -> Gate if body explicitly names a hook file
    # (evidence: HOOK_REF pattern at any line in body)
    if base_class == "Feedback" and HOOK_REF.search(body):
        return "Gate"

    return base_class


# ---------------------------------------------------------------------------
# Hook extraction: what hook file does this Gate reference?
# Provenance: file:line of the first match.
# ---------------------------------------------------------------------------

def extract_hook_refs(body: str) -> list[tuple[str, int]]:
    """Returns [(basename, lineno), ...] for each ~/.claude/hooks/*.py mention."""
    results = []
    for lineno, line in enumerate(body.splitlines(), 1):
        for m in HOOK_REF.finditer(line):
            results.append((m.group(1), lineno))
    return results


# ---------------------------------------------------------------------------
# Registered hook files on disk
# ---------------------------------------------------------------------------

def registered_hooks() -> set[str]:
    """Return basenames of *.py files present in ~/.claude/hooks/."""
    if not HOOKS_DIR.exists():
        return set()
    return {p.name for p in HOOKS_DIR.iterdir() if p.suffix == ".py"}


# ---------------------------------------------------------------------------
# RDFS closure (pure-Python fallback if owlrl unavailable)
# ---------------------------------------------------------------------------

def rdfs_closure_fallback(g: "Graph") -> int:
    """Minimal stratified RDFS closure: subClassOf, subPropertyOf, domain, range.
    Returns number of triples added."""
    added = 0
    changed = True
    while changed:
        changed = False
        new_triples: list[tuple] = []

        # rdfs:subClassOf transitivity: A subClassOf B, B subClassOf C => A subClassOf C
        for a, _, b in g.triples((None, RDFS.subClassOf, None)):
            for _, _, c in g.triples((b, RDFS.subClassOf, None)):
                t = (a, RDFS.subClassOf, c)
                if t not in g:
                    new_triples.append(t)

        # rdfs:type propagation via subClassOf: x a A, A subClassOf B => x a B
        for x, _, a in g.triples((None, RDF.type, None)):
            for _, _, b in g.triples((a, RDFS.subClassOf, None)):
                t = (x, RDF.type, b)
                if t not in g:
                    new_triples.append(t)

        # rdfs:subPropertyOf: p subPropertyOf q, s p o => s q o
        for p, _, q in g.triples((None, RDFS.subPropertyOf, None)):
            for s, _, o in g.triples((None, p, None)):
                t = (s, q, o)
                if t not in g:
                    new_triples.append(t)

        # rdfs:domain: p domain D, s p o => s a D
        for p, _, d in g.triples((None, RDFS.domain, None)):
            for s, _, _ in g.triples((None, p, None)):
                t = (s, RDF.type, d)
                if t not in g:
                    new_triples.append(t)

        # rdfs:range: p range R, s p o => o a R
        for p, _, r in g.triples((None, RDFS.range, None)):
            for _, _, o in g.triples((None, p, None)):
                if isinstance(o, URIRef):
                    t = (o, RDF.type, r)
                    if t not in g:
                        new_triples.append(t)

        for t in new_triples:
            g.add(t)
            added += 1
        if new_triples:
            changed = True

    return added


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def build_graph() -> "Graph":
    """Walk top-level *.md files, extract typed nodes + edges, load schema, apply closure."""
    if not RDFLIB_OK:
        raise RuntimeError("rdflib not installed — run: pip install rdflib")

    g = Graph()
    g.bind("j", J)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)

    # Load schema
    if SCHEMA_TTL.exists():
        g.parse(str(SCHEMA_TTL), format="turtle")

    # Collect top-level *.md files (same exclusion policy as _asp_extract.py)
    excluded_dirs = {"nda-locked", "_obsidian-view", "_system", "__pycache__", "_archive"}
    files = sorted(
        p for p in ROOT.glob("*.md")
        if p.is_file()
        and not any(part in excluded_dirs for part in p.parts)
    )

    hooks_on_disk = registered_hooks()

    # Pass 1: declare nodes
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text, path.name)
        # body = text after frontmatter
        fm_match = FRONTMATTER_RE.match(text)
        body = text[fm_match.end():] if fm_match else text

        slug = slug_from_filename(path.name)
        uri = node_uri(slug)
        cls_name = infer_class(path, fm, body)
        cls_uri = URIRef(f"urn:jarvis:{cls_name}")

        # Provenance: filename is the load-bearing source
        g.add((uri, RDF.type, cls_uri))
        # Corpus-membership marker: asserted only for real files, never inferred by closure.
        # Used by check_wikilink_targets_resolve to distinguish live nodes from
        # range-inferred ghost nodes (RDFS range on links_to would otherwise type all
        # link targets as MemoryNode, hiding dead links).
        g.add((uri, J.isCorpusNode, Literal(True)))

        # frontmatter type literal (provenance: frontmatter block)
        fm_type = (fm.get("type") or "").lower().strip()
        if fm_type:
            g.add((uri, J.primitive_hasType, Literal(fm_type)))

        # Gate: attach hook references (provenance: body:lineno)
        if cls_name == "Gate":
            hook_refs = extract_hook_refs(body)
            for (basename, _lineno) in hook_refs:
                g.add((uri, J.gate_hasHook, Literal(basename)))

    # Pass 2: edges (links_to) — wikilinks + bracket-tags
    # Build slug -> uri map for resolution
    slug_map = {slug_from_filename(p.name): node_uri(slug_from_filename(p.name)) for p in files}

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        src_slug = slug_from_filename(path.name)
        src_uri = node_uri(src_slug)
        seen_edges: set[str] = set()

        for lineno, line in enumerate(text.splitlines(), 1):
            for m in WIKILINK.finditer(line):
                tgt_slug = slug_from_link(m.group(1))
                if tgt_slug and tgt_slug not in seen_edges:
                    seen_edges.add(tgt_slug)
                    tgt_uri = node_uri(tgt_slug)
                    g.add((src_uri, J.links_to, tgt_uri))
            for m in BRACKETTAG.finditer(line):
                tgt_slug = slug_from_link(m.group(1))
                if tgt_slug and tgt_slug not in seen_edges:
                    seen_edges.add(tgt_slug)
                    tgt_uri = node_uri(tgt_slug)
                    g.add((src_uri, J.links_to, tgt_uri))

    # Apply RDFS/OWL-RL closure
    closure_method = "none"
    if OWLRL_OK:
        try:
            owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)
            closure_method = "owlrl.RDFS_Semantics"
        except Exception as exc:
            # owlrl failed — fall back
            added = rdfs_closure_fallback(g)
            closure_method = f"fallback-rdfs ({added} triples added; owlrl err: {exc})"
    else:
        added = rdfs_closure_fallback(g)
        closure_method = f"fallback-rdfs ({added} triples added)"

    g._closure_method = closure_method  # type: ignore[attr-defined]
    g._hooks_on_disk = hooks_on_disk    # type: ignore[attr-defined]
    g._files_loaded = len(files)        # type: ignore[attr-defined]
    return g


# ---------------------------------------------------------------------------
# Consistency checks (SPARQL)
# ---------------------------------------------------------------------------

def check_gate_missing_hook(g: "Graph") -> dict:
    """CHECK 1: Every Gate node must have >= 1 gate_hasHook triple pointing to a hook
    file that EXISTS on disk in ~/.claude/hooks/. A Gate without a real hook is a promise
    without enforcement — equivalent to a 'hook-gated' claim that is actually memory-only.

    Provenance basis: Gate class inferred from filename prefix + body HOOK_REF pattern.
    Hook-on-disk basis: filesystem listing of ~/.claude/hooks/*.py at check time.
    """
    hooks_on_disk = getattr(g, "_hooks_on_disk", set())

    # SPARQL: find all Gates and their hook assertions (if any)
    q = """
    PREFIX j: <urn:jarvis:>
    SELECT ?node ?hook
    WHERE {
        ?node a j:Gate .
        OPTIONAL { ?node j:gate_hasHook ?hook . }
    }
    """
    rows = list(g.query(q))

    # Group by node
    node_hooks: dict[str, list[str]] = {}
    for row in rows:
        node = str(row[0])
        hook = str(row[1]) if row[1] is not None else None
        node_hooks.setdefault(node, [])
        if hook:
            node_hooks[node].append(hook)

    violations = []
    for node_uri_str, hooks in node_hooks.items():
        slug = node_uri_str.replace("urn:jarvis:node/", "")
        missing_hook = (len(hooks) == 0)
        unregistered = [h for h in hooks if h not in hooks_on_disk]
        if missing_hook:
            violations.append({
                "node": slug,
                "kind": "gate_no_hook_triple",
                "detail": "Gate node has no gate_hasHook triple (hook name not extracted from body)",
            })
        elif unregistered:
            violations.append({
                "node": slug,
                "kind": "gate_hook_not_on_disk",
                "hooks_referenced": hooks,
                "hooks_missing_from_disk": unregistered,
                "detail": f"Gate references hook(s) not found in ~/.claude/hooks/: {unregistered}",
            })

    return {
        "check": "gate_missing_hook",
        "description": "Every Gate must have >= 1 gate_hasHook pointing to a real hook file on disk",
        "total_gates": len(node_hooks),
        "violations": violations,
        "passed": len(violations) == 0,
    }


def check_canon_not_deprecated(g: "Graph") -> dict:
    """CHECK 2: No node may be simultaneously typed Canon AND carry a primitive_hasType
    of 'deprecated' (or filename contains 'deprecated'/'archive'). A Canon node is EXALTED;
    deprecation is logically contradictory.

    Provenance: Canon class inferred from _CANON_ filename prefix; type literal from frontmatter.
    """
    q = """
    PREFIX j: <urn:jarvis:>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?node ?typeVal
    WHERE {
        ?node a j:Canon .
        ?node j:primitive_hasType ?typeVal .
        FILTER(LCASE(STR(?typeVal)) = "deprecated")
    }
    """
    rows = list(g.query(q))
    violations = [
        {"node": str(r[0]).replace("urn:jarvis:node/", ""), "type_value": str(r[1])}
        for r in rows
    ]

    # Also check for Canon nodes whose slug contains 'deprecated' or 'archive'
    q2 = """
    PREFIX j: <urn:jarvis:>
    SELECT ?node
    WHERE { ?node a j:Canon . }
    """
    for row in g.query(q2):
        slug = str(row[0]).replace("urn:jarvis:node/", "")
        if "deprecated" in slug or "archive" in slug:
            violations.append({
                "node": slug,
                "type_value": "(inferred from slug)",
                "kind": "canon_slug_implies_deprecated",
            })

    return {
        "check": "canon_not_deprecated",
        "description": "No Canon node may be simultaneously deprecated (frontmatter type=deprecated or slug implies archived)",
        "violations": violations,
        "passed": len(violations) == 0,
    }


def check_wikilink_targets_resolve(g: "Graph") -> dict:
    """CHECK 3: Every [[wikilink]] or [X·brackettag] target must resolve to a node that
    has a j:isCorpusNode marker — meaning it was extracted from a real *.md file, not
    merely inferred into existence by RDFS range closure.

    Why j:isCorpusNode and not rdf:type: the schema declares
    ``links_to rdfs:range MemoryNode``, so RDFS closure types every link target as
    MemoryNode, including dead targets that have no corresponding file. The corpus-node
    marker is asserted only in Pass 1 (file walk) and is never derivable by closure,
    so it cleanly separates real nodes from ghost nodes created by range inference.

    Provenance: edges from wikilink/brackettag extraction; existence from file listing.
    """
    q = """
    PREFIX j: <urn:jarvis:>
    SELECT DISTINCT ?src ?tgt
    WHERE {
        ?src j:links_to ?tgt .
        FILTER NOT EXISTS { ?tgt j:isCorpusNode ?any . }
    }
    """
    rows = list(g.query(q))
    violations = [
        {
            "source": str(r[0]).replace("urn:jarvis:node/", ""),
            "target": str(r[1]).replace("urn:jarvis:node/", ""),
            "kind": "dead_wikilink",
        }
        for r in rows
    ]

    return {
        "check": "wikilink_targets_resolve",
        "description": "Every linked-to node must have >= 1 rdf:type triple (i.e. exist as a file in the corpus)",
        "total_dead_links": len(violations),
        "sample_violations": violations[:10],  # cap output; full list available in graph
        "all_violations": violations,
        "passed": len(violations) == 0,
    }


def check_feedback_links_primitive(g: "Graph") -> dict:
    """CHECK 4 (bonus): Every Feedback node should link to >= 1 Primitive (or Canon, which is
    a subclass of Primitive after closure). Pure-feedback islands with no primitive anchor are
    not reachable from any principle — they are observations that never crystallised into rules.

    Note: this check is advisory (many legitimate feedbacks are standalone behavioural notes).
    Reported as violations only, not hard failures. Corpus may be clean here.
    """
    q = """
    PREFIX j: <urn:jarvis:>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?fb
    WHERE {
        ?fb a j:Feedback .
        FILTER NOT EXISTS {
            ?fb j:links_to ?target .
            { ?target a j:Primitive . } UNION { ?target a j:Canon . } UNION { ?target a j:Gate . }
        }
    }
    """
    rows = list(g.query(q))
    violations = [
        {"node": str(r[0]).replace("urn:jarvis:node/", "")}
        for r in rows
    ]
    return {
        "check": "feedback_links_primitive",
        "description": "Advisory: Feedback nodes should link to >= 1 Primitive/Canon/Gate (crystallisation check)",
        "total_feedback_islands": len(violations),
        "sample_violations": violations[:5],
        "passed": len(violations) == 0,
        "advisory": True,
    }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_checks(g: "Graph") -> list[dict]:
    return [
        check_gate_missing_hook(g),
        check_canon_not_deprecated(g),
        check_wikilink_targets_resolve(g),
        check_feedback_links_primitive(g),
    ]


def main() -> None:
    print(f"LOOP 6: Typed Knowledge + Sound Inference")
    print(f"  root       : {ROOT}")
    print(f"  schema     : {SCHEMA_TTL}")
    print(f"  rdflib     : {'ok' if RDFLIB_OK else 'MISSING — pip install rdflib'}")
    print(f"  owlrl      : {'ok' if OWLRL_OK else 'not installed (fallback active)'}")
    print(f"  yaml       : {'ok' if YAML_OK else 'not installed (minimal fallback)'}")
    print()

    if not RDFLIB_OK:
        print("ERROR: rdflib required. Run: pip install rdflib", file=sys.stderr)
        sys.exit(1)

    g = build_graph()
    print(f"  files loaded   : {g._files_loaded}")       # type: ignore[attr-defined]
    print(f"  triples (post-closure): {len(g)}")
    print(f"  closure method : {g._closure_method}")     # type: ignore[attr-defined]
    print(f"  hooks on disk  : {len(g._hooks_on_disk)}") # type: ignore[attr-defined]
    print()

    results = run_checks(g)

    real_inconsistencies = 0
    for r in results:
        status = "PASS" if r["passed"] else ("ADVISORY" if r.get("advisory") else "FAIL")
        print(f"[{status}] {r['check']}: {r['description']}")
        if not r["passed"]:
            violations = r.get("violations") or r.get("sample_violations") or []
            count = r.get("total_gates") if r["check"] == "gate_missing_hook" else None
            dead = r.get("total_dead_links")
            islands = r.get("total_feedback_islands")
            if dead is not None:
                print(f"        dead links: {dead}")
            if islands is not None:
                print(f"        feedback islands: {islands}")
            for v in violations[:5]:
                print(f"        - {v}")
            if len(violations) > 5:
                print(f"        ... and {len(violations) - 5} more")
            if not r.get("advisory"):
                real_inconsistencies += len(violations)
        print()

    print(f"Real inconsistencies caught (non-advisory): {real_inconsistencies}")
    if real_inconsistencies == 0:
        print("Corpus is sound against all non-advisory checks — checks are valid, corpus happens to be clean.")
    sys.exit(0 if real_inconsistencies == 0 else 1)


if __name__ == "__main__":
    main()
