---
name: Diagnose state before prescribing fix
description: ∀ user-reported error ⇒ diagnose actual system state BEFORE prescribing remediation. Symptom ≠ cause.
type: feedback
originSessionId: 1e564e06-8691-4b72-87f2-6a459bf83873
---
# F·diagnose-state-before-prescribe

∀ user-reported-error ⇒ check actual system-state FIRST, ¬ assume cause from symptom

## Why

2026-05-05 Mac claude-code install. Will reported "command not found" for `brew`. I prescribed full reinstall via curl-pipe-bash. Actual cause = brew installed but ¬ in PATH. Reinstall = duplicate work + extra failure surface (curl 404, dquote-cmdsubst, etc). Will: "no offense but that was poor communication."

## Rule

symptom-reports ⇒ multiple-possible-causes ⇒ MUST diagnose

ex command-not-found:
- cause-A: not-installed ⇒ install
- cause-B: installed-not-in-PATH ⇒ shellenv-fix
- cause-C: aliased-wrong ⇒ unalias

ex permission-denied:
- cause-A: file-perms ⇒ chmod
- cause-B: dir-perms ⇒ chown
- cause-C: SIP/sandbox ⇒ different fix

ex 404:
- cause-A: URL-wrong ⇒ verify URL
- cause-B: paste-corruption (smart-quotes, capitalization) ⇒ retype
- cause-C: network-issue ⇒ retry

## Apply

before recommending fix:
1. ✓ identify candidate causes (≥2)
2. ✓ ask user 5-second diagnostic that DISCRIMINATES (which / type / pwd / ls / cat / version-flag)
3. ✓ prescribe based on diagnostic-result, ¬ symptom-text
4. ✗ "your X is missing, install it" without checking
5. ✗ jump to reinstall before checking PATH
6. ✗ assume worst-case state from limited info

## Failure modes

- ✗ symptom-driven prescription = duplicate-work-best-case, makes-it-worse-worst-case
- ✗ skipping diagnostic to "save time" = often costs more time downstream
- ✗ recommending heavy fix (reinstall, reformat, reset) when light fix (PATH, config) suffices

## Cost

- diagnose-first ≈ +5sec
- wrong-prescription ≈ +5min ∨ more (compounds: each step has its own failure surface)

5sec << 5min ⇒ diagnose-first ALWAYS wins on expected value

## Linked

- [P·legacy-bypass] sibling, don't bypass diagnostics
- [P·sophistication-gap] sibling, don't assume sophistication
- [F·check-before-saying-no] sibling, verify before declaring impossibility
- [F·no-fake-understanding] floor, don't pretend to know state
