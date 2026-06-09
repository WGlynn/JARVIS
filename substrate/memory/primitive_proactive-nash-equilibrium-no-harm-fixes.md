---
name: proactive-nash-equilibrium-no-harm-fixes
description: ∀ unverified-claim ⇒ identify actions with positive-payoff regardless of claim's truth-value. dominant-strategy in info-asymmetric situations. execute no-harm subset NOW, defer verification-dependent.
type: primitive
originSessionId: 8e0b2388-5171-43d5-a501-c272f20c2f6f
---
**Concept:** ∀ claim X with unknown truth-value (T ∨ F) ⇒ identify actions A such that payoff(A | X=T) > 0 ∧ payoff(A | X=F) ≥ 0. these = "no-harm-either-way" actions, dominant-strategy.

> *"that should be a next line of reasoning primitive to think of proactive nash equilibrium, no harm either way fixes"* — Will, 2026-04-30

**Decision matrix:**

| Action class | If claim true | If claim false |
|--------------|---------------|----------------|
| panic-action (rotate, take offline) | helps ⇒ +N | costs ⇒ -M (churn, downtime) |
| verification-dependent | helps after delay | prep wasted |
| **no-harm proactive** | **helps ⇒ +N** | **neutral or +ε ⇒ ≥0** |
| do-nothing | exposed ⇒ -L | safe ⇒ 0 |

**Selection rule:** prefer no-harm-proactive when payoff ≥ 0 in F-case ∧ > 0 in T-case ⇒ dominant by definition.

**Examples:**

| Domain | Unverified claim | No-harm-proactive action |
|--------|------------------|--------------------------|
| Security advisory | "your stack vulnerable" | tighten API-key scopes; update patch versions; verify 2FA |
| Regulatory rumor | "new compliance rule" | review existing compliance; tighten records |
| Competitive intel | "competitor pivoting" | review own positioning; differentiation audit |
| Partner concern | "X may be problematic" | document architectural decision; pre-empt FAQ |
| Phishing-looking msg | "click here urgently" | save forensic record + verify sender + don't click |

**Why load-bearing:**
- info-asymmetric situations are common (security, regulation, business intel, social)
- panic-action class is high-cost in F-case (verified-fake) ⇒ churn + misconfiguration risk
- waiting-for-verification class is high-cost in T-case (real attack while we wait)
- no-harm-proactive splits the difference: act NOW with actions paying off ∀ world-state

**Anti-patterns this prevents:**
- panic-rotation of secrets on unverified advisory ⇒ churn + breakage
- ignoring advisory entirely ⇒ exposed if real
- waiting-for-verification before any action ⇒ wasted time in T-case

**Detection in real-time:**
- ∀ claim arrives requiring action ⇒ first ask: "what subset is no-harm-either-way?"
- partition recommendations into {no-harm subset, verification-dependent subset}
- execute no-harm subset NOW; verification-dependent waits for verification

**Apply (Jarvis triage protocol):**
- ∀ Jarvis triage of alerts (security, operational, partner) ⇒ build the no-harm subset first
- surface to Will as "these are safe to do now without waiting"
- separately surface "these wait for verification + here's how to verify"
- ✗ collapse the two — different decision speeds

**Parents:**
- [StructureDoesTheWork] dominant-strategy = math doing the work
- [FullLeverageOnly] timing primitive (this is action-selection-in-uncertainty)
- [PCPGate] expense gate (no-harm class is by-definition cheap-and-positive)
