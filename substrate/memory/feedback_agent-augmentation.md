---
name: Augment agents better
description: Give subagents better context, instructions, and constraints so they perform at higher quality
type: feedback
---

"You need to augment your own agents better." Agents are being spawned with insufficient context and producing mid-tier results.

**Why:** Will rejected an agent spawn because the instructions weren't good enough. Agents need to be set up for success, not just thrown at problems.

**How to apply:** When spawning agents, include: (1) specific file paths and function names, not just "fix tests", (2) known patterns from this session's fixes as examples, (3) the exact verification command, (4) constraints that matter (RAM, forge profiles). Treat agent prompts like code — precise, complete, tested.
