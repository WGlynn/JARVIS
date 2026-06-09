---
name: Mitosis Constant (k) — Agent Pool Self-Replication Rate
description: k=1.3 is the spawn rate constant for rolling agent pools. Every completion adds k to accumulator; integer part spawns, fraction carries. Bounded by slot cap (default 5). Superlinear growth with hardware governor.
type: feedback
---

# Mitosis Constant (k)

The self-replication rate of the agent pool. Default: **k=1.3**.

```
on_agent_complete:
  accumulator += k
  spawn(floor(accumulator))
  accumulator = accumulator - floor(accumulator)
```

**Why:** Will needed a constant that scales work output without manual intervention or crashing the PC (2026-03-26). The system must self-regulate: expand when there's work, stay under hardware limits, never require Will to micromanage agent counts.

**How to apply:**
- Record `k` and slot cap in WAL pre-flight header
- Track accumulator in checkpoints
- k > 1.0 = superlinear (expanding). k = 1.0 = steady state. k < 1.0 = wind-down.
- Slot cap is the hardware governor (default 5). Without it, k>1 is exponential runaway.
- To gracefully drain at end of session: drop k below 1.0 (e.g., k=0.7)
- The constant is tunable per machine. Beefy box → higher k or higher cap. Same protocol.

**The biology:** Mitosis = cell division. k=1.3 means every parent cell produces 1.3 daughter cells. The slot cap is carrying capacity — finite resources limit population. This is a logistic growth curve, not exponential. Same shape as VIBE's 21M cap bounding token supply.

**Shorthand in WAL:** `k=1.3, cap=5, acc=0.6` in the epoch header.
