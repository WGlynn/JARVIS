"""Typed Primitive object parsed from a markdown file."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


COMPOSES_REF = re.compile(r"\[([PFJOMRU])·([a-zA-Z0-9\-]+)\]")
SLUG_FROM_FILENAME = re.compile(
    r"^(feedback|primitive|project|protocol|reference|user|memory)_([a-zA-Z0-9\-]+)\.md$"
)
KIND_LETTER = {
    "feedback": "F",
    "primitive": "P",
    "project": "J",
    "protocol": "O",
    "reference": "R",
    "user": "U",
    "memory": "M",
}


@dataclass
class Primitive:
    """One memory primitive parsed from a markdown file.

    Frontmatter fields (name, description, type) are required.
    `composes_with` is extracted by scanning the body for [P/F/J/O/R/U]
    bracketed references.
    """

    path: Path
    name: str
    description: str
    kind: str  # feedback | primitive | project | protocol | reference | user
    body: str
    composes_with: list[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        m = SLUG_FROM_FILENAME.match(self.path.name)
        return m.group(2) if m else self.path.stem

    @property
    def ref(self) -> str:
        return f"{KIND_LETTER.get(self.kind, '?')}·{self.slug}"

    @classmethod
    def from_file(cls, path: Path) -> "Primitive":
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            raise ValueError(f"{path}: no frontmatter")
        _, fm, body = text.split("---", 2)
        meta = _parse_frontmatter(fm)
        composes = sorted({f"{k}·{s}" for k, s in COMPOSES_REF.findall(body)})
        return cls(
            path=path,
            name=meta.get("name", path.stem),
            description=meta.get("description", "").strip().strip('"').strip("'"),
            kind=meta.get("type", "feedback"),
            body=body.strip(),
            composes_with=composes,
        )


def _parse_frontmatter(fm: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in fm.strip().splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out
