---
name: ship-web
description: Verification checklist that MUST run before declaring any web artifact (HTML, deck, page, doc) "shipped" / "live" / "done." Enforces viewport meta tag, responsive breakpoints, live-URL probe, cache-bust, format-fit. Born from the VibeSwap deck incident 2026-04-20 where viewport meta was missing and Will had to QA mobile three times before Claude caught it. Also triggers on any "deploy" / "push to vercel" / "go live" request for web artifacts.
argument-hint: '<path-or-url-to-verify>  (optional — inferred from conversation if omitted)'
allowed-tools: Read, Edit, Grep, Glob, Bash, Write
user-invocable: true
metadata:
  emoji: "🚢"
---

# ship-web — verify before shipping web artifacts

**When invoked**: You are about to claim (or have just claimed) that a web artifact is shipped/live/done. This skill is the gate. Do NOT skip steps.

**Context**: On 2026-04-20, Claude shipped a VibeSwap pitch deck to Vercel and declared it "live" three times in a row, each time missing something Will had to catch:
1. First ship: `.pptx` — Will couldn't open it (no PowerPoint).
2. Second ship: Pushed to git master — Vercel git-integration was disabled, actual deploy never ran.
3. Third ship: Added mobile CSS — but forgot the viewport meta tag, so mobile Safari ignored the `@media` rules.

This skill prevents all three. Run every step before claiming "done."

---

## Step 1 — Format-fit check (before writing anything)

Ask yourself: **does the user have software to open the artifact I'm about to produce?**

- For visual/layout artifacts: default to **self-contained HTML** unless the user explicitly asks for `.pptx` / `.pdf` / `.docx`. Will has no PowerPoint. HTML + `Ctrl+P → Save as PDF` covers both use cases.
- For documents: `.md` or `.html` — never `.docx` unless explicitly requested.
- If you're unsure, ask. One question beats one useless artifact.

---

## Step 2 — HTML boilerplate (MUST be in every HTML file I produce)

**Non-negotiable head tags**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#000000">
<title>...</title>
```

**Why the viewport meta is critical**: without it, mobile Safari renders at a ~980px virtual viewport and scales the page down. Any `@media (max-width: 900px)` breakpoint I write will NEVER fire. Mobile CSS becomes dead code. This is the single #1 mobile-responsive blocker. It is not optional. It is not something to remember. It is part of the boilerplate.

**Verification after writing**:
```bash
grep -c 'name="viewport"' <file.html>
```
Must return `1` or more. Zero = go back and add it.

---

## Step 3 — Responsive CSS (every slide / section / page)

If the artifact will ever be viewed on a phone (answer: yes, always):

- Include a `@media (max-width: 900px)` block that:
  - Collapses multi-column grids to single column
  - Relaxes any forced `aspect-ratio` that would clip content
  - Sets `overflow: visible` or explicit height handling
  - Shrinks oversize hero typography (96px+ numbers → 48-56px)
  - Moves `position: absolute` footers to `position: static` so they don't overlap content
  - Reduces padding (40-56px desktop → 20-28px mobile)

- Test in browser DevTools at widths: **375px** (iPhone SE/15 portrait), **430px** (iPhone Pro Max portrait), **768px** (iPad portrait), **1280px** (desktop). If DevTools isn't accessible in my flow, open the file locally and inspect structure mentally at each breakpoint.

---

## Step 4 — Deploy verification (if shipping to Vercel / any host)

**Pre-ship**:

```bash
# Verify which host the domain points to (Vercel may not be the source of truth)
curl -sI "https://<domain>/" | grep -i 'server\|x-vercel'

# Verify Vercel deploy pipeline is actually live (not disabled git integration)
cd <frontend-dir> && vercel ls --yes 2>&1 | head -3
# If last deploy timestamp > 1 day old AND there have been git pushes, integration is OFF.
# Use: vercel --prod --yes  to deploy manually.
```

**Post-ship — MANDATORY live probe**:

```bash
curl -sI "https://<url>" | head -10
```

Read the headers:

- `Content-Disposition: inline; filename="<expected-file>"`  ← must match what you deployed
- `Content-Length: <bytes>`  ← should match local file size
- `Age: 0` or small  ← confirms fresh CDN serve

If `filename="index.html"` but you deployed `deck.html` — the SPA rewrite caught your file. File isn't actually on the deploy. Go fix.

If `Age: 339104` or similar huge number — CDN is serving stale cache. Either deploy actually failed, or cache invalidation is slow. Wait 60s and re-probe; if still stale, the deploy is broken.

---

## Step 5 — Cache-bust URL for the user

When you hand the user a URL right after deploying, append `?v=<timestamp>`:

```
https://frontend-jade-five-87.vercel.app/deck.html?v=2
```

This forces their browser to re-fetch, bypassing any local cache that might show them the old version. On mobile especially, iOS Safari aggressively caches pages — even with `Cache-Control: no-cache` headers — if the tab was already open.

---

## Step 6 — Mobile screenshot sanity check

If the artifact is visual and will be shared externally (decks, landing pages, paper previews):

- If I can launch a headless browser: render at 390×844 (iPhone) and 1280×720 (desktop), confirm nothing is cut off at either.
- If I can't: explicitly tell the user I haven't done a real mobile render test, and ask them to screenshot if it looks wrong. Don't fake the verification.

---

## Step 7 — Honest ship claim

After all six steps pass, I can say "shipped" / "live" / "done" with the URL.

If any step fails or is skipped, use language that invites QA:

- "Draft at <url> — please check on mobile, I haven't done a render test yet"
- "Deployed but not verified — try the URL and let me know if it's cut off anywhere"

**Don't claim done when you mean draft.** That's the lie this whole skill exists to prevent.

---

## Project-specific notes

### VibeSwap frontend (Vercel)
- Manual deploy only — see `memory/project_vercel-manual-deploy.md`
- CLI command from `frontend/`: `vercel --prod --yes`
- Takes ~60-90s (upload ~30s + build ~30s)
- Production alias: `https://frontend-jade-five-87.vercel.app`
- Git push to master does NOT auto-deploy. Must run CLI.

### Related memories (load when relevant)
- `memory/feedback_ship-time-verification-surface.md` — the rule this skill enforces
- `memory/feedback_html-over-pptx.md` — default format choice
- `memory/project_vercel-manual-deploy.md` — deploy gotcha

---

## Short form (for when I'm in a hurry)

```
[ ] viewport meta tag present
[ ] responsive CSS covers 375px / 768px / 1280px
[ ] deploy actually ran (vercel ls check)
[ ] curl -sI the live URL — filename matches, Age=0
[ ] give user a ?v=N cache-bust URL
[ ] if I haven't mobile-tested, say "draft" not "shipped"
```

If I skip this checklist and Will catches a bug, I owe him an apology. If I check it and ship clean, it's one interaction not four.
