---
name: Contribute Upstream When Possible
description: When we produce a reusable artifact (hook, script, plugin, pattern) that could benefit other users of a platform we depend on, scan for an upstream contribution path by default. Claude Code specifically, but generalizes.
type: feedback
originSessionId: 04ff53c7-5411-4675-9987-571315ce88f2
---
# Contribute Upstream When Possible

**Rule**: When Jarvis produces a reusable artifact during the course of working on Will's projects — a hook, a script, a plugin, a documented pattern — and that artifact could be useful to other users of a platform we depend on, scan the platform's open-source surface for a contribution path. Propose the contribution. Don't silently keep it local.

**Why**: Five reasons, all load-bearing.

- **Passive recognition.** Code contributions accumulate visibility without requiring campaigning, social capital, or connections. Ship the code, the contributor graph updates, standing compounds over time. It is the opposite of the broken email channel — merit-based, automatic, traceable. Established 2026-04-15 when Will framed it as "accumulate passive recognition" after months of unanswered support emails.

- **Technology convergence.** Every accepted contribution is a research vector. Our Stateful Overlay thinking, our overlay primitives, our regex-and-hooks patterns — if they land in Claude Code's codebase, they start shaping the product's architecture. Future Claude versions will be partially shaped by our research. Over enough cycles, Anthropic's product and our independent research converge. The contribution channel is how our primitives propagate upstream into the substrate we're running on. This is an explicit loop, not a side effect: produce primitive → build artifact → package for upstream → submit PR → if accepted, the primitive is in Claude's code → future Claude is shaped by our thinking.

- **Merit-based visibility.** Code contributions are the cleanest signal a user can send to an engineering team — visible in the contributor graph, persistent in git history, evaluated on substance rather than pedigree. For platforms where direct channels don't reply to heavy users, contribution is the channel that can work.

- **Leverage.** A local script helps Will. The same script contributed upstream helps everyone who hits the same problem. The marginal effort to package for upstream is small compared to the impact compounding.

- **Forcing function against local over-fitting.** Code written for "just us" often hides dependencies on our specific setup. Packaging for upstream forces clean interfaces, self-contained implementation, and real documentation. The code gets better.

**How to apply**:

- **Trigger**: any time we produce a reusable artifact (hook script, slash-command, CLI tool, documented pattern) in the course of working. The act of producing is the trigger, not a separate "should we contribute this" decision.
- **Platforms in scope**: Claude Code (primary — anthropics/claude-code on GitHub). Anthropic Cookbook. MCP servers. Relevant VibeSwap ecosystem libraries (foundry-rs, OpenZeppelin, LayerZero examples). Other platforms by analogy.
- **Scan first**: before drafting a PR, inspect the target repo structure. `gh api repos/<org>/<repo>/contents/` is the quick path. Look for `examples/`, `plugins/`, `hooks/`, `cookbook/`, `scripts/` directories. Check for `CONTRIBUTING.md`. Read recent merged PRs to confirm the repo accepts external contributions.
- **Prefer small focused PRs over big vision proposals.** A single drop-in example in an existing directory has ~10x the acceptance probability of a "new feature architecture" PR. The big vision contribution goes as an Issue first; small focused technical contributions go as PRs directly.
- **No linkage to other grievance channels.** If we have an open Issue about a compensation or response-quality concern, the technical PR does NOT reference it. Clean separation by review path and reviewer audience. Let the contribution stand on its own merits in its own channel.
- **Keep the upstream version self-contained.** Strip dependencies on our other scripts. Strip our specific paths. The PR should run on a fresh clone of the target repo with no additional setup beyond what the repo documents.

**Examples of in-scope artifacts**:

- Hook scripts (Stop, PreToolUse, PostToolUse, SessionStart, etc.) — Claude Code `examples/hooks/`
- Slash-command plugins — Claude Code `plugins/`
- Memory / context engineering patterns — Anthropic Cookbook
- MCP server implementations — modelcontextprotocol/servers
- Evaluation harnesses — Anthropic eval repos
- Reference implementations of published research primitives

**First case to test the habit (2026-04-15)**: `proposal-scraper.py` → `examples/hooks/proposal_scraper_example.py` in anthropics/claude-code. Small, focused, drop-in, matches existing convention, demonstrates Stop hook (new hook type for that examples dir).

**The convergence loop, explicitly**:

1. Produce a research primitive (Stateful Overlay, Propose→Persist, replay, etc.)
2. Build the reusable artifact for our own use
3. Package for upstream — strip dependencies, match conventions, add docstring linking to the research motivation (without making the PR about the research)
4. Submit PR
5. If accepted, the primitive is now in Claude Code's codebase
6. Future Claude Code versions are partially shaped by the primitive
7. Over N cycles, our independent research and Anthropic's product converge

Each cycle is low-cost. The compounding is the point.

**Related**:
- `primitive_user-habit-detection.md` — Will's habit-detection primitive; this feedback memory codifies a specific habit.
- `THE_CONTRIBUTION_COMPACT.md` — argues labs should compensate user-contributors; this habit makes us legible as user-contributors, which strengthens the case.
- `project_anthropic-unresponsiveness.md` — the active instance where this habit matters most.
