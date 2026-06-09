"""Discover and index all primitives in the substrate."""
from __future__ import annotations

from pathlib import Path

from jarvis.primitive import Primitive


def load_registry(root: Path | str | None = None) -> dict[str, Primitive]:
    """Scan `memory/` under `root` and return {primitive.ref: Primitive}.

    `root` defaults to the repo root inferred from this file's location.
    """
    if root is None:
        root = Path(__file__).resolve().parent.parent
    root = Path(root)
    memory = root / "memory"
    if not memory.is_dir():
        raise FileNotFoundError(f"no memory/ under {root}")

    registry: dict[str, Primitive] = {}
    for path in sorted(memory.glob("*.md")):
        try:
            p = Primitive.from_file(path)
        except ValueError:
            continue
        registry[p.ref] = p
    return registry
