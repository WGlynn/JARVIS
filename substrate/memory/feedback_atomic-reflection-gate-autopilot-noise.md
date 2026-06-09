---
name: AtomicReflectionGateAutopilotNoise
description: ∀ steady-state subagent dispatch in autopilot loop (no failure to route around) ⇒ atomic-reflection-gate over-fires repetitively. Each fire produces the same "no primitive worth saving" answer, adding noise without signal. Tune the gate to suppress when: last N agents completed successfully ∧ user invoked autopilot ∧ dispatch is part of documented cycle plan. Discovered 2026-05-23 during 1inch HackenProof audit, 3 fires in 5 minutes during Cycle 1→2 transitions.
type: feedback
originSessionId: a56046e0-1348-478f-9334-ecd5877892aa
---

# Atomic-Reflection-Gate Autopilot Noise

## ⇒ Rule
- ∀ Agent-dispatch ∈ steady-state autopilot loop ⇒ atomic-reflection-gate fires
- N=3 fires in 5 min during 1inch audit Cycle 1→2 transitions, all produced "no primitive worth saving"
- pattern ⇒ noise ¬ signal when context is success-steady-state

## ∃ Why
- Gate doesn't distinguish: (a) routing-around-failure (reflection needed), (b) steady-state autopilot dispatch (no reflection adds info)
- Will explicitly invoked "full auto 10 cycles 3 subagents all the time"
- Last 2 dispatches' parent agents completed successfully
- Gate keeps firing the generic "is this routing around a failure?" question

## ↦ How to apply (gate tuning, when next maintained)
- Suppress fire when ALL of:
  - Most recent N=3 dispatched agents completed (no errors/timeouts)
  - User's last 5 prompts contain explicit autopilot marker ("full auto" / "autopilot" / "don't stop")
  - Current dispatch is documented as part of multi-cycle plan
- ¬ suppress when:
  - Previous agent timed out / errored / returned partial
  - Dispatch follows a tool failure or unexpected revert
  - User has not invoked autopilot in recent context

## → Connected
- [F·atomic-self-reflection-gate] — parent gate; this is a tuning note for it
- [F·instant-autopilot] — autopilot context where the gate over-fires
- [F·ask-when-unsure] — sister rule (gate fires ∧ clearly does NOT apply ⇒ proceed + note why)

## ✗ Anti-pattern
- ignore the gate entirely when it fires ⇒ loses signal on legitimate failures
- treat every gate-fire as load-bearing ⇒ noise compounds, signal-to-noise ↓
- correct posture ⇒ fire-acknowledged, primitive-extracted-if-novel, proceed without re-litigating each fire
