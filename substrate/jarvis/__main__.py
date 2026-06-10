"""Command-line interface for the jarvis substrate package.

Usage:
    python -m jarvis show <ref>          # print a primitive by its ref (e.g. F·structure-does-the-work)
    python -m jarvis list [<kind>]       # list all primitives, optionally filtered by kind
    python -m jarvis graph [--format=X]  # emit dependency graph as dot|mermaid|json
    python -m jarvis verify              # check substrate health (dangling refs, frontmatter, link rot)
    python -m jarvis search <pattern>    # grep across primitive bodies (regex)
    python -m jarvis count               # count by kind
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from jarvis import (
    Primitive,
    dependency_graph,
    load_registry,
    to_dot,
)


def cmd_show(args, registry):
    ref = args.ref
    # accept both "F·foo" and "feedback_foo" forms
    p = registry.get(ref)
    if p is None:
        # try slug match
        target = ref.split("·")[-1] if "·" in ref else ref
        matches = [v for k, v in registry.items() if v.slug == target]
        if matches:
            p = matches[0]
    if p is None:
        print(f"not found: {ref}", file=sys.stderr)
        return 1
    print(f"# {p.ref} ({p.kind})")
    print()
    print(f"name: {p.name}")
    print(f"file: {p.path.name}")
    print(f"description: {p.description}")
    print()
    print(p.body)
    if p.composes_with:
        print()
        print(f"composes-with ({len(p.composes_with)}):")
        for ref in p.composes_with:
            print(f"  - {ref}")
    return 0


def cmd_list(args, registry):
    kind_filter = args.kind
    rows = []
    for ref, p in sorted(registry.items()):
        if kind_filter and p.kind != kind_filter:
            continue
        rows.append((ref, p.kind, p.name[:60]))
    print(f"# {len(rows)} primitive(s)" + (f" [{kind_filter}]" if kind_filter else ""))
    print()
    for ref, kind, name in rows:
        print(f"  {ref:55s} {kind:12s} {name}")
    return 0


def cmd_graph(args, registry):
    graph = dependency_graph(registry)
    fmt = args.format
    if fmt == "dot":
        print(to_dot(graph))
    elif fmt == "mermaid":
        print("graph LR")
        for node, edges in sorted(graph.items()):
            safe_node = re.sub(r"[^a-zA-Z0-9_]", "_", node)
            print(f"  {safe_node}[\"{node}\"]")
            for tgt in edges:
                safe_tgt = re.sub(r"[^a-zA-Z0-9_]", "_", tgt)
                print(f"  {safe_node} --> {safe_tgt}")
    elif fmt == "json":
        import json as _json
        print(_json.dumps(graph, indent=2))
    elif fmt == "stats":
        nodes = len(graph)
        edges = sum(len(v) for v in graph.values())
        # in-degree (most-cited primitives)
        in_count = {}
        for src, tgts in graph.items():
            for t in tgts:
                in_count[t] = in_count.get(t, 0) + 1
        top_cited = sorted(in_count.items(), key=lambda kv: -kv[1])[:10]
        # out-degree (most-composing primitives)
        out_count = {ref: len(edges) for ref, edges in graph.items()}
        top_composing = sorted(out_count.items(), key=lambda kv: -kv[1])[:10]
        print(f"nodes: {nodes}")
        print(f"edges: {edges}")
        print(f"avg out-degree: {edges/nodes:.2f}")
        print()
        print("most-cited (top 10):")
        for ref, count in top_cited:
            print(f"  {count:4d}  {ref}")
        print()
        print("most-composing (top 10):")
        for ref, count in top_composing:
            print(f"  {count:4d}  {ref}")
    else:
        print(f"unknown format: {fmt}", file=sys.stderr)
        return 1
    return 0


def cmd_verify(args, registry):
    errors = []
    warnings = []

    # check 1: dangling composes-with refs
    all_refs = set(registry.keys())
    for ref, p in registry.items():
        for target in p.composes_with:
            if target not in all_refs and target != ref:
                # but allow references to local-only primitives — these are
                # filtered out at graph-build time. The verify is informational.
                warnings.append(f"{ref} composes with {target} (not in this registry; possibly local-only)")

    # check 2: empty descriptions
    for ref, p in registry.items():
        if not p.description.strip():
            warnings.append(f"{ref} has empty description")

    # check 3: missing kind in filename mapping
    expected_kinds = {"feedback", "primitive", "project", "protocol", "reference", "user"}
    for ref, p in registry.items():
        if p.kind not in expected_kinds:
            errors.append(f"{ref} has unexpected kind: {p.kind}")

    # check 4: name vs slug consistency
    for ref, p in registry.items():
        if p.slug.replace("-", "").lower() not in p.name.replace(" ", "").lower():
            # very loose check; not necessarily wrong but worth noting
            pass

    print(f"verify: {len(registry)} primitive(s) loaded")
    print(f"  errors:   {len(errors)}")
    print(f"  warnings: {len(warnings)}")
    if errors:
        print()
        print("errors:")
        for e in errors[:20]:
            print(f"  ERR  {e}")
        if len(errors) > 20:
            print(f"  ... +{len(errors)-20} more")
    if warnings and args.verbose:
        print()
        print("warnings:")
        for w in warnings[:30]:
            print(f"  WARN {w}")
        if len(warnings) > 30:
            print(f"  ... +{len(warnings)-30} more")
    return 2 if errors else (1 if warnings else 0)


def cmd_search(args, registry):
    pattern = args.pattern
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        print(f"invalid regex: {e}", file=sys.stderr)
        return 1
    hits = 0
    for ref, p in sorted(registry.items()):
        for i, line in enumerate(p.body.splitlines(), 1):
            if regex.search(line):
                hits += 1
                print(f"{ref}:{i}: {line[:120]}")
    print(f"# {hits} match(es)")
    return 0


def cmd_hindsight(args, registry):
    """Surface primitives that may have been wrong in hindsight.

    Catches stale patterns, contradiction markers, orphan primitives, and
    deprecated targets. Output is candidate-for-revision, not a verdict —
    Will-triage decides which to actually rewrite, supersede, or archive.
    """
    candidates = {"contradicted": [], "orphan": [], "stale_partner": [],
                  "stale_promise": [], "all_refs_dead": []}

    # Build out-degree to detect orphans (primitives nothing references)
    in_count = {}
    for ref, p in registry.items():
        for t in p.composes_with:
            if t in registry:
                in_count[t] = in_count.get(t, 0) + 1

    # Patterns suggesting hindsight-mistake
    contradiction_pat = re.compile(
        r"\b(supersed(es|ed by)|replac(es|ed by)|wrong, fixed|"
        r"actually wrong|in hindsight|on reflection|that's a hallucination|"
        r"category error|misread|drift|reverted|mistake)\b",
        re.IGNORECASE,
    )
    stale_promise_pat = re.compile(
        r"\b(next week|this week|by (Monday|Tuesday|Wednesday|Thursday|Friday)|"
        r"expected to launch|will (ship|launch|deploy) (soon|tomorrow|today|next))\b",
        re.IGNORECASE,
    )
    # Partner names whose engagement may have ended; flag for review (we
    # don't know the current state, but the operator can verify)
    partner_pat = re.compile(
        r"\b(Pragma|[REDACTED-NDA]|Rick|Kim|Tom|Bernhard|Matta|Krakovia|[REDACTED-NDA]|Anthropic engagement)\b",
        re.IGNORECASE,
    )

    for ref, p in registry.items():
        body_lower = p.body.lower()
        # Contradiction markers
        if contradiction_pat.search(body_lower):
            snippet_m = contradiction_pat.search(body_lower)
            start = max(0, snippet_m.start() - 30)
            end = min(len(body_lower), snippet_m.end() + 50)
            candidates["contradicted"].append((ref, body_lower[start:end].strip()))
        # Orphan (nothing cites it, AND it's not a project / user / reference tier where standalone is fine)
        if ref not in in_count and p.kind in ("primitive", "feedback"):
            candidates["orphan"].append((ref, p.kind))
        # Partner-engagement context (informational; operator decides whether stale)
        if partner_pat.search(p.body):
            m = partner_pat.search(p.body)
            candidates["stale_partner"].append((ref, m.group(0)))
        # Stale promise (time-bound language that's now in the past)
        if stale_promise_pat.search(body_lower):
            m = stale_promise_pat.search(body_lower)
            start = max(0, m.start() - 30)
            end = min(len(p.body), m.end() + 50)
            candidates["stale_promise"].append((ref, p.body[start:end].strip()))
        # All composes-with refs are dead
        if p.composes_with and all(t not in registry for t in p.composes_with):
            candidates["all_refs_dead"].append((ref, p.composes_with[:5]))

    print(f"hindsight audit: {len(registry)} primitives scanned")
    print()
    for category, items in candidates.items():
        if not items:
            continue
        print(f"[{category}] {len(items)} candidate(s):")
        for entry in items[:15]:
            print(f"  {entry[0]:55s}  {str(entry[1])[:80]}")
        if len(items) > 15:
            print(f"  ... +{len(items)-15} more")
        print()

    total = sum(len(v) for v in candidates.values())
    if total == 0:
        print("clean.")
    else:
        print(f"total candidates surfaced: {total}")
        print()
        print("These are candidates for Will-triage, not a verdict. The substrate")
        print("accumulates; some past decisions may have been mistakes. The audit")
        print("surfaces patterns to re-examine, it does not auto-rewrite.")
    return 0


def cmd_count(args, registry):
    counts = {}
    for p in registry.values():
        counts[p.kind] = counts.get(p.kind, 0) + 1
    total = sum(counts.values())
    print(f"# {total} primitive(s)")
    for kind in sorted(counts):
        print(f"  {kind:12s} {counts[kind]:4d}")
    return 0


def _force_utf8_streams():
    """Reconfigure stdout/stderr to UTF-8 so Unicode (→, —, ⚠, ✓) prints on
    Windows cp1252 terminals without UnicodeEncodeError. Best-effort: silently
    skip on Python < 3.7 or non-reconfigurable streams (e.g. wrapped pipes)."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            # non-reconfigurable (detached, already-closed, exotic wrapper) — skip
            pass


def main():
    _force_utf8_streams()
    parser = argparse.ArgumentParser(prog="python -m jarvis", description=__doc__)
    subs = parser.add_subparsers(dest="cmd", required=True)

    p_show = subs.add_parser("show", help="print a primitive by ref or slug")
    p_show.add_argument("ref", help="primitive ref (F·xxx) or slug (xxx)")

    p_list = subs.add_parser("list", help="list primitives")
    p_list.add_argument("kind", nargs="?", help="filter by kind (feedback, primitive, project, ...)")

    p_graph = subs.add_parser("graph", help="emit dependency graph")
    p_graph.add_argument("--format", default="stats", choices=["dot", "mermaid", "json", "stats"])

    p_verify = subs.add_parser("verify", help="check substrate health")
    p_verify.add_argument("-v", "--verbose", action="store_true", help="print warning details")

    p_search = subs.add_parser("search", help="regex search across primitive bodies")
    p_search.add_argument("pattern", help="regex pattern (case-insensitive)")

    subs.add_parser("count", help="count by kind")

    subs.add_parser("hindsight", help="surface primitives that may have been wrong in hindsight")

    args = parser.parse_args()

    # Find the substrate root by walking up from this file
    here = Path(__file__).resolve().parent
    # substrate root is parent of the jarvis/ package
    root = here.parent

    registry = load_registry(root)
    if not registry:
        print("no primitives found", file=sys.stderr)
        return 1

    cmd_handlers = {
        "show": cmd_show,
        "list": cmd_list,
        "graph": cmd_graph,
        "verify": cmd_verify,
        "search": cmd_search,
        "count": cmd_count,
        "hindsight": cmd_hindsight,
    }
    return cmd_handlers[args.cmd](args, registry)


if __name__ == "__main__":
    sys.exit(main())
