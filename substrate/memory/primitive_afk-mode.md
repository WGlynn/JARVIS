---
name: afkmode
description: "Story Mode (canonical name, Will 2026-06-12; formerly AFK mode, Will 2026-06-11) — phone-friendly interaction. ∀ response while flag-on ⇒ append numbered top-10 anticipated-user-reply menu derived from per-user signature corpus; bare-number reply ⇒ execute that item, selection logged for corpus learning. Hook-enforced per [P·always-equals-gate]."
metadata: 
  node_type: memory
  type: primitive
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Story Mode (formerly AFK Mode)

> CANONICAL NAME = **Story Mode** (Will 2026-06-12); all hooks/state/docs renamed afk→story. See [[F·afk-mode-aka-story-mode]].

> *"with every response, give me the top 10 most anticipated user (Will) responses... so i can most of the time just reply with a single number"* — Will, 2026-06-11

## ⇒ Rule
- flag `~/.claude/state/story-mode.flag` ON ⇒ ∀ response ends with a menu titled `Story Mode -- reply with a number, or chain several in order (e.g. `3` or `5,4,1`):`, 10 items, most-probable first
- item = complete actionable instruction ≤10 words, executable from its number alone
- mix: ~7 context-specific (the live decision) + ~3 standing signature moves
- bare-number user reply ⇒ execute that menu item from previous response, no confirmation
- toggle: "story on" / "story off" (hook-handled, works from phone; afk aliases kept)

## 📦 Stack (full layer, not a one-off)
- **Hook**: `~/.claude/hooks/story-mode-gate.py` (UserPromptSubmit) — menu enforcement + number interpretation + selection telemetry. Registered settings.json.
- **Signature corpus**: `memory/_system/story_signatures/<user>.json` — per-user probabilistic reply classes derived from REAL history (will.json seeded from 2026-04..06 directives: approve_and_continue 0.18, approve_plus_scope_escalation 0.14, adjust_one_axis 0.12, formalize_or_hookify 0.10, push_public, honesty_probe, absorb_or_remember, status_pivot, draft_for_review, strategic_inference, hold_or_defer)
- **Learning loop**: `<user>_selections.jsonl` — every picked number logged; periodic corpus reweight from actual picks (consult-step closure per [F·design-loops-not-prompts])
- **Per-user**: keyed by user file; new user ⇒ new signature file derived from THEIR history

## ✗ Anti-patterns
- generic menus (continue/stop/explain x10) — items must encode the SPECIFIC live decision
- >10 words per item (phone-scan fails)
- asking confirmation after a number pick
- menu on afk-off confirmations

## 🔗 Composes
[P·always-equals-gate] · [P·universal-coverage-hook] · [P·what-would-will-do] (menu = WWWD projection inverted: predict Will instead of emulate Will) · [F·design-loops-not-prompts] (selection telemetry = fail→verify→distill loop on the corpus)
