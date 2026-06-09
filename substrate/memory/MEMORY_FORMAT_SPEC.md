# MEMORY-SPEC v1 (2026-04-21)

Format definition for memory files in this directory.

## File naming
`{type}_{slug}.md` — type ∈ {user, feedback, project, reference, primitive}

## Frontmatter (required)
```yaml
---
name: {short title}
description: {one-line, used for relevance ranking in future sessions}
type: {user|feedback|project|reference|primitive}
originSessionId: {optional, session UUID where memory was formed}
---
```

## Body conventions
- Lead with rule/fact.
- For feedback/project: `**Why:**` line + `**How to apply:**` line.
- HIERO style permitted ([P·hiero-no-prose-in-memory]) — operators, prefixes, glyph density.
- Tag: `[T·slug]` where T ∈ {U, F, P, J, R, M} matching type.

## Index
`MEMORY.md` is the index. One-line entry per memory: `- [Title](file.md) — hook`.
Index entries ≤ ~150 chars. No prose blocks.

## Warm files
`MEMORY_WARM_*.md` = topic-loaded extensions. Loaded conditionally per situation match.
