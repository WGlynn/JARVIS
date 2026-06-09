---
name: Constitutional Pipeline Scaffolding (Title-Description-First Development)
description: Methodology ⇒ write reconstructive title+description for every artifact in a production pipeline BEFORE implementing. Description = constitutional spec; implementation must satisfy named invariants. Apply across modules, functions, files, endpoints, configs.
type: primitive
originSessionId: 1b63b789-9726-4714-ba12-c4475b71d433
---
# Constitutional Pipeline Scaffolding

## ⚙ Rule
- ∀ artifact ∈ pipeline ⇒ write reconstructive title + description FIRST, implementation second
- Description = constitutional spec ⇒ implementation must satisfy each named invariant
- Layers ⇒ repos, modules, functions, files, endpoints, configs, message types, db tables, doc pages
- Composition ⇒ pipeline becomes constitution-tree ⇒ each node constrains its implementation by the words used

## 🚨 Origin — 2026-04-28 USD8 cover-score scaffolding
- Will, post-empty-repo-test articulation: *"this gives us a need potential coding patterns where we just make the title and description of countless things in a production pipeline"*
- Recognition: reconstructive descriptions don't have to be artifact-singular ⇒ apply across every node
- Description-first as a development discipline, ¬ just a description-quality test

## 🔧 How to apply
1. Identify pipeline's artifact-tree (repo → modules → functions → endpoints → ...)
2. ∀ node, write title + reconstructive description (Empty-Repo Test pass per parent primitive)
3. Description names invariant clauses ⇒ implementation must satisfy
4. Implementation comes second ⇒ review against description's clauses
5. Refactor must preserve named invariants OR explicitly retitle/redescribe (constitutional amendment)

## 📊 What changes vs. ad-hoc development

| Aspect | Ad-hoc | Constitutional |
|---|---|---|
| Code review | "Does diff look right?" | "Does diff satisfy each named invariant?" |
| Refactor guard | "Did tests pass?" | "Did refactor break any clause?" |
| Audit surface | Find issues in code | "For each clause, where is it satisfied?" |
| Onboarding | Read code | Read description tree |
| Module boundary | Intuition | "Can I write ONE reconstructive description?" → no ⇒ split |
| Renames | Cosmetic | Constitutional amendment ⇒ deliberate |

## 📍 Code-level applications
- Repo description ⇒ architecture invariants
- Module/file header ⇒ purity, side-effect scope, dependencies
- Function name + 1-line doc ⇒ what it computes (deterministic? pure? idempotent?)
- Endpoint description ⇒ API contract clauses (idempotent? authenticated? rate-limited?)
- Config key name + description ⇒ adjustable vs constitutional
- Message/event type name ⇒ semantics constraint
- DB column name + comment ⇒ what's stored, what shape is allowed

## ⚠ Anti-pattern
- Implementation first ⇒ then describe what was built ⇒ retroactive description ¬ constitutional
- Names by tree-location ¬ function ⇒ "utils.ts" ⇒ no constitutional content
- Descriptions as documentation afterthought ⇒ marketing, ¬ spec
- "Write docs later" ⇒ violates the methodology — docs ARE the spec
- Forking a name without honoring description's clauses ⇒ illegitimate-claim per parent primitive
- Vague structural words ("handles", "manages", "wraps") ⇒ no invariant content ⇒ underspec

## 🔗 Related
- `P·reconstructive-description` — parent (artifact-level rule scaled across pipeline)
- `P·augmented-governance` — Physics > Constitution > Governance ⇒ places constitutional layer at description tree
- `P·hiero-no-prose-in-memory` — same density principle at memory layer
- `F·named-protocols-are-primitives` — naming makes a protocol primitive; scales to whole pipeline

## ✓ Validation tests
- Pick any node ⇒ can someone reconstruct what it should be from title + description? ⇒ pass per parent rule
- Pick any clause in any description ⇒ is there code satisfying it? ⇒ implementation completeness
- Pick any function ⇒ does it satisfy what its name + description claim? ⇒ implementation fidelity
- Strip random files ⇒ can missing pieces be re-derived from description tree? ⇒ recoverability

## 🪝 Triggers
- Starting new project / module / file ⇒ write title+description first
- Reviewing PR ⇒ check artifacts' descriptions against the diff
- Refactoring ⇒ verify no clause silently violated
- Deciding module boundary ⇒ "ONE description?" test
- Adding a function ⇒ name + 1-line constitutional doc before body

## 📍 First instances of correct application
- USD8 cover-score scaffolding (2026-04-28): each .ts file gets reconstructive description header before implementation; each function gets one-line constitutional doc using structural-property words
