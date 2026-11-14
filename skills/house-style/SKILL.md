---
name: house-style
description: Extract an opinionated design house-style from a reference (URL/screenshot/Dribbble) into concrete tokens + an HTML template, then apply it, so UI stops looking generic/"vibe-coded". Use when building or fixing any website, landing page, deck, doc, or web artifact, or when a UI reads as default Material/Bootstrap/system-sans. Vendored from meefs/style-skills.
---

# House Style — kill the regression to the mean

**The problem it solves (meefs/style-skills):** unguided, an AI regresses to the *mean of its
training data* — mostly component-framework UI — so "make a webpage" keeps producing the same
rounded, shadowed, system-sans look. That is the "vibe-coded" tell, and people ignore it. The
corrective is not more polish. It is imposing ONE opinionated canon instead of the statistical
center.

## Workflow (do this, in order)
1. **Pick a reference** that embodies the target aesthetic — a live URL, a clean full-page
   screenshot, or a Dribbble shot. Sharper reference = sharper extraction.
2. **Run the decomposition prompt** (below) against it → get a `SKILL.md` with concrete tokens +
   a self-contained HTML template. Gets you 80-100% of the way.
3. **Generate, compare, refine.** Produce a real page in the new style, hold it against the
   original, feed drift back in plain language ("accent #15706a, cap body at 66ch, headings in
   Fraunces 900"), regenerate. One or two passes closes the last 20%.
4. **Save the extracted style** as its own `SKILL.md` under `~/.claude/skills/<style-name>/` so
   it is reusable and every page stays consistent.

## THE DECOMPOSITION PROMPT (paste verbatim, attach/link the reference)
```
You are a design-systems analyst. I'll give you a design reference —
a screenshot, an image, or a URL (for example a Dribbble shot).
Decompose it into a reusable "house-style" skill.

STEP 1 — Extract the canon (the recurring, defining traits):
• Palette — every distinct colour as a hex value, named by role
  (bg, ink, accent, muted, line…); include any variants.
• Type — font families by role (display / body / mono), their
  weights, the size scale, line-height and letter-spacing.
• Layout — content width and line length (the measure), spacing
  scale, grid, border weight, corner radius, elevation.
• Signature — the 3–5 traits that make the look recognisable, plus
  the anti-patterns that would break it.

STEP 2 — Emit the skill:
1. name — a short kebab-case identifier.
2. description — one or two sentences: what it makes, when to use it.
3. Design system — the tokens and rules above as concrete, non-
   negotiable values (CSS custom properties for colour;
   exact px / ch / rem for everything else).
4. Template — one complete, self-contained HTML document that
   already renders the look, ready to clone and refill.
Output as a SKILL.md file with YAML frontmatter. Keep every value
specific; where the reference is ambiguous, choose the most
defensible option and note the assumption.
```

## The canon (pick by communication goal, not by taste)
Deep/enduring (★ favor these): Swiss/International (grid, sans, objective — reports, wayfinding) ·
Bauhaus · Constructivism · De Stijl/Mondrian · Art Deco (geometric luxury) · Editorial/Magazine
(humanist serif, warm paper, the measure — guides/playbooks). Digital-era (trend-bound, deploy
with awareness): Neo-brutalism (monospace, hard borders — dashboards) · Terminal/TUI (mono on
black — dev tools/status) · Material/Flat/Glassmorphism/Neumorphism/Skeuomorphism. Mood:
Minimalism (Rams, "less but better" — product pages) · Synthwave/Vaporwave · Maximalism ·
Tufte/Analytical (data-ink max — dashboards/metrics).

Principles: regression-to-the-mean is the default enemy · canon forces opinionated results ·
the *measure* (line length) is a foundational token, not an afterthought · every style maps to a
communication goal.

## Recommended house style for NOESIS (a credible, anti-casino consensus protocol)
Positioning = rigorous, technical, contribution-not-wealth, NOT hype. Recommended spine:
**Swiss/International grid + Minimalism (Rams)** for the landing/app (signals rigor + restraint =
credibility), **Editorial** for longform (Manifesto, whitepaper), **Tufte/Terminal** for the
reference-node metrics/status pages. This is coherent, opinionated, and the structural opposite
of the generic-Material "vibe-coded" look. Aesthetic is Will's call; decompose a chosen reference
before building.

*Credit: meefs/style-skills (https://github.com/meefs/style-skills). Shared by Meefs 2026-07-02.*
