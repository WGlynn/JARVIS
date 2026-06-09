---
name: Save task IDs before compression
description: Persist background task/agent IDs to a file before context compresses so they can be checked post-compression
type: feedback
---

When launching background tasks or agents, save their IDs somewhere persistent (e.g. SESSION_STATE.md or a scratch file) BEFORE context compression happens. After compression, task IDs from pre-compression are lost and there's no way to retrieve their output.

Specifically: when at ~10% context remaining and background tasks are still running, write the task IDs to SESSION_STATE.md so the post-compression context can still poll them.
