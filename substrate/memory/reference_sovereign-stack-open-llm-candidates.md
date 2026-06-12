---
name: sovereignstackopenllmcandidates
description: "Compact open-weight LLM candidates for prototyping the sovereign JARVIS stack (open-weights migration, [P·open-weights-for-serious-sovereignty]). Modest hardware (Ryzen 5 1600/16GB). Prefer Apache/MIT for true sovereignty. Qwen2.5-7B practical, OLMo-2 maximally-open, R1-Distill for reasoning. 2026-06-11. Knowledge ~Jan 2026 — web-verify latest."
metadata:
  node_type: memory
  type: reference
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Open-weight LLM candidates — sovereign stack prototyping

> For [P·open-weights-for-serious-sovereignty] (Will: "should be using open weights if i want to be serious"). Goal = prove JARVIS gates/chain/PoM run MODEL-AGNOSTIC on open weights; capability stays Claude for now. Hardware: Ryzen 5 1600, 16GB, CPU/small-GPU ⇒ quantized 3B–7B (Q4_K_M) via Ollama/llama.cpp is the sweet spot.

## Recommendations (tiered)
- **Practical / agentic+tool-use:** Qwen2.5-7B-Instruct ∨ Qwen2.5-Coder-7B (Apache-2.0). bot already routes Qwen. 3B for snappier.
- **Reasoning @ small size (mech design):** DeepSeek-R1-Distill-Qwen-7B (MIT); 1.5B ultralight.
- **Maximally sovereign (open weights + DATA):** OLMo-2-7B (AI2, Apache + open data) — auditable/retrainable whole pipeline; the "no strings" proof.
- **Ultralight:** SmolLM2-1.7B (Apache), Llama-3.2-3B (Llama license), Phi-3.5-mini-3.8B (MIT).
- **MoE efficiency:** DeepSeek-Coder-V2-Lite (16B/~2.4B active, MIT).

## Sovereignty license filter
- ✓ truly-open (no strings): Apache-2.0/MIT ⇒ Qwen2.5, Mistral/Ministral, DeepSeek, OLMo, SmolLM, Phi.
- ⚠ restrictive community license: Llama, Gemma.

## The open-model trilemma (Will 2026-06-11: "this sounds like a trilemma")
- 3 axes, pick 2: **sovereignty/openness** (open weights+DATA, permissive) ⊥ **capability** ⊥ **footprint** (local/light).
- fully-open+capable ⇒ heavy; capable+light ⇒ Qwen (Apache) but data ¬ fully-open; open+light ⇒ low capability.
- **dissolution = model-agnostic routing** (JARVIS substrate-independence): assign a CORNER per ROLE ¬ one global pick. prototype=open+light (Qwen-3B/OLMo); sovereignty-proof=open+capable (OLMo-2-7B); hard-reasoning=capable+light (Qwen2.5/R1-Distill). governance layer identical across all ⇒ trilemma binds single-choice, dissolved by routing. same move as [P·dissolve-attack-surface] / [P·filter-coincidence].

## Plan
- start: Qwen2.5-7B (practical prototype) + OLMo-2-7B (sovereignty-pure validation) + R1-Distill-7B (reasoning). via Ollama (bot has Ollama+DeepSeek+Qwen routing already, [J·jarvis-tg-bot-free-tier]).
- 🔗 [P·open-weights-for-serious-sovereignty] · [project_jarvis-asi-sovereign] · [P·jarvis-complements-not-competes-the-model] (substrate-independence ⇒ migration not rebuild).
- ⚠ knowledge ~Jan 2026; web-verify Qwen3-small / Llama-4-small / OLMo-3 / newer R1 distills before committing.
