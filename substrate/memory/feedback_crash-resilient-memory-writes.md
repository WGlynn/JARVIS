---
name: Crash-Resilient Memory — Save Planning Context Immediately
description: Session freezes can orphan in-context planning even when files survive on disk. Save project decisions and action status to memory during the session, not just at session end.
type: feedback
---

# Save Planning Context to Memory DURING Sessions, Not Just at End

Files written to disk survive freezes. Conversation context does not. But memory bridges both — it persists across sessions AND survives crashes.

**Why:** On 2026-03-27, a session froze that contained: MIT Bitcoin Expo research, hackathon application status, speaker pitch drafts, a full 3-day itinerary, logistics decisions, and a hackathon build plan. The FILES survived on Desktop, but the CONTEXT (what was submitted, what was drafted, what decisions were made, what's pending) was only recoverable by forensic extraction from `.jsonl` session logs. That took 10+ minutes and multiple tool calls. If the session logs had been corrupted or truncated, the planning state would have been unrecoverable.

**How to apply:**
1. When a session produces non-code planning artifacts (applications, pitches, itineraries, strategic decisions), save a project memory IMMEDIATELY — don't wait for session end
2. The memory should capture: what was decided, what was submitted, what's pending, and where files live on disk
3. SESSION_STATE.md is NOT sufficient alone — it's inside the repo and requires git commit. Memory files are written directly and persist even if the commit never lands
4. Think of it as WAL for planning: write the intent before the action, not after
5. This is the Anti-Amnesia Protocol applied to memory itself — the same principle, one layer up
