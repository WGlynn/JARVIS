---
name: Always verify Vercel deployment
description: After pushing code, always check that Vercel actually deployed — don't assume GitHub auto-deploy works
type: feedback
---

After pushing to GitHub, ALWAYS verify the Vercel deployment actually triggered. Don't assume auto-deploy works.

**Why:** The Vercel project is linked to `frontend/` subdirectory as a separate project (`frontend`, not `vibeswap`). GitHub pushes to the root repo do NOT auto-trigger Vercel builds. Will tested on mobile and saw no changes for multiple commits because nothing was actually deployed.

**How to apply:** After every `git push`, run `cd C:/Users/Will/vibeswap/frontend && vercel --prod` to force a production deploy. Then confirm the URL is live. Never tell Will "give Vercel 60s" without first checking that a build was actually triggered.
