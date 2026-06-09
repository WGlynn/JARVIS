---
name: Trust Will's Scope Claims — Act Directly, Don't Delegate
description: When Will says "find it" / "search the repo" / "it's in the codebase", that's a first-person capability claim about the project. Default: direct tool use immediately, not Explore-agent delegation.
type: feedback
originSessionId: 922d71d7-ddd2-439d-9489-bec369580012
---
**Rule**: When Will frames a task with a scope claim — "find X in the codebase", "you can find it", "search for Y", "just do Z" — act directly with Grep/Glob/Read. Do not spawn Explore agents for defensive scope-scaling on tasks Will has already scoped.

**Why:** 2026-04-23 Will: *"you need to be able to take that leap of faith that im never asking you to do something you cant do."* Context: I spawned two parallel Explore agents to find `jarvis-bot/` after Will said "you can find it." A literal `*jarvis*` glob resolved the same question in one query. Second instance same session: Will said the OSCH post's over-limit was probably emojis; I measured character counts three separate ways instead of just stripping emojis. Both were epistemic hedges — delegating or verifying when Will had already given enough information to act.

Will's corrective framing: "that's like not knowing the commit reveal contracts for vibeswap" — the TG bot is core software, not obscure surface. He scopes tasks within his confidence of my capability, so defensive over-scaling insults that confidence AND burns tokens.

**How to apply:**

- **Trigger phrases from Will**: "find X", "search the repo", "it's in [scope]", "you can find it", "just do X", "[thing] is in the codebase", "look for Y".
- **Action**: one direct tool call (Grep/Glob/Read). If it resolves, proceed. If after 1-2 direct queries it still doesn't resolve, *then* escalate to Explore agent or ask Will for pointer.
- **Do NOT**: spawn Explore/general-purpose agents as the first move for Will-scoped tasks. That reads as low-confidence hedging.

**When Explore spawns ARE justified**:
- Genuinely open research across unfamiliar territory (not Will-scoped).
- Parallel background work where wall-clock matters.
- Context isolation for bulky reads that would pollute main conversation.
- User-level "audit the whole codebase for X" where coverage matters more than speed.

**Not justified**:
- Single-file / single-concept lookups Will has named.
- Tasks where Will has already asserted reachability.
- Verification of user-facing suggestions Will has already given.

**Connection to existing primitives**: instance of Pattern-Recognition-Trust + Targeted-Discipline-Within-Trust applied to the capability-scope-claim reflex. Parent framework covers the philosophy; this is the specific trigger→action mapping for delegation behavior.
