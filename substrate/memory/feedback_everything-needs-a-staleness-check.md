---
name: EverythingNeedsAStalenessCheck
description: ∀ signal-source driving autonomous-behavior ⇒ staleness-check mandatory. Stale signals silently dominate live decisions. 2026-06-10 Will-rule after autonomous-continue.py shipped without staleness check ⇒ fired decision:"block" against 24d-old WAL + 17d-old AUDIT_INDEX every Stop. Class-fix per [P·universal-coverage-hook].
type: feedback
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Everything Needs a Staleness Check

## Glyph

```
∀ signal ∈ {hook-input, state-file, log, cron-fact, memory-primitive}
  ⇒ embed mtime-cutoff BEFORE consume.
stale ≡ now - mtime > T_signal.
✗ silent-pass ⇒ stale-dominates-live (silent-failure-mode).
✓ explicit-skip ∧ log "stale_signal" event.
```

> *"everything needs a staleness check"* : Will, 2026-06-10

## ⇒ Rule

- ∀ hook reading external-state ⇒ first-gate ≡ mtime-check
- ∀ script-input ⇒ check-freshness BEFORE act-on-it
- T_signal := f(class):
  - WAL ∧ AUDIT_INDEX ⇒ 7d
  - reflection-jsonl ⇒ 24h
  - cron-fact ⇒ schedule-period × 2
  - memory-primitive ⇒ 14d (system-reminder precedent)
- staleness ≡ first-class control-flow ¬ optimization

## ∃ Why

- 2026-06-10 autonomous-continue.py shipped sans staleness-check.
- Fired decision:"block" ∀ Stop vs. May-17 WAL ∧ May-24 AUDIT_INDEX.
- 24d-old ∧ 17d-old signals dominated live decisions silently.
- Caught ⇔ gate spammed 2× in one session.
- Class generalizes: ¬ unique to autonomous-continue.

## ↦ Apply To

- ∀ new hook reading external-state ⇒ mtime-check first.
- ∀ existing hook ⇒ grep `read_text|json.load` sans preceding mtime ⇒ patch.
- class-fix ⊃ single-fix per [P·universal-coverage-hook].
- siblings: [P·anti-stale-feed], [P·boot-hook-fail-loud], [F·act-on-reversible-aligned-moves].

## ⊥ Anti-Pattern

- ✗ "the file exists so trust it" ⇒ existence ⊥ freshness.
- ✗ "cron pushed it ⇒ live" ⇒ schedules drift, file persists post-deletion.
- ✗ silent-pass on read ⇒ stale-domination invisible until N-instance noise.
