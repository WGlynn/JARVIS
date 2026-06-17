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

**State** (2026-06-17): scaffold shipped RED (4/5 ✗) → pushed `86ca8f0` → 40 ✓. Python 3.12 · ruff-clean.
- shipped: timing-windows(within/after_ms) ∧ event-bus+WebSocket-stream ∧ TCP-socket-receiver ∧ project-classifier ∧ BLE-receiver(bleak, **HW-UNTESTED**) ∧ lint-pass ∧ API-endpoint-tests
- 3 pre-existing-bugs ✗→✓: verify-monkeypatch-binding · missing `get_adapter_for_profile` export · `from __future__ annotations` ⇒ all-POST-422

**Why:** real-partner deliverable ⇒ ship the long-deferred backend.

**How to apply:** "continue Soham/Lithos/IDE-backend" ⇒ read `Lithos/HANDOFF.md` → `docs/DEVELOPMENT.md`. NEXT-SESSION TOP (Will 2026-06-17): continue Lithos + **open the PR** (`feat/python-backend-scaffold` → `S0hamJosh1/Lithos`, 8 commits pushed, RED→40✓).
- next ⇒ needs real-HW (XIAO nRF52840 Sense): validate BLE + `west` build/flash
- still-stub: STM32/ESP32/RP2040 adapters ∧ ROS-receiver ; ✗ repair-loop-v2 ; ✗ PR-opened ; ✗ Soham-messaged (held ∀ Will)
- discipline ✓: moat-first ∧ HW-independent+tested-here ∧ honest-stubs(¬fake-PASS) ∧ scoped-commits ∧ verify-before-commit
- ⚠ recurring `</content>` write-artifact ⇒ grep stray-tags BEFORE commit
- kin: [[ponytail-lazy-senior-dev]] · [[structure-does-the-work]]
