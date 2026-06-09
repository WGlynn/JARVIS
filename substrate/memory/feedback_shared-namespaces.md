---
name: Shared Namespaces Are Attack Surfaces
description: Any shared namespace (variables, keys, rate limits, context) can collide. Isolate by default. Learned from trackMessage name collision that crashed both bots.
type: feedback
---

Shared namespaces are attack surfaces.

**Why:** Added `trackMessage` to shard-dedup.js imports. `tracker.js` already exported `trackMessage`. SyntaxError crashed both Jarvis bots in production. A name collision in a shared namespace took down the entire Mind Mesh.

**How to apply:**
- Always check existing imports before adding new ones with common names
- Prefix module-specific functions: `trackSiblingMessage` not `trackMessage`
- This applies beyond code: shared API keys share rate limits (defeats shard scaling), shared context windows can overflow, shared state can corrupt
- Anything shared can collide. Isolate by default.
- Complexity is fine. Insecure complexity is useless in the long run. Security must scale with complexity.
