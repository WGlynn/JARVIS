---
name: gatesthatgateandloopsthatlearn
description: "2 class-fixes (Will 2026-06-11, self-critique 2+4). (2) safety/resource gate ⇒ BLOCK ¬ advise + log enforcement ⇒ prevention measurable. (4) ∀ persistent-log ⇒ consumer-closes-loop ∨ theater. Verified vs JARVIS-as-OS research sweep."
metadata: 
  node_type: memory
  type: primitive
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Gates that gate, loops that learn

> Will 2026-06-11: *"we need to address criticisms 2 and 4 ... the biggest offenders."*

## ⇒ C2 — gates ¬ gate
- founding-claim: instructions-decay ∧ structure-holds
- violated ⇔ ~40 hooks INJECT advice (additionalContext) ¬ ENFORCE (permissionDecision deny)
- WWWD: 1385 fires × 1 correction × 0 falsification ⇒ measured spoke ¬ prevented
- **rule**: deterministic safety/resource constraint ⇒ blocking-hook ¬ memory-prose ¬ advisory
- **rule**: ∀ denial ⇒ append `state/gate_enforcement.log` ⇒ prevention = countable
- **shipped**: `resource-cgroup-gate.py` (PreToolUse Bash)
  - enforce forge/heavy concurrent-cap ← `state/resource-limits.json` (local ∧ gitignored per [F·local-vs-shared-constraints])
  - converts "max-3-forge / 16GB" prose ([P·always-equals-gate] violation; ⊕ AgentCgroup arXiv 2602.09345) → real deny
  - ✓ proven: cap=0 → deny; ledger-row written

## ⇒ C4 — logs ¬ consumed
- symptom: anticipation "surfaced x23 unactioned" all-session; selections ∧ gate-fires ∧ decisions WRITTEN × ~0 READ-BACK
- ⊕ literature #1 concern (Dive-into-Claude-Code: "Silent Failure ∧ Observability-Eval gap")
- **rule**: ∀ persistent-log ⇒ ∃ consumer (read → behavior-Δ ∨ health-signal). no-consumer = theater
- **shipped**: `afk-corpus-reweight.py` + cron `928fcfcc` (daily 4:19)
  - consume AFK `<user>_selections.jsonl` → top3-hit-rate → corpus `_reweight` block
  - run-1: 7 picks × 71% top-3 → "well-ranked"
  - = template ∀ other write-and-forget loop

## ⌗ Follow-ups (JARVIS-as-OS sweep 2026-06-11)
- biggest-gap = process-lifecycle/scheduler: bg-agents ✗ liveness-supervision ✗ exit-contract
  - fix (AgentRM-MLFQ ⊕ Quine-exit-codes ⊕ Springdrift-watchdog): file-run-queue × priority-class + exit-code-contract + watchdog-cron reaps-zombies. QUEUED ¬ built
- AFK richer-reweight ⇒ log chosen-item move-CLASS ¬ only number
- gate-staleness-audit (Anthropic harness-post): ∀ hook encodes model-deficiency-assumption; some Claude-3.7-era ⇒ quarterly-cron candidate
- `sync-public-substrate` self-defers-on-live-agent (companion class-fix same-day)

## 🔗 Composes
[P·always-equals-gate] · [P·universal-coverage-hook] · [P·class-elimination-not-instance-patch] · [F·design-loops-not-prompts] · [P·structure-does-the-work]
