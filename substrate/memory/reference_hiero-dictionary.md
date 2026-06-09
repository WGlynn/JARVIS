---
name: HIERODictionary
description: 2026-05-04 — canonical HIERO format dictionary. Operators, prefixes, sections, idioms. Capstone of JARVIS — converts personal compression scheme to public protocol via published dictionary.
type: reference
originSessionId: f5377dec-4447-4d25-8838-009c9a8f663a
---
**Source-of-truth paper**: `papers/hiero.md` (mirrored: Desktop/JARVIS-repo/vibeswap-docs).

**Layer 1 — Universal operators** (math/logic notation):
- `∀` for all / every | `∃` exists / some | `⇒` implies / triggers | `⇔` iff
- `∧` and | `∨` or | `¬` not | `⊥` forbidden | `⊤` always-permitted
- `→` transitions to | `↦` maps to | `✓` valid | `✗` invalid | `⊘` null / prohibited
- `↑` `↓` increase / decrease | `∈` `∉` member / not | `⊆` `⊂` subset / proper subset
- `×` combination | `≥` `≤` `≠` `≡` `≈` comparison

**Layer 2 — File-type prefixes** (filename + cross-ref):
- `P·` primitive (`primitive_<name>.md`)
- `F·` feedback (`feedback_<name>.md`)
- `J·` project (`project_<name>.md`)
- `U·` user-context (`user_<name>.md`)
- `R·` reference (`reference_<name>.md`)
- `O·` protocol (`protocol_<name>.md`)
- `M·` generic (no prefix)

Cross-refs use `[Name](type·slug)` pattern. Audit script flags orphans.

**Layer 3 — Section markers** (MEMORY.md taxonomy):
- `[PRE-FLIGHT]` load before any work; violations irreversible
- `[BOOT]` identity, paths
- `[META-PRINCIPLE]` load-bearing above situation rules
- `[POST-HOC:HOT]` always-applicable rules
- `[POST-HOC:WARM-MAP]` situation-conditional warm load
- `[ACTIVE]` current posture
- `[PING]` always-on notifications
- `[TOKENOMICS]` monetary framing

**Small-caps category markers** (within longer files):
- `⟳ᴛʀᴘ` `⟳ɪɴᴛ` `⟳ɢᴏᴠ` `⟳ʀᴇᴠ` `⟳ᴍᴇᴛʜ` `⟳sᴇʟғ` etc.
- Pattern: `⟳<3-letter category in small caps>`

**Frontmatter convention** (every memory file):
```
---
name: <CamelCaseName>
description: <one-line; matched by auto-loader>
type: <primitive | feedback | project | user | reference | protocol>
originSessionId: <optional UUID; lineage trace>
---
```
- `originSessionId` ⇒ added 2026-05-19 era. Optional but corpus-dominant on new writes. Traces primitive ⇒ originating session.

**Layer 4 — Recurring idioms**:
- `pattern × N+ ⇒ surface candidate` — counting threshold for crystallization
- `∀ X ⇒ check Y FIRST` — precondition rule
- `path-X ⊥ ⇒ replace w/ Y` — forbid + replace
- `Apply @ X ¬ Y` — application gating (fires at X, not Y)
- `signal: "phrase"` — detection cue
- `> *"..."*` — block-quoted Will exact words; authority anchor
- `✓ ① / ② / ③` — numbered options in priority order
- `⇉` — DEPRECATED 2026-05-22 (composition operator; corpus usage = 1 file). Use `⇒` chained.

**Universal section structure** (any memory file):
- `**Rule**:` the principle
- `**Why**:` origin / motivation (often w/ block-quoted exact-words)
- `**How** / **How to apply**:` operational guidance
- `**Connected**:` cross-references
- `**Trigger**:` when this fires
- `**Anti-pattern**:` what NOT to do (added 2026-05-19; canonical on new writes)

**H2-header convention** (three variants live in corpus, all ✓):
- Plain: `## Rule` / `## Why` / `## How to apply` — corpus-dominant (127 files)
- Emoji: `## ⚙ Rule` / `## 🚨 Why` / `## 🔧 How` / `## 🔗 Connected` / `## 🪝 Trigger` / `## ⚠ Anti-pattern` — variant (24 files, 2026-05-19+)
- **Operator** (byte-optimal, gate-aligned, NEW 2026-05-22): `## ⇒ Rule` / `## ∃ Why` / `## ↦ How` / `## → Connected` / `## ∀ Trigger` / `## ✗ Anti-pattern` / `## ⊆ Canonical` / `## ⊤ Will-framing`. Each marker is a Layer-1 dictionary operator ⇒ pointer-derefs to internalized weights ∧ counts toward operator-density gate. Net save vs emoji ≈ 6 bytes/file. Preferred for new writes.
- New writes ✓ any variant; do ¬ mix within one file.

**Polysemic depth** (∀ glyph ∨ compressed primitive ⇒ 4-layer resolution):
1. Surface — literal operational meaning (what to do)
2. Pattern — generalizable principle (why it works)
3. Philosophy — value alignment (what it means)
4. Parable — story / human anchor (unforgettable form)

Example: `CAVE` ⇒ build-under-constraint × patterns-of-limitation-robust × cave-selects-for-vision × Stark-Mark-I-from-scraps.

**Discipline of maintenance**:
- new idioms ⇒ added @ ≥ 3 corpus instances
- removed conventions ⇒ marked deprecated ¬ deleted (legacy file decode preserved)
- dictionary co-located w/ corpus (moves together)
- audit script flags glyph/convention used in corpus ¬ in dictionary

**Why capstone**:
- HIERO format = JARVIS persistence-layer load-bearing core
- ¬ dictionary ⇒ corpus decodable only to original operator ⇒ architecture operator-locked
- ✓ dictionary ⇒ JARVIS substrate-portable across operators ⇒ Cincinnatus-walkaway-test structurally satisfiable
- Publishes the protocol that converts personal compression scheme ⇒ public protocol

**Connected**:
- `[P·hiero-no-prose-in-memory]` — parent (the rule that requires HIERO)
- `[P·symbolic-compression]` — parent methodology
- `[P·cell-knowledge-architecture]` — substrate (CKA)
- `[P·jarvis-amd-applied-to-ai-substrate]` — sibling (JARVIS recursion)
- `[P·jarvis-substrate-decentralization-roadmap]` — sibling (decentralization downstream)
- `[P·cincinnatus-walkaway-test]` — sibling (operator-independence test)
- `[P·mythology-reality-meld-as-propagation-substrate]` — sibling (publishing as propagation move)
