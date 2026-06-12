---
name: storymode
description: "Story Mode automation layer (Will 2026-06-11; named 2026-06-12) — phone-friendly interaction. ∀ response while flag-on ⇒ append numbered top-10 anticipated-user-reply menu derived from per-user signature corpus; number reply (single ∨ chained 5,4,1) ⇒ execute that item(s), selection logged for corpus learning. Hook-enforced per [P·always-equals-gate]. Formerly AFK mode."
metadata: 
  node_type: memory
  type: primitive
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Story Mode

> *"with every response, give me the top 10 most anticipated user (Will) responses... so i can most of the time just reply with a single number"* — Will, 2026-06-11

Canonical name **Story Mode** (Will 2026-06-12, "it's confusing now"); **formerly "AFK mode"** — all hooks/state/docs renamed afk→story 2026-06-12. See [[primitive_gamified-vibe-coding]] (what it IS), [[primitive_story-mode-menu-objective]] (the loss fn), [[primitive_story-mode-meta-convergent-monomyth]] (deeper framings), [[feedback_afk-mode-aka-story-mode]] (protagonist framing).

## ⇒ Rule
- flag `~/.claude/state/story-mode.flag` ON ⇒ ∀ response ends with a menu titled `Story Mode — reply with a number, or chain several in order (e.g. 3 or 5,4,1):`, 10 items, most-probable first
- item = complete actionable instruction ≤10 words, executable from its number alone
- mix: ~7 context-specific (the live decision) + ~3 standing signature moves
- number reply (single ∨ chained `5,4,1`) ⇒ execute that item(s) from previous response in order, no confirmation
- toggle: "story on" / "story off" (afk aliases kept; hook-handled, works from phone)

## 📦 Stack (full layer, not a one-off)
- **Hook**: `~/.claude/hooks/story-mode-gate.py` (UserPromptSubmit) — menu enforcement + number interpretation (single + chained) + impression/selection telemetry. Registered settings.json.
- **Signature corpus**: `memory/_system/story_signatures/<user>.json` — per-user probabilistic reply classes from REAL history (will.json: approve_and_continue 0.18, approve_plus_scope_escalation 0.14, adjust_one_axis 0.12, formalize_or_hookify 0.10, push_public, honesty_probe, absorb_or_remember, status_pivot, draft_for_review, strategic_inference, hold_or_defer)
- **Learning loop**: `<user>_impressions.jsonl` (every turn, pick/off-menu = catch-rate denominator) + `<user>_selections.jsonl` (per-pick = precision); `story-mode-reweight.py` consumes both per [P·story-mode-menu-objective] + [F·design-loops-not-prompts]
- **Per-user**: keyed by user file; new user ⇒ new signature file derived from THEIR history

## ✗ Anti-patterns
- generic menus (continue/stop/explain x10) — items must encode the SPECIFIC live decision
- >10 words per item (phone-scan fails)
- asking confirmation after a number pick
- menu on story-off confirmations
- hiding the multi-pick affordance — the title MUST show `5,4,1` so first-timers see they can chain

## 🔗 Composes
[P·always-equals-gate] · [P·universal-coverage-hook] · [P·what-would-will-do] (menu = WWWD projection inverted: predict Will instead of emulate Will) · [F·design-loops-not-prompts] (telemetry = fail→verify→distill loop on the corpus) · [P·gamified-vibe-coding] (Story Mode = the instance)
