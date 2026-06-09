# Advice actionable — VibeSwap frontend / contracts / infra

Populated by Odysseus cron loops § COMMANDMENT 2.5 per [F·odysseus-as-advisory-substrate].

Entries below are advice surfaced on pewdiepie-archdaemon/odysseus that the C2.5 classifier judged directly-applicable to our substrate. Each entry awaits Will-triage before any codebase work.

Format:
```
## [YYYY-MM-DD HH:MM ET] — <shape summary>
- Source: #NNNN comment by @author (URL)
- Their advice (paraphrase): ...
- Our substrate state: ...
- Suggested action: ...
- Will-triage: pending
```

---

## [2026-06-09 13:38 ET] — AI-cosplay single-purpose bloat files (langIcons.js shape)

- Source: Odysseus comment id `58plmahm02xg1` (author handle not in Will's paste; comment exists per `static/js/langIcons.js` being a real file in the repo). Reaction: @georgebrianb +1'd and offered CI/CD + autodeploy + LLM-security-check help as their first OSS contribution.
- Their advice (paraphrase): The static-JS shape (huge manual `langIcons.js` lookup file) is "AI cosplaying Odysseus avoiding the draft" — a sprawling hand-rolled artifact for what should be a library lookup or a config-driven mapping. First-order fix: migrate to a real framework + a component framework themed through ONE file.
- Our substrate state: VibeSwap frontend = React 18 + Vite 5 + Tailwind (already a "real framework"; the Nuxt-specific advice does NOT apply). HOWEVER the meta-shape ("AI generated a huge single-purpose file when a library or 10-line config would do") plausibly applies to several places — needs audit, not assumed.
- Suggested action: audit `vibeswap/frontend/src/` for AI-cosplay bloat shapes specifically: hardcoded large arrays/maps (chains, tokens, icons, locale strings), components that re-implement well-known library primitives, theming spread across many files instead of a single source. Output: ranked list of bloat-candidates with size + estimated library replacement.
- Will-triage: pending

## [2026-06-09 13:50 ET] — CI security-scanning baseline with blocking-vs-advisory split

- Source: PR #1314 by @nopoz "ci: security scanning suite and governance (consolidates #305-310)" — https://github.com/pewdiepie-archdaemon/odysseus/pull/1314 . Felix-active.
- Their advice (paraphrase): adds 8 new `.github/` workflows, each scanner is its own workflow with explicit blocking-vs-advisory classification, so the security gate can be required *incrementally* (start advisory, ratchet to blocking per-scanner) rather than all-or-nothing. Consolidates 6 prior per-scanner PRs into one reviewable change. Nothing existing modified.
- Our substrate state: VibeSwap CI status unknown from my context — known to use Foundry tests + Vercel deploy for the frontend. No explicit security-scanning baseline visible in CLAUDE.md. The repo has Solidity contracts + a Python oracle + React frontend, each with different scanner needs (slither for Solidity, bandit/pip-audit for Python, npm audit / Trivy for FE).
- Suggested action: audit `vibeswap/.github/workflows/` to see what scanners exist; if absent, adopt the same advisory-first-then-blocking pattern. Specifically: slither (Solidity), bandit + pip-audit (Python oracle), npm audit + Trivy filesystem (FE).
- Will-triage: pending

## [2026-06-09 15:55 ET] — Merge/review policy as stabilization priority (VibeSwap-side)

- Source: Issue #3694 by @RaresKeY. https://github.com/pewdiepie-archdaemon/odysseus/issues/3694
- Their advice (paraphrase): define explicit review/merge policy v1 BEFORE PR volume scales further. Differentiate trivial (docs/typo) vs sensitive (auth, data-loss, CI, tool execution). Sensitive PRs require independent review + cooling-off window. Latest-commit-changes-after-approval invalidates approval.
- Our substrate state: VibeSwap-side, contracts/incentives/ shapes financial outcomes; contracts/messaging/ touches cross-chain auth; contracts/core/CommitRevealAuction.sol is the MEV-dissolution mechanism. Self-merging changes to these without independent review is exactly the risk-pattern RaresKeY names.
- Suggested action: introduce a `CRITICAL_PATHS` config in `.github/` that tags `contracts/incentives/`, `contracts/messaging/`, `contracts/core/`, plus `script/Deploy.s.sol` and `chain-spec/`. PRs touching these require either second-reviewer approval OR a 24h cool-off before merge. Trivial PRs (docs, comments, test additions) stay fast-lane.
- Will-triage: pending

## [2026-06-09 15:55 ET] — Test-suite hardening via small incremental PRs, not big rewrite

- Source: Issue #2523 by @alteixeira20. https://github.com/pewdiepie-archdaemon/odysseus/issues/2523
- Their advice (paraphrase): test suite has grown; structure is flat; foundations have landed (area markers, focused runner, fast-lane support, duration visibility, import-state helpers, helper docs). Continue improving via small safe PRs rather than a big rewrite. The discipline = keep adding incremental structure without breaking the green-test baseline.
- Our substrate state: VibeSwap test/ has fuzz/, security/, integration/ subdirs already, plus the Foundry profile discipline (default no via_ir, named profiles for full/ci/deploy). Same shape as Odysseus — partially structured, room for incremental tightening (test-helper consolidation, missing area markers on newer test files).
- Suggested action: catalog VibeSwap test/ files NOT under fuzz/security/integration/ and tag them with intended area in a per-test comment header. Audit which helpers in tests/helpers/ are reused vs orphan. Goal: every test file knows its area + every helper has at least 2 callers. Compose with [F·foundry-perf-rules] hardware caps already in place.
- Will-triage: pending

## [2026-06-09 17:55 ET] — AGPL over MIT for VibeSwap contracts/frontend

- Source: Discussion #1342 by @Zaptosis. 44 upvotes. https://github.com/pewdiepie-archdaemon/odysseus/discussions/1342
- Their advice (paraphrase): MIT is inadequate protection if the goal is keeping the work free-as-in-freedom forever. AGPL/copyleft requires distributors to share source with users.
- Our substrate state: VibeSwap is MIT licensed. The thesis is that VibeSwap = coordination primitive, not casino — propagation via adoption matters more than capture-via-token. A proprietary fork of the Solidity contracts that strips the structural-fairness mechanisms (commit-reveal, Shapley distribution, augmented governance) and reskins the surface would defeat the propagation. AGPL prevents that at the license layer for derivative works.
- Suggested action: evaluate AGPL relicense for `contracts/`, `frontend/`, `oracle/`. Smart contract licensing has a wrinkle (on-chain bytecode is technically distributed-on-deploy) — verify the AGPL trigger fires correctly for chain-deployed Solidity. The frontend and oracle are clearer cases. Composes with the JARVIS-side companion entry.
- Will-triage: pending (high-priority constitutional decision; legal review may be appropriate before relicense)

## [2026-06-09 17:50 ET] — Fast-lane + duration visibility implementation (companion to #3699)

- Source: PR #3659 by @alteixeira20. https://github.com/pewdiepie-archdaemon/odysseus/pull/3659
- Their advice (paraphrase): the implementation of the slow-test marking discipline from #3699/#2523. Adds `slow` pytest marker, `tests/run_focus.py --fast` (= `not slow`), `--durations N` forwarded, `--durations-min SECONDS` (only when `--durations` set), validation for negative values, rejection of duration-reporting-only invocations, runner tests. Notably: no tests marked slow IN this PR — slow classification deferred to a small evidence-backed PR later.
- Our substrate state: Foundry has implicit duration-tier behavior via gas reports but no explicit slow-marker convention. The PR pattern (ship infrastructure first, then classify in evidence-backed PRs) is the right shape for VibeSwap test discipline. Compose with #3699 entry.
- Suggested action: scaffold equivalent in Foundry — `forge test --gas-report --json` already exists; add a Will-runnable script `script/test-fast.sh` that filters tests by duration threshold from a previous gas-report JSON. No tests classified slow in the same PR — classification is a separate evidence-backed PR after a week of CI runs.
- Will-triage: pending

## [2026-06-09 16:01 ET] — Mark slow tests from duration evidence (data-driven test categorization)

- Source: Issue #3699 by @alteixeira20. https://github.com/pewdiepie-archdaemon/odysseus/issues/3699
- Their advice (paraphrase): use observed duration data from the focused-runner instrumentation to identify the tests that are actually slow, then mark them so the fast-lane runner can skip them by default. Avoids guessing-which-tests-are-slow vs measuring-which-tests-are-slow.
- Our substrate state: VibeSwap Foundry tests have varying durations; some fuzz tests sweep huge input spaces. `forge test --match-path` is the fast-lane equivalent. We don't currently mark tests by observed-duration tier — devs guess which to skip.
- Suggested action: instrument Foundry to log per-test duration on CI runs, accumulate over a week, then add a `@slow` style marker (Solidity convention via test name prefix or comment) for tests above the 95th-percentile. Update CLAUDE.md foundry rules to add a "fast-lane" variant that excludes `@slow` tests for everyday iteration. Compose with [F·foundry-perf-rules].
- Will-triage: pending

## [2026-06-09 15:09 ET] — Pain-points-first audit before structural rewrites

- Source: Issue #605 comment by @hinode-codes. https://github.com/pewdiepie-archdaemon/odysseus/issues/605
- Their advice (paraphrase): pushing back on "rewrite everything in React" with a list of concrete pain points to solve FIRST: dev-server hot reload (currently full rebuild on every change), established project structure for separation of concerns + tooling discipline (pnpm, biome), routing. Principle: identify the actual operational pain before committing to a structural rewrite that might not address it.
- Our substrate state: VibeSwap-FE is React + Vite + Tailwind. Vite already handles dev-server HMR, so hinode-codes' specific React-critique does not apply directly. BUT the meta-principle (audit current pain points before structural rewrite) IS relevant: VibeSwap has a backlog of refactor temptations (state-management consolidation, component library migration, design-token unification). Each should pass a "what concrete operational pain does this solve" test before going on the roadmap.
- Suggested action: before any VibeSwap-FE structural change leaves the discussion phase, write a one-paragraph "current pain that triggered this" alongside the proposed change. If the pain is not articulable in plain terms, defer the change. Compose with [P·full-leverage-only-moves] — wait until a real pain is total, not partial.
- Will-triage: pending
