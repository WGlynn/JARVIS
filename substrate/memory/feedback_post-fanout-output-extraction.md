---
name: post-fanout-output-extraction
description: "post-fan-out Workflow/Task .output extraction chokes on Windows (cp1252 stdout + nested result-string wrapper) ⇒ use ~/.claude/bin/wf-extract.py, ✗ inline python"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4148696e-14e5-4f0a-8052-668d7167154b
---

∀ post-fan-out (Workflow ∨ Task) `.output` read ⇒ ✗ hand-write inline python. Chokes 2 ways, every time:
(1) **cp1252 stdout** ⇒ `UnicodeEncodeError` on `→`/`ε`/`⊕`/em-dash; (2) **nested wrapper**
`{summary,agentCount,logs,result}` where `result` = JSON-**string** ⇒ naive `json.load(f)[key]` KeyErrors.

⇒ USE `python ~/.claude/bin/wf-extract.py <file> [key]` (default key=`synthesis`). force-utf8 stdout +
`deep_load` recursive JSON-string parse + BFS `find_key` anywhere in tree. `--keys` lists whole tree;
`--json [key]` pretty-prints non-string values.

**Why:** recurring bottleneck — Will 2026-06-23 *"python always chokes here post-fan-out research"* (choked
2× in one session before the fix). **How to apply:** on Workflow/Task completion, extract via wf-extract,
never inline python. ≡ [[primitive_bottleneck-dissolutions]] + [[primitive_universal-coverage-hook]]
(dissolve-once ¬ re-patch-each-time); sibling of [[feedback_atomic-self-reflection-gate]] (extract
primitive at the friction-moment).
