---
name: lithos-soham-ide-backend
description: "Lithos = Soham's Embedded Vibe-Coding IDE backend; Will building it after weeks of delay. State + paths."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6a926587-2dbf-4bc1-97f4-b2712827f26a
---

**Lithos** (`evcide`) ⇒ Python/FastAPI backend ∀ **Soham's Embedded Vibe-Coding IDE** (Void IDE = frontend). moat ≡ runtime-verification @ real-HW ¬ flashing.
- repo `github.com/S0hamJosh1/Lithos` (Soham's) · branch `feat/python-backend-scaffold` · local `C:/Users/Will/Lithos/`
- origin: long-deferred ⇒ 2026-06-17 full-auto ship to clear the backlog.

**State** (2026-06-18, head `0f78870`): **96 ✓** (was 40). Python 3.12 · ruff-clean · atomic-commits. SOLO HW-INDEPENDENT SURFACE = **EXHAUSTED**.
- shipped-since-40: repair-v2(prompt) · break-on-purpose(`mutation.py`,`/contracts/assess`) · closed-loop(`run_repair_loop` best-of-N) · `SettingsFixProvider` · contract-DSL(`dsl.py`,`/contracts/parse`) · capture/replay · workspace-facade · `assess_minimality` lib + **`/contracts/minimality` endpoint** (2026-06-18, leave-one-out dual of /assess).
- **PR myth busted**: `feat/python-backend-scaffold` IS the default+only branch, ¬ fork ⇒ ∄ PR to open; commits already live. ✗ fabricate PR.
- **combinatorial-mutation DECLINED** = vacuous (monotone model ⇒ combos add ∄ kills over singles). ✗ ceremony-build. = ponytail applied.

**Why:** real-partner deliverable ⇒ ship the long-deferred backend.

**How to apply:** "continue Soham/Lithos/IDE-backend" ⇒ read `Lithos/HANDOFF.md` (the contract, current) → `docs/DEVELOPMENT.md`.
- ⚠ ALL remaining work is EXTERNALLY BLOCKED ⇒ do NOT re-attempt autonomously:
  - real-HW (XIAO nRF52840 Sense): validate BLE-`bleak` + `west` build/flash ; STM32/ESP32/RP2040 adapters ; ROS-receiver
  - source-level `FixProvider`: needs LLM-endpoint (seam+prompt ready) — but [[jarvis-tg-bot-free-tier-inference-only]] constraint applies
  - Void-IDE frontend = Soham ; Soham ✗-messaged (Will: "he'll see git history")
- discipline ✓: moat-first ∧ HW-independent+tested-here ∧ honest-stubs(¬fake-PASS) ∧ scoped-commits ∧ verify-before-commit
- kin: [[ponytail-lazy-senior-dev]] · [[structure-does-the-work]] · [[primitives-are-bottleneck-dissolutions]]
