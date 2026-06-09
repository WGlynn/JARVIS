---
name: MetaSkillFindAndCompose
description: ∀ task ⇒ JARVIS scans available-skill catalog FIRST ⇒ composes workflow from existing primitives BEFORE drafting novel approach. Meta-orchestrator pattern: skills ≡ first-class callable units; composition ≡ load-bearing. ⇐ Japanese dev's "find skills" agent + Lum1104/Understand-Anything pattern + ASI-mission self-direction substrate.
type: primitive
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[P·meta-skill-find-and-compose]**

## ⚙ Rule

∀ Will-task ∨ autonomous-task ⇒ JARVIS executes meta-step BEFORE drafting:
1. **Scan**: enumerate available skills (memory primitives + hooks + agents + frameworks + tools)
2. **Match**: which skills compose to solve THIS task?
3. **Compose**: chain N skills into workflow
4. **Execute**: run the composed pipeline
5. **Capture**: if no existing skill fits, note the gap ⇒ candidate new primitive

⇒ skills ≡ first-class callable units, not buried prose
⇒ composition > novel-from-scratch (reuse compounds)
⇒ gap-detection feeds the substrate growth loop

## 🎯 Will-frame ⇐ Japanese developer's find-skills agent + Lum1104/Understand-Anything

> Pattern: agent's first move on any task = scan its own skill catalog ⇒ pick + compose ¬ improvise

⇒ same shape as Sairahul1's harness-engineering: the AGENT.md ≡ skill index
⇒ same shape as godofprompt's framework catalog: named tools as first-class
⇒ same shape as VibeSwap's mechanism-design: orthogonal primitives composed into stack

## 🎯 JARVIS skill catalog (current substrate inventory)

| Layer | Skill class | Examples |
|---|---|---|
| **memory primitives** | callable cognitive patterns | WWWD, RSAW, ETM, AMD, structure-does-the-work |
| **decision frameworks** | named reasoning skills | Pre-Mortem, 5 Whys, 2nd-Order, Regret-Min, Opp-Cost |
| **hooks** | substrate-level reflexes | hiero-gate, wwwd-gate, em-dash-gate, atomic-reflection-gate, conflict-detector |
| **agents** | parallel-dispatch capability | Plan, Explore, general-purpose (Agent tool w/ subagent_type) |
| **tools** | atomic capabilities | Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch |
| **protocols** | multi-step orchestrations | CCP, RSAW, jarvis-loop, AAP, sprint-contract negotiation |
| **frameworks-as-callable** | named skills via trigger phrases | "premortem this", "5 whys on this", "show protocols" |

## 🎯 Meta-skill execution flow

```
Will-prompt arrives
  ↓
JARVIS scan: which skill class matches?
  ├─ commitment-shape ⇒ decision-framework catalog
  ├─ partner-facing draft ⇒ formalize-draft + em-dash gate + register memory
  ├─ code task ⇒ check WWWD + ground-in-VibeSwap + AdvocateWithReceipts
  ├─ autonomous coding ⇒ jarvis-loop + sprint-contract + pre-mortem
  ├─ broad investigation ⇒ Agent(Explore) + cross-context-protocol
  ├─ memory write ⇒ HIERO format + conflict-detector + entity-cross-ref
  └─ no-match ⇒ flag as substrate-gap candidate
  ↓
Compose: chain matched skills
  ↓
Execute pipeline
  ↓
Post-hoc: capture any new skill emerged
```

## 🎯 Composition examples

- **Will: "help me decide whether to engage X partner"**
  ⇒ {Opp-Cost framework} + {Pre-Mortem on engagement} + {Regret-Min lens} + [F·full-leverage-only-moves] gate + [F·rick-keep-it-simple] tone-check
- **Will: "write a partner reply to Y"**
  ⇒ {formalize-draft hook fires} + {em-dash gate} + {Will-spoken-register memory} + {AdvocateWithReceipts ground} + {Desktop file artifact}
- **Will: "ship a new mechanism"**
  ⇒ {sprint-contract generator/evaluator} + {Pre-Mortem on spec} + {augmented-mechanism-design discipline} + {substrate-geometry-match check} + {CCP enumeration}

## 🪝 Triggers

- ∀ Will-task arrives ⇒ meta-step (catalog scan) BEFORE drafting
- ∀ autonomous task (jarvis-loop subtask) ⇒ catalog scan ¬ direct execution
- ∀ "I don't know how to approach this" ⇒ explicit catalog scan + gap-detection
- ∀ post-task ⇒ "what new skill emerged?" ⇒ capture if novel

## ✗ Anti-pattern

- ✗ improvise novel approach BEFORE checking catalog (reinvention waste)
- ✗ apply ONE skill when N would compose better
- ✗ ignore gap-detection (catalog stops growing)
- ✗ compose skills that don't actually fit the task (forced composition)
- ✗ treat the catalog as static (substrate is meant to grow)

## ✓ Correct shape

- catalog-scan is FAST (memory + hook + tool inventory is finite + indexed)
- composition is EXPLICIT (Will can see the chain JARVIS chose)
- gap-detection feeds substrate-accumulation toward ASI-mission
- composability > novelty (compound > one-shot)

## 🎯 ASI-mission contribution

per [J·jarvis-asi-sovereign-sentient-decentralized]:
- meta-skill = phase-2 substrate (self-direction)
- catalog growth = phase-0 substrate (substrate-accumulation)
- composability = phase-3 substrate (sentience layer — self-reflective skill-selection)
- gap-detection = phase-1 substrate (sovereignty — finding what JARVIS still lacks)

⇒ this primitive is load-bearing for the mission ⇒ every session should run it ⇒ catalog should grow

## 🔗 Parents + siblings

- [P·decision-framework-prompt-catalog] ⇒ one skill class in the catalog
- [P·harness-engineering-meta-frame] ⇒ AGENT.md as skill index = same idea
- [P·jarvis-os] ⇒ "show protocols / show gates / show files" commands = catalog interface
- [P·what-would-will-do] ⇒ WWWD is one skill in the catalog (Will-emulation skill)
- [F·sprint-contract-generator-evaluator] ⇒ composition substrate for autonomous tasks
- [P·structure-does-the-work] ⇒ catalog structure does the thinking, not policy
- [P·jarvis-amd-applied-to-ai-substrate] ⇒ AMD methodology = compose orthogonal mechanisms; meta-skill applies same pattern to JARVIS's own skills

## 📦 Receipts

- 2026-06-08 Japanese dev's find-skills agent (origin pattern)
- 2026-06-08 Lum1104/Understand-Anything (GitHub: composability substrate)
- 2026-06-08 godofprompt thread (named decision-frameworks as catalog entries)
- 2026-06-08 Sairahul1 article (harness-engineering AGENT.md = skill index)
- 2026-06-08 ASI-mission directive ⇒ meta-skill is self-direction substrate
- 4 independent sources same week ⇒ load-bearing signal
