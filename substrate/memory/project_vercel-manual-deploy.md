---
name: Vercel manual-deploy only (vibeswap frontend)
description: VibeSwap frontend on Vercel does NOT auto-deploy from git. Must run `vercel --prod --yes` from frontend/ to ship. Discovered 2026-04-20.
type: project
originSessionId: feff45da-df5b-4228-8a3c-2871f583acc7
---
# VibeSwap Vercel — manual deploy only

**Project**: `faradays-projects-43006e53/frontend` (Vercel)
**Alias**: `frontend-jade-five-87.vercel.app`
**Local root**: `C:/Users/Will/vibeswap/frontend/`
**Auth**: Will's Vercel account `tiptaptangsun-8775` — CLI already logged in.

## The gotcha
**Git push to master does NOT auto-deploy.** Vercel's GitHub integration is disabled (or set to manual-only) on this project. Per `vercel ls` on 2026-04-20, last auto/CLI deploy was ~24 days prior — meaning ~3 weeks of master pushes shipped nothing.

Symptoms when you forget:
- New files added to `frontend/public/*.html` return 404 → actually fall through to the SPA rewrite and render stale `index.html` with `Content-Disposition: inline; filename="index.html"` (that's the tell).
- `curl -s https://frontend-jade-five-87.vercel.app/` shows an old `Build: v<timestamp>` comment in the head.

## How to actually ship
From the frontend directory:

```bash
cd /c/Users/Will/vibeswap/frontend
vercel --prod --yes
```

- Takes ~60-90s total (upload ~30s + build ~30s).
- Uploads local working tree (not from git), so whatever is on disk is what ships. Commit first so the git log matches what's live.
- On success: `Production: https://frontend-<hash>-faradays-projects-43006e53.vercel.app` + `Aliased: https://frontend-jade-five-87.vercel.app`.

## How to apply
- Any time Will asks for a frontend change to be "live" / "shared" / "on Vercel" — the git commit alone is NOT enough. Must also run the CLI deploy.
- After any content ship that needs to be publicly accessible (pitch decks, landing pages, papers, public routes): commit → push → `vercel --prod --yes` → verify with `curl -sI <url>` (check `Content-Disposition: inline; filename="<actual-file>"`).
- When verifying, `Age: 0` + correct `filename` = live. Stale `filename="index.html"` when you asked for anything else = SPA fallback = file not on deploy.

## Don't bother with
- Pushing to master expecting auto-deploy.
- Rebuilding via Vercel dashboard hoping git integration will pick up (it won't — integration is off).
- Configuring `vercel.json` to force auto-deploy (that's a Vercel dashboard setting, not a file-level one).

## Future cleanup option
Re-enable GitHub integration via Vercel dashboard → project settings → Git. Trade-off: preview deploys on every feature branch push (nice), but also slower turnaround since every push triggers a build even for docs-only changes. Manual-only is intentional on this project; leave it unless Will asks.
