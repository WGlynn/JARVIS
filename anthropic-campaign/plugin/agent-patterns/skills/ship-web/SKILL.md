---
name: ship-web
description: A verification checklist to run before declaring a web artifact (HTML page, deck, doc) shipped, live, or done. Catches the three failures that survive a casual look — a format the recipient cannot open, a deploy that never actually ran, and a missing viewport tag that silently disables mobile styles. Use right before claiming a web artifact is finished or asking to deploy it.
---

# ship-web

Before you say a web artifact is shipped, run these checks. Each one exists because it is a failure that looks fine until someone else opens the page.

## 1. Format fit

Will the recipient have software to open what you produced? For anything visual, default to a single self-contained HTML file rather than a slideshow or word-processor format, unless they explicitly asked otherwise. HTML opens everywhere and prints to a PDF from the browser. One question about format beats one unopenable file.

## 2. The deploy actually ran

"Pushed to the repo" is not "live." Confirm the deploy pipeline ran and the URL serves the new content: fetch the live URL and check for a string you just changed. If the host's git integration is off, a push deploys nothing and the old page stays up.

## 3. Viewport tag, every time

Every HTML file needs this in the head:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

Without it, mobile browsers render at a desktop-width virtual viewport and scale down, so every `@media (max-width: ...)` rule you wrote never fires and your mobile layout is dead code. This is the single most common mobile-responsive break. Treat it as boilerplate, not as something to remember.

## 4. Cache

After a redeploy, check with a cache-busting request (a query string, or a hard reload) before declaring it fixed, so you are testing the new version and not a cached old one.

Run all four against the specific artifact or URL at hand, and report which passed rather than asserting "done."
