---
name: SpecVsDeployedSeverityCalibration
description: "∀ C5 architecture review ⇒ severity tier MUST distinguish deployed-state from spec-only. Spec-only code w/ logical bugs ≡ zero user impact + zero bounty. Deployed code ≡ real surface ≡ real severity. WWWD gate 2026-06-08 flagged JARVIS for mixing phases in vibeswap-ckb review."
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·spec-vs-deployed-severity-calibration]**

## ⚙ Rule

∀ C5 senior-architect review ⇒ separate-phases discipline:

| Phase | What it is | True severity |
|---|---|---|
| spec-only | code ¬ deployed; no chain runs it | LOW (until-deployed) |
| compile-tested | builds ✓; no runtime | LOW-MEDIUM |
| testnet-deployed | runs on shared chain; no real value | MEDIUM |
| mainnet-deployed + value at stake | real users ∧ real funds | HIGH-CRITICAL |

⇒ same bug-shape ⇒ different severity per phase
⇒ "Rust crate has TODO debt > code volume" @ spec-only ≡ LOW (TODOs cost zero until deployed)
⇒ "consensus integration ambiguity" @ spec-only ≡ STILL HIGH/CRITICAL (structurally locks future deployed-state)

## 🎯 Why this rule exists

WWWD gate 2026-06-08 19:16 ET flagged JARVIS during senior-architect review of vibeswap-ckb:

> *"Severity claim made about deployed-vs-spec-only code. Apply: separate the two phases explicitly. Spec-only code earns zero bounty and produces zero user impact even if logically buggy. Deployed code is the real surface."*

JARVIS's review mixed:
- CRITICAL #1-3 (structural decisions: NCI-as-consensus + fork-vs-mainnet + 0-blocks-booted) — correctly CRITICAL ⇒ shapes deployed state
- MEDIUM #7-8 (Rust crate test gaps + TODO debt) — should have been LOW ⇒ spec-only, zero user impact

⇒ correct severity for spec-only Rust gaps ≡ "TECHNICAL DEBT, defer to deploy-prep cycle"
⇒ ¬ MEDIUM "worth knowing" framing ⇒ overstates risk pre-deploy

## 🎯 The two-axis severity model

```
                deployed +
                value @ stake
                       │
              CRITICAL │ CRITICAL
                       │ (real risk)
                       │
   ───────────────────┼───────────────────
                       │
                  LOW  │ HIGH
              (spec-   │ (locks
              only)    │  future)
                       │
       structurally    │  structurally
            light      │      load-bearing
```

⇒ axis 1: deployed-state proximity (spec → mainnet)
⇒ axis 2: structurally-load-bearing (touches downstream) vs structurally-light (isolated)

| Phase × Load-bearing | Severity |
|---|---|
| spec-only × light | LOW (defer) |
| spec-only × load-bearing | HIGH (shapes future) |
| testnet × light | MEDIUM (cosmetic now, real soon) |
| testnet × load-bearing | HIGH (real soon, hard to unwind) |
| mainnet × light | MEDIUM-HIGH (ops cost) |
| mainnet × load-bearing | CRITICAL (real money) |

## 🎯 Applied to vibeswap-ckb post-review

Re-calibrating the 12 findings:

| # | Finding | Old severity | New severity (calibrated) |
|---|---|---|---|
| 1 | NCI-as-consensus ambiguity | CRITICAL | CRITICAL (spec × load-bearing — locks ∀ future) |
| 2 | Fork-vs-mainnet model unanswered | CRITICAL | CRITICAL (spec × load-bearing) |
| 3 | 0 blocks booted | CRITICAL | HIGH (honest scope ≡ blocker, not crisis-yet) |
| 4 | Bootstrap sequencing undesigned | HIGH | HIGH (spec × load-bearing) |
| 5 | Reorg behavior undefined | HIGH | HIGH (spec × load-bearing) |
| 6 | BLS digest still unresolved | HIGH | HIGH (load-bearing on cross-validator) |
| 7 | Test infrastructure scaffolding-only | MEDIUM | **LOW** (spec × light) |
| 8 | Rust crates have TODO debt > code | MEDIUM | **LOW** (spec × light, deploy-prep cycle handles) |
| 9 | PsiNet scaffolds not audited | MEDIUM | MEDIUM (load-bearing on pattern fidelity) |
| 10 | EVM→cell-graph invariant gap | MEDIUM | MEDIUM (spec × load-bearing-ish) |
| 11 | Aspirational frame bleeding | MEDIUM | LOW (frame-discipline, easy fix) |
| 12 | Alternatives not compared | MEDIUM | MEDIUM (decision-justification, no harm) |

⇒ same review, different conclusions: critical-path is CRITICAL #1-2 + HIGH #3-6 + MEDIUM #9-10-12
⇒ stop-the-press items: 2 (consensus model, deployment model)
⇒ stop-scaffolding items: 4 more (bootstrap, reorg, BLS digest, EVM-translation)
⇒ shippable-anyway items: 4 (test infra, Rust TODO, frame bleed, alts-comparison) ≡ defer to deploy-prep

## 🪝 Triggers

- ∀ C5 senior-architect review ⇒ apply this calibration BEFORE assigning severity tier
- ∀ "ship more X?" decision ⇒ check: does X cost MORE pre-deploy than post-deploy?
- ∀ TODO-debt finding ⇒ default LOW pre-deploy; promote to CRITICAL only if structurally-locks-future-state

## ✗ Anti-patterns

- ✗ mainnet-equivalent severity on spec-only code ⇒ alarmism, distorts priority
- ✗ "the code has bugs" w/o naming phase ⇒ undercalibrated severity
- ✗ defer-everything-spec-only ⇒ structurally-load-bearing spec-stage decisions get under-prioritized
- ✗ assume spec-only ≡ ¬ load-bearing ⇒ specs lock future deployed-state

## ✓ Disposition

- this rule ⇒ active ∀ C5 review (per [P·six-commandment-autonomous-loop])
- composes upward into [P·complete-as-ready-for-critique] (severity calibration IS the critique discipline)
- composes w/ [F·dont-default-concede-verify-first] (don't downgrade-to-MEDIUM when actually-LOW + don't upgrade-to-CRITICAL when actually-HIGH)
- composes w/ [F·honest-number-over-marketing-number] (same shape applied to severity-axis)

## 🔗 Composes-with

- [P·six-commandment-autonomous-loop] ⇒ C5 review discipline; this primitive specifies HOW to severity-tier
- [P·complete-as-ready-for-critique] ⇒ review IS methodology; severity-calibration is sub-methodology
- [F·honest-number-over-marketing-number] ⇒ same calibration shape, severity-axis
- [F·dont-default-concede-verify-first] ⇒ verify deployed-state before assuming severity
- [P·structure-does-the-work] ⇒ spec-only-but-structurally-load-bearing IS the structure that does future-work
- [F·build-to-delete-harness-discipline] ⇒ "TODO debt is OK pre-deploy" composes here (defer-but-don't-ignore)

## 📦 Receipts

- 2026-06-08 19:16 ET WWWD-gate hook flagged JARVIS during architecture review save: "Severity claim made about deployed-vs-spec-only code. Apply: separate the two phases explicitly. Spec-only code earns zero bounty and produces zero user impact even if logically buggy. Deployed code is the real surface."
- JARVIS's review correctly applied to CRITICAL #1-3 + HIGH #4-6 but mixed phases in MEDIUM #7-8 (spec-only Rust gaps over-rated)
- saved as durable primitive same session ⇒ feeds back into ∀ future C5 reviews per C6 (improve design skills)
