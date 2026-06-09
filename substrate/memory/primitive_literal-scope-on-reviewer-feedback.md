---
name: Literal scope on reviewer feedback
description: ∀ review feedback from a co-dev / maintainer ⇒ act on the LITERAL list, ¬ broaden to "what feels related." Surface 2026-04-30 after I framed Cerron's "drop UUPSUpgradeAdapter + tests + FORK.md" as "drop everything," confused Will, paused execution.
type: primitive
originSessionId: 588939e2-f831-47b6-8c49-cead6e2a61ba
---
# P·literal-scope-on-reviewer-feedback

**Trigger**: ∀ collaborator (PR reviewer, maintainer, co-dev) gives a list of changes ⇒ act on EXACTLY that list. ¬ broaden. ¬ "while I'm at it." ¬ "the equivalent move would be."

## Anti-pattern (the mistake here)

Cerron asked: drop {UUPSUpgradeAdapter.sol, test/UUPSUpgradeAdapter.t.sol, FORK.md}. Keep {.gitignore, .gitmodules, lib/forge-std, foundry.lock, IntentGuardModule.sol with restored assert}.

I framed it as "drop everything else" — wrong. The branch contained ONLY 8 files; I conflated the noisy diff view (working-tree contamination from a separate branch) with the actual branch contents. Will questioned: "why are we dropping everything? is that what he wanted?"

Result: I had to walk it back, re-read Cerron's literal instruction, and proceed with the 3-file drop he actually asked for.

## Correct pattern

1. Quote the reviewer's literal instruction back to yourself.
2. Build a tracked checklist: drop list, keep list, modify list.
3. Execute against the checklist.
4. If you encounter ambiguity, ask the reviewer or the user — don't broaden silently.

## How to apply

**Before action on any reviewer feedback:**

- Write down the LITERAL list (what to drop / keep / change).
- Verify each item exists in the actual scope (don't mentally invent items).
- For ambiguous items: surface the ambiguity, don't resolve by broadening.

**During action:**

- Touch ONLY items on the literal list.
- If diff view shows extra noise (working-tree contamination, unrelated files), pause and reconcile before mass operations.

**Anti-checklist** (things I SHOULD have caught):

- The "60+ file diff" was the working tree, not the branch — but I started narrating "drop everything" anyway. Should have inspected the BRANCH state first.
- "drop UUPSUpgradeAdapter and FORK.md" is THREE files (adapter + test + FORK). I should have counted them and checked the branch had exactly those.

## Detection heuristic

If the reviewer's "drop X" feels like it scales to "drop everything" — pause. Almost always means the working scope is contaminated, OR you're misreading the request.

## Class of error

Pattern-match-broadening on literal instructions. The closest sibling: F·jarvis-prep-not-delivery-for-partner-chat (don't escalate scope of a partner ask). This is the same shape applied to reviewer feedback on code.

## Related

- F·jarvis-prep-not-delivery-for-partner-chat (don't escalate partner scope)
- P·signed-intent-binds-security-property (sister primitive from same Cerron review — bind what you sign)
- P·anti-stale-feed (verify state before asserting)
- F·verify-credentials-before-publishing (verify before public push)
- F·rick-keep-it-simple (depth ✓, volume ✗ — applies broadly to collaboration)
