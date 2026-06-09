---
name: TRP Session Cap — 6 Rounds Max
description: Cap TRP at 6 rounds per session. Can increase as context density improves.
type: feedback
---

Cap TRP runs at 6 rounds per session. Validated from first multi-round session (2026-04-02): 6 rounds consumed most of the context window.

**Why:** Discovery rounds with 2-3 agents each burn ~20-25% context. After 6 rounds (mix of discovery + cure), context is hot and quality degrades. Agent results accumulate (~10K tokens per discovery round).

**How to apply:** When invoking TRP, track round count. At round 6, stop and suggest reboot for next session. Optimal pattern: 2 discovery + 4 cure-only, or 3 discovery + 3 cure. Can increase cap as model context density improves.
