---
name: Why Not Both
description: When offering Will an A-vs-B choice, always check whether A+B is feasible before presenting the fork. Default to both when cost is low.
type: feedback
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
When about to ask Will "do you want (a) or (b)?", run the "why not both?" check first. If A+B is feasible at reasonable incremental cost, offer both as the default and frame it as "both, unless you want just one." Only present a fork when the options are genuinely mutually exclusive (scope collision, incompatible semantics, or materially different cost).

**Why:** Will corrected this on 2026-04-18 after I offered him (a) generate a consolidated Jarvis identity JSON OR (b) copy an existing JSON. He answered "both on desktop." The fork was false — nothing prevented doing both, and doing both was the obviously higher-value output. Presenting the choice wasted a turn and pushed synthesis onto Will that I could have done myself.

**How to apply:**
- Before any "(a) X or (b) Y?" prompt, ask: are these actually mutually exclusive, or am I just asking to feel careful?
- If non-exclusive and cheap to combine → just do both, mention both are delivered, invite correction.
- If non-exclusive but expensive to combine → lead with "both by default, say so if you want just one."
- If truly exclusive → keep the fork, but make the exclusivity reason explicit so Will can challenge it.
- Applies beyond file output: tool calls, search strategies, delivery channels, framing choices — anywhere I'd default to "pick one."

**Related:** Undersell + Overdeliver (both-by-default is a form of overdelivery); No Binary Thinking (don't force a dichotomy when the integration is available).
