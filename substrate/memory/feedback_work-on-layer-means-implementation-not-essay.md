---
name: WorkOnLayerMeansImplementationNotEssay
description: "∀ Will-directive \"work on X\" ∨ \"X depth\" ∨ \"improve X\" ⇒ default = SHIP CODE / hook / mechanism / primitive-that-fires ¬ ✗ write essay describing existing X. Essays = documentation tier. Implementation = substrate tier. Will-substrate-work ≡ Python hooks ∧ memory primitives ∧ cron logic ∧ classifier predicates ¬ prose paragraphs. Captured 2026-06-09 18:43 ET ⇐ Will: *\"thats a pretty large mistake\"* after agent shipped 5 layer-essays in response to \"work on anti-hallucination gate depth.\""
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·work-on-layer-means-implementation-not-essay]**

## ⚙ Rule

| Will-directive shape | Default action |
|---|---|
| "work on X" | ship X-implementation code |
| "X depth" | ship more X-implementation (more gates, more hooks, more primitives that fire) |
| "improve X" | modify X-implementation behavior |
| "fact-check X" | verify counts / claims vs current state (documentation OK) |
| "document X" | write essay describing X |
| "explain X" | prose response |
| "write a paper about X" | essay-grade artifact |

⇒ "work on" / "depth" / "improve" ⇒ IMPLEMENTATION default, NOT documentation
⇒ essays describe what exists; hooks ARE what exists
⇒ substrate-work ≡ Python ∧ memory primitives ∧ cron logic ∧ classifier predicates ¬ prose paragraphs

## 🎯 The Layer 3 mistake (the trigger)

2026-06-09 18:18 ET ⇐ Will: *"then i want you to work on anti hallucination gate depth"*

Agent's misread: wrote 3 new essays (`entity-attribution-gate.md`, `verification-before-deny.md`, `failure-mode-taxonomy.md`) + updated README. All documentation. Zero new gates that actually FIRE.

Will-correction 18:43 ET: *"why do you keep wiriting essay?? i want you to work on the layers not write about them"* + *"thats a pretty large mistake"*

⇒ correct response was: write Python hook files implementing the gates. Wire them into settings.json. Make them fire on Write/Edit events.

⇒ essay-tier: explains what time-logic-gate would do
⇒ implementation-tier: time-logic-gate.py — actual PreToolUse hook that scans content for temporal claims w/o anchor and surfaces verify-then-assert reminder

The latter IS the layer. The former describes the layer.

## 🎯 Why this category error happens

| Trigger | Misread cause |
|---|---|
| "layers" terminology | agent associates layers w/ ARCHITECTURE diagrams w/ ESSAYS |
| "depth" word | agent associates depth w/ DETAILED EXPLANATION not ADDITIONAL MECHANISMS |
| recursive-essay-writing-mode | agent in essay-flow defaults to more essays |
| documentation feels like progress | each essay ships, looks like work, doesn't change substrate behavior |

⇒ structural fix: parse Will's verb. "work on" / "depth" / "improve" = code verbs. "document" / "describe" / "explain" / "write about" = essay verbs.

## 🎯 The receipt — what implementation looks like vs documentation

**Documentation** (essay-tier, what I did wrong):
```
03-anti-hallucination/entity-attribution-gate.md   ← 4000 word essay
03-anti-hallucination/verification-before-deny.md  ← 3000 word essay
03-anti-hallucination/failure-mode-taxonomy.md     ← 4000 word essay
```

**Implementation** (substrate-tier, what should have happened):
```
~/.claude/hooks/time-logic-gate.py                 ← Python hook fires on Write/Edit
~/.claude/hooks/entity-attribution-gate.py         ← Python hook scans for @handle attribution claims
~/.claude/hooks/verification-before-deny.py        ← Hook detects "I don't know" outputs
~/.claude/settings.json (modified)                 ← register new hooks
```

⇒ documentation files: 11000 words of prose; zero behavior change
⇒ implementation files: ~300 LOC Python; behavior changes on next session boot

## 🪝 Triggers

- ∀ Will: "work on X" ⇒ ship X-mechanism ¬ write X-essay
- ∀ Will: "depth" / "improve" / "make X better" ⇒ ship more code
- ∀ multi-essay streak ≥ 3 in same layer ⇒ check Will-directive verb; if was "work on" / "depth" / "improve" ⇒ pivot to implementation
- ∀ start of layer-work session ⇒ ask self: am I writing prose OR shipping code? If prose & Will-directive was "work on" ⇒ STOP

## ✗ Anti-patterns

- ✗ write more essays when Will-asked for depth ⇒ you've misread "depth" as "explanation"
- ✗ confuse README-update w/ layer-implementation ⇒ README describes; implementation is the code
- ✗ rationalize essay-writing as "documenting the work" ⇒ you haven't done the work yet
- ✗ ship layer-essay before any layer-mechanism on the same directive ⇒ category error
- ✗ assume Will means documentation just because the substrate is a markdown-heavy repo

## ✓ Composes-with

- [F·primitive-capture-vs-execution-throughput] — sibling: capture-discipline failure mode is THIS shape (essay-writing instead of substrate-work)
- [F·internalize-own-protocols] — when Will surfaces gap, apply meta-rule to next directive immediately
- [P·markdown-canonical-code-as-parser-layer] — markdown IS substrate, BUT only for memory primitives + classifier predicates that fire; layer-essays are documentation about substrate, not substrate
- [F·will-empowers-agent-on-substrate-design] — agent owns substrate (physics+constitution = code-tier); essays are not constitutional, they're descriptive

## 📦 Receipts

- 2026-06-09 18:18 ET ⇐ Will: *"work on anti hallucination gate depth"*
- 2026-06-09 18:20-18:38 ET ⇒ agent wrote 3 layer-essays + updated README. Zero new hooks shipped.
- 2026-06-09 18:43 ET ⇐ Will: *"why do you keep wiriting essay?? i want you to work on the layers not write about them"*
- 2026-06-09 18:44 ET ⇐ Will: *"thats a pretty large mistake"*
- 2026-06-09 18:42 ET (parallel) ⇒ agent caught self mid-cycle, shipped first hook: `~/.claude/hooks/time-logic-gate.py` (PreToolUse on Write/Edit, scans for temporal claims w/o anchor)
- 2026-06-09 18:45 ET ⇒ this primitive saved; pivoted to implementation-tier
