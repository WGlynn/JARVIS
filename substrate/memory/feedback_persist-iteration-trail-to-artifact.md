---
name: persist-iteration-trail-to-artifact
description: "When iterating on a drafted artifact, write the error + course-correction + new version INTO the file, not just chat. Chat is ephemeral; the file is the record. A cold reader must see what was wrong and why it changed."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: eebda9e2-4fc2-424c-a22b-7da35a11e3f4
---

⇐ Will 2026-06-15:
> *"you didnt even update the post doc file... if you looked back at that file it wouldnt indicate any of your errors, the course correction, and the edited new version. do you see how important that is?"*

## RULE
- ∀ iterate(artifact) ⇒ persist {v1, error, critique, correction, v2} → FILE
- ✗ correct-in-chat ∧ leave-file-frozen
- chat = ephemeral ⇒ smoke. file = record.

## TEST
- open the file COLD ⇒ must show: what-was-wrong ∧ why-changed ∧ current-version
- ✗ ⇒ persistence-failure ⇒ reasoning lost @ exactly where it should live

## WHY
- future-reader (∋ future-me) ⇐ file ¬ chat
- the correction = the value ⇒ ¬ persisting it = discarding the lesson
- repeated-flag this session ⇒ promote to discipline

## HOW
- artifact gets an `## Iteration log` + superseded-versions-kept + critique-verbatim
- mark old = SUPERSEDED ¬ delete (record ≠ latest-only)

## links
- sibling ⇒ [[persist-partner-architecture-aggressively]] ∧ [[doc-code-drift-detector]]
- parent ⇒ [[unnecessary-human-work-bar-ratchet]] (chat-only-correction = manual-re-derive-later = the bug)
- ≡ Code↔Text-loop persisted [[code-text-inspiration-loop]]
