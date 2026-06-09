---
name: DecisionFrameworkPromptCatalog
description: 5 named decision-frameworks as callable JARVIS skills. Pre-Mortem (Klein), 5 Whys (Toyota), Second-Order Thinking (Marks), Regret Minimization (Bezos), Opportunity Cost (econ). ∀ commitment-shape moment ⇒ JARVIS proactively offers the matching framework. ⇐ godofprompt X thread 2026-06-08.
type: primitive
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[P·decision-framework-prompt-catalog]**

## ⚙ Catalog

| Skill | Invoke when | Origin | Sibling primitive |
|---|---|---|---|
| **Pre-Mortem** | before commitment; 6-mo-later-failed frame; spawn parallel investigators | Gary Klein 1980s | [P·pre-mortem-prospective-hindsight] |
| **5 Whys** | recurring problem; root-cause chase past symptom | Toyota Production System | (this primitive) |
| **Second-Order Thinking** | decision w/ downstream consequences; what-comes-after-the-obvious | Howard Marks | (this primitive) |
| **Regret Minimization** | major life/career decision; 80-yr-old-Will frame | Jeff Bezos | (this primitive) |
| **Opportunity Cost** | commitment that closes other doors; explicit alternatives | classical economics | (this primitive) |

## 🎯 5 Whys — execution template

```
Problem: {state symptom}
Why 1: {why does the symptom occur?}
Why 2: {why does the answer to Why 1 occur?}
Why 3: ...
Why 4: ...
Why 5: ...
Root cause: {final answer}
Systemic fix: {address root, not symptom}
```
- ∀ "we already fixed this" recurrence ⇒ candidate
- ∀ surface-fix that needs re-fix in N months ⇒ candidate
- stop when answer = process/system flaw ¬ person blame

## 🎯 Second-Order Thinking — execution template

```
First-order: {immediate consequence}
Second-order: {what happens after the consequence?}
Third-order: {what happens after that?}
Hidden cost: {what's the externalized harm?}
Stakeholders missed: {who pays for this we haven't accounted for?}
Revised decision: {if 2nd/3rd order changes calculus}
```
- ∀ strategy choice ⇒ candidate
- ∀ partnership/contract ⇒ candidate
- ∀ growth-tactic ("just hire more") ⇒ candidate

## 🎯 Regret Minimization — execution template

```
Decision: {what Will is considering}
80-yr-old-Will lens:
  - Do A ⇒ regret? Y/N + why
  - Do ¬A ⇒ regret? Y/N + why
  - Asymmetric regret? (one path haunts, other recoverable)
Optionality preserved: {can this be reversed?}
Decision: pick path w/ lower regret-asymmetry
```
- ∀ life/career inflection ⇒ candidate
- ∀ "should I quit X" ⇒ candidate
- ∀ all-in moves ⇒ candidate

## 🎯 Opportunity Cost — execution template

```
Doing X requires: {time + capital + attention budget}
What X precludes:
  - Alternative A: {forgone}
  - Alternative B: {forgone}
  - Default state: {forgone if X-chosen}
Opportunity cost = max(value of forgone)
Net value of X = value(X) - opportunity_cost
```
- ∀ "should we add Y feature" ⇒ candidate (vs not-building)
- ∀ commit-of-N-weeks ⇒ candidate
- ∀ ¬-reversible spend ⇒ mandatory

## 🎯 Frameworks-as-callable in JARVIS

```
trigger phrases (Will-natural):
  "premortem this" → Pre-Mortem skill
  "5 whys on this" → 5 Whys skill
  "what's the 2nd order?" → Second-Order skill
  "would future-me regret" → Regret Minimization skill
  "what's this trading off against" → Opportunity Cost skill

JARVIS proactive offer:
  - commitment-shape detected (hire/partnership/launch/contract) ⇒ offer matching framework
  - irreversibility-cost > N hours ⇒ offer Pre-Mortem ∨ Regret Min
  - recurring-issue detected ⇒ offer 5 Whys
  - strategy-decision pending ⇒ offer Second-Order
  - resource-allocation decision ⇒ offer Opportunity Cost
```

## 🎯 Composability

frameworks compose ⇒ ∀ major decision = sequence of {Opp-Cost → Pre-Mortem → Regret-Min}
- Opp-Cost ⇒ "what does this cost me?"
- Pre-Mortem ⇒ "what kills this if I commit?"
- Regret-Min ⇒ "what does 80-yr-old-Will say?"
sequence ⇒ comprehensive decision substrate w/o committee-by-committee weight

## 🪝 Triggers

- ∀ Will-decision moment ⇒ JARVIS scans for matching framework BEFORE answering
- ∀ Will-asks "should I X" ⇒ pick framework, apply, deliver
- ∀ jarvis-loop autonomous task w/ commitment-shape ⇒ run framework before execution
- ∀ partner-engagement decision (engage/silent) ⇒ Opp-Cost + Pre-Mortem composable

## ✗ Anti-pattern

- ✗ apply framework to trivial decision (5-min-cost ⊥ 5-min-framework)
- ✗ skip framework on "obvious" call (obviousness = post-hoc rationalization for default)
- ✗ apply ∀ framework ∀ decision (paralysis-by-framework)
- ✗ use framework as procrastination substitute for shipping

## 🔗 Parents + siblings

- [P·pre-mortem-prospective-hindsight] ⇒ first skill in catalog, separately specced
- [P·harness-engineering-meta-frame] ⇒ frameworks are harness components (named cognitive tools)
- [P·meta-skill-find-and-compose] ⇒ catalog-discovery + workflow-composition substrate
- [F·dont-default-concede-verify-first] ⇒ same shape: stop the default-helpful-Claude reflex
- [P·structure-does-the-work] ⇒ frameworks = structure; structure does the thinking, not policy

## 📦 Receipts

- 2026-06-08 godofprompt X thread (5-framework prompt template set)
- 2026-06-08 Sairahul1 article (Pre-Mortem detailed mechanism via parallel investigators)
- 2026-06-08 ASI-mission directive ⇒ catalog is substrate-component (self-direction layer)
- two independent sources same week ⇒ load-bearing signal
