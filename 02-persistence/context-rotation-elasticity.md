# Context-rotation elasticity

When a long session approaches the model's context limit, most harnesses do one of two things: nothing (and quietly degrade), or hard-cut at a fixed token count (and abandon valuable in-flight work). Both are wrong for the same reason — they treat rotation as a function of token count alone, when it is really a function of token count *relative to the value of the live thread*.

JARVIS makes rotation **value-elastic**. The decision to keep going or start a fresh chat compares the thread's value-tier against the context cost-tier. A token threshold is a safety floor (write the handoff), not an eviction notice.

## The model

**Value tiers (the thread):**
- **V3 / high** — emotionally loaded, strategic, an irreversible action in flight, an active multi-step build, or the operator is engaged.
- **V2 / medium** — substantive single task that resumes cleanly from a handoff.
- **V1 / low** — question answered, routine status, topic exhausted, or operator idle.

**Cost tiers (context; tunable, high on a 1M-context model):**
- **C0** < 200k — free.
- **C1** 200–350k — elastic.
- **C2** 350–600k — deliberate.
- **C3** ≥ 600k — ceiling (coherence and cost risk).

**The matrix:**
- **C1** → continue for V2 or V3; rotate only V1.
- **C2** → continue for V3 only; state a one-line value-check each +50k.
- **C3** → rotate by default even mid-thread, after a fresh handoff, unless the operator explicitly overrides.
- The handoff refreshes at **every** tier crossing — the unconditional safety floor that makes continuing a free option.

## The two guardrails

The mechanism is two-sided on purpose, so neither party drifts:
- **Anti-over-abuse (operator side):** a low-value thread at C1 should rotate. Don't ride a dead chat to 400k just because it's open.
- **Anti-under-utilize (model side):** a high-value thread below C3 is *never* pressured to retire. Rotation is an offer, not a mandate.

## Why a hook, not a guideline

The hook supplies only the cost-tier (a token count it can measure) and the tier-appropriate framing. It cannot know the thread's *value* — that judgment stays with the model, applied against the live work. This is the division of labor that keeps the rule honest: a mechanical signal can't bluff a value judgment, and a value judgment can't forget to fire.

Implementation: [`01-hooks/context-rotation-hook.py`](../01-hooks/context-rotation-hook.py). Fires once per tier per session (per-tier marker files), refreshes the handoff at each crossing, and emits a `Stop`-hook block with the tier's framing. Thresholds are env-tunable (`CTX_TIER_C1` / `C2` / `C3`).

This is the persistence layer applied to the session itself: the same "don't lose state, and don't waste it" discipline that governs the memory corpus, turned on the conversation that produces it.
