---
name: x-thread-char-limit-gate
description: Every X/Twitter thread draft must verify each post <=280 chars BEFORE handing to Will. Drafting to meaning without gating to format = recurring miss.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c68bf9df-70e9-4b3e-bf99-9fdae6ab08ac
---

∀ X/Twitter-thread draft ⇒ verify each post ≤280 chars BEFORE delivery. ✗ draft-to-meaning-only.

**Why:** 2026-06-15 — drafted the "model was never the product" thread for substance, never gated post-length. 6/10 posts overran 280 (286/297/283/290/350/306); priority-hardening edits made 9+10 the worst. Will fixed it by hand and flagged: *"nearly every piece of that x thread went over the character limit."* Format-fit is a hard constraint on X like viewport-meta is on web ([[ship-web]] deck incident shape).

**How to apply:** after writing any thread draft, run a per-post char count (split on `N/` markers, `len(body)>280` → trim) and report PASS before handing over. Counting snippet lives in this session's transcript. Note: X Premium allows long posts, but default constraint = 280/post unless Will says otherwise. Sibling of [[em-dash-filter-for-conversations]] scrub-gate — both are pre-delivery format checks on partner-facing drafts.

**Hook candidate** (per [[always-equals-gate]] + [[universal-coverage-hook]]): PostToolUse Write|Edit on `Desktop/*thread*.md` → scan numbered posts, surface any >280 as a warning. Augmentation not block (Premium exception). Ship pending Will-approval — same pattern as the em-dash gate.
