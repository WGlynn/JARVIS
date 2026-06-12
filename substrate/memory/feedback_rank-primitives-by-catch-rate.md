---
name: rankprimitivesbycatchrate
description: "Will 2026-06-11: primitives/gates should be RANKED by how often they CATCH things (useful-fire rate), and the WORST get the most attention — for improvement OR removal. Telemetry-driven natural selection on the gate layer; anti-bloat. Catch ≠ fire (needs a usefulness signal). Builds on protocol_telemetry.jsonl + *_gate_fires.jsonl + dormancy/memory_to_hook audits."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Rank primitives/gates by catch-rate; worst → improve or remove

> Will 2026-06-11: *"primitives you have should be ranked by how often they catch things, and the worst ones get the most attention for either improvement or removal."*

## ⇒ Rule
- ∀ primitive/gate ⇒ score by **catch-rate**, ¬ mere fire-count.
- **worst performers get the MOST attention** (improve ∨ remove):
  - **dormant** (never fires) ⇒ remove-candidate (dead weight; [P·universal-coverage-hook] says a rule that never fires earns nothing).
  - **hyperactive-low-signal** (fires constantly, catches nothing useful) ⇒ noise ⇒ improve (tighten) ∨ remove. ([F·repetition-is-useless]: a gate firing identical noise ≡ no gate.)
  - **high catch-rate** (fires rarely but catches real issues) ⇒ keep + protect.

## ◈ Catch ≠ fire (the hard part)
- telemetry logs FIRES, not whether the fire was USEFUL. need a **usefulness signal**: did the fire change the output / get acted on / prevent a real error?
- candidate signals: (a) output changed after the gate fired, (b) WWWD-correction followed, (c) Will-acted-on it, (d) caught a verified error (e.g. the Shapley/leak finds this session). without it, fire-count is a weak proxy.

## ⚙ Build path (operationalize)
- data exists: `_system/protocol_telemetry.jsonl` (5382+ events), `aa4_research_gate_fires.jsonl`, `wwwd_gate_fires.jsonl`, `code_mode_nudge_fires.jsonl`, `memory_to_hook_audit`, dormancy detectors.
- ⇒ a periodic **gate-performance triage** (evolution-loop): rank by catch-rate, surface bottom-K for Will-review (improve/remove). natural-selection on the substrate.
- ties: [P·gates-that-gate-and-loops-that-learn] (every log gets a consumer) · [O·cross-context-protocol] · the evolution_proposals loop · [P·what-would-will-do] (corrections feed catch-quality).
- TODO: define the usefulness signal + build the triage ranker (the AFK-corpus-reweight already does a v0 of this for the AFK menu hit-rate).
