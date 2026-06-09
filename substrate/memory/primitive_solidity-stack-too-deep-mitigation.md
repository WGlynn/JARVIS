---
name: solidity-stack-too-deep-mitigation
description: Solidity 0.8.20 default profile (no via_ir) stack budget tight @ ~16 slots. Symptom: "Stack too deep · value1 is N slot(s) too deep." ✗ shortcut via FOUNDRY_PROFILE=full unless escape required. ✓ Refactor patterns: split helpers · drop diagnostic events · single-purpose returns · scoped blocks.
type: primitive
originSessionId: 2d5ae2e5-2926-42ce-a369-e66ee74c9c61
---
## Symptom

```
Error: Compiler error: Stack too deep · value1 is 1 slot(s) too deep.
Try compiling with `--via-ir` ... Otherwise, try removing local variables.
```

## ✗ Shortcut

via_ir-everywhere violates `vibeswap/CLAUDE.md` Foundry rule:
> Default profile = via_ir: false. NEVER override to true unless using FOUNDRY_PROFILE=full or deploy. Via IR OOMs this machine when agents run in parallel.

⇒ FOUNDRY_PROFILE=full is legit escape for build-validation, ¬ default.

## ✓ Mitigation patterns (ordered: simplest first)

### Pattern 1: Split N-tuple returns into M < N-tuple returns

✗ `_scanX(...) returns (a, b, c, d, e, f)` ⇒ destructuring at caller eats 6 stack slots.

✓ Split into 2 single-purpose helpers: `_statsX(...) returns (a, b, c)` + `_collectX(...) returns (d, e)`.

⇒ Caller only holds 3 locals at peak; intermediate state ✗ retained.

### Pattern 2: Drop diagnostic events; revert carries same info

✗ `emit ConditionNotMet(taskId, staker, wins, losses, "reason"); revert ConditionError(wins, losses, threshold);`

5-arg event + string-on-stack + 3-arg revert = stack pressure.

✓ Just revert with the error: `revert ConditionError(wins, losses, threshold);`

⇒ Same info to caller (via decoded revert reason); zero stack cost.

### Pattern 3: Extract sub-checks into separate `view` helpers

✗ Long fn body w/ many sequential checks + locals shared across.

✓ `_checkA(taskId)` + `_checkB(taskId)` + `_checkC(taskId)`, each pure single-purpose.

⇒ Each fn has its own stack frame; parent only holds final result.

### Pattern 4: Single-purpose helpers return exactly-sized arrays

✗ buffer-then-trim pattern: `address[] buf = new address[](MAX); ...fill...; finalArr = new address[](count); copy buf → finalArr;`

✓ Two-pass: count first, allocate exact size, fill once:
```solidity
uint256 count = _countX(input);
out = new T[](count);
for (i in input) { if (matches) out[idx++] = ...; }
```

⇒ ✗ buf locals carried alongside output.

### Pattern 5: Scoped blocks `{ ... }` to release locals

✓ ```solidity
{ Bond memory b = vault.getBond(id); staker = b.staker; amount = b.amount; }
// b released; only staker + amount remain in scope
```

⇒ Solidity stack analysis still conservative across scopes but sometimes helps for memory-struct vars.

### Pattern 6: Inline storage reads vs caching

✗ `uint256 threshold = losingThresholdBps; if (x < threshold) ...` (local slot for threshold)

✓ `if (x < losingThresholdBps) ...` (SLOAD inline, no local)

⇒ Gas cost of repeated SLOAD vs stack budget tradeoff. Apply only when stack-pressed.

## When to escalate to FOUNDRY_PROFILE=full

After exhausting patterns 1-6 AND the function is genuinely irreducible (e.g., large math expression, audit-locked logic). Cite explicit reason in commit message. Verify via `forge build --profiles full` round-trips clean.

## Example case

`vibeswap/contracts/consensus/SlashRouter.sol` (2026-05-24) hit stack-too-deep 3× on initial drafts:
- Iter 1: 6-tuple return from _scanSubmissions
- Iter 2: split helpers but kept diagnostic event
- Iter 3: dropped event, default profile compiled

Final form: dispatchSlash + _checkTaskSettled + _checkBondLocked + _adjudicate + _checkStakerIsLoser + _stakerStats + _collectWinners. 7 fns total; each ≤ 7 locals at peak.

## Connects

- `vibeswap/CLAUDE.md` Foundry rule (default profile no via_ir)
- `[P·structure-does-the-work]` — splitting fns IS the structural fix
- `[F·account-model-agnostic]` — sibling at substrate-port layer (different substrate, same kind of constraint forcing minimal-shape design)

## Origin

2026-05-24, mid-SlashRouter build. Three failed compiles taught the lesson; recorded so next contract author doesn't redo the iteration cycle.
