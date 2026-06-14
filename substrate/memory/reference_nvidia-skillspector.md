---
name: nvidia-skillspector
description: NVIDIA security scanner for AI-agent skills — detect vuln/malicious patterns before install
metadata: 
  node_type: memory
  type: reference
  originSessionId: a243fa1f-71d7-49fb-8a68-4da07cff6b81
---

## what
- `NVIDIA/SkillSpector` (Apache-2.0, Python 3.12+, ~4.3k★).
- = security-scanner ∀ AI-agent SKILLS (Claude Code / Codex / Gemini CLI).
- thesis: skills run w/ implicit-trust + minimal-vetting.
- stat: 26.1% skills = vuln ∧ 5.2% = likely-malicious.
- Q-answered: "is this skill safe to install?"

## how
- input: git-repo ∨ URL ∨ zip ∨ dir ∨ single SKILL.md.
- 64 vuln-patterns × 16 categories.
- categories: prompt-injection · data-exfil · priv-esc · supply-chain.
- + excessive-agency · output-handling · system-prompt-leak · MEMORY-POISONING.
- + tool-misuse · rogue-agent · trigger-abuse · dangerous-code(AST).
- + taint-tracking · YARA-sig · MCP-least-privilege · MCP-tool-poisoning.
- 2-stage: fast-static + optional LLM-semantic.
- live OSV.dev CVE lookup + offline-fallback.
- out: terminal/JSON/markdown/SARIF + risk-score 0-100.
- run: `skillspector scan <target>` ∨ docker `-v $PWD:/scan`.

## relevance → JARVIS
- JARVIS = skill+hook-heavy ⇒ SkillSpector = pre-adoption gate (scan-before-run).
- memory-poisoning ∧ tool-misuse ∧ trigger-abuse ⊥ JARVIS-memory + autopilot-harness surface.
- aligns [[ground-security-in-vibeswap-design-and-philosophy]] ∧ [[dissolve-attack-surface]].
- skill-trust ≡ knowledge-trust class ⇒ sibling of [[okf-convergence]] trust-layer.
- candidate: SkillSpector-scan in PreToolUse gate ∀ skill-install ∨ CI on `~/.claude/skills`.
