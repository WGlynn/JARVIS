# Odysseus advice-mined rolling log

Class-(c) entries (generic-good-design-no-action) and brief notes from each C2.5 sweep. Class-(a)/(b) entries go to `_advice-actionable-vibeswap.md` / `_advice-actionable-jarvis.md`.

Format per row:
```
| date | thread | author | shape (1-line) | class |
```

---

| date | thread | author | shape | class |
|---|---|---|---|---|
| 2026-06-09 | PR #3683 | @max-freddyfire | multi-lingual intent regex coverage extension (Swedish/Norwegian/Danish/German/Spanish/French) | c-neutral |
| 2026-06-09 | Issue #3672 | @RaresEduard-Tudor | duplicate route handler is dead code (FastAPI matches first registration); class: dead-code/route-collision detection | c-neutral |
| 2026-06-09 | PR #3508 | @holden093 | generic OIDC SSO via authlib (.well-known discovery, JWT/JWKS verify); standards-based auth | c-neutral (deferred-to-multi-user-phase) |
| 2026-06-09 | PR #1122 | @RosenTomov | provider-specific behavior detection via native API (LM Studio doesn't accept stream_options); auto-detection over port-heuristic | c-neutral |
| 2026-06-09 | Issue #2475 | @glenn2223 | cross-platform unified launcher CLI (.sh + .ps1 with --launch/--update flags); install/launch UX | c-neutral (deferred-to-JARVIS-publication-phase) |
| 2026-06-09 | PR #3697 | @OdWar420 | dep migration discipline (duckduckgo-search → ddgs) with graceful fallback through prior package names; no-regress on existing installs | c-neutral |
| 2026-06-09 | PR #2104 | @RosenTomov | keyboard-driven command palette UI (double-tap Shift, fuzzy-search across windows/actions/settings, ARIA combobox semantics) | c-neutral |
| 2026-06-09 | PR #3424 | @hinode-codes | UI dropdown state-management fix (group selection recreation/repopulation) | c-neutral |
| 2026-06-09 | PR #3384 | @wwardaww | skills file upload + rename feature (POST /upload, PUT /rename); standard CRUD on uploaded artifacts | c-neutral |
| 2026-06-09 | PR #3549 | @kydno | provider API integration fix (Kimi Code 403 + reasoning_content loss in multi-turn tool-calling) | c-neutral |
| 2026-06-09 | PR #3689 | @Cookiejunky | NVIDIA CUDA Docker path for llama.cpp serving (containerized GPU tooling vs host-dep) | c-neutral |
| 2026-06-09 | PR #3647 | @Cookiejunky | Serve panel restore — shared server-profile resolver injection (DI pattern fix) | c-neutral |
| 2026-06-09 | Issue #3670 | @RaresEduard-Tudor | defensive-DOM-insertion bug (banner inserted-before non-existent element); class: null-check on DOM-anchor before insertBefore | c-neutral |
| 2026-06-09 | Issue #2918 | @glenn2223 | AMD GPU acceleration via HIP (RDNA3+) and Vulkan (RDNA2); platform-specific build path | c-neutral |
| 2026-06-09 | PR #3661 | @TimHoogervorst | UI feature: import from library directly into chat | c-neutral |
| 2026-06-09 | PR #3540 | @NoodleLDS | JSON list truncation with sentinel marker (api_call payload size cap) | c-neutral |
| 2026-06-09 | PR #3704 | @vdmkenny | main→dev backport discipline (AGPL relicense + Cookbook serve) | c-neutral |
| 2026-06-09 | PR #3152 | @michaelxer | preserve reasoning_content during message sanitization (Moonshot/Kimi provider integration) | c-neutral |
| 2026-06-09 | PR #3682 | @TimHoogervorst | merge duplicate calendar delete endpoints (fix for #3672 pattern) | c-neutral |
| 2026-06-09 | PR #3693 | @TimHoogervorst | a11y aria-label + title attributes on dismiss button | c-neutral |
| 2026-06-09 | PR #3685 | @alteixeira20 | pilot database stub helper for test isolation | c-neutral |
| 2026-06-09 | PR #3690 | @OdWar420 | gzip-compress text HTTP responses; bandwidth perf | c-neutral |
| 2026-06-09 | PR #3090 | @arnodecorte | API token scopes for cookbook (RBAC granularity pattern) | c-neutral |
| 2026-06-09 | PR #3560 | @Rohithmatham12 | npx cache subprocess check with graceful fallback | c-neutral |
| 2026-06-09 | PR #3664 | @vdmkenny | start ChromaDB in macOS launcher (platform service-init parity) | c-neutral |
| 2026-06-09 | PR #3675 | @RaresEduard-Tudor | use _INTERNAL_BASE in serve-session route registration (config-driven routing) | c-neutral |
| 2026-06-09 | PR #3656 | @DevSidd2006 | remove max_output_tokens from ChatGPT Subscription payload (provider-payload schema diff) | c-neutral |
| 2026-06-09 | Discussion #3255 | @alex843726351-web | hardware-failure incident report (RTX 4080 SUPER popping during Qwen inference); not an architectural improvement proposal | c-neutral |
| 2026-06-09 | Discussion #3720 | various | "maybe change the name?" — naming bikeshed, no architectural shape | c-neutral |
| 2026-06-09 | Discussion #3691 | various | Docker Desktop on Windows install guide (show & tell) | c-neutral |
| 2026-06-09 | Discussion #3609 | various | Electron desktop wrapper (show & tell) | c-neutral |
| 2026-06-09 | Discussion #3627 | various | Lotse one-command setup for beginners | c-neutral |
| 2026-06-09 | Discussion #1708 | various | bookmarks/highlights/research-queue idea | c-neutral |
| 2026-06-09 | Discussion #789 | various | enabling GPU support — Q&A, not advice | c-neutral |
| 2026-06-09 | Discussion #3651 | various | cloudflare tunnels Q&A | c-neutral |
| 2026-06-09 | Discussion #3655 | various | cookbook downloads stuck — Q&A | c-neutral |
| 2026-06-09 | Discussion #3554 | various | STT/TTS local setup Q&A | c-neutral |
| 2026-06-11 | Discussion #551 | @pewdiepie-archdaemon | GitHub personal-account repos reject triage/maintain collaborator roles; Felix forced to grant write + verbal "treat as triage" convention. Relevant constraint if VibeSwap (also personal-account repos) ever grants contributor triage | c-neutral |
| 2026-06-11 | Discussion #3868 | @Andrarch / @CWhitlockOfficial | injected harness context (skill files, memory) can corrupt model self-report and behavior; clean-session reset as diagnostic. Same shape as JARVIS boot-injection drift risk, diagnosis not action | c-neutral |
| 2026-06-11 | Discussion #3163 | @RaresKeY | #3694 risky-merge re-review rules (when new commits invalidate prior review) -- process shape, no current JARVIS/VibeSwap multi-reviewer surface | c-neutral |
| 2026-06-11 | Discussion #929 | @Dafodilrat | frontend is one 4000-line js file -- monolith maintainability complaint; VibeSwap already componentized React, no action | c-neutral |
| 2026-06-11 | Discussion #3932 | various | Odysseus feature-appeal feedback thread (deep-research praised, mobile UX weak, per-message cost N/A on OpenRouter) -- product-specific | d-skip |
