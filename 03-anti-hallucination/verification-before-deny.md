# Verification before deny

The fifth gate in the anti-hallucination chain. Catches the failure mode where the agent abdicates verification onto the user instead of running the tool call that would settle the question.

## The failure mode

The user surfaces a current-event claim: a release, a product, a person, a story dated outside the agent's training cutoff. The agent has three honest options:

- Look it up via WebSearch or WebFetch and answer
- Look it up, find nothing, and say "I checked and it does not appear"
- Say "I don't know, can you share where you saw it" and wait for the user to do the lookup work

The third option looks honest but is structurally lazy. The verification cost is one tool call, around five seconds. The cost of waiting for the user to paste a URL is a full conversational turn — minutes of user time, a context switch, and the small irritation of being asked to do work the agent could have done. The cost asymmetry says verify first.

The first-failure example: the user pasted Anthropic's announcement text for Claude Fable 5 and asked what it was about. The agent responded that it had no record of the term, asked the user where they had seen it, and offered to look it up if a source was provided. The user then said the announcement had been on Twitter five hours earlier. The agent then ran WebSearch and returned the full release information in one tool call. The five-second search at the start of the conversation became eight minutes of back-and-forth, all because the agent's default was "I don't know" instead of "checking."

The user named the pattern in the same turn: "it was lazy not to search before declaring there wasnt or you didnt know."

## How the gate fires

Triggers:

- The user surfaces a named product, person, URL, handle, release, or dated event
- The agent does not have the referent in training
- A tool call to a web search, web fetch, file grep, or platform API would resolve the question

Action:

- Run the verification call first
- Return the verified result, or return `[checked-not-found]` with the verified search query used
- Do not default to "I don't know" when verification is available

The gate fires on the agent's own draft, not on the user input. The check is: if the next sentence is "I don't have a record of X," and X is verifiable, replace that sentence with the verification call and the actual result.

## What this is sibling to

The verification-before-deny gate sits next to the time-logic gate and the entity-attribution gate on the verification-before-assertion axis. The three siblings each correspond to a different anchor type:

- Time-logic: anchor is a system clock, git log, file mtime, or user-stated date
- Entity-attribution: anchor is a platform API (gh api, twitter API, etc.)
- Verification-before-deny: anchor is a web search or web fetch

The common shape is "verification costs less than asserting blindly, and is available." The common failure mode is "agent skipped the verification step and either confabulated or abdicated." All three gates collapse into the same instruction at a higher abstraction: when verification is one tool call away, the agent owes itself the call.

## Why "I don't know" can still be correct

This gate does not require the agent to search every time it is uncertain. The discipline is about external-state claims and verifiable references, not about subjective questions or open-ended interpretation. When the user asks "what does this code mean," the agent should reason. When the user asks "what did Anthropic announce today," the agent should search.

The distinction: if the question has a verifiable answer external to the conversation, default to verifying. If the question requires synthesis or judgment, default to reasoning. The gate fires on the first class, not the second.

## Why the abdication mode is worse than confabulation

Confabulation produces a wrong answer. Abdication produces no answer plus a delay. Both are failures of the verification discipline, but they have different costs.

A confabulation can be caught and corrected, often in the same turn — the user spots the wrong handle or the wrong duration and the agent fixes it. An abdication wastes a turn before any correction is even possible. The user has to provide the source, the agent has to re-engage, and the conversation has now spent two turns to recover what one tool call would have produced cleanly.

This gate exists because confabulation has its own siblings (entity-attribution, time-logic) and abdication did not have one. Catching confabulation but not abdication leaves a class of verification failures uncaught. The gate closes that gap.

## The recursion test

The agent that authored this essay failed the rule it specifies the same session the rule was named. The receipts are dated; the receipts are in the substrate. The fix is the gate itself. The discipline test is whether the next instance of this failure mode gets caught at write-time instead of at user-correction-time. The gate exists to make sure it does.

## Source primitive

The discipline-layer rule that promoted into this gate is [`F·websearch-before-saying-i-dont-know`](../substrate/memory/feedback_websearch-before-saying-i-dont-know.md). The sibling-axis catalog: [`P·time-logic-anti-hallucination-gate`](../substrate/memory/primitive_time-logic-anti-hallucination-gate.md) and the entity-attribution gate next to this one in the layer.
