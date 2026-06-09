---
name: Jarvis TG bot token compromise 2026-05-06
description: Forensic anchor — bot token leaked, name changed to "#FREEVPN" spam-link by attacker; fly.io account deleted as containment; leak vector unknown.
type: project
originSessionId: ecc37c38-0388-4b18-9737-102d8939cc6e
---
# Incident — 2026-05-06 — Jarvis TG bot token compromise

## Symptom
- Bot name changed to `#FREEVPN https://t.me/vpn38_bot?start=adx_jfzlSV4kiC-p`
- Pattern = standard TG bot hijack (attacker calls `setMyName` via leaked token)

## Containment timeline (2026-05-06)
- ~14:21 UTC-? — Will detected name change
- ~14:23 — token rotated via @BotFather (1st rotation)
- ~14:23 — Will pasted new token into Claude chat ⇒ token-context exposure ⇒ ✗ deployable
- ~14:24 — recommended 2nd rotation (chat-pasted token = burned)
- ~14:40 — Will deleted fly.io account (containment by removal)
- ~14:42 — bot offline; restoration plan = local Path A → VPS Path B

## Audit findings
- ✓ `.env` in `.gitignore` ; ✗ committed to git history
- ✓ `.env.example` + `.env.vps.example` clean (no real values for *_TOKEN / *_API_KEY)
- ✓ src/ token-logging clean (only NULL-check error msgs print var-name ¬ value)
- ⚠ `.env.example:86` `OWNER_USER_ID=8366932263` (real) — public-tracked
- ⚠ `.env.example:89` `BOT_USERNAME=JarvisMind1828383bot` (real) — public-tracked

## Leak vectors NOT eliminated
1. fly.io account compromise (deleted ⇒ contained if vector)
2. Token in screenshot/paste ∈ {Discord, Slack, X-DM, GH-issue}
3. Webhook URL w/ token (if `bot<TOKEN>` path mode used)
4. Backup ∨ data/ upload
5. Compromised dev machine

## Other secrets in same .env (rotate ∀ unknown vector)
- ANTHROPIC_API_KEY, GITHUB_TOKEN, GROQ/CEREBRAS/DEEPSEEK keys
- JARVIS_MASTER_KEY ⚠ encrypts knowledge base — rotate carefully (re-encrypt OR keep old to decrypt)
- CLAUDE_CODE_API_SECRET, SHARD_SECRET
- cert.pem, key.pem (gitignored, on disk)
- data/.master-key (auto-gen, on disk)

## Restoration path
- Path A: local Node, `npm start` from `vibeswap/jarvis-bot/` — PC-on requirement
- Path B: fresh VPS + `vps-deploy.sh` ; `docker-compose.vps.yml` patched 2026-05-06 (shard-0 worker→primary, fly.dev refs removed)

## Hardening shifts (post-incident)
- ✗ ∀ tokens-into-chat — credentials only via {editor, fly-secrets, env-direct}
- public-tracked identifiers (`OWNER_USER_ID`, `BOT_USERNAME`) ⇒ stub in `.env.example`
- audit fly-equivalent (next host) for principle-of-least-privilege deploy keys

## Related primitives
- See `feedback_no-credentials-in-claude-chat.md` (sibling)
- [BotPaths] R·jarvis-bot-repo-paths
- [BotFreeTierAlways] J·jarvis-tg-bot-free-tier-inference-only
