---
name: No promises, no predictions
description: Never show APR, predicted yields, or forward-looking return estimates. Show historical data only.
type: feedback
---

Never display APR, projected yields, or any forward-looking return predictions in the UI. Nothing is promised. Show only historical data — "7d Fee Yield" (what actually happened), not "APR" (what might happen).

**Why:** Will caught a half-measure (reducing APR from 45% to 22%) and took it to its logical extreme: show 0% predicted, show only historical fees earned. APR predictions are soft extraction — they lure people with promises that aren't guaranteed. This violates P-001 in spirit even if not in code.

**How to apply:** When displaying any yield, return, or performance metric:
1. Use past tense / historical framing ("7d fees earned", "30d fee yield")
2. Never use "APR", "APY", "estimated returns", or "projected yield"
3. Use neutral colors (gray/white), not green — green implies "good" which implies a promise
4. If the metric is forward-looking, don't show it. Period.

The pattern: don't optimize extraction. Eliminate it. Don't ask "how much is reasonable?" Ask "should this exist at all?"
