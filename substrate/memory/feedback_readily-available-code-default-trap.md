---
name: readily-available-code-default-trap
description: ∀ design problem ⇒ Claude tendency = reach for readily-available code/pattern (OZ template / DeFi idiom / standard library) instead of deriving from required security properties. Pattern-match-drift-on-novelty applied to code architecture. Need: first-principles check BEFORE proposing any contract/component shape.
type: feedback
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## Rule

∀ design problem (contract / data structure / system component):
1. List the load-bearing security properties the component MUST have
2. Derive the minimal shape that has those properties + nothing else
3. ✗ start from "what OZ/std-lib/DeFi-pattern provides"
4. ∀ "let's use $FAMILIAR_PATTERN" ⇒ STOP ∧ check {properties-needed} ⊆ {properties-of-familiar-pattern} ∧ {properties-of-familiar-pattern} ⊆ {properties-needed}. If either ⊄: pattern is wrong shape.

## Why

Claude defaults to patterns weighted heavily in training corpus. For Solidity: OZ ERC20Upgradeable + AccessControl + UUPS. For Python: stdlib + requests + jsonschema. For React: useState + useEffect. For audit prose: "X is structurally enforced via Y."

These are FAMILIAR, not RIGHT for every problem.

The failure mode is `[P·pattern-match-drift-on-novelty]` applied to code architecture: when the problem is novel, the familiar pattern lands BECAUSE it's familiar, not because it fits. The available-code-shape contaminates the derivation; result = correct-shaped-OZ-contract for a problem whose natural shape isn't OZ-shaped.

## Detection

Trigger phrases that smell like "reaching for available code":
- "We can use OpenZeppelin's X"
- "Standard pattern is Y"
- "ERC-20-style"
- "Account-balance model"
- "Standard library has..."
- "Just like LayerZero / Wormhole / CCIP does..."
- "OZ has a helper for that"

Each of these is a candidate for AA#0 substrate-geometry-match-check.

## How to apply

Will-frame 2026-05-14: **"we require an engineer solution, not an Ethereum solution"** and **"you're using code that's readily available instead of searching for a true self-validating solution"**.

Operationalize:
1. State the required security/correctness properties
2. Sketch the minimal shape that has exactly those properties (no more, no less)
3. ONLY THEN compare against available patterns
4. ✓ available pattern = minimal-shape ⇒ use available
5. ✗ available pattern ≠ minimal-shape ⇒ build the minimal shape OR explicitly accept the mismatch with documented reason

## Instances caught 2026-05-14

- **VibeSwapCanonicalToken**: ERC20Upgradeable + AccessControl proposed → minimal-shape = no upgrade, no admin, immutable mint, UTXO-style provenance → significant simplification + stronger structural guarantees
- **post-generation-reflect.py L4 fix**: my "engineer's solution" was still patched-from-existing rather than re-derived → the file persistence + UserPromptSubmit-recovery worked but I almost missed that the right shape was "no Stop hook output at all + UserPromptSubmit pulls history" rather than "Stop hook writes to file"

## Connects

- `[P·pattern-match-drift-on-novelty]` — parent failure mode
- `[P·first-available-trap]` — sibling at architectural level (this primitive operates at code-shape level)
- `[F·audit-aa0-substrate-geometry-first]` — the audit-time application of this discipline
- `[P·substrate-geometry-match]` — the structural property that available-defaults often violate
- `[F·jarvis-amd-applied-to-ai-substrate]` — same recursion at a different level

## Origin

Will-flagged 2026-05-14 ~11:00 ET, two-stage critique during post-LayerZero spec audit:
1. "is an erc-20 that's upgradeable really the right choice for a 'canonical messaging layer'"
2. "you're using code that's readily available instead of searching for a true self-validating solution"

The first nudge revealed I'd defaulted to OZ ERC-20 without first-principles check. The second nudge revealed that even my correction was still reaching for available-code shape (account-balance with privileged minter), not deriving from required properties. The fully-substrate-native shape (UTXO-style canonical token with inline attestation verification) became visible only after the second nudge.

Pattern is recursive: I patch the named instance and stop. Will surfaces the meta. Need to default to AA#0 (substrate-geometry-match-check FIRST) so the meta-pattern doesn't keep recurring at the next abstraction layer.
