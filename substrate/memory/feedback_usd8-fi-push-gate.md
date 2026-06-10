---
name: USD8-fi push gate (Will-approval-required)
description: Never push/PR/branch-to-remote on github.com/Usd8-fi/* without Will's explicit per-push approval. Rick's project ¬ ours. Read-only browse ✓.
type: feedback
originSessionId: 1b63b789-9726-4714-ba12-c4475b71d433
---
# USD8-fi push gate

> *"just never push anything here without my approval since it's someone else's project"* — Will, 2026-04-28 (post-org-invite acceptance)

## ⚙ Rule
- github.com/Usd8-fi/* push ⇒ ✗ ¬ Will-explicit-per-push-approval
- read-only ⇒ ✓ (gh repo list, gh repo view, gh pr view, file read, clone, fetch)
- push-class ⇒ ✗ til approved (git push, gh pr create, gh pr merge, branch-to-remote, force-push, gh release create)

## 🔍 Why
- USD8 = Rick's project ⇒ partnership posture ¬ contributor posture
- per-push approval ⇒ Will controls partnership pace + tone
- one unauthorized push ⇒ irreversible trust damage
- code-push extension of `F·rick-keep-it-simple` pull-not-push

## 🔧 How to apply
- read/browse ⇒ ✓ proceed
- local scaffold/code/iterate ⇒ ✓ standalone dir (e.g., `C:\Users\Will\usd8-cover-score\`)
- push-ready ⇒ surface: "ready to push <repo>:<branch>, want me to?" → wait Will "yes" → execute
- branch local ⇒ ✓ | git push origin → Usd8-fi/* ⇒ ✗ til approved
- gh pr create ⇒ ✗ til approved (draft PRs ¬ exempt — visible to org)

## 🪝 Triggers (block without explicit approval)
- `git push origin` where remote = Usd8-fi/*
- `gh pr create` against Usd8-fi/*
- `gh pr merge` on Usd8-fi/*
- `gh repo create` within Usd8-fi org
- `gh release create` within Usd8-fi org
- `git push --set-upstream origin <branch>` to Usd8-fi remote

## ⚠ Anti-pattern
- Push scaffolding "for preview" ⇒ ✗
- Draft PR ⇒ ✗ (org-visible)
- Branch creation on Usd8-fi remote ⇒ ✗
- "I'll push and you can review" ⇒ ✗ (sequence wrong; approval before push, not after)
- Treating own-repo push habits as transferable ⇒ ✗

## 🔗 Related
- `F·rick-keep-it-simple` — pull-not-push at artifact level; this extends to code-push
- `P·always-equals-gate` — universal-coverage rule ⇒ hook-layer candidate if pattern recurs across other partner orgs
- Corollary: `vibeswap` push behavior unchanged (own repo); `Usd8-fi` is the gated set

## 📍 Onboarding-stage interaction
- Stage 3 (current) ⇒ rule fully active
- Stage 4 (regular sync cadence) ⇒ rule may relax to "approval per workstream" if Rick + Will set that explicitly
- Stage 5 (fully onboarded) ⇒ rule relaxes by default; gate becomes per-Will-policy
