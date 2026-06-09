---
name: Signed intent binds security property
description: ∀ defense mechanism w/ signed hash ⇒ signed-bytes MUST bind every property cited in the security claim. Mutable post-sign state ¬ load-bearing. Surface 2026-04-30 after Cerron caught codehash-binding-gap in UUPSUpgradeAdapter PR — public reputation cost.
type: primitive
originSessionId: 588939e2-f831-47b6-8c49-cead6e2a61ba
---
# P·signed-intent-binds-security-property

**Trigger**: ∀ adapter / attestation / commitment / signed-hash with a security claim ⇒ before publishing, verify each property in the claim is INSIDE the signed bytes (¬ in mutable policy).

## Anti-pattern (the bug Cerron caught)

```
intentHash binds {target, value, impl_addr, callDataHash}
policy carries {expected_codehash}  ← MUTABLE via setImplCodehash
docstring claims "CREATE2-redeployment defense"
```

**Attack**: redeploy impl_addr w/ new code ∧ owner updates policy.expected_codehash ⇒ old signatures still valid ⇒ defense ✗ holds.

Mutable-policy-substitution defeats the stated defense entirely. The signature did NOT authorize the bytecode that ends up running — only the address.

## Correct pattern

∀ property cited in security narrative ⇒ inside the signed hash.
Mutable policy = defense-in-depth (extra layer) ¬ load-bearing (the layer the claim depends on).

For UUPS upgrade specifically:
- Bind `(target, value, newImpl, callDataHash, expectedCodehash)` in intentHash
- validate() recomputes intent + checks `newImpl.codehash == expectedCodehash` from signed value
- intentHash() also fails closed for unallowed proxies/impls (¬ just validate)
- Reject `newImpl.code.length == 0` (empty-code impl bricks the proxy)

## Why (2026-04-30 incident)

> *"the implementation codehash is only checked against mutable adapter policy during validate(), but the codehash is not included in the signed intentHash. ... If the implementation address is redeployed with different code and the adapter policy is updated before execution, the old signatures can still authorize the upgrade."* — Uwe Cerron, PR #2, uwecerron/intent-guard

I shipped UUPSUpgradeAdapter to public fork + upstream PR. Cerron caught the gap in <2h. Reputation cost: a security-claiming defense that doesn't defend against the claimed threat IS WORSE than no defense — it's false security.

## How to apply

1. Write the threat in 1 sentence BEFORE writing the adapter (e.g. "CREATE2-redeployment of approved impl address").
2. For each load-bearing noun in the threat sentence: trace where it's bound.
   - Bound in signed-bytes ⇒ ✓
   - Bound in mutable post-sign state ⇒ ✗ → fix
3. `intentHash()` MUST fail closed for inputs `validate()` rejects.
4. Run the "if the policy changes between sign and execute, does the security argument still hold?" check.

## Detection heuristic (review checklist)

- ∃ `setX(...)` owner can mutate after signing
- ∧ `X` is referenced in the security docstring
- ∧ `intentHash()` does NOT include `X`
- ⇒ vulnerability — fix by binding `X` in the intent

## Class of bugs

- "Binding the address but not the bytecode"
- "Binding the action but not the recipient"
- "Binding the call but not the asset"
- General form: bind ALL nouns the security claim depends on; mutable policy is for defense-in-depth, not the load-bearing layer.

## Related

- F·verify-credentials-before-publishing (verify before public push)
- P·empty-repo-test (descriptions must reconstruct artifact ⇒ implementation must match descriptions)
- F·partner-facing-substance-gate (term-vs-mechanism mismatch at doc layer; same pattern at code layer)
- P·anti-stale-feed (verify state before asserting)
- P·dont-make-will-look-dumb (a public-PR vulnerability is the parent shape)
