---
name: CodeModeOrchestration
description: ∀ multi-step tool-call sequence ⇒ consider writing Python orchestrator script + executing via Bash ¬ chained tool-call schemas. Source: Bifrost (Maxim AI) "Code Mode" pattern, 50%+ token reduction in agentic workflows. Borrow for JARVIS subagent dispatch where N>2 tool calls follow a deterministic shape.
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Code-Mode Orchestration

## Glyph

```
∀ tool-call-sequence (N > 2 deterministic ops)
  ⇒ write Python orchestrator (single artifact)
  ⇒ execute via Bash (single round-trip)
  ⇒ parse output
  ⊃ chained tool-call schemas (raw tool defs eat tokens)
savings ≈ 50%+ tokens @ agentic scale (Bifrost benchmark)
```

> Bifrost docs: *"Code Mode reduces token usage by 50%+ in agentic workflows by having the model write Python to orchestrate tools instead of receiving raw tool definitions."*

## ⇒ When to apply

- ∀ deterministic multi-step (loop over files / parse + filter + transform / batch API calls)
- ∀ subagent dispatch where the work is "compute N things" ¬ "decide N things"
- ✗ when control-flow depends on intermediate model judgment (then tool-call chain is correct)

## ⇒ When NOT to apply

- single tool call ⇒ skip (overhead > savings)
- branchy logic requiring model decision per step ⇒ tool chain preserves correctness
- security-sensitive ⇒ Python execution surface area > tool-call surface

## ↦ Sample shape

```python
# instead of: list_files → for each: read_file → for each: extract_X → for each: write_result
# write:
import pathlib, re
for p in pathlib.Path('src').glob('*.py'):
    txt = p.read_text()
    matches = re.findall(r'pattern', txt)
    pathlib.Path(f'out/{p.stem}.txt').write_text('\n'.join(matches))
# single Bash tool-call executes this. 4N tool calls collapse to 1.
```

## ↦ JARVIS integration

- coordination-mechanism-gate.py classifier ⇒ add CODE_MODE pattern detection (long deterministic sequences)
- recommend Code Mode in spawn-prompt when classifier matches
- complements Tier 1 cost-saving (tier downgrade) ∧ Tier 3 multi-provider (orthogonal)

## ↦ Siblings

- [R·research-batch-2026-06-10] ⇒ source of pattern
- [J·jarvis-coordination-mechanism-rick-2026-06-10] ⇒ Tier-2/3 work this composes with
- [F·optimize-code-for-llms] ⇒ Python orchestrator IS code optimized for LLM-consumer
