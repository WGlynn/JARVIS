---
name: Embedded Vibe-Coding IDE (Soham + Will, June 2026)
description: Autonomous embedded firmware loop IDE. Soham (MIT-hackathon collaborator) + Will. Built on Void IDE frontend, embedded runtime verification layer as the moat. Tier 1 boards STM32 + ESP32; Tier 2 RP2040 + Nordic nRF (incl Seeed XIAO nRF52840 Sense from Soham's summer 2025 morphing-robotic-foot research lab). Source-of-truth PDF on Desktop, 19 pages, mtime 2026-06-09.
type: project
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Embedded Vibe-Coding IDE

## STATUS 2026-06-12 — backend BUILT (was: docs-only, Soham's callout correct)
* repo `C:/Users/Will/embedded-vibe-coding` @ 6e061ea, 40 tests green, local git only (remote = Will+Soham gate)
* HANDOFF.md in repo = current state + next increments. Read it before any EVC-IDE work.
* moat shipped: verify engine 16 expectation kinds + classification + evidence; demo --dry proven (fake log FAILS rate check, live 1Hz PASSES)
* next: BLE receiver (bleak) -> Soham's XIAO demo; then live-hardware pass; then STM32/ESP32

## Glyph
```
EVC-IDE  prompt -> code-edit -> build -> compile-repair -> flash ->
         output-receive -> verify -> runtime-repair -> PASS|FAIL.
         moat == runtime-verification ! flashing.
```

## Source-of-truth
* `Desktop/Embedded_Vibe_Coding_IDE_Master_Documentation_v2.pdf` (19 pages, 385 KB, 2026-06-09)
* `Desktop/Embedded Vibe Coding Ide Master Documentation.pdf` (older v1, 120 KB)

## Partners
* **Soham** -> MIT-hackathon collaborator. Summer 2025 research lab: sensory suite for a morphing robotic foot. Pain point: setting up XIAO nRF52840 + ROS package to receive data was friction-heavy. Vision: AI IDE that closes the build->flash->verify loop = landmark.
* **Will** -> co-founder posture. Project genre maps to JARVIS-substrate philosophy (autonomous loops + verification gates + adapter pattern).

## Will's compressed framing (paste verbatim)

> "the idea behind this project was to automate firmware and embedded systems. I worked in a research lab this summer where we worked with a sensory suite for a morphing robotic foot. Everyone was using AI to write code, I had a thought that if there was an embedded systems ide which could write code, flash it onto chips AND verify output that flow would be a landmark achievement. For example we were using a xiao ble chip and used a rod package to receive data. And it was a hassle to set up, if an ai ide could do it we could genuinely go somewhere with this."

* "rod package" -> ROS package (Robot Operating System)
* "xiao ble chip" -> Seeed XIAO nRF52840 Sense

## Architecture (from PDF v2)

* **Frontend** == Void IDE shell -> editor | file tree | AI chat | device panel | build/flash/runtime console | verification panel | agent timeline
* **Backend** == Node.js/TS orchestrator + Python microservices + WebSockets + Redis/BullMQ + Docker sandbox + local-first hardware ops
* **Board adapter interface** -> `detect / createProject / importProject / build / flash / openOutputChannel / verify / repairHints`
* **Tier 1 boards** -> STM32 Nucleo (F401RE / F446RE / H743ZI later) + ESP32 (DevKitC / S3 / C3 / C6)
* **Tier 2 boards** -> RP2040/RP2350 (Pico, Pico W, Pico 2) + Nordic nRF52/nRF53/nRF54 (XIAO nRF52840 Sense, nRF52840-DK, nRF5340-DK)

## Receivers (runtime verification surfaces)

| receiver | MVP? | examples |
|---|---|---|
| Serial | required | UART logs, USB-CDC, boot msgs, sensor prints |
| BLE | Tier-2 nRF demos | BLE-adv, GATT discovery, IMU packet stream |
| WiFi / Socket | ESP32 2nd wave | TCP/UDP telemetry, HTTP health, WebSocket logs |
| ROS topics | robotics expansion | /imu /force /joint_state /diagnostics |
| CSV / File | useful early | helper-script logs, ROS-output |
| HIL | future | GPIO readback, PWM freq, logic analyzer, current draw |

* `RuntimeEvent` schema -> `{source, timestampMs, boardId, streamId, type, raw, parsed, metadata}`

## Verification contracts

* JSON expectations -> `contains / count_min / message-rate / field-presence / numeric-sanity / protocol-checks / ROS-topic-rate`
* `VerificationResult` -> `{status, contractId, checks[], evidence[], failureClassification, repairHints[], agentSummary}`
* Translate vague prompt -> measurable PASS/FAIL

## Autonomous agent loop (10 steps from spec)

```
1 understand request -> infer board/framework/peripherals/expectations/safety
2 inspect files + board profile + toolchain + prior logs
3 generate or patch firmware (diff-based)
4 build + parse diagnostics
5 if build-fail -> repair w/ bounded retries
6 flash + verify deployment
7 open configured runtime receiver
8 run verification contract on live output
9 if verify-fail -> classify + targeted repair
10 stop w/ clear PASS|FAIL + evidence + changed-files + next-action
```

## Positioning

* "Cursor for embedded systems, but with hardware output verification"
* Differentiator vs Arduino IDE / STM32CubeIDE / PlatformIO / Cursor -> autonomous repair loop AGAINST runtime evidence, not just code generation
* Lead demo path -> Soham's actual research-lab setup: XIAO nRF52840 Sense + IMU streaming via BLE + verification contract checks sample rate

## How to apply

* ∀ EVC-IDE work -> read PDF first; this primitive is index, not spec
* ∀ architecture decision -> map to substrate-port-pattern (board-adapter == JARVIS-hook-equivalent)
* ∀ verification-contract design -> AMD framing: math-enforced invariant > discretionary policy
* ∀ runtime-receiver -> parsed-fields are first-class (not just raw bytes)
* ∀ Soham-facing artifact -> Desktop draft per [F·formalize-replies-to-docs] + scrub em-dashes per [F·em-dash-filter-for-conversations]

## Sibling memory

* `[P·substrate-port-pattern]` -> board-adapter pattern == JARVIS hook-adapter
* `[F·augmented-mechanism-design-paper]` -> verification contracts as math-enforced invariants
* `[P·universal-coverage-hook]` -> agent loop steps 4-9 are hook-shaped
* `[J·mit-bitcoin-expo-2026]` -> where Soham relationship originated
* `[F·named-protocols-are-primitives]` -> why this file exists immediately on naming

## Open questions for Will

* Soham's current ship status (PDF v2 dated 2026-06-09 = yesterday)
* Build / fundraise / hackathon-target / open-source posture
* JARVIS-substrate integration scope: does the IDE consume JARVIS hooks, or does it stay standalone
* Demo deadline (next hackathon? research-lab pitch? investor?)
