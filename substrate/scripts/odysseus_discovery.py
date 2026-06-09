#!/usr/bin/env python3
"""
Odysseus discovery script.

Fetches recent activity on pewdiepie-archdaemon/odysseus and scores each
thread for domain-fit against the Will-VibeSwap mechanism-design /
coordination / social-scalability lens.

Outputs ranked JSON to stdout. Cron-fired Claude session reads the JSON,
picks top candidate above threshold, runs convergence-proof gate, drafts +
dispatches under standing-auth per [F·odysseus-daily-discussion-campaign].

Usage:
    python odysseus_discovery.py [--limit 20] [--min-score 5]

Domain-positive keywords (each instance adds to score):
    mechanism design / coordination / governance / ownership / allocation /
    attribution / structural / incentive / sybil / fairness / decentralized /
    DRI / code owners / ADR / milestone / roadmap / contributor / maintainer /
    scaling / attention / burnout / consensus / centraliz / hierarchy /
    delegation / authority / accountability / load-bearing

Domain-negative (each instance subtracts — pure-support / non-substantive):
    won't install / doesn't work / how do I / setup error / config error /
    not working / broken / help me / can someone / windows error / mac error
"""

import sys
import io
import json
import argparse
import subprocess
from datetime import datetime, timezone

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = "pewdiepie-archdaemon/odysseus"

POSITIVE_KEYWORDS = [
    "mechanism design", "coordination", "governance", "ownership", "allocate",
    "allocation", "attribution", "structural", "incentive", "sybil",
    "fairness", "decentral", "DRI", "code owner", "CODEOWNERS", "ADR",
    "milestone", "roadmap", "contributor", "maintainer", "scaling",
    "attention", "burnout", "consensus", "centraliz", "hierarchy",
    "delegate", "delegation", "authority", "accountability", "load-bearing",
    "load bearing", "substrate", "trust", "permission", "review process",
    "PR review", "triage", "duplicate", "fork", "downstream", "upstream",
    "shapley", "first-come", "first come", "first-look", "first look",
    "tie-break", "tiebreak", "single point of failure", "bottleneck",
    "rate limit", "spam", "moderation", "abuse", "noise",
]

NEGATIVE_KEYWORDS = [
    "won't install", "doesn't work", "how do i install", "setup error",
    "config error", "not working", "broken on my", "help me",
    "can someone", "windows error", "mac error", "linux error",
    "won't start", "doesn't start", "crash on launch", "won't open",
    "download not working", "missing file", "where is the",
    "tutorial", "guide me", "step by step",
]

# Heavy boost if these specific structural patterns appear (Will's domain match)
HEAVY_POSITIVE_PHRASES = [
    "who decides", "who owns", "who should own", "who allocates",
    "felix needs to", "felix should", "felix has to", "passion project",
    "structural", "mechanism", "governance", "coordination model",
    "contributor coordination", "maintainer coordination",
    "review priority", "merge priority", "decision authority",
    "trust allocation", "load-bearing", "scales without",
]


def run_gh(*args, jq=None):
    """Run gh CLI and return stdout. Returns "" on failure."""
    cmd = ["gh"] + list(args)
    try:
        if jq:
            result = subprocess.run(
                cmd + ["--jq", jq],
                capture_output=True, text=True, timeout=30, encoding="utf-8"
            )
        else:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30, encoding="utf-8"
            )
        if result.returncode != 0:
            return ""
        return result.stdout
    except Exception:
        return ""


def fetch_discussions(limit=30):
    """Get most-recently-updated discussions."""
    query = '''
    query {
      repository(owner: "pewdiepie-archdaemon", name: "odysseus") {
        discussions(first: ''' + str(limit) + ''', orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            number title bodyText updatedAt url
            category { name }
            author { login }
            comments(last: 0) { totalCount }
          }
        }
      }
    }
    '''
    out = run_gh("api", "graphql", "-f", f"query={query}")
    if not out:
        return []
    try:
        data = json.loads(out)
        return data["data"]["repository"]["discussions"]["nodes"]
    except Exception:
        return []


def fetch_recent_issues(limit=20):
    """Get most-recently-updated open issues."""
    out = run_gh(
        "issue", "list",
        "--repo", REPO,
        "--state", "open",
        "--limit", str(limit),
        "--json", "number,title,body,updatedAt,url,labels,author",
        "-s", "updated",
    )
    if not out:
        return []
    try:
        return json.loads(out)
    except Exception:
        return []


def score_text(text):
    """Score text for domain-fit. Returns (total, positive, negative, heavy)."""
    if not text:
        return (0, 0, 0, 0)
    lower = text.lower()
    pos = sum(lower.count(k.lower()) for k in POSITIVE_KEYWORDS)
    neg = sum(lower.count(k.lower()) * 2 for k in NEGATIVE_KEYWORDS)  # 2x penalty
    heavy = sum(3 for p in HEAVY_POSITIVE_PHRASES if p.lower() in lower)  # 3x bonus
    total = pos + heavy - neg
    return (total, pos, neg, heavy)


def check_prior_engagement(thread_url):
    """Check if WGlynn has already commented on this thread."""
    # Quick proxy: pull commenter list, look for WGlynn
    number = thread_url.rstrip("/").rsplit("/", 1)[-1]
    if "discussion" in thread_url:
        query = '''
        query {
          repository(owner: "pewdiepie-archdaemon", name: "odysseus") {
            discussion(number: ''' + number + ''') {
              comments(last: 50) {
                nodes { author { login } }
              }
            }
          }
        }
        '''
        out = run_gh("api", "graphql", "-f", f"query={query}")
        try:
            data = json.loads(out)
            commenters = [n["author"]["login"] for n in data["data"]["repository"]["discussion"]["comments"]["nodes"] if n.get("author")]
            return "WGlynn" in commenters
        except Exception:
            return False
    else:
        # Issue
        out = run_gh("issue", "view", number, "--repo", REPO, "--json", "comments")
        try:
            data = json.loads(out)
            commenters = [c["author"]["login"] for c in data.get("comments", []) if c.get("author")]
            return "WGlynn" in commenters
        except Exception:
            return False


def compute_budget(discussion_number):
    """Compute information-proportionality word budget for a target discussion.

    Returns dict with budget + diagnostics. Formula:
        budget = clamp(100, 300, ceil(p75(prior_comment_word_counts) * 1.1))

    p75 chosen because max is outlier, median is typical, p75 = "what the thread
    tolerates as a serious contribution." Our budget targets that benchmark.
    """
    import math
    query = '''
    query {
      repository(owner: "pewdiepie-archdaemon", name: "odysseus") {
        discussion(number: ''' + str(discussion_number) + ''') {
          title
          comments(last: 100) {
            nodes { bodyText author { login } }
          }
        }
      }
    }
    '''
    out = run_gh("api", "graphql", "-f", f"query={query}")
    if not out:
        return {"error": "fetch failed", "budget": 250, "fallback": True}
    try:
        data = json.loads(out)
        discussion = data["data"]["repository"]["discussion"]
        comments = discussion["comments"]["nodes"]
    except Exception as e:
        return {"error": str(e), "budget": 250, "fallback": True}

    # Word counts of all prior comments (excluding any WGlynn own-comments)
    word_counts = []
    for c in comments:
        author = c.get("author", {}).get("login") if c.get("author") else None
        if author == "WGlynn":
            continue  # Exclude own comments so we don't drift our own budget upward
        body = c.get("bodyText", "") or ""
        wc = len(body.split())
        if wc > 0:
            word_counts.append(wc)

    if len(word_counts) < 3:
        # Not enough signal to compute distribution; use sensible default
        return {
            "budget": 200,
            "fallback_reason": "fewer than 3 non-WGlynn prior comments",
            "n_comments_seen": len(word_counts),
            "thread_title": discussion.get("title", ""),
        }

    # Compute p75 manually (avoid numpy dependency)
    sorted_counts = sorted(word_counts)
    idx = int(0.75 * (len(sorted_counts) - 1))
    p75 = sorted_counts[idx]

    # Also compute diagnostics
    mean = sum(word_counts) / len(word_counts)
    median = sorted_counts[len(sorted_counts) // 2]
    max_seen = max(word_counts)

    # Budget = ceil(p75 * 1.1), clamped [100, 300]
    raw_budget = math.ceil(p75 * 1.1)
    budget = max(100, min(300, raw_budget))

    return {
        "budget": budget,
        "raw_p75_x_1_1": raw_budget,
        "p75": p75,
        "median": median,
        "mean": round(mean, 1),
        "max_seen": max_seen,
        "n_comments": len(word_counts),
        "thread_title": discussion.get("title", ""),
        "fallback": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20, help="Top N candidates to output")
    parser.add_argument("--min-score", type=int, default=5, help="Threshold to include")
    parser.add_argument("--skip-engagement-check", action="store_true",
                        help="Skip the prior-engagement filter (faster, less accurate)")
    parser.add_argument("--budget-for", type=int, default=None,
                        help="Compute information-proportionality budget for a specific discussion number")
    args = parser.parse_args()

    if args.budget_for is not None:
        # Budget-only mode — skip the discovery pipeline
        result = compute_budget(args.budget_for)
        print(json.dumps(result, indent=2))
        return

    candidates = []

    # Fetch discussions
    discs = fetch_discussions(limit=30)
    for d in discs:
        # Concatenate title + body for scoring
        text = (d.get("title", "") + "\n\n" + d.get("bodyText", "") or "")[:5000]
        total, pos, neg, heavy = score_text(text)
        if total < args.min_score:
            continue
        candidates.append({
            "type": "discussion",
            "number": d["number"],
            "title": d.get("title", "")[:200],
            "category": d.get("category", {}).get("name", ""),
            "url": d.get("url", ""),
            "updated_at": d.get("updatedAt", ""),
            "comment_count": d.get("comments", {}).get("totalCount", 0),
            "author": d.get("author", {}).get("login", "") if d.get("author") else "",
            "score": total,
            "pos_hits": pos,
            "neg_hits": neg,
            "heavy_hits": heavy,
            "body_preview": (d.get("bodyText", "") or "")[:500],
        })

    # Fetch issues
    issues = fetch_recent_issues(limit=20)
    for i in issues:
        text = (i.get("title", "") + "\n\n" + (i.get("body", "") or ""))[:5000]
        total, pos, neg, heavy = score_text(text)
        if total < args.min_score:
            continue
        candidates.append({
            "type": "issue",
            "number": i["number"],
            "title": i.get("title", "")[:200],
            "category": "",
            "url": i.get("url", ""),
            "updated_at": i.get("updatedAt", ""),
            "comment_count": 0,  # issue API call doesn't include without extra request
            "author": i.get("author", {}).get("login", "") if i.get("author") else "",
            "score": total,
            "pos_hits": pos,
            "neg_hits": neg,
            "heavy_hits": heavy,
            "body_preview": (i.get("body", "") or "")[:500],
        })

    # Sort by score desc
    candidates.sort(key=lambda c: -c["score"])

    # Trim to limit
    candidates = candidates[:args.limit]

    # Add prior-engagement check on top candidates (expensive — only top 10)
    if not args.skip_engagement_check:
        for c in candidates[:10]:
            c["wglynn_already_commented"] = check_prior_engagement(c["url"])
    else:
        for c in candidates:
            c["wglynn_already_commented"] = None

    output = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "repo": REPO,
        "discussions_fetched": len(discs),
        "issues_fetched": len(issues),
        "candidates_above_threshold": len(candidates),
        "min_score_threshold": args.min_score,
        "candidates": candidates,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
