---
name: HTML over PPTX for decks
description: Default to HTML (single file, Google-fonts CDN, Ctrl+P for PDF) for pitch decks and visual artifacts. Not .pptx. Will's call 2026-04-20 — "HTML is the GOAT."
type: feedback
originSessionId: feff45da-df5b-4228-8a3c-2871f583acc7
---
# Rule
When asked to produce a pitch deck, slide deck, or any visual-layout artifact for VibeSwap (or similar), **default to a single self-contained HTML file** — not `.pptx`, `.pdf`, `.md`, or anything else.

## Why
Will doesn't have PowerPoint ("$150 is laughable, I ain't downloading that shit"). The `.pptx` I initially produced was unusable to him. HTML is:
- **Universal**: opens in any browser on any OS
- **Faithful**: matches the VibeSwap frontend design system 1:1 (same CSS, same fonts via Google Fonts CDN)
- **Exportable**: `Ctrl+P → Save as PDF` is built into every browser, one page per slide with `@page size: 13.333in 7.5in`
- **Shareable**: the HTML file OR the printed PDF both work
- **Editable**: Will can tweak CSS directly; no proprietary file format

Will's exact words: *"HTML is the GOAT ... until we design our own version lol."*

## How to apply
- For any deck/slide request: build `artifact.html` with `@page` rules for PDF export, pull Inter + JetBrains Mono from Google Fonts, use the VibeSwap palette (matrix #00ff41, terminal #00d4ff, black #000, border #252525).
- Structure: each slide = one `<section class="slide">` with `aspect-ratio: 16/9` for screen + fixed-size `@media print` overrides for PDF.
- Include the terminal-motif design language: `[ BRACKET_KICKERS ]`, `> prompts`, `//` captions, `→` bullets, `::` separators, corner brackets on hero regions, gradient-fade dividers, ambient grid overlay.
- Open after building: `start "" "<path>.html"` on Windows, or tell Will to double-click the file.
- Skip `.pptx` unless Will explicitly asks for an editable PowerPoint file.

## Future direction
"Until we design our own version" — the eventual target is a `vibeswap.org/deck` page in the frontend, live breathing dot + hover states, shareable via `/pitch/:topic` routes, viewer analytics. Deck-as-first-class-protocol-artifact. File this as a frontend cycle candidate when the time comes.

## Where the pattern lives
- Reference impl: `Desktop/Memecoin_Intent_Market_2026-04-20/pitch_deck.html` (2026-04-20)
- Retired: `Desktop/Memecoin_Intent_Market_2026-04-20/pitch_deck.pptx` (unusable for Will)
