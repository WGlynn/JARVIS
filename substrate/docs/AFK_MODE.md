# AFK Mode — single-digit steering from a phone

When typing is hard (phone, commute, one hand), every assistant response ends with a
numbered menu of the 10 most probable replies *for this specific user at this specific
decision*. The user steers multi-hour autonomous work by replying "3".

## Why it works
The menu is not generic (continue/stop/explain). It is derived from a per-user
**signature-response corpus**: the reply classes this user actually uses, weighted by
frequency, learned from their real history. Prediction quality compounds: every number
the user picks is logged, and the corpus reweights from actual selections.

## Components
| Piece | Path | Role |
|---|---|---|
| Gate hook | `hooks/afk-mode-gate.py` | UserPromptSubmit: injects the menu contract every turn while the flag is on; interprets bare-number replies as menu selections; logs picks |
| Flag | `~/.claude/state/afk-mode.flag` | On/off switch. The hook handles "afk on" / "afk off" typed (or dictated) by the user |
| Signature corpus | `memory/_system/afk_signatures/<user>.json` | Per-user weighted reply classes. Seed from `hooks/afk_signature_template.json`, then replace examples with the user's real recurring replies |
| Selection telemetry | `memory/_system/afk_signatures/<user>_selections.jsonl` | Every picked number, timestamped. Reweight the corpus from this periodically |

## Install
1. Copy `afk-mode-gate.py` into your hooks dir and register it on the `UserPromptSubmit`
   chain in `settings.json` (timeout 3).
2. Copy the template to `memory/_system/afk_signatures/<user>.json`. Set `AFK_USER`
   env var if the user key is not the default.
3. Derive the corpus: grep your session transcripts for the user's actual short
   directives. Classify into the template's move classes, adjust weights to observed
   frequency. The classes are starting points — add classes your user actually has.
4. Say "afk on".

## Menu contract (enforced by the injected context)
- 10 items, most-probable first; ~7 shaped to the live decision + ~3 standing moves
- each item ≤10 words and executable from its number alone, no follow-up typing
- a bare-number reply executes that item from the previous menu without confirmation

## Design notes
- Enforcement is a hook, not an instruction in memory: "every response" rules decay
  in long sessions unless structurally injected per turn.
- The signature corpus is the per-user inversion of operator-emulation: instead of
  acting as the user, predict the user's next steering input.
- Privacy: the signature corpus and selections stay local (this repo ships only the
  template). Your reply patterns are behavioral data — treat accordingly.
