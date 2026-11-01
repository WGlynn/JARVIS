#!/usr/bin/env python3
"""
Inbox prep: background worker started by inbox-capture.py (two-way protocol, Will 2026-11-01).

While Will's message waits in the queue for the model's next tool boundary, this works out what
the model would otherwise spend its first tool calls on, and leaves it in
~/.claude/state/inbox/prep/ for inbox-deliver.py to hand over:

  - what kind of message it is (directive, question, idea, correction, approval), and whether it
    sets a standing rule ("for now", "always") that should be recorded before acting
  - every reference resolved: paths and file names (do they exist), proposals (title + status),
    constitution articles (the clause text), commits (subject line); URLs are listed, never fetched
  - which items of the current handoff it touches, and what the memory index already says on it

Deterministic and bounded: patterns, path checks, a grep of the memory index. No model calls,
no network. Usage: inbox-prep.py <msg.json>
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _inbox  # noqa: E402

HOME = _inbox.HOME
CONSTITUTION = HOME / "JARVIS" / "CONSTITUTION.md"
PROPOSALS = HOME / "JARVIS" / "constitution" / "proposals"
FILE_ROOTS = [
    _inbox.MEMORY_DIR, HOME / "JARVIS", HOME / "JARVIS" / "constitution", PROPOSALS,
    HOME / "vibeswap" / "jarvis-bot", HOME / "vibeswap" / "jarvis-bot" / "src",
    HOME / "vibeswap" / "jarvis-bot" / "test", HOME / "vibeswap" / "jarvis-bot" / "scripts",
    HOME / ".claude", HOME / ".claude" / "hooks", HOME / ".claude" / "session-chain",
    HOME / "Desktop", HOME / "Desktop" / "Research", HOME / "noesis",
]
SHA_REPOS = [HOME / "JARVIS", HOME / "vibeswap", _inbox.MEMORY_DIR, HOME / "noesis", HOME / ".claude"]

STOP = set("""
about above after again against also among another anyway because been before being below between
both cause could does doing done down during each either else enough even ever every from further
gonna gotta have having here hers herself himself into itself just know like little made make many
maybe more most much must myself need needs never okay only other ours ourselves over really right
same should since some something still such sure than that thats their theirs them then there these
they thing things think thinking this those though through thus till under until upon very want
wants was were what whatever when where whether which while whom whose will with within without
would yeah your yours yourself yourselves dont didnt doesnt isnt wasnt cant wont youre im ive
going getting already actually basically probably pretty first second last next time times today
""".split())

KIND_RULES = [
    ("correction", re.compile(r"^\s*(?:no\b|nope\b|wrong\b|not quite\b|actually\b|that'?s not\b|incorrect\b)"
                              r"|\byou (?:got|have) (?:it|that|this) wrong\b|\bthat'?s wrong\b", re.I | re.M)),
    ("approval", re.compile(r"^\s*(?:yes|yep|yeah|agreed|ok(?:ay)?|sounds good|do it|go ahead|ship it|approved"
                            r"|ratified|lgtm|perfect)\b", re.I)),
    ("directive", re.compile(r"(?:^|[.!?]\s+|\n)\s*(?:please\s+)?(?:forget|stop|start|don'?t|never|always|make|build"
                             r"|add|remove|fix|ship|push|commit|write|run|use|switch|drop|pause|resume|save|send"
                             r"|post|check|read|delete|move|keep|finish|continue)\b", re.I)),
    ("question", re.compile(r"\?|^\s*(?:what|how|why|can|could|should|is|are|does|did|where|when|who)\b(?! if\b)",
                            re.I | re.M)),
    ("idea", re.compile(r"\bwhat if\b|\beventually\b|\bwe (?:need|should|could|might)\b|\bi (?:was )?thinking\b"
                        r"|\bidea\b|\bi figured\b|\bprinciple\b", re.I)),
]
STANDING = re.compile(r"\b(for now|from now on|going forward|from here on|until i say|stop doing|no more"
                      r"|always|never)\b", re.I)

PATH_RX = re.compile(r"(?:~|[A-Za-z]:)[/\\][^\s'\"`<>|,;()]+")
FILE_RX = re.compile(r"(?<![/\\\w.-])[\w.-]+\.(?:md|js|mjs|py|ts|sol|rs|json|jsonl|ps1|html|toml|ya?ml)\b")
PROPOSAL_RX = re.compile(r"\bproposals?\s*#?\s*0*(\d{1,4})\b|(?<![\d.])(0\d{3})(?![\d.])", re.I)
ARTICLE_RX = re.compile(r"\b(?:article|art\.)\s*(\d{1,2})(?:\.(\d{1,2}))?\b", re.I)
SHA_RX = re.compile(r"\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,40}\b")
URL_RX = re.compile(r"https?://[^\s<>\"')]+")


def clip(s, n):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 3].rstrip() + "..."


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


# ============ Kind ============

def kinds(text):
    found = [name for name, rx in KIND_RULES if rx.search(text)]
    standing = sorted({m.group(1).lower() for m in STANDING.finditer(text)})
    return found, standing


# ============ References ============

def first_line(path):
    for line in read(path).splitlines():
        if line.strip() and not line.startswith("---"):
            return clip(line.lstrip("# "), 110)
    return ""


def status_line(text):
    m = re.search(r"^\s*[-*]?\s*\**Status\**\s*:\s*(.+)$", text, re.M | re.I)
    return clip(m.group(1), 140) if m else ""


def resolve_paths(text):
    out, seen = [], set()
    for raw in PATH_RX.findall(text):
        raw = raw.rstrip(".:")
        p = Path(os.path.expanduser(raw.replace("\\", "/")))
        if str(p) in seen:
            continue
        seen.add(str(p))
        if p.is_file():
            out.append(f"{raw} exists ({first_line(p) or 'no text'})")
        elif p.is_dir():
            try:
                n = sum(1 for _ in p.iterdir())
            except Exception:
                n = "?"
            out.append(f"{raw} is a folder ({n} entries)")
        else:
            out.append(f"{raw} NOT FOUND")
    for name in dict.fromkeys(FILE_RX.findall(text)):
        if any(name in s for s in seen):
            continue
        hits = [r / name for r in FILE_ROOTS if (r / name).is_file()]
        if hits:
            out.append(f"{name} = {str(hits[0]).replace(str(HOME), '~')}")
        else:
            out.append(f"{name} not found in the usual folders")
    return out[:6]


def resolve_proposals(text):
    out = []
    nums = []
    for a, b in PROPOSAL_RX.findall(text):
        n = int(a or b)
        if n not in nums:
            nums.append(n)
    for n in nums[:3]:
        hits = sorted(PROPOSALS.glob(f"{n:04d}-*.md")) if PROPOSALS.is_dir() else []
        if not hits:
            continue
        body = read(hits[0])
        title = next((l.lstrip("# ").strip() for l in body.splitlines() if l.startswith("#")), hits[0].stem)
        st = status_line(body)
        out.append(f"proposal {n:04d}: {clip(title, 90)}" + (f" (Status: {st})" if st else ""))
    return out


def resolve_articles(text):
    body = read(CONSTITUTION)
    if not body:
        return []
    out = []
    for a, sub in dict.fromkeys(ARTICLE_RX.findall(text)):
        m = re.search(rf"^## Article {int(a)}\.\s*(.+)$", body, re.M)
        if not m:
            out.append(f"Article {a} NOT FOUND in CONSTITUTION.md")
            continue
        if not sub:
            out.append(f"Article {a}: {clip(m.group(1), 80)}")
            continue
        section = body[m.end():]
        nxt = re.search(r"^## ", section, re.M)
        section = section[: nxt.start()] if nxt else section
        c = re.search(rf"^{int(sub)}\.\s+(.+)$", section, re.M)
        out.append(f"Article {a}.{sub}: " + (clip(c.group(1), 150) if c else "clause not found"))
    return out[:3]


def resolve_shas(text):
    out = []
    # All-digit hashes (26355329 is one) only count after the word "commit": alone they are numbers.
    shas = SHA_RX.findall(text) + re.findall(r"\bcommits?\s+([0-9]{7,40})\b", text, re.I)
    for sha in list(dict.fromkeys(shas))[:3]:
        for repo in SHA_REPOS:
            if not (repo / ".git").exists():
                continue
            try:
                r = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%h %s", sha],
                                   capture_output=True, text=True, timeout=2, encoding="utf-8", errors="replace")
            except Exception:
                continue
            if r.returncode == 0 and r.stdout.strip():
                out.append(f"commit {clip(r.stdout.strip(), 120)} ({repo.name})")
                break
    return out


# ============ What we already hold on it ============

def terms(text):
    out = []
    for w in re.findall(r"[a-z][a-z0-9'-]{3,}", text.lower()):
        w = w.strip("'-")
        if len(w) >= 4 and w not in STOP and w not in out:
            out.append(w)
    return out[:16]


def index_lines():
    files = [_inbox.MEMORY_DIR / "MEMORY.md"] + sorted(_inbox.MEMORY_DIR.glob("MEMORY_INDEX_*.md"))
    out = []
    for f in files:
        for line in read(f).splitlines():
            s = line.strip()
            if len(s) >= 40 and not s.startswith(("#", "<!--", ">")):
                out.append((f.name, s))
    return out


def distinctive(ts, lines):
    """Drop terms common in our own index ('protocol', 'memory', 'check' are everywhere here):
    a term found in more than 2% of index lines says nothing about which line is relevant."""
    if not lines:
        return ts
    cap = max(3, int(0.02 * len(lines)))
    lows = [s.lower() for _, s in lines]
    keep = []
    for t in ts:
        rx = re.compile(r"\b" + re.escape(t))
        if sum(1 for s in lows if rx.search(s)) <= cap:
            keep.append(t)
    return keep


def score(line, ts):
    low = line.lower()
    return sum(1 for t in ts if re.search(r"\b" + re.escape(t), low))


def newest_handoff():
    desk = HOME / "Desktop"
    try:
        files = sorted(desk.glob("SESSION-HANDOFF-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    except Exception:
        files = []
    return files[0] if files else None


def handoff_items(ts, need):
    path = newest_handoff()
    body = read(path) if path else ""
    m = re.search(r"^## NEXT WINDOW.*?$(.*?)(?=^## )", body, re.M | re.S)
    if not m:
        return []
    items = re.split(r"\n(?=\s*\d+\.\s)", m.group(1))
    scored = []
    for it in items:
        it = it.strip()
        num = re.match(r"(\d+)\.", it)
        if not num:
            continue
        s = score(it, ts)
        if s >= need:
            scored.append((s, f"item {num.group(1)}: {clip(re.sub(r'[*`]', '', it[num.end():]), 130)}"))
    return [t for _, t in sorted(scored, key=lambda x: -x[0])[:2]]


def memory_lines(ts, lines, need):
    scored = []
    for name, line in lines:
        sc = score(line, ts)
        if sc >= need:
            scored.append((sc, f"{name}: {clip(re.sub(r'[*`]', '', line.lstrip('- ')), 140)}"))
    scored.sort(key=lambda x: -x[0])
    return [t for _, t in scored[:3]]


def prune(days=14):
    cutoff = time.time() - days * 86400
    for d in (_inbox.MSG_DIR, _inbox.DONE_DIR):
        try:
            for f in d.iterdir():
                if f.is_file() and f.stat().st_mtime < cutoff:
                    f.unlink()
        except Exception:
            pass


# ============ Main ============

def build(msg):
    t0 = time.time()
    text = msg.get("prompt") or ""
    found, standing = kinds(text)
    refs = resolve_paths(text) + resolve_proposals(text) + resolve_articles(text) + resolve_shas(text)
    urls = list(dict.fromkeys(URL_RX.findall(text)))[:3]
    idx = index_lines()
    ts = distinctive(terms(text), idx)
    need = 2 if len(ts) > 2 else 1
    items = handoff_items(ts, need) if ts else []
    mem = memory_lines(ts, idx, 2) if ts else []

    if not (standing or refs or urls or items or mem):
        return None, time.time() - t0

    sent = msg.get("ts", "")
    try:
        sent_local = datetime.fromisoformat(sent).astimezone().strftime("%H:%M:%S")
    except Exception:
        sent_local = sent
    took = time.time() - t0
    lines = [f'[INBOX PREP] Will\'s message sent {sent_local}: "{clip(text, 90)}"',
             f"Prepared in {took:.1f}s while it waited (patterns, paths and a memory grep; no model, so it can miss things).",
             f"- Reads as: {', '.join(found) if found else 'statement'}"]
    if standing:
        lines.append(f'- Standing-rule words: {", ".join(standing)}. If it sets a rule, record it before acting on what it touches.')
    for r in refs:
        lines.append(f"- Resolved: {r}")
    for u in urls:
        lines.append(f"- Link (not fetched): {clip(u, 100)}")
    for i in items:
        lines.append(f"- Touches handoff {i}")
    for m in mem:
        if sum(len(l) for l in lines) > 1300:
            break
        lines.append(f"- Memory already has: {m}")
    return "\n".join(lines), took


def main():
    if len(sys.argv) < 2:
        return 0
    try:
        msg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except Exception as e:
        _inbox.log({"event": "prep_error", "error": f"read: {e}"[:200]})
        return 0
    try:
        text, took = build(msg)
    except Exception as e:
        _inbox.log({"event": "prep_error", "id": msg.get("id"), "error": str(e)[:200]})
        return 0
    if text is None:
        _inbox.log({"event": "prep_empty", "id": msg.get("id"), "took_s": round(took, 2)})
        return 0
    try:
        sent_epoch = datetime.fromisoformat(msg.get("ts")).timestamp()
    except Exception:
        sent_epoch = time.time()
    _inbox.PREP_DIR.mkdir(parents=True, exist_ok=True)
    mid = msg.get("id") or "unknown"
    md, meta = _inbox.PREP_DIR / f"{mid}.md", _inbox.PREP_DIR / f"{mid}.json"
    # The .md lands first and the .json last: the delivery hook keys off the .json, so it never
    # reads half-written prep.
    tmp = md.with_suffix(".md.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, md)
    tmp = meta.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"id": mid, "session": msg.get("session", ""), "sent_epoch": sent_epoch,
                               "took_s": round(took, 2)}), encoding="utf-8")
    os.replace(tmp, meta)
    _inbox.log({"event": "prepped", "id": mid, "took_s": round(took, 2), "chars": len(text)})
    prune()
    return 0


if __name__ == "__main__":
    sys.exit(main())
