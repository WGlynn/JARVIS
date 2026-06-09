---
name: API Death Shield
description: Client-side hook system that persists conversation state when Anthropic API errors kill the session — crash markers, conversation log, heartbeat, auto-commit
type: feedback
originSessionId: 0101333f-9e7e-4925-8d8b-9a8a834253dd
---
# API Death Shield

All existing crash recovery (WAL, SSL Gate, auto-checkpoint) requires the AI to be alive to write state. When Anthropic's API throws 500 errors, the AI can't do anything — the session just dies mid-response.

**Why:** On 2026-04-13, repeated Anthropic 500 errors killed a session mid-conversation during CogCoin mining work. Rich conversation context (cousin pitch, mining results, $70 BTC discussion) existed only in volatile context and was unrecoverable except via .jsonl forensics.

**How to apply:** The shield runs CLIENT-SIDE via Claude Code hooks — independent of AI liveness.

## Architecture

| Hook Event | Handler | What It Saves |
|------------|---------|---------------|
| `UserPromptSubmit` | Log user messages | Human side of conversation → `shield/conversation.log` |
| `Stop` | Heartbeat | Last-known-good turn + git HEAD → `shield/heartbeat.json` |
| `StopFailure` | **CRITICAL PATH** | Crash marker + chain finalize + auto-commit dirty files |
| `PreCompact` | Chain sync | Finalize pending + git push before compression |

## Files

- Script: `~/.claude/session-chain/api-death-shield.py`
- Config: `~/.claude/settings.json` (hooks section)
- Crash markers: `~/.claude/session-chain/shield/crashes/`
- Conversation log: `~/.claude/session-chain/shield/conversation.log`
- Heartbeat: `~/.claude/session-chain/shield/heartbeat.json`
- Shield log: `~/.claude/session-chain/shield/shield.log`

## Recovery on Next Boot

```bash
python ~/.claude/session-chain/api-death-shield.py report    # See what happened
python ~/.claude/session-chain/api-death-shield.py clear-crashes  # After processing
```

The SessionStart hook could be extended to auto-check for crash markers and inject the report into context.

## Key Insight

The shield inverts the trust model: instead of trusting the AI to write state before dying, we trust the CLIENT to capture state after the AI dies. The conversation log + heartbeat + crash marker triangle gives the next session enough to reconstruct what happened without .jsonl forensics.
