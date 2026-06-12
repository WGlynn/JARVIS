#!/usr/bin/env python3
"""Runtime heartbeat — one telemetry line per turn, unconditionally.

The problem it fixes (found 2026-06-12 during a continuous-runtime record attempt):
`protocol_telemetry.jsonl` only gets a line when some OTHER hook calls `log_event`.
A turn made of long single-tool stretches (a big test run, a multi-file edit) can fire
no logged protocol event, leaving a >10min GAP in the log even though work never
stopped. Any "longest continuous chain (gap < N min)" analysis then undercounts real
operation — the instrument is lossy.

This hook is wired to BOTH Stop and UserPromptSubmit (the two events that fire every
single turn), so the telemetry chain reflects actual continuous operation rather than
incidental hook chatter. It is pure instrumentation: reads nothing, decides nothing,
emits `{}` (or stays silent), and never blocks. Per [P.universal-coverage-hook].

Schema: event="heartbeat", meta.phase in {"stop","user-prompt"}.
"""
import sys

try:
    from _telemetry import log_event
except Exception:
    # Telemetry must never break the turn. If the helper can't import, no-op.
    def log_event(*a, **k):
        return None


def main() -> int:
    phase = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    log_event("runtime-heartbeat", "heartbeat", meta={"phase": phase})
    # Stop/UserPromptSubmit accept an empty object as "no opinion".
    print("{}")
    return 0


if __name__ == "__main__":
    main()
