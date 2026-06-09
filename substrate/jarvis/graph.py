"""Dependency graph derived from `composes-with` references."""
from __future__ import annotations

from jarvis.primitive import Primitive


def dependency_graph(
    registry: dict[str, Primitive],
) -> dict[str, list[str]]:
    """Return adjacency: {ref: [refs it composes with that exist in registry]}.

    Dangling references (composes-with a primitive that doesn't exist in
    the loaded registry) are silently dropped. This is intentional:
    cross-references to local-only primitives don't appear in the public
    substrate by design.
    """
    return {
        ref: [r for r in p.composes_with if r in registry and r != ref]
        for ref, p in registry.items()
    }


def to_dot(graph: dict[str, list[str]], title: str = "jarvis-substrate") -> str:
    """Emit a graphviz DOT representation of the dependency graph."""
    lines = [f'digraph "{title}" {{', '  rankdir=LR;', '  node [shape=box];']
    for node, edges in sorted(graph.items()):
        lines.append(f'  "{node}";')
        for tgt in sorted(edges):
            lines.append(f'  "{node}" -> "{tgt}";')
    lines.append("}")
    return "\n".join(lines)
