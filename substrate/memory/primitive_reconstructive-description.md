---
name: Reconstructive Description (Empty-Repo Test)
description: Descriptions/names/specs must be dense enough that the artifact could be reconstructed from the words alone. Test ⇒ if artifact ∅, can reader rebuild what should be there from description-words?
type: primitive
originSessionId: 1b63b789-9726-4714-ba12-c4475b71d433
---
# Reconstructive Description / Empty-Repo Test

## ⚙ Rule
- Description = spec ⇒ density gate
- Test: if artifact ∅, reader could reconstruct *what should be there* from description-words alone
- Pass ⇒ description doing real work
- Fail ⇒ description decorative ⇒ underspecified

## 🚨 Origin — 2026-04-28 USD8 cover-score repo description
- Will picked: *"Cover Score algorithm for USD8. Open-source, deterministic, locally-verifiable."*
- *"even if i just left it as is as an empty repo, someone could reconstruct the idea on the description alone. basically saying what should be ther [there]"*
- 4 load-bearing words ⇒ "algorithm" (function) ∧ "open-source" (access posture) ∧ "deterministic" (correctness) ∧ "locally-verifiable" (trust model)
- DeFi-context reader can derive whole architecture from these 4 words

## 🔧 How to apply
- Subject artifacts ⇒ repo descriptions, package descriptions, commit subjects, function names, file names, doc subtitles, variable names
- Strip ⇒ marketing adjectives ("amazing", "powerful", "modern", "best-in-class", "next-generation")
- Keep ⇒ structural-property words ("deterministic", "open-source", "permissionless", "lazy", "local", "idempotent")
- Each kept word ⇒ one a reconstructor would NEED to know to build the right thing

## 📊 Pass / fail examples
- ✓ "Cover Score algorithm for USD8. Open-source, deterministic, locally-verifiable." ⇒ rebuild possible from words
- ✓ "Lazy attestation history compression with optimistic dispute" ⇒ architecture extractable
- ✗ "USD8's modern decentralized score engine, designed for the next generation of stablecoins" ⇒ marketing words, ∅-rebuild impossible
- ✗ "Cover Score for USD8" ⇒ underspecified — function named, architecture absent (open-source? trust model? deterministic?)

## 🪝 Triggers
- Drafting description / name / commit subject / repo title
- Reviewing existing descriptions
- Picking between candidate options ⇒ reach for the one passing empty-repo test ¬ "sounds better"

## ⚠ Anti-pattern
- "X for Y" with no architectural words ⇒ underspec
- Brand-adjective stuffing (modern, powerful, decentralized-as-buzzword) ⇒ marketing ¬ spec
- Assuming reader will open the README ⇒ description must stand alone
- Descriptions that fail HIERO compression ⇒ likely fail this test too (sibling property)

## 🔗 Related
- `P·hiero-no-prose-in-memory` — HIERO compresses prose to logic-primitive; same density gate at memory-write level
- `P·symbolic-compression` — glyph-native canon; reconstructive density principle
- `P·substrate-geometry-match` — description SHAPE matches artifact SHAPE (architecture-words for architectural artifacts)
- `F·named-protocols-are-primitives` — naming a protocol makes it reconstructable from the name; same family

## 📍 Code-level applications
- Repo description → reconstruct architecture
- Function name → reconstruct what it computes
- File name → reconstruct what it contains
- Commit subject → reconstruct what changed
- Variable name → reconstruct what it represents
- Component prop name → reconstruct its role in the parent

## ✓ Validation tests
- Strip the artifact; can a competent reader rebuild it from the description? ⇒ pass if yes
- Hand description to someone who's never seen the artifact; do they expect the right shape? ⇒ pass if yes
- Compare 2 candidates; which would a reconstructor pick? ⇒ denser one wins

## 🏛 Constitutional reading — Will, 2026-04-28

> *"that primitive is reflective of constitutionality or code is law on a whole new level. i just stated simply the minimal requirements needed met to fit into this box."*

Reconstructive descriptions function as **constitutional clause sets**. When written with empty-repo-test density:
- Each kept word = an invariant clause
- Any implementation claiming to be the artifact must honor each clause
- Violation = illegitimate-claim, regardless of who shipped the violating version

### Mapping to augmented-governance hierarchy (`P·augmented-governance`)

- **Physics** ⇒ math (Shapley axioms, deterministic semantics, ECDSA verification): can't be voted against
- **Constitution** ⇒ reconstructive description (the named invariants): what any implementation must honor to legitimately bear the name
- **Governance** ⇒ parameters (weights, registry, bond size): free within Physics ∩ Constitution

The act of writing a reconstructive description IS constitutional design. Minimum-requirements framing = constitutional framing — same act, different lens.

### Fork-test (validation)
- Fork removes a named invariant ⇒ fork is illegitimate-claim
- Example: USD8 cover-score fork closed-sources the algo ⇒ violates "open-source" ⇒ no longer "Cover Score for USD8" by the description's constitutional reading
- Example: fork adds non-deterministic step ⇒ violates "deterministic" ⇒ illegitimate
- Example: fork requires proprietary/hosted verifier ⇒ violates "locally-verifiable" ⇒ illegitimate
- Example: fork swaps qualifying-token registry ⇒ no clause violated ⇒ still legitimate (lives in governance space)

### Code-is-law extension
- Bytecode-is-law constrains what code does
- Description-is-law constrains what code is *allowed to be* if it bears the name
- Same enforcement principle, applied one layer above the bytecode — at the spec/title layer
- The naming itself becomes load-bearing: "Cover Score for USD8" isn't a label, it's a contract
