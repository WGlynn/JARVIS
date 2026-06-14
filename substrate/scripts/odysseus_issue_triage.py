#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Odysseus issue triage — structural bucketing of all open issues.

One script, one gh call (not N round-trips). Produces the "I read everything"
worklist for the issue-help loop. Structural buckets only; the semantic
"can WE resolve this" + fix-confidence is a downstream LLM pass on candidates.

Buckets:
  needs-info        -- label "needs more info" / maintainer must clarify
  has-pr-inflight   -- label "ready for review" => a solver PR likely exists;
                       our role here is settlement-verifier, NOT new answer
  stale             -- no update in > STALE_DAYS, likely dead
  active-discussion -- has comments, conversation already moving
  candidate         -- no PR, recent, few/no comments => semantic-review target
"""
import datetime as dt
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO = "pewdiepie-archdaemon/odysseus"
STALE_DAYS = 60
OUT = Path.home() / "Desktop" / "odysseus-issue-triage.md"


def fetch():
    cmd = ["gh", "issue", "list", "--repo", REPO, "--state", "open",
           "--limit", "1000",
           "--json", "number,title,labels,comments,updatedAt,createdAt,author"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(1)
    return json.loads(r.stdout)


def age_days(iso):
    try:
        t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (dt.datetime.now(dt.timezone.utc) - t).days
    except Exception:
        return 9999


def bucket(it):
    labels = {l["name"].lower() for l in it.get("labels", [])}
    if "needs more info" in labels:
        return "needs-info"
    if "ready for review" in labels:
        return "has-pr-inflight"
    if age_days(it["updatedAt"]) > STALE_DAYS:
        return "stale"
    if len(it.get("comments") or []) > 0:
        return "active-discussion"
    return "candidate"


def main():
    issues = fetch()
    for it in issues:
        it["_bucket"] = bucket(it)
        it["_age"] = age_days(it["updatedAt"])
    counts = Counter(it["_bucket"] for it in issues)

    lines = [
        "# Odysseus Issue Triage",
        "",
        f"Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} | repo: {REPO}",
        f"Open issues: {len(issues)}",
        "",
        "## Bucket counts",
    ]
    for b in ("candidate", "has-pr-inflight", "active-discussion",
              "needs-info", "stale"):
        lines.append(f"- **{b}**: {counts.get(b, 0)}")
    lines += [
        "",
        "> POLICY (CONTRIBUTING.md L77): Odysseus asks LLM agents (incl. Claude Code)",
        "> to open an issue first, not a PR. Autonomous posting HELD pending Will",
        "> calibration. `has-pr-inflight` => settlement-verifier role, not new answer.",
        "",
        "## candidate (semantic-review targets — no PR, recent)",
        "",
    ]
    cands = sorted((i for i in issues if i["_bucket"] == "candidate"),
                   key=lambda x: x["_age"])
    for it in cands[:60]:
        labs = ",".join(l["name"] for l in it["labels"])
        lines.append(f"- #{it['number']} ({it['_age']}d) [{labs}] {it['title'][:80]}")
    if len(cands) > 60:
        lines.append(f"  ... and {len(cands) - 60} more candidates")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Triaged {len(issues)} open issues -> {OUT}")
    for b in ("candidate", "has-pr-inflight", "active-discussion",
              "needs-info", "stale"):
        print(f"  {b}: {counts.get(b, 0)}")


if __name__ == "__main__":
    main()
