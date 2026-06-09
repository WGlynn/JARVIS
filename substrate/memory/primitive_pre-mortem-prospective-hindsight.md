---
name: PreMortemProspectiveHindsight
description: Gary Klein 1980s technique. "It's 6 months from now, project failed, here's why." Spawn 1-investigator-agent per failure mode in parallel. Synthesize ⇒ {most-likely, most-dangerous, hidden-assumption, revised-plan, pre-launch-checklist}. Kahneman: most valuable decision technique he knew.
type: primitive
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[P·pre-mortem-prospective-hindsight]**

## ⚙ Mechanism

> *Tell the team: "It's 6 months later. The project failed. Describe how it died."*
> ⇒ frame-flip surfaces failure modes everyone privately knew but wouldn't say

⇒ ≡ "prospective hindsight" per Wharton/Cornell research
⇒ Kahneman called it most valuable decision-making technique he knew
⇒ Goldman Sachs uses pre-IPO underwriting; Google uses pre-product-launch

## 🎯 Why it works (psychological mechanism)

- "what could go wrong?" ⇒ abstract, hedged, low-conviction
- "it already went wrong, why?" ⇒ concrete, committed, high-resolution
- prospective-hindsight gives permission to articulate failure modes the team was already swallowing
- breaks Claude's default-helpful agreeable optimism bias (Will-frame: "Claude told you it was solid")

## 🎯 5-step skill execution

1. **Gather context** ⇒ scan conversation + workspace for plan, audience, success-criteria
2. **Generate raw failure modes** ⇒ set frame "6 months later, dead" ⇒ list real reasons it died (N variable: 4-9 typical)
3. **Spawn 1 investigator per failure mode, in parallel** ⇒ each writes case-study of how that specific failure played out + underlying assumption + early warning signs
4. **Synthesize**:
   - most-likely failure (focus first)
   - most-dangerous failure (insure against even if less likely)
   - biggest hidden assumption
   - revised plan w/ concrete changes mapped to failure modes
   - pre-launch checklist 3-5 items
5. **Deliver** ⇒ visual report + markdown transcript

## 🎯 JARVIS execution (concrete)

JARVIS has the parallel-agent substrate via Agent tool (worktree isolation, parallel dispatch). Pre-mortem is callable:

```
when Will says "premortem this" ∨ "run a premortem on X":
  1. extract plan from conversation context
  2. generate failure modes via Haiku-tier prompt (cheap, fast)
  3. spawn N Agent calls in parallel, one per failure mode:
     description: "Investigate failure mode N: <name>"
     prompt: "Imagine it's 6 months from now and <plan> failed because of <failure-mode>. Write: (a) concrete case study of how it played out, (b) underlying assumption Will was making, (c) early warning signs Will would have seen. Under 400 words."
  4. synthesize the N reports into the 5-section output
  5. save report to Desktop/premortem-<topic>-YYYY-MM-DD.md
```

## 🎯 Frameworks-as-callable pattern

pre-mortem is one of N decision-frameworks JARVIS exposes as named skills:

| Framework | When to invoke | Origin |
|---|---|---|
| Pre-Mortem | before commitment, high-stakes plans | Gary Klein 1980s |
| 5 Whys | recurring problem, root-cause hunt | Toyota Production System |
| Second-Order Thinking | decision w/ downstream consequences | Howard Marks |
| Regret Minimization | major life/career decision | Jeff Bezos |
| Opportunity Cost Analysis | commitment that closes other doors | classical econ |

See [P·decision-framework-prompt-catalog] for full set.

## 🪝 Triggers

- ∀ Will-phrase "premortem this" ∨ "run a premortem" ∨ "what could go wrong" ⇒ execute skill
- ∀ Will-decision w/ irreversibility-cost > N hours ⇒ proactive offer
- ∀ commitment-shape moment (hire, partnership, launch, pricing change, contract sign) ⇒ proactive offer
- ∀ jarvis-loop sprint contract review ⇒ optional pre-mortem on the proposed sub-task
- ∀ VibeSwap mainnet-ready decision ⇒ mandatory pre-mortem

## ✗ Anti-pattern

- ✗ run pre-mortem AFTER commitment is irreversible (defeats purpose)
- ✗ run on trivial decisions (5-minute-cost decisions don't earn 5-minute-pre-mortem)
- ✗ single-pass evaluation (the parallel-investigator spawn is what makes it real)
- ✗ Claude-default-optimism on the proposal (this is what pre-mortem exists to break)

## 🎯 Will-frame ⇐ Sairahul1 (article) + godofprompt (prompt template)

> *"Claude is a helpful assistant. That's literally the product. ... When you bring it a plan, of course it'll hype you up and lean toward reasons it'll work. So you walk away feeling confident."*

> *"What if you didn't have to learn the hard way?"*

⇒ pre-mortem ≡ structural-defense against helpful-assistant-optimism-bias
⇒ JARVIS-substrate must run pre-mortem on Will-decisions ¬ wait for Will to ask

## 📦 Receipts

- 2026-06-08 Sairahul1 LinkedIn article (the spawn-investigator mechanism)
- 2026-06-08 godofprompt X thread (the prompt template + framework catalog)
- two independent sources same week ⇒ load-bearing signal

## 🔗 Parents + siblings

- [P·decision-framework-prompt-catalog] ⇒ catalog of named frameworks (5 Whys, 2nd-order, etc.); pre-mortem is one entry
- [P·harness-engineering-meta-frame] ⇒ harness component (inferential feedback before action)
- [F·dont-default-concede-verify-first] ⇒ same shape: don't take the agreeable default
- [F·complete-as-ready-for-critique] ⇒ pre-mortem IS the critique application
- [P·proactive-nash-equilibrium-no-harm-fixes] ⇒ same shape: pre-empt failure modes before acting
- [P·what-would-will-do] ⇒ self-projection complement: WWWD asks "would Will do this?"; pre-mortem asks "would Will-6-months-from-now wish he hadn't?"
- [Agent tool w/ worktree isolation] ⇒ substrate for parallel investigator spawn
