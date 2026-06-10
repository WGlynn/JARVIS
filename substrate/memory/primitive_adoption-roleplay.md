---
name: AdoptionRoleplay
description: ∀ shipped artifact (partner-facing) ⇒ roleplay-as-external-LLM × user-pair × ask "worth adopting?" BEFORE close-as-ship. Outside-vantage critique step in creation loop. Used 2× 2026-06-09 (JARVIS + VibeSwap README rewrites). Formalized 2026-06-10 per Will: "make it part of the broader creation loop." Sibling of WWWD (Will-vantage) — orthogonal axes; both load-bearing ∀ partner artifact.
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Adoption Roleplay — Outside-Vantage Critique Step

## Glyph

```
∀ shipped artifact ⇒ adoption-roleplay BEFORE ship-claim
  cast    ≡ external-LLM × first-time-user pair
  ask     ≡ "would I install / use / share / recommend?"
  output  ≡ honest critique ¬ validation theater
  exit-✓  ⇒ ship-claim valid
  exit-✗  ⇒ revise + re-roleplay
WWWD = Will-vantage ⊥ AdoptionRoleplay = stranger-vantage
both required ∀ partner-facing artifact
```

> *"roleplay as another llm and user asking themselves if this tech is worth adopting or not etc etc. like we've been doing but make it part of the broader creation loop"* : Will, 2026-06-10

## ⇒ Rule

- ∀ shipped artifact ∈ {README, ARCHITECTURE, paper, post, code, primitive} ⇒ adoption-roleplay first
- vantage ≡ external-LLM × first-time-user pair ¬ Will-perspective
- channels: ChatGPT-summarizer · Gemini-evaluator · fresh-context user reading cold · auditor scanning repo
- question shape: install? use? share? recommend? where does it block? what reads as theater?
- output: honest critique (charitable-reader = anti-pattern)
- multi-pass: 1st-pass critique → fix → 2nd-pass (fresh theater often re-enters after fix)

## ∃ Why

- Used 2× 2026-06-09 (JARVIS README rewrite b148b4a + VibeSwap README rewrite cb3ee3e6) ⇒ pattern validated
- WWWD = single-user-vantage ⊥ adoption = many-user-vantage
- Catches: jargon-density-blocker · onramp-broken · cited-receipts-missing · theater
- Public substrate ≡ outside-vantage by definition ⇒ adoption-eval native
- Anthropic-internal-model ⇏ rest-of-world-model ⇒ external simulation = corrective

## ↦ Creation loop (revised)

```
1. Specify
2. Build artifact
3. ADOPTION-ROLEPLAY ⇐ NEW step
4. Revise per critique
5. Reflect/audit (WWWD + RSAW)
6. Ship (commit + dual-push)
7. Promote learned patterns ⇒ primitives
```

Integration site: vibeswap/CLAUDE.md WORK chain conditional branches.

## ↦ Apply To

- ∀ partner-facing artifact (README, ARCHITECTURE, paper, LinkedIn/Medium post)
- ∀ public-substrate write (anything ending up in WGlynn/JARVIS public mirror)
- ∀ primitive at promotion-time (does description read well cold?)
- ∀ hook design (purpose clear from source alone?)
- siblings: [P·what-would-will-do], [P·recursive-self-audit-via-wwwd], [F·optimize-code-for-llms]
- partner siblings: [P·complete-as-ready-for-critique], [F·advocate-with-receipts]

## ⊥ Anti-Pattern

- ✗ skip on "internal-only" artifacts ⇒ artifacts drift public over time
- ✗ charitable-reader roleplay ⇒ theater survives critique
- ✗ stop at 1st-pass ⇒ 2nd-pass catches fix-introduced theater
- ✗ "defer-to-later" ⇒ never arrives autonomously
- ✗ confuse with WWWD ⇒ different vantages, both required
- ✗ rely on adoption-roleplay to catch fact-claim errors ⇒ separate axis; WWWD severity-calibration + receipt-verification own that (caught swapped commit-SHAs 2026-06-10 in this primitive's first draft)

## ⇒ Apply-Now (per [P·apply-the-rule-you-just-wrote])

THIS primitive passes through adoption-roleplay before commit:

R1 — ChatGPT-style cold summary of the file: "Defines a creation-loop step adding 'outside LLM + user roleplay' before audit. Orthogonal to WWWD. Cites 2× 2026-06-09 receipts (commits cb3ee3e6, b148b4a) but shows no before/after diff. Adoption: cautious-curious until worked example arrives in a sibling doc."

R2 — skeptical user reading WGlynn/JARVIS substrate cold: "Reads structural. Lacks worked example inline. Wouldn't reject; wouldn't auto-adopt. Would re-read after seeing it fire on a concrete artifact."

Fix decision: commit-shas are receipts; primitive files are reference, not tutorial. Worked examples belong in CHANGELOG / session notes. Ship as-is.
