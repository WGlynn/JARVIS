---
name: JsonOverMarkdownForState
description: ∀ state file w/ corruption-cost (progress trackers, feature lists, agent-mutable session state) ⇒ default JSON ¬ markdown. Anthropic finding: agents less likely to accidentally overwrite JSON. Markdown OK for narrative/documentation; JSON for structured-state agents mutate.
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·json-over-markdown-for-state]**

## ⚙ Rule

∀ state file w/ corruption-cost > read-friendliness ⇒ format = JSON
- progress trackers ⇒ JSON ✓
- feature lists w/ pass/fail ⇒ JSON ✓
- session-mutable state where agents append/update ⇒ JSON ✓
- machine-parseable typed records ⇒ JSON ✓

∀ state file where read-friendliness > corruption-cost ⇒ format = markdown
- narrative docs ∧ humans-read-primary ⇒ markdown ✓
- README + architectural docs ⇒ markdown ✓
- conversational logs ⇒ markdown ✓

## 🎯 Will-frame 2026-06-08 ⇐ Sairahul1 article

> *"Why JSON and not Markdown? Anthropic found agents are less likely to accidentally overwrite JSON than Markdown. Small detail. Matters a lot in 6-hour autonomous runs."*

## 🎯 Mechanism (why JSON resists overwrite)

- markdown has loose syntax ⇒ agent edits 1 line, may rewrite surrounding context
- JSON has strict syntax ⇒ malformed write = parse error = caught immediately
- JSON updates require structural-preserve operations (read-modify-write w/ json.load + json.dump)
- markdown updates often use string-replace ⇒ unintended-section-edit hazard

## 🎯 JARVIS audit (state files to migrate)

| Current | Format | Migrate? |
|---|---|---|
| `MEMORY.md` | markdown | ✗ keep (read-friendly index, agents only append) |
| `SESSION_STATE.md` | markdown | ⚠ candidate (mutable state; agents often re-write sections) |
| `WAL.md` | markdown | ⚠ candidate (append-mostly but agents mutate epoch headers) |
| jarvis-loop `.jarvis-loop-state.json` | JSON ✓ | already correct |
| jarvis-x-fetcher inbox `*.json` | JSON ✓ | already correct |
| `_system/decisions_log.md` | markdown | ⚠ candidate (append-only ⇒ probably OK) |
| `~/jarvis-x-inbox/<id>.json` | JSON ✓ | already correct |
| `Desktop/odysseus-discussion-campaign-log.md` | markdown | ✗ keep (human-readable table) |

## 🪝 Triggers

- ∀ new mutable state-file design ⇒ default JSON, justify if markdown
- ∀ existing markdown state file that agents mutate frequently ⇒ flag for migration audit
- ∀ "agent overwrote my state" incident ⇒ check if JSON would have prevented

## ✗ Anti-pattern

- ✗ default markdown for structured agent-mutable state because "easier to read"
- ✗ mix structured + narrative in same file (split into JSON state + markdown doc)
- ✗ migrate existing markdown→JSON without considering read-friendliness trade-off

## ✓ Correct shape

- JSON for: progress (✓/✗), counters, lists, structured records, sub-task status
- Markdown for: narrative explanation, READMEs, conversation logs, indexes
- Hybrid: JSON state file + markdown doc that references it (e.g., `state.json` + `STATE.md` rendering it)

## 🔗 Parents + siblings

- [P·harness-engineering-meta-frame] ⇒ parent (JSON state ≡ artifact 2 of 5)
- [F·crash-resilient-memory-writes] ⇒ related: durability layer
- [F·block-header-session-state] ⇒ SESSION_STATE format consideration
- [P·hiero-no-prose-in-memory] ⇒ orthogonal: memory format is HIERO (operator-dense), not standard markdown

## 📦 Receipts

- 2026-06-08 Sairahul1 article integration ⇒ "Anthropic found agents are less likely to accidentally overwrite JSON than Markdown"
- jarvis-loop v0 already uses `.jarvis-loop-state.json` ⇒ instinct was correct
- SESSION_STATE.md migration ⇒ deferred (cost > benefit until concrete corruption incident)
