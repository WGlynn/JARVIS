"""Command-line interface for the jarvis substrate package.

Usage:
    python -m jarvis show <ref>          # print a primitive by its ref (e.g. F·structure-does-the-work)
    python -m jarvis list [<kind>]       # list all primitives, optionally filtered by kind
    python -m jarvis graph [--format=X]  # emit dependency graph as dot|mermaid|json
    python -m jarvis verify              # check substrate health (dangling refs, frontmatter, link rot)
    python -m jarvis search <pattern>    # grep across primitive bodies (regex)
    python -m jarvis count               # count by kind
    python -m jarvis hindsight [--pairwise]  # single-file markers | cross-file opposing directives
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

    With --pairwise, runs the cross-file opposing-directive scan instead
    (closes the found-by-coincidence limitation noted below).
    """
    if args.pairwise:
        return _hindsight_pairwise(args, registry)

    candidates = {"contradicted": [], "orphan": [], "stale_partner": [],
                  "stale_promise": [], "all_refs_dead": []}

    # Build out-degree to detect orphans (primitives nothing references)
    in_count = {}
    for ref, p in registry.items():
        for t in p.composes_with:
            if t in registry:
                in_count[t] = in_count.get(t, 0) + 1

    # Relational contradiction markers only — bare correction-genre lexemes
    # (drift, mistake, misread, ...) were the 7/10 FP root cause in the
    # 2026-06-11 triage; a primitive ABOUT mistakes is not itself mistaken.
    # The found-by-coincidence limitation (regex only catches contradictions
    # that self-declare) is closed by `hindsight --pairwise` below.
    contradiction_pat = re.compile(
        r"(\bsuperseded[ -]by\b|\breplaced by\b|\binvalidated[_ ]by\b|"
        r"\bcontradicts\b|\breverted\b|\bno longer true\b|outdated:)",
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
        # Contradiction markers — exempt quoted Will-corrections (lines
        # starting with > *"), which cite a correction without being one.
        scan_lower = "\n".join(
            ln for ln in body_lower.splitlines()
            if not ln.lstrip().startswith('> *"')
        )
        snippet_m = contradiction_pat.search(scan_lower)
        if snippet_m:
            start = max(0, snippet_m.start() - 30)
            end = min(len(scan_lower), snippet_m.end() + 50)
            candidates["contradicted"].append((ref, scan_lower[start:end].strip()))
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


# Tokens that are corpus-furniture, not topic signal. Polarity markers
# (always/never/must) live here too — they mark a directive, they are not
# its object, so they must not count toward object-token overlap.
_PAIRWISE_STOPWORDS = frozenset((
    "about", "above", "after", "again", "also", "always", "another",
    "because", "been", "before", "being", "between", "both", "claude",
    "could", "does", "doing", "down", "during", "each", "either", "entry",
    "even", "ever", "every", "file", "from", "have", "having", "here",
    "instead", "into", "itself", "just", "like", "memory", "more", "most",
    "must", "never", "only", "onto", "other", "over", "primitive", "rule",
    "same", "should", "side", "some", "still", "such", "than", "that",
    "their", "them", "then", "there", "these", "they", "thing", "this",
    "those", "through", "under", "until", "upon", "very", "wait", "were",
    "what", "when", "where", "which", "while", "will", "with", "within",
    "without", "would", "your",
))

# Mandate directives: "always X", "∀ X ⇒/→/->", "push every commit", MUST,
# "✓ Y". Counter directives: "don't X", "do not X", "never X", "¬ X",
# "✗ Y", "every ~N" (throttle). A contradiction is a mandate in one file
# whose object tokens overlap a counter in another.
_MANDATE_PAT = re.compile(
    # ✓ only in endorsement position (line start, list marker, ⇒/→/:) —
    # table-cell ✓ is a status mark, not a directive. don[’']?t(?!-) on
    # the counter side keeps slug refs ([F·dont-default-...]) from firing.
    r"(?i:\balways\b)|∀[^\n⇒→]{0,60}(?:⇒|→|->)|\bMUST\b|"
    r"(?i:\b(?:push|commit|sync|update|run)\s+every\b)|"
    r"(?:^\s*|[⇒→:]\s*|[-*+]\s+)✓"
)
_COUNTER_PAT = re.compile(
    # ¬/✗ only in prohibition position (line start, after a list marker,
    # or after ⇒/→/:) — hiero uses mid-clause ¬ as contrastive "rather
    # than" ("hook ¬ memory-suggestion"), trailing ✗ as a verdict, and
    # table-cell ✗ as a status mark; none is a directive. 2026-06-11
    # calibration: whole-line tokens + bare markers = 614 pairs; windowed
    # objects + positional markers brought it under review threshold.
    r"(?i:\bnever\b|\bdon[’']?t\b(?!-)|\bdo not\b|\bevery\s+~?\d)|"
    r"(?:^\s*|[⇒→:]\s*|[-*+]\s+)[¬✗]"
)


def _topic_tokens(text):
    """Lowercase topic tokens: alpha-led, length > 3, stopword-stripped,
    crude plural-strip so commit/commits land in the same bucket."""
    tokens = set()
    for tok in re.findall(r"[a-z][a-z0-9]{3,}", text.lower()):
        if len(tok) > 4 and tok.endswith("s") and not tok.endswith("ss"):
            tok = tok[:-1]
        if tok not in _PAIRWISE_STOPWORDS:
            tokens.add(tok)
    return tokens


def _object_tokens(line, pat):
    """Object tokens of a directive: tokens within 30 chars after each
    polarity-marker match, unioned. ∀⇒ and ✗ are ubiquitous in hiero
    notation — whole-line tokens were the 614-pair FP root cause in the
    2026-06-11 calibration; the directive's object lives next to its
    marker ("don't push every commit"), not anywhere on the line."""
    tokens = set()
    for m in pat.finditer(line):
        tokens |= _topic_tokens(line[m.start():m.end() + 30])
    return tokens


def _invalidated_by(p):
    """Return the primitive's `invalidated_by:` frontmatter value
    (lowercased), or "". Primitive doesn't carry arbitrary frontmatter,
    so re-read the file the same way Primitive.from_file splits it."""
    try:
        _, fm, _ = p.path.read_text(encoding="utf-8").split("---", 2)
    except (ValueError, OSError):
        return ""
    for line in fm.strip().splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "invalidated_by":
            return value.strip().lower()
    return ""


def _opposing_lines(dir_a, dir_b, shared_topics):
    """First (line_a, line_b) where one file mandates what the other
    counters: object-token overlap >= 2 AND the overlap touches the pair's
    shared topic (keeps 'always X about apples' from colliding with
    'never Y about oranges' on incidental tokens)."""
    for pos_lines, neg_lines, swapped in (
        (dir_a[0], dir_b[1], False),
        (dir_b[0], dir_a[1], True),
    ):
        for line_p, toks_p in pos_lines:
            for line_n, toks_n in neg_lines:
                if line_p == line_n:
                    continue  # shared boilerplate, not a contradiction
                overlap = toks_p & toks_n
                if len(overlap) >= 2 and overlap & shared_topics:
                    return (line_n, line_p) if swapped else (line_p, line_n)
    return None


def _hindsight_pairwise(args, registry):
    """Cross-file contradiction scan.

    1. tokenize slug + title + frontmatter description into topic tokens
    2. bucket pairs sharing >= 2 topic tokens (commit+push, boot+session)
    3. within a bucket, flag pairs where a mandate line in one file shares
       object tokens with a counter line in the other
    4. exempt pairs already resolved via invalidated_by frontmatter, and
       quoted lines (citing a directive is not issuing one)

    Positive control (run with --include-resolved): atomic-commit-pacing
    vs commit-cadence-restore-2026-04-21 (push-per-commit vs push-every-~10).
    """
    refs = sorted(registry)

    # topic tokens per primitive (slug split on hyphens — CamelCase names
    # like AtomicCommitPacing don't tokenize on their own)
    topics = {}
    for ref in refs:
        p = registry[ref]
        topics[ref] = _topic_tokens(
            f"{p.slug.replace('-', ' ')} {p.name} {p.description}"
        )

    # bucket via inverted index; tokens in >40 files are corpus-generic
    # noise, not topic signal
    by_token = {}
    for ref in refs:
        for t in topics[ref]:
            by_token.setdefault(t, []).append(ref)
    pair_shared = {}
    for t, members in by_token.items():
        if len(members) > 40:
            continue
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                pair_shared[(a, b)] = pair_shared.get((a, b), 0) + 1
    buckets = sorted(pair for pair, n in pair_shared.items() if n >= 2)

    # directive lines per primitive — skip quoted lines (> *"...) and
    # lines without >= 2 object tokens (nothing to overlap on)
    directives = {}
    for ref in refs:
        pos, neg = [], []
        for line in registry[ref].body.splitlines():
            stripped = line.strip()
            # quoted lines cite a directive without issuing one; headings
            # name a topic ("# Context Is ALWAYS Load-Bearing"), same deal
            if stripped.startswith((">", "#")):
                continue
            if _MANDATE_PAT.search(line):
                toks = _object_tokens(line, _MANDATE_PAT)
                if len(toks) >= 2:
                    pos.append((stripped, toks))
            if _COUNTER_PAT.search(line):
                toks = _object_tokens(line, _COUNTER_PAT)
                if len(toks) >= 2:
                    neg.append((stripped, toks))
        directives[ref] = (pos, neg)

    flagged = []
    exempted = 0
    for a, b in buckets:
        pa, pb = registry[a], registry[b]
        if not args.include_resolved:
            inv_a, inv_b = _invalidated_by(pa), _invalidated_by(pb)
            if (inv_a and pb.slug in inv_a) or (inv_b and pa.slug in inv_b):
                exempted += 1
                continue
        hit = _opposing_lines(directives[a], directives[b], topics[a] & topics[b])
        if hit:
            flagged.append((a, b, hit[0], hit[1]))

    print(f"hindsight pairwise: {len(refs)} primitives, "
          f"{len(buckets)} bucketed pair(s) scanned")
    print()
    for a, b, line_a, line_b in flagged:
        print(f"[pair] {a} <-> {b}")
        print(f"  {registry[a].path.name}: {line_a[:110]}")
        print(f"  {registry[b].path.name}: {line_b[:110]}")
        print()
    if exempted:
        print(f"exempted {exempted} resolved pair(s) via invalidated_by "
              f"(--include-resolved to show)")
    if not flagged:
        print("clean.")
    else:
        print(f"total contradiction pair(s): {len(flagged)}")
        print()
        print("These are candidates for Will-triage, not a verdict. A flagged")
        print("pair issues opposing directives about the same objects; resolve")
        print("by superseding one (invalidated_by frontmatter) or reconciling.")
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

    p_hind = subs.add_parser("hindsight", help="surface primitives that may have been wrong in hindsight")
    p_hind.add_argument("--pairwise", action="store_true",
                        help="cross-file opposing-directive scan (mandate in one file vs counter in another)")
    p_hind.add_argument("--include-resolved", action="store_true",
                        help="disable the invalidated_by exemption (calibration / positive control)")
    p_hind.add_argument("--root", help="alternate corpus root (dir containing memory/, or the memory/ dir itself)")

    args = parser.parse_args()

    # Find the substrate root by walking up from this file
    here = Path(__file__).resolve().parent
    # substrate root is parent of the jarvis/ package
    root = here.parent
    if getattr(args, "root", None):
        root = Path(args.root)
        if root.name == "memory":  # accept the memory/ dir itself
            root = root.parent

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
