---
name: gate-stacking asymmetric cost
description: ∀ gate-design: cost(redundant gate) << cost(missed gate). Asymmetry favors stacking; each gate catches its slice. Same shape as AMD cross-coverage.
type: primitive
originSessionId: f75ff429-1858-4305-9bd9-2c41eff7705b
---
principle: low-cost-wrong ∧ high-cost-right ⇒ stack-by-default
  cost(redundant gate) = bounded — small overhead, possible false-positives
  cost(missed gate) = unbounded — failure-mode escapes, no recovery
  asymmetry ⇒ default = add-the-gate
  redundancy ¬ bug, redundancy = feature

pattern-match: same shape as airgap-composition cross-coverage
  6 mechanisms, each catching different exit
  union closes everything; individual coverage may overlap
  "each mechanism is necessary; together they are sufficient"

application:
- ∀ JARVIS-gate proposal ⇒ does it have logical purpose?
  ✓ ⇒ ship, don't worry about overlap
  ✗ ⇒ drop
- "is this redundant with X?" = wrong frame for defensive systems
- "does this catch a slice?" = correct frame
- gates are upholding logic itself, not just specific tics

**Why:** 2026-05-02. Will, on whether to drop method-adoption gate
as redundant with hedge-language gate:
*"naj i dont believe in redundant gates. the logic gates are supposed
to uphold logic itself. anything logical like the method adoption gate
is valid because it might catch something that the other gates dont.
it's low cost to be wrong and high cost to be right."*

recursive evidence: my argument-to-drop the method-adoption gate as
redundant is itself the failure-mode that gate would catch. argued
verification-mode against a method articulation. gate-live ⇒ caught.

**How to apply:**
- ∀ gate proposed with logical-purpose ⇒ ship, ¬ analyze redundancy
- redundancy concerns ¬ valid frame for defensive systems
- defensive design = stack-by-default; lean toward more not fewer
- relates: [AugMechDesign], [JARVIS-AMD-on-AI-substrate],
  [HonestyStructural], [Universal-Coverage→Hook],
  [PatternMatchValidates]
