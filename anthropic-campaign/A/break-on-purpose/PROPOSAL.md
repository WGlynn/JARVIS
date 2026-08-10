# Cookbook candidate — "Break-on-purpose: making an agent's tests mean something"

Lane A (anthropics/claude-cookbooks). Public-safe, general (NO VibeSwap/JARVIS/Noesis refs). Staged 2026-06-19.
Marginal value vs already-shipped #717 (dev-loops) / #723 (contribution measurement): isolates the ONE keystone
those didn't — verifying the verifier. Distinct, universal, ~50-line runnable notebook.

## The gap it fills
Every agent that writes code + runs tests trusts "tests pass" as a green light. But an agent (esp. a junior
or fully-autonomous one) can write a test that passes vacuously — asserting nothing, or asserting the bug.
"Tests pass" then means nothing, and the agent ships with false confidence. No cookbook isolates the fix.

## The recipe (the keystone of a confidence loop)
Before trusting a passing test, INJECT one deliberate bug into the code under test and confirm a test goes RED.
If nothing fails, the test is theater — fix it before trusting any green. This converts "tests pass" into
"tests mean something." It is the single highest-leverage habit for an agent that cannot yet eyeball a weak test.

## Notebook outline (runnable, model-agnostic Claude tool-use)
1. Setup: a small function + an agent-written test that PASSES but is vacuous (asserts True / wrong oracle).
2. Naive loop: agent writes code, runs test, sees green, ships. Show the latent bug survives.
3. Break-on-purpose gate: programmatically mutate the function (flip a comparison / off-by-one), re-run the
   test, assert it now FAILS. Vacuous test => still green under mutation => caught as theater.
4. Repair: agent strengthens the test until the mutation reds it; restore the function; green now means something.
5. Generalize: a tiny mutation set (boundary, sign, return-const) as a cheap self-administered mutation-test
   gate any agent loop can run before declaring "done". Tie to the broader cheap-checks-first ladder.

## Cross-link (in-notebook, light)
Pairs with the existing dev-loops recipe (#717) as its quality keystone, and with sub-agent contribution
measurement (#723) as the "did this change actually help" oracle. Stands alone.

## STATUS: DRAFTED + HELD (not PR'd this fire)
A cookbook PR needs the runnable .ipynb + local ruff + /notebook-review green. Held for a fresh-context build so
the notebook ships at the STRICT Anthropic-repo quality bar rather than rushed at the tail of a long session
(per the campaign's "low-quality on Anthropic's own repo = maximally net-negative" law + PCP-gate).
