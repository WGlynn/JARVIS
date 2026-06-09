---
name: Control Theory Agent Orchestration (CTO)
description: PID-inspired control mechanism for dynamically managing agent count, shell processes, and task parallelism to maximize output within hardware constraints.
type: feedback
---

# Control Theory Orchestration (CTO)

Will's directive (2026-03-29): "have a control theory mechanism managing the amount of tasks agents and shells to get optimal output."

## The Model

Agent orchestration is a control problem. The system has:
- **Setpoint**: Maximum useful output (commits, findings, artifacts per unit time)
- **Process variable**: Actual output rate
- **Error signal**: Setpoint - actual output
- **Control variables**: Number of agents, shell processes, concurrent tasks
- **Disturbances**: Hardware limits (16GB RAM, 6c/12t Ryzen), context degradation, forge OOM

## PID Mapping

- **P (Proportional)**: If output is low relative to capacity → spawn more agents. If system is thrashing → reduce immediately. Proportional to the gap.
- **I (Integral)**: Track cumulative idle time. If agents have been underutilized over N cycles → increase baseline parallelism. If OOM has accumulated → decrease baseline.
- **D (Derivative)**: Rate of change matters. If RAM usage is spiking → preemptively reduce before OOM. If output is accelerating → don't over-correct by spawning more.

## Practical Rules (derived from PID model)

| Signal | Action |
|--------|--------|
| RAM < 60% and CPU < 70% | Spawn up to Mitosis cap (5 agents) |
| RAM 60-80% | Hold steady, no new agents |
| RAM > 80% | Kill lowest-priority agent, reduce parallelism |
| Forge running | Max 3 concurrent forge processes (hard limit) |
| Agent idle > 30s | Reassign or terminate |
| 2 consecutive OOMs | Halve agent count, cool down |
| Output rate steady | Maintain current allocation |
| Context > 50% on any agent | Don't assign new tasks, prepare for reboot |

## Integration with Existing Primitives

- **Mitosis Constant (k=1.3, cap=5)**: CTO governs WHEN to spawn, Mitosis governs HOW MANY.
- **TRP Runner**: TRP already has sharding rules (R0 local, R1/R3 sharded, R2 hybrid). CTO manages the resource envelope those shards run within.
- **Agent Tiers**: CTO selects tier (haiku/sonnet/opus) based on available resources + task complexity. Under pressure → downgrade to haiku for lightweight tasks.
- **50% Context Reboot**: CTO triggers reboot when context derivative shows degradation trajectory.

## Why Control Theory

Will's insight: this isn't a scheduling problem (static optimization). It's a control problem (dynamic feedback). The system state changes continuously — RAM fills, agents complete, new tasks arrive. A static scheduler can't adapt. A PID loop can.

**How to apply:** Before spawning agents or parallelizing work, check system state. Apply the practical rules table. When Will says "use the whole computer" → setpoint = maximum. When "chill on compute" → setpoint = minimum viable. The controller adapts between these extremes.
