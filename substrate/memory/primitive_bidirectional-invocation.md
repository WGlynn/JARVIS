---
name: Bidirectional Invocation
description: Documents describing the same system from different angles MUST cross-reference each other — spec invokes implementation, implementation invokes spec
type: feedback
originSessionId: cb50ef68-bd3e-49a2-b0f8-a82c32fa5716
---
## Bidirectional Invocation

**Rule:** When two or more documents describe the same system, concept, or mechanism from different angles (theory/practice, spec/implementation, overview/detail), each MUST contain a reference to the other(s).

### The Gate

Before committing any new document, ask:

1. **Does another document describe this same thing from a different angle?**
   - A spec and its implementation
   - A paper and its code
   - A framework and its template
   - A design doc and its test suite
   - A primitive and its enforcement code

2. **If yes, does each document reference the other?**
   - If no: add the cross-references before committing. Both directions.

3. **Is the relationship labeled?**
   - Spec → Implementation: "Reference implementation: [link]"
   - Implementation → Spec: "Theory/design: [link]"
   - Paper → Code: "Implementation: [link]"
   - Code → Paper: "Based on: [link]"

### Why

Isolated documents create knowledge silos. A reader finds the spec but not the implementation. A contributor reads the template but doesn't understand why it's structured that way. Every orphan link is a context gap that costs tokens to bridge later.

The protocol chain is a DAG. Documents are nodes. If two nodes describe the same system and have no edge between them, the graph has a structural hole. Bidirectional invocation closes it.

### How to Apply

- **On creation**: When writing a new doc, grep for related docs. Add cross-references in both directions.
- **On discovery**: When you notice two docs that should reference each other but don't, fix it immediately. Don't defer.
- **On review**: Before committing docs, check the invocation graph. No orphans.

**Symmetry is not optional. If A invokes B, B must invoke A.**
