---
name: Ottie — Go-based self-evolving crypto AI agent
description: Competitor/peer to JARVIS. Single Go binary, 22 blockchain skills, 9 chains, multi-agent coordination. AGPL-3.0.
type: reference
---

**Ottie** by jiayaoqijia — Go crypto AI agent, single binary, multi-chain.

**Key features:** 22 blockchain skills, 9 chains (incl Base), 13+ messaging platforms, multi-agent via shared task boards, <10MB binary, $5/month VPS.

**Comparison to JARVIS:**
- Their multi-agent coordination = shared task boards (primitive). Ours = CRPC 4-phase commit-reveal (cryptographic).
- Their LLM fallback = provider chain. Ours = Wardenclyffe cascade (same concept, different name).
- Their deployment = single Go binary. Ours = Node + Docker (heavier but more flexible).
- Their skill disclosure = 3 transparency levels. Worth studying for UX.

**Lessons:** Single binary model is elegant. Free-tier API cascade is validated pattern. Progressive skill disclosure is a good UX primitive.

**License:** AGPL-3.0 (study only, can't absorb without open-sourcing)

**Source:** https://github.com/jiayaoqijia/ottie
