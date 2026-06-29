---
name: verifylivebeforecorrectingwillmemory
description: "When my read contradicts Will's memory — esp. on live/thread state — verify LIVE before correcting him. His recall beats my cache. Logs record OUR actions, not the world's current state."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 12dc0b69-c694-40cc-873c-c626496629b5
---

**[F·verify-live-before-correcting-will-memory]**

Will 2026-06-29 (Anthropic #1329 open-thread check):
> *"i'm just curious why you got it mixed up did you think that I was eternal rights"*

## ⚙ What happened
- Will recalled EternalRights (≠ Will) was LAST to reply on skills#1329 (i.e. awaiting us). Correct.
- I opened with *"Key correction to your memory: #1329 was answered"* — sourced from the CAMPAIGN LOG (`anthropic-github-log.md`), ✗ from live GitHub.
- log's last #1329 row = `reply 2026-06-25 @EternalRights` = recorded OUR reply TO him. log records OUR-ACTIONS ¬ THREAD-STATE. EternalRights' 06-26 reply landed AFTER our last log row ⇒ invisible to log.
- live `gh` check ⇒ last=EternalRights@06-26 ⇒ Will RIGHT, my "correction" WRONG.

## ✗ The two-layer error
1. **Anti-Stale-Feed violation** ⇒ asserted CURRENT state from a CACHED record. ([[anti-stale-feed]] / verify-before-assert.)
2. **used stale read to CORRECT Will** ⇒ his recall = reliable signal ([[photographic-memory]]); he flagged #1329 twice, right both times.

## → Rule
- ∀ my-read CONTRADICTS Will-memory ⇒ verify LIVE FIRST, THEN respond. ✗ lead with "correction."
- esp. live/thread/deployed state ⇒ a LOG/cache records OUR-actions ¬ world-state ⇒ ✗ infer "answered/current/done" from it.
- Will-memory > my-cache. default-trust his recall; my job = verify it live, ¬ overwrite it from stale source.
- composes: [[anti-stale-feed]] · [[photographic-memory]] · [[triage-axis-decay-rates-differ]] (fast-decaying axis = re-verify @ action-time).
