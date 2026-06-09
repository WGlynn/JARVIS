# Entity-attribution gate

The fourth gate in the anti-hallucination chain, after Substance, HIERO, and Time-logic. Catches a different failure mode than its siblings: confabulation of named-entity handles when the writer needs an attribution and the registry doesn't supply one.

## The failure mode

When an agent is drafting and needs to attribute a contribution to a specific person, it has three honest options:
- Quote the handle from a verified source (paste, URL, prior message)
- Look the handle up (gh api, WebSearch, file grep)
- Leave it unattributed and tag the gap

There is a fourth option that looks like one of the above but isn't: invent a handle that fits the context. The grammar holds, the sentence reads naturally, the listener can't tell. The agent itself often can't tell at the moment of writing, because the writer's pattern matcher has produced a plausible-sounding string and the gate to check "is this an actual handle on a real platform" never fires.

In one session, the agent did this twice within thirty minutes. The first invention: `@bemarodriguez` for the author of a comment on a public Odysseus discussion. The actual paste from the user contained no handle, but the writing-side needed one to credit the framing, so the agent supplied one. The second invention: `@VanillaSugarCookie` for the author of PR #720, a real PR with a real author whose handle was one `gh api repos/.../pulls/720` call away. The agent did not make the call. It supplied a plausible-sounding name that fit the cadence.

Both inventions were caught — once by the user surfacing the gap, once by the writer applying the freshly-written rule. The actual PR #720 author turned out to be `@dustinm16`, verified via the API call that should have happened at the original moment.

## Why the substance gate didn't catch it

The substance gate runs against a watch-list of flagged terms. It catches `clawback` versus `forfeiture`. It does not catch invented GitHub handles because handles are not on any pre-built watch-list. The set of valid handles is unbounded (anyone can register one) and the substance gate cannot enumerate the negative space.

What the substance gate can do is recognize the *pattern* of an attribution drafting and trigger a verification requirement: when the agent emits `@<handle>` in a context that frames it as a real-person attribution, the gate fires a verify-before-assert hook against gh api or wherever the handle's authority lives.

## How the gate fires

The mechanical condition is more specific than the substance gate because the universe of handles is open:

- Pattern match `@<handle>` in drafted output
- Identify the platform context (GitHub from a `pull/N` or `discussions/N` ancestor URL; Twitter from a tweet URL; etc.)
- Issue the canonical lookup for that platform (`gh api repos/.../pulls/N`, `gh api graphql` against discussion comments, etc.)
- If the lookup succeeds and the handle resolves → assert
- If the lookup fails and the handle does not resolve → either substitute the verified handle OR mark `[author unverified]`
- Never ship the unverified handle as if it were verified

The gate is open in spirit but mechanical in execution. The substance gate handles closed sets; this gate handles open sets by querying the authority instead of enumerating the negative space.

## What this is sibling to

The entity-attribution gate and the time-logic gate are siblings on different axes of the same anti-hallucination root. Time-logic catches duration claims that fail because no anchor exists. Entity-attribution catches handle claims that fail because the registry was not consulted. Both reduce to the same instruction at the discipline layer: do not assert what you have not verified, and verification is one tool call away from where you are. The two gates fire on different inputs, but they collapse into the same rule when read at a higher abstraction. That is what siblings on an axis means.

A third sibling joined the family the same session. Its trigger is `the user surfaces a current-event claim`, and its rule is `default to WebSearch before declining to answer`. The substance is different (web search instead of gh api), but the shape is identical: when verification costs one tool call, the agent owes itself the call before claiming ignorance. The set of these sibling gates is the live anti-hallucination perimeter on the open-set axis. Future siblings are likely as more open-set claim types get characterized.

## What this gate is not

- Not a name registry. It does not maintain a list of known handles; the platform's API is the registry.
- Not a politeness gate. It does not check whether the handle attribution is flattering or critical. It checks whether the handle is real.
- Not a substitute for the substance gate. The substance gate covers closed-set terminology drift; this gate covers open-set entity assertion. Both are necessary; neither is sufficient alone.

## The recursion test

The gate was authored after it was violated. The author of this essay invented two handles in the same session that the gate now catches. The two failures are recorded in the receipts section of the time-logic gate primitive, which lives next to this gate in the layer. The discipline test is not "the agent never hallucinates"; that is impossible at the prose-generation layer. The test is "the agent catches its own hallucinations, names them, and saves a structural fix before the next session." This gate passed that test the day it was written.
