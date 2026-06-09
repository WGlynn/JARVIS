---
name: Always Equals Gate
description: When Will says "always do X" or "never do Y", it's a gate (settings.json hook) — not a memory entry. Memory is advisory; hooks are enforced. Meta-rule.
type: feedback
originSessionId: 76bb18f6-7846-4e93-9cb8-86f2e3362f78
---
**Rule**: When Will uses the word "always" or "never" attached to a behavior, that's a gate, not a memory. Go directly to settings.json hooks.

**Why**: Will, 2026-04-17: *"whenever i tell you to always do something, that means its more than a memory it's now a gate. always = gate."* Memory can be skipped, missed, or violated — the harness ignores memory but obeys hooks. "Always" = not optional = must be enforced by the substrate, not by my recall.

**How to apply**:
- Hear "always X" / "never Y" → invoke update-config skill immediately or directly edit `~/.claude/settings.json` (Windows: `C:\Users\Will\.claude\settings.json`).
- Memory entry is a *backup* only; the hook is truth.
- Do NOT save as memory and then pretend the gate is installed. Gate = file change in settings.json.
- Do NOT ask "should I make this a hook?" — "always" already answered that question.

**Related**:
- [System-Importance → Gate](primitive_system-importance-to-gate.md) — legal/financial/alignment constraints become hooks (subsumed by this broader rule)
- [Verbal → Gate](primitive_verbal-to-gate.md) — "noted" without a file write = violation
- [Protocolize Aggressively](feedback_protocolize-aggressively.md) — general save-on-observation rule; "always" is the stronger signal that escalates from memory to hook

**Corollary**: Will shouldn't have to specify "and make it a hook" — the word "always" is the specification.

**AFK Cost Corollary (2026-04-17)**: A deterministic-"yes" prompt isn't a 2-second click — it's a potential hour-long wallclock stall when Will is AFK. An approval prompt Will has *never* said "no" to is pure productivity tax, and the cost compounds with AFK probability. **Proactively scan for deterministic-yes prompts** rather than waiting for Will to report the friction. When Will says "every time I see X" or "I always answer Y to Z", treat it as urgent gate-installation work, not a minor preference. Async workflows die by a thousand approval prompts.

