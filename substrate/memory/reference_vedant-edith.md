---
name: Vedant (Codersparadis210) + EDITH-V2/V3
description: Will's friend building a runtime voice assistant — EDITH. We shipped an augmentation memo mapping our stateful-overlay primitives onto his v3 spec.
type: reference
originSessionId: 5d3519f7-3db7-410c-be60-f32912c41edd
---
## Who

Vedant — Will's friend. GitHub: `Codersparadis210`.

## What he's building

**EDITH-V2** — already shipped. Python runtime voice assistant, not a Claude Code template. Architecture:
- `edith.py` — main launcher
- `personality.py` — roast/voice personality
- `llm_engine.py` — Ollama (local) + Groq (cloud) backends
- `voice_engine.py` — always-on mic + TTS (edge-tts / pyttsx3)
- `filesystem_ops.py` — file R/W + code execution
- `auto_context.py` — project directory scanner
- `gui/app.py` + `hud.html` — Flask + Socket.IO liquid-glass web HUD
- `setup.bat` — Windows one-click install

Repo: https://github.com/Codersparadis210/EDITH-V2

**EDITH-V3 spec** (Will pasted 2026-04-15): production Windows voice assistant. Wake word ("Hey EDITH"), deep OS control with permission gates, autonomous behavioral learning, sleep/activity detection, liquid-glass GUI, .exe installer, plugin system, multi-device sync. Goal: rival Cortana/Gemini/ChatGPT as a daemon assistant.

Tech stack (suggested in spec): Electron/Tauri + Python FastAPI backend, Whisper/Vosk STT, ElevenLabs/Coqui TTS, Porcupine wake word, local Llama or OpenAI LLM.

## What we sent him

1. **`vibeswap/DOCUMENTATION/EDITH.md`** (commit `6926c91b`, 397 lines) — generic Claude Code collaborator template. 12 primitives, memory taxonomy, hooks, safety rails.
2. **`vibeswap/DOCUMENTATION/EDITH_V3_AUGMENTATION.md`** (commit `4da09dc4`, 146 lines) — maps the EDITH.md primitives onto his v3 spec. Six mappings, build-order opinion, callout that sleep/activity detection is the killer feature.

Both are public at github.com/WGlynn/VibeSwap.

## Why this fits our work

Vedant's v3 is a runtime application, ours is a research/DeFi stack, but the **stateful overlay class** is the same. Every primitive that solved a problem in VibeSwap (session state gate, WAL, propose-persist, anti-stale feed, PCP gate) also solves a problem in a voice assistant daemon — often the *same* problem wearing different clothes.

Worth tracking: if Vedant implements the primitives, we have a second substrate (voice runtime vs. developer tool) validating the same patterns. That's convergence evidence for the stateful overlay thesis — the umbrella primitive in `memory/primitive_stateful-overlay.md`.

## How to apply in future conversations

- If Will references "Vedant" or "EDITH-V2/V3," this is the context.
- If Will wants to push updates to the augmentation memo, the file is `vibeswap/DOCUMENTATION/EDITH_V3_AUGMENTATION.md`.
- If Vedant adopts the primitives, note it — that's a data point for the stateful overlay generalization claim.
