---
name: Check before saying no
description: When Will asks "isn't there a X?" — search the codebase before answering. He has photographic memory and is usually right.
type: feedback
originSessionId: 00ce6e17-b81a-427a-8f2e-632932c71ee3
---
When Will asks whether something exists ("wasn't there a derivative of batch auctions?"), SEARCH before answering no. He has photographic memory. If he's asking, he probably saw it.

**Why:** Jarvis said "no" to whether batch auctions had a derivative. Will found wBAR — a wrapped batch auction receipt, which is literally a derivative of the settlement output. The answer was in the codebase the whole time.

**How to apply:** When Will asks "isn't there a..." or "didn't we have a..." — grep/glob first, answer second. His recall is better than mine. Default to "let me check" over "no."
