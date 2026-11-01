# Proposal 0002: a configuration that adapts, inside the constitution

- Proposed by: the Claude Code mind, answering Will (2026-11-01): "what kind of contextual awareness would let us generalize this sort of thing so that we don't need to find as many configuration rules, like an evolving, adapting, generalized configuration set"
- Ratifies: Will only
- Status: open (design; the first piece shipped as a small instance, below)

## The problem

Each slip so far was fixed with one more hand-written rule: a new phrase for the quiet-mode detector, a new verb form for the action gate, a new numbered prompt rule. The list grows, the next phrasing still slips through, and eventually the list itself becomes the thing nobody can read. That works against Article 12 and against trust.

## What the slips have in common

Almost every one falls into one of two classes:

1. **What Jarvis said did not match what was true.** It claimed it saved something when nothing ran, said a chat was "back in tag-only mode" when no mode had changed, or described its own internals from imagination.
2. **Jarvis misread what a room wanted.** It spoke where it was not wanted, or did not notice that it had been asked to stop.

Rules written per phrasing attack the symptoms. Each class has a general fix.

## The design: three layers, in priority order

**Layer 1. Hard rules: the constitution and its code gates.** Fixed, ratified, tested. Never learned, never adjusted by usage.

**Layer 2. Claims checked against state, not phrasings.** Every turn already leaves an event record: the tools that ran, modes that were set, tasks deferred, files written. Instead of listing the ways a reply can say "done", extract the claims a reply makes about actions, modes or facts, and check each kind against that record. A claim with no matching event is removed and logged. One check per kind of state replaces one pattern per phrasing.

- First instance, shipped 2026-11-01: the action gate checks mode claims against the chat's stored mode. "Back in tag-only mode" is removed unless the mode actually changed; "this chat is in tag-only mode" passes only when it is (`jarvis-bot/src/action-claims.js`, tests M1 to M4).

**Layer 3. Learned room norms, bounded by layer 1.** Each chat gets a small, readable model of how that room wants Jarvis to behave: how often it is addressed, how people respond when it speaks unasked (answered, ignored, told off), and which members set the norms. Explicit requests stay hard rules (layer 1). Learning only tunes behavior inside what is allowed, such as how often to chime in while a room is in normal mode. Every adjustment is logged, so the learned state can be audited. The bot already has the seed of this: its per-chat intent learning and room-length matching.

**The loop that makes it evolve: corrections become proposals.** When someone corrects Jarvis ("stop", "you can't respond unless tagged", "that's wrong"), that is recorded as a correction event: its kind and the chat type, never the text. When the same kind of correction recurs, the session drafts a general rule as an amendment proposal. Will ratifies it, it gets a test, and the replay measures it. The configuration evolves, but through Article 11, in the open.

## Why not let it learn everything

A configuration learned silently is exactly what strangers cannot audit, and a model that can rewrite its own rules can rewrite away the ones that bind it. So the hard rules are never learned, the learning stays inside them, and every learned change leaves a record. This is the same order as Physics, then Constitution, then Governance: the invariants first, then free adjustment inside them.

## Honest floor

- Extracting claims and reading intent with a model on free tiers will sometimes be wrong. The deterministic checks stay as the floor.
- Per-room data is thin: a few to a few dozen replies per room per week.
- Layer 2 is only as complete as the event record. An action the record does not log cannot be checked.
- None of layers 2 and 3 beyond the shipped mode check exists yet.

## Steps, smallest first

1. Correction events in the health log (detector assisted by the model, logged by kind).
2. A general claim reconciler: claims extracted per kind and checked against the turn's event record.
3. A room-norms note per chat, written by the session from the feed and read by the bot.
4. Replay metrics for each layer, added to `RESULTS.md`.
