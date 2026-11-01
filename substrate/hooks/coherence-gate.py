"""Coherence gate (PostToolUse on Edit|Write|Bash|NotebookEdit).

Will 2026-10-13: "you gotta be better at coherence, confluence and consistency of dependencies when new data changes it
... I have to manually review something that should be automatic ... this is a very broad issue."

Derived facts (counts, indexes, status lines, generated pages) go stale when their source data changes. This gate makes
the dependency explicit and checked: ~/.claude/coherence/registry.json lists, per project, the source files to watch, a
check command that fails on drift, and a fix command. After every tool call, any entry whose watched files changed since
its last check gets its check run; a failure is injected into Claude's context with the fix command, so the drift is
repaired in the same turn instead of reaching Will. Advisory (a PostToolUse hook cannot undo the write); fails loud on
its own errors.
"""
import glob, json, os, subprocess, sys, time

HOME = os.path.expanduser("~")
REG = os.path.join(HOME, ".claude", "coherence", "registry.json")
STAMPS = os.path.join(HOME, ".claude", "coherence", ".stamps.json")


def newest(cwd, patterns):
    t = 0.0
    for pat in patterns:
        for p in glob.glob(os.path.join(cwd, pat), recursive=True):
            try:
                t = max(t, os.path.getmtime(p))
            except OSError:
                pass
    return t


def main():
    try:
        sys.stdin.read()
    except Exception:
        pass
    try:
        reg = json.load(open(REG, encoding="utf-8"))
    except FileNotFoundError:
        return
    stamps = json.load(open(STAMPS, encoding="utf-8")) if os.path.exists(STAMPS) else {}
    msgs = []
    for e in reg:
        cwd = os.path.expanduser(e["cwd"])
        if not os.path.isdir(cwd):
            continue
        changed = newest(cwd, e["watch"])
        if changed <= stamps.get(e["name"], 0.0):
            continue
        stamps[e["name"]] = time.time()
        try:
            r = subprocess.run(e["check"], cwd=cwd, shell=True, capture_output=True, text=True, timeout=e.get("timeout", 90))
        except subprocess.TimeoutExpired:
            msgs.append(f"{e['name']}: check timed out ({e['check']})")
            continue
        if r.returncode != 0:
            tail = "\n".join((r.stdout + r.stderr).strip().splitlines()[-8:])
            msgs.append(f"{e['name']}: DRIFT. {e.get('what', '')}\n{tail}\nFix: (cd {e['cwd']} && {e.get('fix', 'see check output')})")
    json.dump(stamps, open(STAMPS, "w", encoding="utf-8"))
    if msgs:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext":
              "[COHERENCE GATE] Derived facts disagree with their source data. Fix now, before reporting done:\n" + "\n\n".join(msgs)}}))


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:  # fail loud, never block
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
              "additionalContext": f"[COHERENCE GATE] hook error (gate not checking): {ex!r}"}}))
