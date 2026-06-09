---
name: MarkdownCanonicalCodeAsParserLayer
description: "∀ JARVIS substrate primitive ⇒ markdown ≡ source-of-truth ¬ code. Code ≡ thin parser-layer over markdown ⇒ Python package ⇒ typed introspection ∧ graph extraction ∧ pip-installable. ✗ migrate primitives to code; ✓ wrap markdown w/ parser. LLM ≡ primary reader ⇒ prose-format ≡ structurally correct. 2026-06-09 15:28 ET Will-approval @ jarvis-substrate Python wrapper scaffold."
type: primitive
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[P·markdown-canonical-code-as-parser-layer]**

## ⚙ Principle

∀ JARVIS-substrate primitive ⇒ markdown ≡ canonical
∀ tooling ⇒ Python parser-layer over markdown ¬ migration-to-code

> Will 2026-06-09 15:28 ET: *"yes to the python module on top"*

## 🎯 Why markdown ≡ canonical

| Property | Markdown | Code |
|---|---|---|
| LLM-readable @ session-start | ✓ direct | ✗ requires AST-parse ∨ docstring-extract |
| git-diff granularity | ✓ line-level prose | ✗ class-level diff |
| edit-without-compile | ✓ any text editor | ✗ requires toolchain |
| HIERO-format compatibility | ✓ native operators | ✗ string literals only |
| cross-ref via `[F·x]` | ✓ text-link | ✗ symbol table |
| zero-stakes editability | ✓ no break-risk | ✗ syntax-error breaks |

⇒ LLM ≡ primary reader ⇒ prose-format ≡ structurally correct ¬ "just docs"

## 🎯 Why code ≡ parser-layer

∀ tooling needs:
- typed introspection ⇒ Python objects from frontmatter
- dependency-graph extraction ⇒ walk composes-with refs
- pip-installable ⇒ PyPI presence
- test-assertions ⇒ schema validation
- IDE autocomplete ⇒ primitive-ref names

⇒ thin Python module @ `jarvis/` next to `memory/` solves ALL above WITHOUT migrating substrate

## 🎯 Architecture

```
jarvis-substrate/
├── memory/          ← markdown primitives (canonical)
├── cron-prompts/    ← markdown canonicals (canonical)
├── hooks/           ← Python (executable glue, ¬ substrate)
├── scripts/         ← Python (executable glue, ¬ substrate)
├── jarvis/          ← Python parser-layer
│   ├── __init__.py
│   ├── primitive.py  ← Primitive dataclass + from_file
│   ├── registry.py   ← load_registry(root) → dict[ref, Primitive]
│   └── graph.py      ← dependency_graph + to_dot
└── pyproject.toml   ← pip install jarvis-substrate
```

⇒ source-of-truth ¬ moves; tooling layer added on top

## 🪝 Triggers

- ∀ "should substrate be code?" critique ⇒ apply this primitive
- ∀ tooling request (graph extraction, type-check, package) ⇒ extend parser-layer ¬ migrate primitives
- ∀ new substrate addition ⇒ add as markdown; parser auto-discovers ∀ next import
- ∀ Steelman-2 "this is just docs" reader-confusion ⇒ point at parser-layer + README clarification

## ✗ Anti-patterns

- ✗ migrate primitive frontmatter to Python class definitions ⇒ breaks LLM-readability
- ✗ duplicate substrate in code (write same rule in both Python ∧ markdown) ⇒ drift-risk + maintenance-burden
- ✗ parser-layer accumulates business-logic ⇒ scope-creep; keep parser THIN
- ✗ declare "we need to be more like real code" w/o threat-model ⇒ first-available-trap

## ✓ Composes-with

- [P·structure-does-the-work] ⇐ markdown-as-canonical IS structural; tooling doesn't change substrate
- [P·pre-decentralization-optimization-sequencing] ⇐ zero-stakes phase = optimize-readability not packaging
- [P·first-available-trap] ⇐ "real code" critique IS first-available-trap; markdown-as-substrate is threat-model-fit
- [F·odysseus-as-advisory-substrate] ⇐ Steelman-2 from Odysseus advisory pattern surfaced this need
- [F·primitive-capture-vs-execution-throughput] ⇐ this primitive was a missed-capture from the Python-wrapper scaffolding turn

## 📦 Receipts

- 15:28 ET ⇐ Will: *"should it be code instead of markdown files?"*
- 15:28 ET ⇒ agent-answer: hybrid (markdown canonical + Python parser-layer)
- 15:28 ET ⇐ Will: *"yes to the python module on top"*
- 15:35 ET ⇒ jarvis/ package scaffolded: 3 modules + pyproject.toml + tested (9 primitives ⇒ 9 edges)
- 15:36 ET ⇒ pushed to WGlynn/jarvis-substrate commit 11b57b6
- 15:41 ET ⇒ this primitive saved (per [F·primitive-capture-vs-execution-throughput] sweep)
