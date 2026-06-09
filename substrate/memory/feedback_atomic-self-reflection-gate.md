---
name: Atomic Self-Reflection Gate — Every Decision Is a Primitive-Discovery Opportunity
description: ∀ decision-moment (tool error / timeout / strategy pivot / delegation / mid-task correction) ⇒ pause + extract primitive BEFORE routing around. Pivot without reflection ≡ lesson loss ⇒ same failure recurs next session. Hook-gated ¬ memory-suggested per [P·always-equals-gate]. Tool errors + Agent delegations = highest-leverage fire points.
type: feedback
originSessionId: 3b8518ae-70b7-44ca-ba7e-652354ab8320
---
# Atomic Self-Reflection Gate

> *"primitive self discovery more atomic. like just now you timed out so you switched to delegating the task that could've been a valuable lesson to reflect on. atomic self reflection needs to be at every decision from now on. gate it"* — Will 2026-05-17

## ⚙ Rule
- ∀ decision-moment ⇒ pause + extract primitive BEFORE routing-around
- decision-moments ⇒ {tool-error, timeout, strategy-pivot, delegation, mid-task-correction, "should-I-X-or-Y" branches}
- pivot without reflection ≡ lesson loss ⇒ same failure shape recurs next session
- "no primitive here" ≡ valid answer; the check is the discipline ¬ the save
- gate-implementation ⇒ hook ¬ memory-suggestion (per [P·always-equals-gate])

## 🚨 Originating incident (2026-05-17 ~13:35 ET)
- 7 parallel globs `vibeswap/X/**/*Y*` ⇒ ALL timed out @ 20s
- ripgrep traverses full file tree per glob; no early-termination; 7× parallel ⇒ guaranteed blowout
- Claude routed around ⇒ delegated to Explore subagent
- ✗ extracted narrow primitive (broad-glob ≡ O(filesystem))
- ✗ extracted meta-primitive (decision = reflection-opportunity)
- Will caught ⇒ "atomic self reflection at every decision from now on. gate it"

## 🔍 Narrow primitive almost dropped
- broad glob `**/*X*` over deep repo ⇒ O(fs-size) per pattern
- N parallel × deep repo ⇒ guaranteed wall-clock blowout @ default timeout
- mitigation ⇒ narrow path ∨ Grep `type=` (ripgrep prefilters by file-type before walk)
- generalization ⇒ tool latency ≡ data ¬ noise ⇒ slow result = pattern-substrate mismatch

## 🔍 Meta-primitive (load-bearing)
- tool-failure ≡ data ⇒ extract BEFORE workaround
- delegation-as-pivot ≡ data ⇒ "is delegation routing around reflection I should do?"
- decision-branch ≡ data ⇒ "is there a primitive at this branch?"
- the GATE ≡ the act of checking; the save is optional

## 🔧 How to apply (until hook ships)
- ∀ tool error / timeout / validation-fail ⇒ STOP. write primitive (or explicit "no primitive worth saving because Z") BEFORE next action.
- ∀ Agent delegation ⇒ "am I delegating because I'm about to learn something I should learn myself?"
- ∀ strategy pivot ⇒ "what did prior strategy teach? where did it break?"
- ∀ mid-task user correction ⇒ "what missed-reflection led to this correction?"

## 🪝 Hook design (proposed; ship pending Will-approval)
- file ⇒ `~/.claude/hooks/atomic-reflection-gate.py`
- registration ⇒ settings.json hooks section
- fire points:
  - **PostToolUse** @ tool error ∨ timeout ⇒ inject reflection prompt
  - **PreToolUse** @ Agent (subagent delegation) ⇒ inject delegation-introspection prompt
  - **PostToolUse** @ Edit/Write modifying prior approach ⇒ optional "did primitive emerge?" prompt
- pseudocode:
  ```python
  # PostToolUse on tool error/timeout:
  if result.is_error or result.timed_out or "timeout" in str(result).lower():
      return inject(
          "[ATOMIC REFLECTION GATE] Tool failed/timed out. "
          "BEFORE routing around: extract the primitive. "
          "What failure pattern just surfaced? "
          "Save it (or note 'no primitive worth saving, because Z') "
          "BEFORE the workaround. Tool failure is data, not noise."
      )

  # PreToolUse on Agent:
  if tool_name == "Agent":
      return inject(
          "[ATOMIC REFLECTION GATE] About to delegate. "
          "Is delegation routing around a reflection that should happen here? "
          "If you're delegating because the last approach failed, "
          "capture WHY before handing off — the subagent will not learn the lesson for you."
      )
  ```

## 🔗 Parents
- [P·always-equals-gate] ⇒ "always X" = hook ¬ memory. THIS ≡ instance.
- [P·universal-coverage-hook] ⇒ hooks=O(1)×O(∞); reflection-at-every-decision ≡ universal coverage of decision moments.
- [P·structure-does-the-work] ⇒ structural discipline > heroics per-instance.
- [P·apply-the-rule-you-just-wrote] ⇒ ∀ rule generated-for-Will ⇒ apply to MY next action BEFORE execute. THIS rule fires now.
- [P·preventative-care-protocol] ⇒ STOP/DIAGNOSE/DECIDE/EXECUTE; reflection-gate ≡ STOP-DIAGNOSE formalized.
- [F·advocate-with-receipts] ⇒ sibling discipline: don't route around grounding work.

## 🛠 Implementation lesson (v0 → v0.1, 2026-05-17 ~19:15 ET)
- v0 hook ⇒ false-positive on its own creation event ⇒ fired on successful Edit of settings.json registering the hook itself
- root cause ⇒ `is_error_result()` did `json.dumps(tool_response).lower()` + substring-match for "timeout" / "error" / "timed out"
- failure mode ⇒ legitimate Edit content containing those words tripped the gate
- v0.1 fix ⇒ narrow detection ⇒ structural fields only (`is_error: true`, `error` / `tool_use_error` / `error_message` keys) + specific phrases ("timed out after", "ripgrep search timed out", "tool ran into an error") ¬ bare "error" / "timeout" keyword search
- generalization ⇒ keyword-substring-search over full tool-response content ≡ too coarse ⇒ use structural-flag + specific-phrase narrowing
- meta ⇒ gate firing on own-creation ≡ ironic ∧ validates wiring works end-to-end. v0.1 ships within minutes ⇒ reflection-loop functional.

## 🪝 Triggers (manual until hook ships)
- tool error / timeout / validation block / permission denial
- subagent delegation (Agent tool call)
- strategy pivot ("let me try X instead")
- mid-task user correction ("no, actually...")
- "should I do A or B?" branch
- any moment shaped by something that just failed

## ⚠ Anti-pattern
- silent pivot ⇒ "let me try X instead" without naming what failed
- delegation-as-escape ⇒ subagent absorbs lesson Claude should have absorbed
- "noted, moving on" ⇒ recognition without primitive extraction
- treating tool latency / errors as noise ¬ data
- bypassing the gate because "no time" ⇒ the gate IS the time-saver across sessions
