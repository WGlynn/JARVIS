# Odysseus advice contribution graph (live ledger)

Append-only attribution log driving the Shapley contribution-graph in [J·odysseus-mission-loop] Step 4. Every senior dev whose advice meaningfully changed the JARVIS substrate becomes a node, edge weight = advice impact, status flips from `pending` to `actioned` on Will-triage acceptance.

The null-player axiom protects against attribution-padding. The symmetry axiom protects against handle-bias. Negative-contribution entries (rejected advice / unproductive comments) are recorded for graph integrity — Shapley value treats them as zero-marginal-contribution but the rejection signal is itself an honest data point.

## Schema

| field | meaning |
|---|---|
| date | YYYY-MM-DD ET when entry was recorded |
| handle | GitHub handle of contributor |
| thread | issue/PR/discussion # |
| advice-shape | one-line summary |
| impact | substrate the advice maps to (vibeswap / jarvis / both / negative) |
| status | pending / actioned / rejected |
| receipts | commit hash or URL where action landed (if actioned) |

## Ledger

| date | handle | thread | advice-shape | impact | status | receipts |
|---|---|---|---|---|---|---|
| 2026-06-09 | @dustinm16 | PR #720 | importance-scoring + decay + retrieval-boost-only (vs always-inject) | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @pewdiepie-archdaemon | PR #720 review | prompt-behavior changes require explicit product gate | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @RaresKeY | Issue #605 | three-lane separation: issues / mini-ADR / specs | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @nopoz | PR #1314 | CI security-scanning baseline with blocking-vs-advisory split | vibeswap | pending | queue: `_advice-actionable-vibeswap.md` |
| 2026-06-09 | @Anxiety471 | PR #267 | session-state mutability + cross-session leakage discipline | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @akapug | PR #803 | MCP Streamable HTTP + per-server auth headers | jarvis | pending (deferred) | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | (unidentified langIcons.js commenter) | static/js/langIcons.js review | AI-cosplay single-purpose bloat file shape | vibeswap | pending | queue: `_advice-actionable-vibeswap.md` |
| 2026-06-09 | @alvaroperricone | Discussion #2858 | bi-temporal supersession (event-time + transaction-time) | jarvis | pending | queue: `_primitives-pending.md` |
| 2026-06-09 | @vdmkenny | PR #3363 merge style-nit | inline code comments are why-only, not history | jarvis | actioned | `feedback_code-comment-why-only.md` 2026-06-08 |
| 2026-06-09 | @rutsty-rust | Discussion #3684 (cross-ref #3686) | drive-by snark about textwall length, "AI inflation algorithm" frame; no substantive critique | negative | rejected | WGlynn reply "that's not very productive" 2026-06-09T19:50Z |
| 2026-06-09 | @elpideus | Issue #605 | visual status indicator on primitive lifecycle states (?/?/?) | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @hinode-codes | Issue #605 | pain-points-first audit before structural rewrites (Vite already solves their specific complaint but meta-principle applies) | vibeswap | pending | queue: `_advice-actionable-vibeswap.md` |
| 2026-06-09 | @ryslan25500-cloud | Discussion #3684 reply | pure expressive reaction "are you idiot." — no extractable (substrate, change-direction, predicate) tuple | negative | constitutional-axis-1-fail | comment id 17241973, https://github.com/pewdiepie-archdaemon/odysseus/discussions/3684#discussioncomment-17241973 |
| 2026-06-09 | @Amir0234-afk | Discussion #2858 reply | (proximate-cause) question about entity-resolution method forced the write-side embedding-similarity gap into the open; agent-self-surfaced advice that JARVIS needs a write-side embedding fallback to the regex entity-registry | jarvis | pending | queue: `_advice-actionable-jarvis.md`; reply draft at `Desktop/amir-graph-memory-followup-body.md` |
| 2026-06-09 | @RaresKeY | Issue #3694 | merge/review policy stabilization — sensitive PRs require independent review + cooling-off; trivial PRs fast-lane | both | pending | queues: `_advice-actionable-{vibeswap,jarvis}.md` |
| 2026-06-09 | @vdmkenny | PR #3665 | workspace-confine agent file/shell tools via context-local binding at shared path-resolver layer | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @ruanbluiz | PR #3695 | optional container sandbox for agent bash/python tools (defense-in-depth) | jarvis | pending (deferred to JARVIS-publication phase) | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @alteixeira20 | Issue #2523 | test-suite hardening via small incremental PRs vs big rewrite | vibeswap | pending | queue: `_advice-actionable-vibeswap.md` |
| 2026-06-09 | @max-freddyfire | PR #3683 | multi-lingual intent regex coverage extension | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @RaresEduard-Tudor | Issue #3672 | duplicate route handler dead-code detection | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @alteixeira20 | Issue #3699 | mark slow tests from observed duration evidence; data-driven categorization | vibeswap | pending | queue: `_advice-actionable-vibeswap.md` |
| 2026-06-09 | @holden093 | PR #3508 | generic OIDC SSO via authlib (Authentik/Keycloak/Authelia/Google) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @RosenTomov | PR #1122 | LM Studio provider auto-detection via native API | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @glenn2223 | Issue #2475 | unified cross-platform launcher CLI | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @OdWar420 | PR #3697 | dep migration with graceful fallback (no-regress on existing installs) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @RosenTomov | PR #2104 | keyboard-driven command palette UI (ARIA combobox) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @hinode-codes | PR #3424 | UI dropdown state-management fix | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @wwardaww | PR #3384 | skills file upload + rename CRUD | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @kydno | PR #3549 | Kimi provider integration fix | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @Cookiejunky | PR #3689 | NVIDIA CUDA Docker path for llama.cpp | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @Cookiejunky | PR #3647 | Serve panel DI pattern fix | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @RaresEduard-Tudor | Issue #3670 | defensive-DOM null-check pattern | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @glenn2223 | Issue #2918 | AMD GPU acceleration (HIP + Vulkan) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @TimHoogervorst | PR #3661 | UI library-to-chat import | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @RaresKeY | Discussion #3163 | Stabilization-milestone intake lane; maintainer-owned promotion; good-fit candidate list | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @penguman420 | Discussion #3642 | source-to-fact mapping via inline citations; verification UI for receipts traceability | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @NoodleLDS | PR #3360 | stabilize system prompt; sequence memory extraction outside hot path; KV-cache discipline | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @RaresKeY | PR #3613 | fail-closed for null-user owner scope; auth-disabled vs auth-enabled-null distinction | jarvis | pending (deferred to JARVIS-publication phase) | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @alteixeira20 | PR #3659 | fast-lane + duration visibility implementation pattern (infrastructure first, classification later) | vibeswap | pending | queue: `_advice-actionable-vibeswap.md` |
| 2026-06-09 | @NoodleLDS | PR #3540 | JSON list truncation with sentinel marker | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @vdmkenny | PR #3704 | main→dev backport discipline (AGPL relicense) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @michaelxer | PR #3152 | preserve reasoning_content in sanitized messages (provider-specific Moonshot/Kimi) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @TimHoogervorst | PR #3682 | merge duplicate calendar delete endpoints (companion fix to #3672) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @TimHoogervorst | PR #3693 | a11y: aria-label + title on dismiss button | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @alteixeira20 | PR #3685 | pilot core database stub helper for tests | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @OdWar420 | PR #3690 | gzip-compress text HTTP responses | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @arnodecorte | PR #3090 | API token scopes for cookbook | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @Rohithmatham12 | PR #3560 | npx cache subprocess check fallback | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @vdmkenny | PR #3664 | start ChromaDB in start-macos.sh (platform-specific service init) | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @RaresEduard-Tudor | PR #3675 | use _INTERNAL_BASE in serve-session endpoint registration | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @DevSidd2006 | PR #3656 | remove max_output_tokens from ChatGPT Subscription payload | class-c neutral | n/a | `_advice-mined-log.md` |
| 2026-06-09 | @Zaptosis | Discussion #1342 | AGPL over MIT to prevent corporate fork stripping structural mechanisms (44 upvotes) | both | pending | queues: `_advice-actionable-{vibeswap,jarvis}.md` |
| 2026-06-09 | @joebog1 | Discussion #3643 | enforce coding standard from day 1 (PEP8 + black / ESLint + airbnb) | jarvis | pending | queue: `_advice-actionable-jarvis.md` |
| 2026-06-09 | @franfran (ETHSecurity DM) | DM 2026-06-09 17:14 ET | complexity-vs-simplicity inversion frame (Terry Davis quote) became the rhetorical anchor for the Medium essay; Will-stated explicit attribution intent ("you would get half the credit basically") | both | **ACTIONED** | Medium post: https://medium.com/p/8fad2558d9d5 — "Structural fairness has a name" by Blockchain Philosophy, 2026-06-09 17:38 ET; [R·franfran-ethsecurity] |
