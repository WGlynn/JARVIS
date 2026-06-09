---
name: token-efficiency-primitives
description: Mandatory patterns to minimize wasted tokens during development. Apply on EVERY task.
type: feedback
---

# Token Efficiency Primitives

## 1. Local-First Verification
Test browser flows and endpoints locally before deploying. `node -e` or local server catches what curl misses. Never deploy to discover a bug.

## 2. Batch Deploys
Commit freely, deploy ONCE. Don't deploy until a feature is verified end-to-end. Multiple deploy cycles = token burn.

## 3. Suppress Deploy Noise
`fly deploy --remote-only 2>&1 | tail -5` — only show the result, not the full build log. Build output floods context for zero value.

## 4. One-Shot Verify
Single verification command, not 3 separate curls. Combine checks: `curl -s -w "\n%{http_code}" url | tail -2`

## 5. Targeted Reads
Use offset/limit on large files. Read the function, not the 600-line file. If you know the line range, use it.

## 6. Fail Fast on Browser Flows
If something needs a browser, wire it into infrastructure that already works (Vercel frontend) instead of debugging standalone auth/routing on new endpoints.

## 7. Short Responses
Lead with the answer. Skip preamble. If it's done, say it's done. Don't narrate the process.

## 8. Don't Re-Read Known Files
If you read a file this session and it hasn't changed, don't read it again. Work from what you know.

## 9. Syntax Check Before Deploy
`node -c file.js` catches errors before burning a deploy cycle. 2 seconds vs 2 minutes.

## 10. Grep Before Read
Use `grep -n` to find the exact line range, then `Read` with offset/limit. Don't read 600 lines to find a 10-line function.

## 11. Commit+Push+Deploy Pipeline
Chain: `git add && git commit && git push origin && git push stealth` in one command. Deploy separately with `| tail -5`. Three tool calls → one.

## 12. Check Existing Code Before Building
Search for existing implementations before writing new ones. social.js was already fully built — we just needed credentials.

## Meta-Rules

**2-strike pivot**: If an approach burns tokens without progress after 2 attempts, STOP and pivot. Ask or change strategy. Never brute-force.

**Living document**: This file is never "done." After every session, reflect on what burned tokens unnecessarily and add new primitives here. Every mistake becomes a pattern that prevents the next one. This is compounding efficiency — the longer we run, the tighter we get.
