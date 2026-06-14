---
name: story-mode-feature-set
description: Story Mode shipped feature set (4 live in story-mode-gate.py) + backlog (4 designed ¬ built). Sibling of chained-pick grammar; menu/interaction layer.
metadata: 
  node_type: memory
  type: project
  visibility: public
  originSessionId: a9a165d8-328b-482a-bfba-3391ed9a4a88
---

Story Mode = ranked end-of-turn menu ∧ number-nav ∧ multi-pick.
- pick-resolution grammar ⇒ [[primitive_story-mode-chained-pick-grammar]]
- THIS = feature layer (menu-gen ∧ input affordances)
- ∀ SHIPPED ⇒ verified live `~/.claude/hooks/story-mode-gate.py` 2026-06-14

## ✓ SHIPPED (∈ story-mode-gate.py)
1. **inline-modifier** `N: <tweak>` (∨ `N.` ∨ `N -`) ⇒ run N + adjust, case-preserved.
   - e.g. `3: only the auth part` · `3 - use sonnet`
   - parse L110-118 → MODIFIER clause injected L178-179
2. **irreversible ⚠ mark** ⇒ send∨publish∨deploy∨delete∨push∨message∨email∨post item ⇒ lead `⚠ `.
   - phone-tapper sees consequence pre-tap
   - menu-gen L209-211 ∧ contradiction/dep route-into-irreversible guarded L173-174
3. **diversity/dedup** ⇒ 10 items ⊇ ≥5 signature-move-classes ∧ ✗ paraphrase-pairs. L209-212
4. **off-menu regret-mining** ⇒ freetext-instead-of-N → `_system/story_signatures/{USER}_offmenu.jsonl` (L140-144).
   - pick⊥off-menu = catch-rate denominator (L102); off-menu ≡ menu-wrong ≡ training-signal

## ◐ BACKLOG (designed ¬ built; ⇐ 2026-06-14 handoff)
- ranges/exclusions ⇒ `2-5` · `all except 3`
- condition-bounded loops ⇒ `story loop until <predicate>` (vs fixed `story loop N`)
- "why N?" ⇒ interrogate item-ranking pre-pick
- confidence-display ⇒ show P-estimate ∀ item

## ⚙ open knob
- chained-pick contradiction default = **later-wins** (grammar L23)
- alts ✗chosen: surface-ask ∨ safe-wins
- revisit ⇔ contradiction routes → irreversible (cf ✓#2 guard)

origin: 4 ✓ landed via story-loop self-play; doc-debt flagged [[project_session-2026-06-14-pewds-solver-storymode-pom]] L25 (code ✓ ∧ primitive ✗) ⇒ THIS closes debt.
product-frame: [[project_story-mode-product-thesis]]
