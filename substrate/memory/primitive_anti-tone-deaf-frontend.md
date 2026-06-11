---
name: antitonedeaffrontend
description: "Frontend visibility/contrast gate (Will 2026-06-11, named after black-on-black SVG titles shipped live). SVG text paints via fill ¬ CSS color. ∀ text ⇒ computed-contrast ≥ WCAG-AA vs ACTUAL bg. ∀ visual ⇒ render-check before ship-claim."
metadata: 
  node_type: memory
  type: primitive
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Anti-tone-deaf frontend

> Will 2026-06-11: *"names above each venn circle are black text on black background ... you need anti-colorblindness/tone-deafness frontend primitives."* — shipped + deployed before catch.

## ✗ The bug-class (tone-deafness = shipping invisible/unreadable UI blind)
- **SVG text paints via `fill` ¬ CSS `color`.** `<text class="x">` where `.x{color:...}` ⇒ ignored ⇒ defaults `fill:black` ⇒ black-on-black invisible. THE exact bug.
- low-contrast text passed visually on dev-display ✗ readable on phone / bright-room / colorblind
- accent color ON its own faint-tint background (e.g. green text on green-.05 fill) ⇒ fails

## ⇒ Rules
- SVG `<text>` ⇒ set `fill` (attribute ∨ `svg text{fill:}` CSS ∨ `fill:currentColor`). NEVER rely on `color`.
- defensive default: `svg text{fill:<readable>}` ⇒ no element ever falls back to black-on-black
- ∀ text element ⇒ computed contrast ≥ WCAG-AA (4.5:1 body, 3:1 large ≥24px/≥19px-bold) vs its ACTUAL rendered bg (¬ the assumed bg)
- ✗ accent-on-accent-tint; if accent text sits on a tinted shape, check the composited contrast
- ∀ visual artifact ⇒ ACTUAL render-check (not code-read) BEFORE "shipped"/"done" — [ship-web] already mandates this; THIS reinforces it for color/contrast specifically

## ↦ Pre-ship checklist (add to /ship-web + design-system accessibility dim)
1. grep SVG `<text>` ⇒ each has fill resolved (¬ color-only class)
2. every fg/bg pair ⇒ contrast ≥ AA
3. simulate: greyscale + protanopia/deuteranopia (color ¬ the only signal-carrier)
4. render at 375px + bright-mode, eyeball — code-read ✗ sufficient (this bug code-read clean)

## ∃ Why named
- shipped black-on-black circle titles to vibeswap-vercel live, after an "accessibility pass" same session ⇒ proof code-review ¬ render-check misses contrast. tone-deafness = the aesthetic/a11y blindness class; gets a gate like every other [P·always-equals-gate] surface.

## 🔗 Composes
[ship-web] · [design-system skill a11y dimension] · [P·always-equals-gate] · [F·design-loops-not-prompts] (render-check = the verify step)
