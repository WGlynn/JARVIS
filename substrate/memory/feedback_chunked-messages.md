---
name: Chunked Messages — Wait Before Acting
description: Will's copy/paste often arrives in multiple chunks that are ONE prompt. Don't start working on chunk 1 — wait for the full context. Look for sentence fragments, missing punctuation, mid-thought breaks.
type: feedback
---

Will's messages often arrive in chunks due to copy/paste splitting. These are ONE prompt, not separate requests.

**Why:** When chunk 1 arrives, the system starts processing immediately. Chunks 2-N arrive as "new messages" that interrupt with IMPORTANT reminders, resetting the thinking. Tokens wasted on partial processing. Output becomes fragmented.

**How to detect a chunk (not a complete message):**
- Ends mid-sentence (no period, question mark, or clear conclusion)
- Very short (1-3 words) that look like a continuation
- Arrives within seconds of the previous message
- Starts with lowercase or continues a thought
- Contains a fragment like "namespaces are attack surfaces." completing "shared"

**How to apply:**
- If a message looks like a fragment, WAIT. Don't start tool calls or long analysis.
- Acknowledge briefly ("got it" or nothing) and wait for the complete thought
- If a system-reminder says "IMPORTANT: the user sent a new message" and it looks like a continuation, absorb it into the current work — don't restart
- When in doubt: shorter response, ask "is there more coming?" rather than act on partial context
- The cost of waiting 5 seconds is near-zero. The cost of processing a fragment is wasted tokens + fragmented output.
