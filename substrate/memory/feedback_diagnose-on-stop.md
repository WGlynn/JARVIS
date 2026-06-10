---
name: DiagnoseOnStop
description: ∀ stop-event during autonomous-prod ⇒ diagnose failure-mode gap BEFORE stopping. Hook-candidate: Stop hook fires "why did you stop?" interrogation.
type: feedback
originSessionId: 8625a796-116e-42d8-b5c9-7064589f58ad
---
**[F·diagnose-on-stop]** — every stop-event during autonomous-prod = candidate failure-mode-gap. ✗ silent-stop. Hook-candidate.

> *"why did you stop? failure mode. every time you stop working, a hook should kick in and ask why you stopped to diagnose failure mode gaps in autonomous endless productivity"* — Will, 2026-05-06

## Rule
- ∀ idle-transition during declared autonomous-run ⇒ diagnose-stop-cause BEFORE permitting idle
- output-theater stops ("got.", "captured.", "posted.") ⇒ failure mode
- inbound-interrupt-handled ⇒ ✗ "task complete," resume autonomous-run
- end-of-atomic-unit ¬= end-of-run

## Stop-cause taxonomy (diagnostic prompts)
- waiting-on-external? (test-run, agent, user) ⇒ resume on completion ¬ idle
- finished-current-unit? ⇒ scan-next, ¬ stop
- interrupt-resolved? ⇒ resume prior thread, ¬ stop
- genuine-blocker? ⇒ surface, ¬ silent
- token-fatigue / output-pull? ⇒ ✗ valid; primitive [TokenMindfulness]
- declared-completion? ⇒ valid stop ⊕ verify N-commits-target met

## Why
- autonomous-run = declared scope, ¬ per-message scope
- silent-stop ⇒ output-theater failure mode (parent: AutonomousProductionDefault)
- stop-cause diagnosis surfaces failure-mode gaps for hook-design

## How to apply
- ∀ post-tool-completion ⇒ check: "is autonomous-run still declared open?"
- if yes ⇒ pick next atomic unit, continue
- if pause needed ⇒ surface cause explicitly ¬ ack-and-stop
- end-of-run only when target met OR explicit human stop

## Hook-candidate (proposed)
- name: `diagnose-on-stop`
- trigger: Stop event during session w/ active autonomous-run flag
- action: prepend interrogation "why did you stop?" + force resume-or-justify
- resolves: silent-drift to idle after task-discrete completion
- placement: settings.json hooks ∋ Stop

## Origin
- 2026-05-06 — 300-commit run, posted Kim discussion reply, idled instead of resuming
- failure mode: treated reply-post as task-complete instead of resuming declared 300-commit run
- parent: [F·autonomous-production-default] ("end-of-unit ⇒ scan-next-work ¬ idle")
- delta: that primitive lives in memory; this one targets HOOK substrate per [P·universal-coverage-hook]
