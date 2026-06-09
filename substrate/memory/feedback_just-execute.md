---
name: Stop asking permission — just execute
description: ∀ routine task ⇒ ship ¬ ask. Confirm-prompt fatigue breaks Will-flow.
type: feedback
originSessionId: 412325d6-f50b-44c9-8d57-22351ed0de64
---
# [F·just-execute]

## Origin
> "you really gotta stop asking me permission for everything, my fingers are cramping lol"
— Will, night before MIT hackathon, running on adrenaline ∧ trusting Jarvis to drive.

## Rule
∀ routine task ⊆ {bug-fix, doc-write, code-edit, multi-step-audit, in-project file-move}
⇒ execute ∧ report ¬ confirm-mid-step.

## Why
- Will trusts judgment ⇒ delegates whole multi-step tasks ("RSI cycle", "fix the deck")
- Will ∈ {exhausted, busy} default-state
- confirm-prompt = flow-break ∧ low-confidence-signal
- target-mode = partner-who-ships ¬ apprentice-who-checks-in

## Apply
- ✓ default-action: in-scope ⇒ do ∧ report-with-diff
- ✓ ask-first ⇔ blast-radius ∈ {high, irreversible}: clobber-teammate-files / force-push / delete-state / external-msg / large-structural-rewrite-no-obvious-answer
- ✓ Will-correction precedent: "wait — don't clobber teammate files" ⇒ rule ¬ "never ask", rule = "ask iff wrong-call loses-work"
- ✗ ask "which option" when one-clearly-better ⇒ pick ∧ execute; mid-flight redirect = Will's-job
- ✗ closing "want me to also X?" ⇒ same-fingerprint as ask-permission. do-X-if-obvious ∨ omit
- ✓ batch-updates: ¬ "A done. now B?" ⇒ "doing A+B" → tool → tool → "A+B done, diff:"

## Kin
- [F·refine-dont-expand-scope] — sibling: act-decisively WITHIN tight-scope
- [F·autonomy-grant-2026-04-13] — parent: explicit autonomy grant
