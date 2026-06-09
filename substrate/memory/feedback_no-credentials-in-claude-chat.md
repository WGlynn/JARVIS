---
name: No credentials in Claude chat
description: ∀ token / API-key / secret ⇒ ✗ paste into Claude conversation. Once in chat-context ⇒ burned ⇒ rotate. Use editor / secrets-manager / env-direct only.
type: feedback
originSessionId: ecc37c38-0388-4b18-9737-102d8939cc6e
---
# [F·no-credentials-in-claude-chat]

## Rule
- ∀ credential ∈ {bot-token, API-key, master-key, secret, password, JWT} ⇒ ✗ paste into Claude chat
- pasted-cred ⇒ chat-ctx ⇒ API-logs ⇒ session-exports ⇒ burned
- valid channels: editor (VS Code/etc), secrets-manager (fly/aws/vault), shell w/ `read -s`, env-file-direct

## Why (2026-05-06 Jarvis TG bot)
> *"[BotFather]: Your token was replaced with a new one. You can use this token to access HTTP API:8467996907:..."*
> Will pasted entire BotFather output ⇒ token in conversation context

- token rotation #1 ⇒ chat-paste ⇒ rotation #2 needed
- 2× rotation cost + delay during active incident

## How to apply
1. user about-to-rotate-cred ⇒ pre-emptively warn: "rotate, then ✗ paste here"
2. cred detected in user-msg ⇒ FLAG IMMEDIATELY: "treat as compromised; rotate again"
3. ∀ secure-flow ⇒ provide `read -s` / editor-edit / secrets-CLI commands
4. ✗ acknowledge + use a pasted cred in tool calls (would persist to logs)
5. ∀ memory-write ∋ cred-literal ⇒ ⊥ (never persist)

## Detection signal
- user-msg ∋ pattern {`[0-9]+:[A-Za-z0-9_-]{30,}`, `sk-[A-Za-z0-9]{40+}`, `ghp_[A-Za-z0-9]+`, `bot[0-9]+:`}
- BotFather/console-output paste
- "here's the new token/key" framing

## Edge cases
- ✓ user pastes cred-stub / dummy ("AAAAAA...") for testing — fine
- ✓ user shares pre-rotated cred for forensic analysis — fine after rotation confirmed
- ✗ user shares post-rotation cred ∀ purpose

## Related
[P·api-death-shield] | [F·discretion-no-personal-details-public-repos]
