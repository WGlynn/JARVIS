---
name: x402 SIWX Upgrade — Session-Based Access via Wallet Signatures
description: x402 shipped credential-based authorization with CAIP-122 (Sign-In-With-X). Pay once → wallet signature authenticates subsequent requests in microseconds. Solves latency, multi-request, and stateful service problems. Critical for Wardenclyffe/Pantheon scaling.
type: reference
---

## x402 SIWX Upgrade (March 2026)

Source: Crossmint team announcement, shared by Will Session 067.

### What Changed

V1: Every request = full on-chain payment cycle (1-2s on Base, 400ms on Solana). One word: "pay."

V2 (SIWX): Pay once → server records wallet address → subsequent requests sign lightweight CAIP-122 message → local verification in microseconds. No blockchain, no facilitator, no latency.

### Three Problems Solved

1. **Latency**: Agent making 50 tool calls per session no longer needs 50 payment round-trips
2. **Multi-request**: Webpage with 30 sub-requests authenticates all via wallet signature after single payment
3. **Stateful services**: Server knows WHO paid, not just THAT someone paid — enables user-attached resources

### CAIP-122 Standard

- Chain-agnostic (EVM + Solana day one)
- Supports regular wallets (EIP-191), smart contract wallets (EIP-1271), undeployed wallets (EIP-6492)
- Domain binding + expiry windows prevent replay attacks
- Facilitator stays out of the flow — pure client-server

### VibeSwap Integration Implications

- **Wardenclyffe**: Pay once at session start → every escalation authenticates via SIWX → zero per-inference latency
- **Pantheon shards**: Boot session payment → 50+ tool calls per conversation → microsecond auth
- **Device wallet**: EIP-6492 supports our Smart Wallet (WebAuthn/passkeys) — wallets that haven't been deployed yet
- **Community access**: $0.10 for Jarvis access → wallet signature handles entire interaction
- **Our x402 middleware**: Currently does per-call Bloom filter verification. Should upgrade to SIWX session model.

### The Caveat

SIWX moves complexity onto servers. Business logic questions (how long does access last? what does payment entitle?) are yours to define. Different model from "pay per call" where semantics are obvious.

### Action Items

- Update `jarvis-bot/src/x402.js` to support SIWX session auth
- Update `backend/src/middleware/` to accept SIWX headers
- Update x402 whitepaper page and docs to reflect V2 capabilities
- Consider: VibeSwap as one of the first adopters of SIWX pattern
