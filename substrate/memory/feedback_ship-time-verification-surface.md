---
name: Ship-time verification surface
description: Before declaring anything "shipped," test it in its actual usage conditions — responsive for web, live-URL probe for deploys, cross-browser, etc. Don't make Will the mobile QA / deploy QA / browser QA.
type: feedback
originSessionId: feff45da-df5b-4228-8a3c-2871f583acc7
---
# Rule

**Before saying "shipped" / "live" / "done" on any artifact, verify it in every realistic usage condition — not just the one I built for.**

Will's 2026-04-20 prompt:
> "why not just check for these type of things naturally?"

The pattern that earned this rule (same session):
1. Built `.pptx` assuming Will had PowerPoint. He didn't. Needed rescue.
2. Pushed deck to git master, declared it "deploying." Vercel git-integration was disabled. 404 for the user until I actually ran the CLI deploy.
3. Built desktop-only 16:9 deck. Declared "live." Slide 12 cut off on mobile.

Three bugs. Same shape. Each one cost Will a round-trip and visible friction.

## Why

- **Web artifacts ship on every device, not one.** A pitch deck at a public URL is opened on phones by at least half the audience. Responsive is table stakes, not a patch.
- **Deploys aren't "done" when you push.** Done = live URL serves expected content. Curl the URL, check `Content-Disposition`, check `Age`, check the actual bytes match.
- **Files aren't "open-able" just because I produced them.** Confirm the user's software stack can actually consume the format before declaring success.
- **Verification-first is faster.** One curl + one mobile DevTools preview takes 30 seconds. A back-and-forth costs 5 minutes AND erodes trust.

## How to apply

Before I say "shipped" / "live" / "deployed" / "done" on any artifact:

### For web artifacts (HTML, decks, pages, docs)
- [ ] **`<meta name="viewport" content="width=device-width, initial-scale=1">` is non-negotiable.** Without it, mobile Safari renders at ~980px virtual viewport and your `@media (max-width: 900px)` will never fire. Include this **before** writing any responsive CSS. This is the #1 mobile-responsive blocker and it bit us 2026-04-20 on the VibeSwap deck — mobile CSS was correct, viewport meta was missing, spent 3 round-trips before catching it.
- [ ] **Responsive**: render check at 375px (phone), 768px (tablet), 1280px (desktop). Footer not overlapping content. No horizontal scroll. Text not truncated.
- [ ] **Actual URL probe** (if hosted): `curl -sI <url>` — verify `Content-Disposition: inline; filename="<expected>"` and `Content-Length` matches local file.
- [ ] **Font fallbacks**: if pulling Google Fonts, it works — but consider what happens offline.
- [ ] **Cache-bust if I just redeployed**: serve the user a `?v=N` URL so browser cache doesn't lie to them.

### HTML doc starter — include these by default
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#000000">  <!-- or whatever bg -->
```

### For deploys
- [ ] **Verify the pipeline**: git push ≠ deploy unless integration is confirmed. Check last deploy time via `vercel ls` / equivalent. If stale by > a day, integration is probably off — deploy manually.
- [ ] **Live probe**: curl the final URL. Don't trust the build logs alone.

### For files the user will open
- [ ] **Format fit**: does the user actually have the software to open this? (Will has no PowerPoint. Default to HTML / PDF / plain text for visual artifacts.)
- [ ] **Open it yourself first**: if a desktop app is needed, launch it to confirm the file opens cleanly.

### For code changes that affect runtime
- [ ] **Test path covered**: `forge test --match-path <specific test>`.
- [ ] **Adjacent regressions**: if a function is called by N other functions, the test run should exercise at least the hot ones.

## The bigger pattern
This is a special case of "anti-stale feed" applied to my own output. The stale feed isn't just memory — it's my mental model of "what done looks like." Done = user can use it. Not = I wrote the artifact.

When the user shouldn't have to QA me, I've failed the shipping standard.

## Anti-example
- "Shipped at `/deck.html`" (URL returns 404) — this happened. Should have curled first.
- "Deck is beautiful" when mobile slide 12 is cut off — this happened. Should have previewed at phone width.
- "Opens in PowerPoint / Keynote / Google Slides" when user has none of these — this happened. Should have asked what they open files with, or defaulted to HTML.

## When to relax this
Never for "shipped" claims. Sometimes for "here's a draft, check if you like the direction" — that's a different claim, one that invites Will's QA rather than asserting completion. Use that phrasing honestly when I haven't finished verifying.
