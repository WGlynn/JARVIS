% _asp_rules.lp -- Phase 1 rule set for the memory-graph (stratified Datalog).
% Exactly one stable model => fully deterministic. Zero LLM calls.
% Phase 1 scope: wikilinks + primitives only (no bracket-tags, no declared structure yet).

% a node is referenced iff some edge points at it
referenced(B) :- links(_, B).

% dead link: a wikilink whose target no file defines (typos + not-yet-written primitives surface)
dead_link(A, B) :- links(A, B), not primitive(B).

% unreferenced: a real node nothing links to
% NOTE Phase 1: index/warm/canon files show here until Phase 2 adds index_entry/canon facts.
unreferenced(P) :- primitive(P), not referenced(P).

% slug collision: two distinct files canonicalize to the same node id ⇒ ambiguous node,
% every [[slug]] link to it is ambiguous. High-severity integrity bug (set-dedup hides it).
dup_slug(S, F1, F2) :- file(S, F1), file(S, F2), F1 < F2.

#show dead_link/2.
#show unreferenced/1.
#show dup_slug/3.
