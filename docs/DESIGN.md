---
name: Real-Fruit-Snacks — Cyclorama Dawn
description: Theatrical lighting-desk design system sweeping from matte Blackout through Glacial Steel and Maritime Beacon Orange into Alabaster Day.
world: "stagecraft-theater-lighting-cyclorama-dawn"
colors:
  cyc-steel: "#1f547a"
  cyc-steel-fill: "#18496b"
  cyc-beacon: "#f06e2b"
  ground-dark: "#050507"
  rail-dark: "#070709"
  surface-dark: "#0c0c10"
  ink-dark: "#f4f5f8"
  ink-muted-dark: "#b3b5c0"
  border-dark: "rgba(255, 255, 255, 0.14)"
  border-strong-dark: "#62646d"
  accent-steel-dark: "#74b8e8"
  accent-beacon-dark: "#ff9254"
  code-bg-dark: "#08080b"
  focus-dark: "#ff9254"
  ground-light: "#f5f7f9"
  rail-light: "#eaeef2"
  surface-light: "#ffffff"
  ink-light: "#0d1016"
  ink-muted-light: "#474d59"
  border-light: "rgba(13, 16, 22, 0.16)"
  border-strong-light: "#6e7682"
  accent-steel-light: "#164669"
  accent-beacon-light: "#ad3d0a"
  code-bg-light: "#eef2f5"
  focus-light: "#ad3d0a"
typography:
  display:
    fontFamily: '"Big Shoulders Stencil", "Arial Narrow", sans-serif'
    fontSize: "clamp(2.55rem, 1.4rem + 3.4vw, 4.95rem)"
    fontWeight: 700
    lineHeight: 0.96
    letterSpacing: "0.055em"
  headline:
    fontFamily: '"Big Shoulders Stencil", "Arial Narrow", sans-serif'
    fontSize: "clamp(2rem, 1.4rem + 2vw, 3.15rem)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.055em"
  title:
    fontFamily: '"Big Shoulders Stencil", "Arial Narrow", sans-serif'
    fontSize: "1.65rem"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.055em"
  body:
    fontFamily: '"Albert Sans", system-ui, -apple-system, sans-serif'
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0em"
  label:
    fontFamily: '"Albert Sans", system-ui, -apple-system, sans-serif'
    fontSize: "0.78rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.09em"
  mono:
    fontFamily: '"Azeret Mono", ui-monospace, "Cascadia Code", Consolas, monospace'
    fontSize: "0.8rem"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "0em"
    fontFeature: '"tnum" 1'
rounded:
  thumb: "0.25rem"
  sm: "0.375rem"
  md: "0.625rem"
  token: "4px"
spacing:
  rail-w: "15rem"
  stage-pad-x: "clamp(1.25rem, 1rem + 2.4vw, 3.25rem)"
  hero-pad-y: "clamp(2rem, 1.5rem + 2vw, 3.25rem)"
  band-pad-y: "clamp(2.5rem, 1.8rem + 2.4vw, 4.25rem)"
  gap-xs: "0.45rem"
  gap-sm: "0.75rem"
  gap-md: "1.25rem"
  gap-lg: "2rem"
components:
  button-primary:
    backgroundColor: "{colors.cyc-steel-fill}"
    textColor: "{colors.surface-light}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.65rem 1.45rem"
    height: "2.85rem"
  button-secondary:
    backgroundColor: "rgba(5, 7, 10, 0.42)"
    textColor: "{colors.ink-dark}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.65rem 1.25rem"
    height: "2.85rem"
  button-secondary-light:
    backgroundColor: "rgba(255, 255, 255, 0.72)"
    textColor: "{colors.ink-light}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.65rem 1.25rem"
    height: "2.85rem"
  scheme-toggle:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.ink-dark}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.5rem 0.8rem"
    height: "2.7rem"
  filter-chip:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.ink-muted-dark}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.45rem 0.95rem"
    height: "2.45rem"
  filter-chip-active:
    backgroundColor: "{colors.cyc-steel-fill}"
    textColor: "{colors.surface-light}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.45rem 0.95rem"
    height: "2.45rem"
  input-search:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.ink-dark}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "0.45rem 0.75rem"
    height: "2.45rem"
  nav-item:
    backgroundColor: "transparent"
    textColor: "{colors.ink-muted-dark}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.5rem 0.7rem"
    height: "2.6rem"
  phase-tile:
    backgroundColor: "{colors.ground-dark}"
    textColor: "{colors.ink-dark}"
    rounded: "{rounded.md}"
    padding: "0.95rem 0.85rem 0.8rem"
    height: "9.85rem"
  card-proof-desk:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.ink-dark}"
    rounded: "{rounded.md}"
    padding: "1.25rem"
---

# Design System: Real-Fruit-Snacks — Cyclorama Dawn

## Overview

**Creative North Star: "The Lighting-Desk Cyclorama"**

Cyclorama Dawn stages the **Real-Fruit-Snacks** (`RFS`) utility catalog as a theatrical lighting desk and seamless cyclorama sweep (`stagecraft-theater-lighting-cyclorama-dawn`, `seed:10db92dfb92a9692`) locked to the **Steel & Beacon Orange** palette. Absorbent matte stage black holds the dense technical inventory—seventeen active public tools with tabular `IN -> OUT` proofs, four core principles, and three supporting repositories (`rfs-brand`, `rfs-themes`, `rfs.tools`)—while projected washes of glacial steel and maritime beacon orange establish atmosphere and drive the native continuum from Dark Mode (`LX 001`–`LX 389`) to Alabaster Day Light Mode (`LX 455`–`LX 512`).

The system departs from flat warm-charcoal legacy themes while refusing both generic dark-SaaS card grids and retro CRT terminal costumes, pairing cold architectural steel with high-visibility maritime beacon orange inside a modern theatrical horizon. Every element is built for solo-authored engineering credibility: zero tracking, zero build framework overhead, self-hosted variable WOFF2 typography, crisp `1px` full-perimeter hairlines, high-contrast dual themes, and progressive enhancement so core content and links work cleanly with JavaScript disabled.

Motion follows a single theatrical cue grammar rather than decorative page choreography. Six GPU-composited lighting curtains crossfade in `480ms` on an exponential ease-out curve (`cubic-bezier(0.16, 1, 0.3, 1)`), paired with an optional scroll-linked `22px` stage-floor beam drift (`animation-timeline: scroll(root)`). Under `prefers-reduced-motion: reduce`, all curtain fades snap instantaneously and scroll drift disables completely.

**Key Characteristics:**
- Depthless neutral matte black grounds (`#050507`) with zero blue-slate drift, countered by crisp Alabaster Day (`#f5f7f9`).
- Seamless Glacial Steel-to-Beacon Orange lighting washes interpolated in `oklab`, guarded by directional readability scrims and dual-mode accessible ink tokens.
- Six interactive `LX` lighting cues (`LX 001 Blackout` through `LX 512 Alabaster Day`) unifying hero atmosphere, theme switching, and deep-linked tool selection.
- Self-hosted variable WOFF2 typography pairing `Big Shoulders Stencil` display caps, `Albert Sans` geometric UI/prose, and `Azeret Mono` strictly for tabular codes, slugs, and `IN -> OUT` data.
- Full-perimeter `1px` hairlines, restrained technical radii (`6px` / `10px`), inline `1.5px` stroke SVGs, and complete `forced-colors: active` and No-JS parity.

## Colors

The palette divides cleanly between absorbent achromatic stage architecture (matte blackout dark and cool-alabaster daylight) and projected maritime stage light (Glacial Steel and Beacon Orange), tuned in `site/styles.css` for WCAG AA/AAA text legibility across both color schemes (`5.41:1`–`19.04:1`).

### Primary
- **Glacial Cyclorama Steel** (`#1f547a`, `--cyc-steel`): Canonical cool steel horizon anchor declared on `:root`, paired with adjacent calibrated steel stops (`#1e5078`, `#215175`, `#225c87`, `#184769`, `#133954`) across hero curtains, brand lockup rules, primary CTAs, and proof-desk wash headers.
- **Action Steel Fill** (`#18496b`, `--cyc-steel-fill`): Solid high-contrast fill for active stack filter chips (`9.53:1` with `#ffffff`), text selection highlight, skip-to-content pill, native `accent-color`, and translucent active-row (`20%`), active-nav (`22%`), and secondary-button hover (`24%`) washes via `color-mix(in oklab, ...)`.
- **Dark-Mode Ink Steel** (`#74b8e8`, `--accent-steel-dark`): Illuminated glacial-steel text token for cue indices (`#01`–`#17`), `OUT` trace markers, core-principle rule codes, hover links, and copy confirmation checkmarks on dark surfaces (`9.08:1` on `#0c0c10`, `9.30:1` on `#08080b`).
- **Light-Mode Ink Steel** (`#164669`, `--accent-steel-light`): Deepened steel text token for cue indices, `OUT` markers, rule codes, and interactive highlights on Alabaster Day surfaces (`9.93:1` on `#ffffff`, `8.82:1` on `#eef2f5`).

### Secondary
- **Maritime Beacon Orange** (`#f06e2b`, `--cyc-beacon`): Warm stage-horizon beacon stop, stage-floor horizon beam highlight, active phase-tile outline ring (`2px solid var(--cyc-beacon)`), and active rail-navigation border tint (`56%` mix via `color-mix(in oklab, ...)`).
- **Dark-Mode Ink Beacon** (`#ff9254`, `--accent-beacon-dark` / `--focus-dark`): High-contrast warm orange text token for `IN` trace markers, text `caret-color`, scheme-toggle hover border, and dark-mode keyboard focus outlines (`8.82:1` on `#0c0c10`, `9.04:1` on `#08080b`).
- **Light-Mode Ink Beacon** (`#ad3d0a`, `--accent-beacon-light` / `--focus-light`): Deepened burnt-beacon ink for `IN` trace markers, text `caret-color`, scheme-toggle hover border, and light-mode keyboard focus outlines on Alabaster Day surfaces (`6.09:1` on `#ffffff`, `5.41:1` on `#eef2f5`).

### Neutral
- **Absorbent Matte Cyclorama Black** (`#050507`, `--ground-dark`): Primary dark page canvas and dark hero backdrop—deliberately neutral without blue-slate cast.
- **Stage Rail Black** (`#070709`, `--rail-dark`): Left matte lighting-desk rail background in dark phases.
- **Cue Sheet Surface** (`#0c0c10`, `--surface-dark`): Primary dark container fill for the cue table, sticky proof desk, filter chips, search input, and supporting cards.
- **Code Well Black** (`#08080b`, `--code-bg-dark`): Recessed dark background for `IN -> OUT` proof traces and `git clone` command rows.
- **Stage White Ink** (`#f4f5f8`, `--ink-dark`): Primary dark-mode copy (`18.68:1` on `#050507`, `17.91:1` on `#0c0c10`).
- **Muted Stage Ink** (`#b3b5c0`, `--ink-muted-dark`): Secondary dark-mode descriptions, column headers, and stack metadata (`9.98:1` on `#050507`, `9.56:1` on `#0c0c10`).
- **Dark Hairline & Strong Borders** (`rgba(255, 255, 255, 0.14)` `--border-dark` / `rgba(255, 255, 255, 0.30)` `--border-strong-dark`): Full-perimeter structural boundaries and interactive control strokes in dark mode.
- **Alabaster Day Ground** (`#f5f7f9`, `--ground-light`): Crisp cool-alabaster daylight page canvas and light-phase hero backdrop.
- **Alabaster Day Rail** (`#eaeef2`, `--rail-light`): Left navigation rail ground in light mode.
- **Alabaster Day Surface** (`#ffffff`, `--surface-light`): Clean paper containers for tables, proof desk, controls, and cards in light mode.
- **Alabaster Day Code Well** (`#eef2f5`, `--code-bg-light`): Recessed cool-neutral container for `IN -> OUT` proof traces and clone bars in light mode.
- **Alabaster Day Ink** (`#0d1016`, `--ink-light`) & **Alabaster Day Muted Ink** (`#474d59`, `--ink-muted-light`): Primary (`17.73:1` on `#f5f7f9`, `19.04:1` on `#ffffff`) and secondary (`7.90:1` on `#f5f7f9`, `8.49:1` on `#ffffff`) light-mode copy.
- **Light Hairline & Strong Borders** (`rgba(13, 16, 22, 0.16)` `--border-light` / `rgba(13, 16, 22, 0.32)` `--border-strong-light`): Structural hairlines and interactive boundaries in light mode.

### Lighting Phases (LX 001–LX 512)

Six discrete atmospheric curtains sit behind the hero stage (`data-cue="0"` through `data-cue="5"`), crossfading via GPU opacity. Gradients progressively upgrade to Cartesian perceptual interpolation through `--in-oklab` (used across all cyclorama washes so cool steel and warm orange blend cleanly through neutral twilight without green or magenta hue swing).

| Cue | Index & Slug | Phase Name | Scheme | Paired Tool | Hero Curtain Gradient (`site/styles.css`) | Swatch Tile Fill & Ink |
| --- | --- | --- | --- | --- | --- | --- |
| `LX 001` | `0` (`lx-001`) | Blackout | `dark` | `pwn-broker` | `linear-gradient(114deg var(--in-oklab), #050709 0%, #0b141c 60%, #152b3d 100%)` | `180deg`: `#070a0d` → `#111c26` (76%) → `#050709`; ink `#f4f5f8` |
| `LX 127` | `1` (`lx-127`) | Glacial Steel | `dark` | `port-sync` | `linear-gradient(114deg var(--in-oklab), #06080b 0%, #12283b 38%, #1e5078 76%, #4f88b5 100%)` | `180deg`: `#102436` → `#1c4c70` (74%) → `#0a1724`; ink `#f6f8ff` |
| `LX 263` | `2` (`lx-263`) | Beacon Horizon *(dark default)* | `dark` | `screen-mark` | `linear-gradient(114deg var(--in-oklab), #05070a 0%, #132738 28%, #215175 50%, #cc5016 76%, #f5d7c4 93%, #ffffff 100%)` | `180deg`: `#18364d` → `#91380f` (76%) → `#1f120b`; ink `#ffffff` |
| `LX 389` | `3` (`lx-389`) | Maritime Flame | `dark` | `carify` | `linear-gradient(116deg var(--in-oklab), #0d0806 0%, #3d1c0c 28%, #bd4612 58%, #f09559 83%, #fcf4ee 100%)` | `180deg`: `#5c200a` → `#a63b0d` (74%) → `#2e1005`; ink `#ffffff` |
| `LX 455` | `4` (`lx-455`) | Warm Frost | `light` | `certapi` | `linear-gradient(115deg var(--in-oklab), #ebf0f5 0%, #dce6ef 46%, #f8e1d2 80%, #ffffff 100%)` | `180deg`: `#efd7c7` → `#faf0e8` (76%) → `#e0c3b0`; ink `#16100c` |
| `LX 512` | `5` (`lx-512`) | Alabaster Day *(light default)* | `light` | `open-file` | `linear-gradient(115deg var(--in-oklab), #f5f7f9 0%, #ebf1f6 54%, #fceee4 85%, #ffffff 100%)` | `180deg`: `#f3f5f8` → `#ffffff` (78%) → `#e4e8ee`; ink `#0d1016` |

Directional hero readability scrims guard copy over every wash:
- **Dark phases (`data-cue` `0`–`3` and No-JS dark):** `linear-gradient(90deg, rgba(5, 7, 10, 0.74) 0%, rgba(5, 7, 10, 0.42) 52%, transparent 82%)` over hero base `#050507` (`var(--ground-dark)`) with ink `#f6f7fb`.
- **Light phases (`data-cue` `4`–`5` and No-JS light):** `linear-gradient(90deg, rgba(246, 248, 250, 0.86) 0%, rgba(246, 248, 250, 0.48) 56%, transparent 86%)` over hero base `#f5f7f9` (`var(--ground-light)`) with ink `#0d1016` (`var(--ink-light)`).

### CSS Custom Properties & Dual-Scheme Resolution

`site/styles.css` declares `color-scheme: light dark` on `:root` and resolves every semantic token through a four-tier cascade: light fallback → `@media (prefers-color-scheme: dark)` → `@supports (color: light-dark(white, black))` → explicit `:root:has(> head > meta[name="color-scheme"][content="dark|light"])` overrides synced with `localStorage` (`color-scheme`, `rfs-cyc-cue`) and cross-tab `storage` events.

| Semantic Property | Light Token Value | Dark Token Value | Browser / UI Binding |
| --- | --- | --- | --- |
| `--ground` | `--ground-light: #f5f7f9` | `--ground-dark: #050507` | Page background, scrollbar track, tooltip ink |
| `--rail` | `--rail-light: #eaeef2` | `--rail-dark: #070709` | Sticky matte stage left rail |
| `--surface` | `--surface-light: #ffffff` | `--surface-dark: #0c0c10` | Table frame, proof desk, controls, cards |
| `--ink` | `--ink-light: #0d1016` | `--ink-dark: #f4f5f8` | Primary text, tooltip fill, active nav ink |
| `--ink-muted` | `--ink-muted-light: #474d59` | `--ink-muted-dark: #b3b5c0` | Lead copy, labels, table headers, placeholders |
| `--border` | `--border-light: rgba(13, 16, 22, 0.16)` | `--border-dark: rgba(255, 255, 255, 0.14)` | Section rules, table rows, resting panel edges |
| `--border-strong` | `--border-strong-light: rgba(13, 16, 22, 0.32)` | `--border-strong-dark: rgba(255, 255, 255, 0.30)` | Interactive control outlines, proof desk frame, scrollbar thumb |
| `--accent-steel` | `--accent-steel-light: #164669` | `--accent-steel-dark: #74b8e8` | Cue numbers, `OUT` labels, rule indices, hover states, copy check |
| `--accent-beacon` | `--accent-beacon-light: #ad3d0a` | `--accent-beacon-dark: #ff9254` | `IN` labels, text `caret-color`, scheme toggle hover |
| `--code-bg` | `--code-bg-light: #eef2f5` | `--code-bg-dark: #08080b` | `IN -> OUT` proof trace and `git clone` command wells |
| `--focus` | `--focus-light: #ad3d0a` | `--focus-dark: #ff9254` | Global `3px solid var(--focus)` keyboard focus ring |

Physical stop custom properties (`--cyc-steel: #1f547a`, `--cyc-steel-fill: #18496b`, `--cyc-beacon: #f06e2b`) and browser-surface rules (`::selection` `var(--cyc-steel-fill)` / `#ffffff`, `accent-color: var(--cyc-steel-fill)`, `scrollbar-color: var(--border-strong) var(--ground)`, `caret-color: var(--accent-beacon)`, `text-underline-offset: 0.22em`, `text-decoration-thickness: 1.5px`) ensure native browser surfaces inherit the palette. *(Build note: `--cyc-steel` is declared on `:root` as the canonical mid-steel physical stop, while multi-stop gradients inline adjacent steel hex stops tuned for contrast at each stop position.)*

### Named Rules
**The Neutral Blackout Rule.** Matte dark surfaces stay strictly achromatic neutral black (`#050507` ground, `#070709` rail, `#0c0c10` surface) with zero blue-slate tint; color enters exclusively as projected stage light, active cue indicators, and interactive accents.

**The Scrim-Guarded Wash Rule.** Luminous steel and beacon orange washes never carry copy without a directional readability scrim (`rgba(5, 7, 10, 0.74)` dark; `rgba(246, 248, 250, 0.86)` light) and theme-calibrated accent ink tokens holding at least `4.5:1` contrast (`5.41:1`–`19.04:1` verified across all shipping pairs).

**The Steel-to-Beacon Polarity Rule.** Every chromatic wash and accent stays strictly within the Glacial Steel (`#1f547a` / `#74b8e8`) and Maritime Beacon Orange (`#f06e2b` / `#ff9254`) polarity, interpolated in `oklab` across opposing ends so washes stay clean and architectural—never muddy warm-charcoal themes or unrelated neon hues.

## Typography

**Display Font:** `Big Shoulders Stencil` (fallback: `"Arial Narrow", sans-serif`)
**Body Font:** `Albert Sans` (fallback: `system-ui, -apple-system, sans-serif`)
**Label/Mono Font:** `Azeret Mono` (fallback: `ui-monospace, "Cascadia Code", Consolas, monospace`)

**Character:** Monumental condensed stencil caps cut straight from theatrical lighting plots paired with a crisp geometric sans for legible prose and UI chrome, anchored by tabular monospace reserved solely for cue numbers, repository slugs, and command traces.

All three families are self-hosted as variable WOFF2 binaries in `site/fonts/` (`font-display: swap`) with zero external font requests, and the three `latin` subsets are preloaded in `<head>`:
- `big-shoulders-stencil-latin.woff2` & `big-shoulders-stencil-latin-ext.woff2` (`font-weight: 700 900`)
- `albert-sans-latin.woff2` & `albert-sans-latin-ext.woff2` (`font-weight: 400 700`)
- `azeret-mono-latin.woff2` & `azeret-mono-latin-ext.woff2` (`font-weight: 400 600`)

### Hierarchy
- **Display** (`700`, `clamp(2.55rem, 1.4rem + 3.4vw, 4.95rem)`, line-height `0.96`, tracking `0.055em`, uppercase, `text-wrap: balance`): Hero `<h1>` statement only ("Real-Fruit-Snacks. Built local-first.").
- **Headline** (`700`, `clamp(2rem, 1.4rem + 2vw, 3.15rem)`, line-height `1`, tracking `0.055em`, uppercase, `text-wrap: balance`): Band section `<h2>` headings ("Complete cue sheet", "Core principles").
- **Title** (`700`–`800`, `1.22rem`–`2.35rem`, line-height `0.92`–`1.08`, tracking `0.055em`–`0.09em`, uppercase): Sub-display stencil marks—`RFS` brand wordmark (`2.35rem`, `800`, `0.09em`; `1.75rem` on `≤ 960px`), rail live cue code (`2rem`, `800`, `0.06em`, `tabular-nums`), core-principle `<h3>` titles (`1.65rem`, `700`), hero telemetry phase header (`1.55rem`, `700`, `0.07em`), and horizon phase-tile titles (`clamp(1.22rem, 1.05rem + 0.45vw, 1.4rem)`, `700`).
- **Body** (`400`, `1rem` base; `clamp(1rem, 0.95rem + 0.35vw, 1.15rem)` hero lead, line-height `1.55`, `text-wrap: pretty`): Running prose and tool summaries constrained to `58ch` (hero stand), `64ch` (band leads), `62ch` (principle notes), and `60ch` (footer copy).
- **Label** (`600`–`700`, `0.7rem`–`0.84rem`, tracking `0.05em`–`0.16em`, uppercase in `Albert Sans`): Primary/secondary buttons (`0.84rem`, `0.1em`), rail nav links (`0.8125rem`, `0.1em`), filter chips (`0.8125rem`, `0.05em`), scheme toggle and desk labels (`0.78rem`, `0.09em`–`0.1em`), table headers (`0.74rem`, `0.09em`), and `IN`/`OUT` trace markers (`0.7rem`, `700`).
- **Mono** (`500`–`600`, `0.7rem`–`1.22rem`, `font-variant-numeric: tabular-nums`): Proof-desk repo heading (`1.22rem`), supporting repo headings (`1rem`), cue-sheet selectable repo slugs (`0.92rem`), cue numbers (`#01`–`#17`) and principle codes (`01 / LOCAL`–`04 / DIRECT`) (`0.8rem`), `IN -> OUT` proof traces (`0.75rem`–`0.8rem`), `git clone` command (`0.74rem`, `overflow-wrap: anywhere`), and tile cue codes (`0.7rem`).

### Named Rules
**The Open Stencil Bridge Rule.** `Big Shoulders Stencil` is set at weight `700` with `0.055em` letter-spacing across all headings and tile titles (weight `800` reserved exclusively for the compact `RFS` wordmark and `LX` rail cue readout), keeping stencil cutouts crisp and open at every viewport width.

**The Honest Voice Split Rule.** `Albert Sans` owns every button, navigation link, filter chip, caption, and paragraph; `Azeret Mono` is strictly limited to real technical identifiers, tabular numbers, `IN -> OUT` traces, and shell commands—never used as a decorative "tech" costume on general chrome.

## Layout

The flagship uses an asymmetric two-column Stage Shell (`grid-template-columns: var(--rail-w) minmax(0, 1fr)`) with a sticky `15rem` (`240px`) full-height (`100dvh`) matte navigation rail on the left and a fluid cyclorama stage column on the right (`--stage-pad-x: clamp(1.25rem, 1rem + 2.4vw, 3.25rem)`).

- **Hero Stage Grid:** Asymmetric `minmax(0, 1.35fr) minmax(15rem, 0.65fr)` split (`2rem` gap) placing the monumental stencil headline, lead, and actions left of the `19rem` lighting telemetry card, above the full-width 3-column Horizon Desk fader bar (`auto minmax(0, 1fr) auto`) and 6-column Horizon Swatch Strip (`repeat(6, minmax(0, 1fr))`, `0.75rem` gap).
- **Catalog & Proof Desk:** Asymmetric `minmax(0, 1.62fr) minmax(18.5rem, 0.82fr)` split (`1.35rem` gap) pairing the horizontally safe 17-row cue-sheet table with a `app-shell below-header scroll (.rfs-shell / .rfs-scroll-region); top: 1.5rem` live Proof Desk.
- **Principles & Supporting Rhythm:** Vertical bands carry generous `clamp(2.5rem, 1.8rem + 2.4vw, 4.25rem)` vertical padding separated by `1px` full-width hairlines. Core principles use a 3-column ledger (`7.5rem minmax(14rem, 0.9fr) minmax(0, 1.3fr)`), and supporting repos (`rfs-brand`, `rfs-themes`, `rfs.tools`) form a 3-column grid.

### Responsive Breakpoints
- **`≤ 1180px` (Compact Catalog):** Horizon Strip shifts from 6 columns to 3 (`repeat(3, minmax(0, 1fr))`); catalog layout collapses to 1 column and Proof Desk unsticks (`position: static`).
- **`≤ 960px` (Rail Collapse):** Stage Shell becomes single-column. The sticky left rail transforms into a static top header bar (`brand toggle` on row 1, horizontally scrollable single-row `nav` on row 2), dropping `.desk-cue-readout` and `.nav-count` to preserve above-the-fold height. Hero grid, principle rows, and supporting repo grid stack to single columns.
- **`≤ 640px` (Mobile Stack):** Horizon Strip collapses to 2 columns (`repeat(2, minmax(0, 1fr))`), Horizon Desk stacks to 1 column, Cue Table hides column 4 (`IN -> OUT Proof`, which remains fully readable in the stacked Proof Desk), and the search input expands to `100%` width—maintaining zero horizontal overflow down to `390px`.

### Cross-Surface Extension Guidance
- **`rfs-brand` (Brand Portal & Asset Templates):** Share the exact `:root` Steel & Beacon Orange token sheet, self-hosted WOFF2 trio, `RFS` favicon badge (`site/favicon.svg`), and `RFS` stencil wordmark with its `2px` Steel-to-Beacon bottom beam (`#225c87` → `#f5752f`). Replace the flagship's 6-tile horizon strip with token/asset index tables using the same `1px` hairline frames and `Albert Sans` / `Azeret Mono` voice split.
- **`rfs.tools` (Minimal Front Door):** Omit the full sticky left rail on single-screen link portals; use a full-bleed `LX 263` Beacon Horizon (dark) / `LX 512` Alabaster Day (light) cyclorama curtain with its directional readability scrim, `Big Shoulders Stencil` `RFS` mark, concise `Albert Sans` routing copy, and Steel-to-Beacon primary action button (`#184769` → `#b53f0a`).
- **Repository Social / OG Covers (`1280×640`):** Render the `LX 263` Beacon Horizon diagonal wash (`#05070a` → `#215175` → `#cc5016` → `#f5d7c4` → `#ffffff`) anchored by the horizontal `2px` floor beam (`#215175` → `#4f88b5` → `#f06e2b` → `#FFFFFF`), dark readability scrim on the left, `Big Shoulders Stencil` repo title in uppercase, one-line `Albert Sans` job description, and a single `Azeret Mono` `IN -> OUT` proof strip—never stock icon badges or muddy flat-charcoal cards.
- **Tool Documentation Pages:** Adopt the matte rail + Alabaster Day / Blackout dual-scheme token stack so docs pages transition seamlessly from the flagship without losing readability on long technical prose.

### Named Rules
**The Matte Rail Anchor Rule.** Navigation, scheme switching, and live cue telemetry live in a quiet flat matte rail (`#070709` dark / `#eaeef2` light) separated by a `1px` hairline; saturated lighting washes remain strictly on the main stage canvas.

## Elevation & Depth

Cyclorama Dawn is flat and architectural at rest, separating planes through `1px` full-perimeter hairlines (`--border`, `--border-strong`) and subtle matte tonal steps (`--ground` → `--rail` → `--surface` → `--code-bg`). Depth enters through two deliberate mechanisms: atmospheric light layering in the hero stage (six GPU-composited `.cyc-curtain` washes beneath a non-blurred opacity scrim and lower-floor perspective beam SVG) and soft ambient drop shadows reserved exclusively for lifted foreground controls and sticky inspection hardware.

### Shadow Vocabulary
- **Primary CTA Rest** (`box-shadow: 0 10px 24px rgba(0, 0, 0, 0.34)`): Soft ambient separation lifting the Steel-to-Beacon action button off both dark and light cyclorama washes.
- **Primary CTA Hover** (`box-shadow: 0 14px 30px rgba(0, 0, 0, 0.42)`): Paired with `translateY(-1px)` (`160ms var(--ease-expo)`) to give tactile confirmation on hover.
- **Active Horizon Tile** (`box-shadow: 0 12px 24px rgba(0, 0, 0, 0.36)`): Applied alongside `border-color: #ffffff` and `outline: 2px solid var(--cyc-beacon)` (`2px` offset) when `aria-pressed="true"`.
- **Sticky Proof Desk** (`box-shadow: 0 14px 32px rgba(0, 0, 0, 0.22)`): Grounds the sticky right-column inspector above scrolling cue-sheet rows.
- **Horizon Fader Thumb** (`box-shadow: 0 2px 8px rgba(0, 0, 0, 0.45)`): Mechanical lighting-desk fader cap lift over the spectrum track.

### Named Rules
**The Hairline-First Depth Rule.** Resting containers rely on full-perimeter `1px` hairlines and subtle matte luminance steps rather than shadows or glassmorphism; soft shadows appear strictly on primary actions, the active phase tile, the fader thumb, and the sticky proof desk.

## Shapes

Form language is crisp, restrained, and technical—closer to an anodized studio lighting console than soft consumer cards.

- **Small Technical Radius (`0.375rem` / `6px`, `--radius-sm`):** Applied to all interactive controls and compact containers—primary/secondary buttons, scheme toggle, rail nav items, filter chips, search input, copy button, trace and clone code wells, and skip link.
- **Medium Panel Radius (`0.625rem` / `10px`, `--radius-md`):** Applied to structural containers—hero telemetry card, horizon fader desk, stepped horizon swatch tiles, cue-sheet table frame, sticky proof desk, and supporting repo cards.
- **Mechanical Fader Cap (`0.25rem` / `4px`) & Spectrum Track (`999px`):** The custom range slider pairs a tight rectangular white thumb (`1.5rem × 1.15rem`, `2px solid #05070a`) with a `0.5rem`-tall pill track; `0.36rem` circular dots (`999px`) form the 6-dot atmospheric cue progression bar inside each horizon tile.
- **Full-Perimeter Hairlines Only:** Rounded panels always carry continuous 4-sided `1px` borders; no one-sided colored accent bars or inset stripes are used. The unrounded brand lockup uses a single `2px` bottom gradient rule (`border-image: linear-gradient(90deg var(--in-oklab), #225c87 0%, #f5752f 100%) 1`).
- **Stroke Iconography, Stage Floor Art & `RFS` Favicon:** Every UI icon is an inline geometric SVG (`14px`–`16px`) drawn exclusively with `1.5px`–`1.75px` `currentColor` strokes and `fill="none"`. The hero lower-floor SVG (`viewBox="0 0 1440 220"`, `height: 14rem`) anchors a `2px` horizontal steel-to-beacon-to-white stage beam (`y="22"`, `#215175` → `#4f88b5` → `#f06e2b` → `#FFFFFF`) with four `1px` white perspective lines fading downward into the stage floor. The site favicon (`site/favicon.svg`) renders a `64×64` matte black badge (`#05070A`, `rx="12"`) framing a `56×56` (`rx="9"`) diagonal Steel-to-Beacon wash (`#05070A` → `#215175` → `#CC5016` → `#F5E4D7`), a `2.2px` white horizon bar (`y="45"`), and bold condensed `RFS` lettering (`font-weight="800"`, `letter-spacing="1.5"`).

## Components

Every component is built from semantic HTML, native CSS custom properties, and progressive vanilla JavaScript—maintaining full keyboard operability, `3px solid var(--focus)` (`3px` offset) `:focus-visible` rings, `44px`-class tap heights, and `@media (forced-colors: active)` fallbacks (`Canvas` / `CanvasText` / `Highlight`).

### Buttons
- **Character:** Direct, architectural console actions—zero pill fluff, uppercase `Albert Sans` labels, crisp contrast in both schemes.
- **Primary (`button-primary`):** Small radius (`0.375rem`), `min-block-size: 2.85rem`, padding `0.65rem 1.45rem`, `1px solid rgba(255, 255, 255, 0.24)`, Steel-to-Beacon wash (`linear-gradient(95deg var(--in-oklab), #184769 0%, #b53f0a 100%)`, `5.71:1`–`9.79:1` with `#ffffff` ink), ambient shadow (`0 10px 24px rgba(0, 0, 0, 0.34)`). Hover lifts `-1px` (`160ms var(--ease-expo)`) and deepens shadow to `0 14px 30px rgba(0, 0, 0, 0.42)`.
- **Secondary (`button-secondary`):** Small radius (`0.375rem`), `min-block-size: 2.85rem`, padding `0.65rem 1.25rem`, `1px solid currentColor`, translucent matte fill (`rgba(5, 7, 10, 0.42)` in dark cues, `rgba(255, 255, 255, 0.72)` in Alabaster Day cues). Hover shifts background to `color-mix(in oklab, var(--cyc-steel-fill) 24%, transparent)` (`160ms ease`).
- **Scheme Toggle (`scheme-toggle`):** Full rail width (`auto` on `≤ 960px`), `min-block-size: 2.7rem`, `1px solid var(--border-strong)` on `--surface`, displaying "Daylight" with a `15px` sun stroke icon in dark mode and "Night Cue" with a `15px` crescent icon in light mode (pure CSS toggled via `:has(> head > meta[name="color-scheme"])`), plus a `14px` swap icon; hover shifts border to `--accent-beacon`.
- **Copy Command Button:** `2.25rem × 2.25rem` square (`0.375rem` radius, `--surface`, `1px solid var(--border-strong)`), driven by standard Invoker Commands (`command="--copy" commandfor="clone-cmd"`) with click fallback, swapping a `15px` copy SVG for a `--accent-steel` checkmark and fading an accessible `role="status"` tooltip (`Copied` / `Copy failed`) for `2000ms`.

### Chips
- **Character:** Quiet, scannable stack filter toggles anchored above the cue sheet (`All (17)`, `Rust (5)`, `Go (1)`, `Python & Kali (8)`, `Windows (10)`, `Browser (3)`).
- **Style:** Small radius (`0.375rem`), `min-block-size: 2.45rem`, padding `0.45rem 0.95rem`, `1px solid var(--border-strong)`, `--surface` ground, `--ink-muted` `0.8125rem` `Albert Sans` weight `600`.
- **States:** Hover lifts ink to `--ink` and border to `--accent-steel` (`150ms ease`). Selected (`aria-pressed="true"`) locks to solid `--cyc-steel-fill` (`#18496b`) fill and border with `#ffffff` ink (`9.53:1` contrast).

### Cards / Containers
- **Sticky Proof Desk (`card-proof-desk`):** Medium radius (`0.625rem`), `1px solid var(--border-strong)` on `--surface`, `box-shadow: 0 14px 32px rgba(0, 0, 0, 0.22)`. Topped by a full-bleed atmospheric wash header (`linear-gradient(98deg var(--in-oklab), #133954 0%, #a83908 100%)`, `#ffffff` ink at `6.45:1`–`12.06:1`) carrying tabular cue index (`#01 / 17`) and language. Body (`1.25rem` padding) holds the `Azeret Mono` repo heading, summary, recessed `--code-bg` `IN -> OUT` trace box (beacon orange `INPUT` / centered hairline platform divider / glacial steel `OUTPUT`), `git clone` copy row, and side-by-side Project Page + GitHub Source CTAs.
- **Hero Telemetry Panel:** `max-width: 19rem`, medium radius (`0.625rem`), translucent dark (`rgba(5, 7, 10, 0.68)`, `rgba(255, 255, 255, 0.22)` border) in cues `0`–`3` and crisp white (`rgba(255, 255, 255, 0.88)`, `rgba(13, 16, 22, 0.18)` border) in cues `4`–`5`; pairs `Big Shoulders Stencil` phase title (`LX 263 · BEACON HORIZON`) with 4 label/tabular-value rows (`17 public repos`, `03 · brand, themes, web`, `Rust, Go, Py, TS, C#`, `Zero accounts`).
- **Supporting Cards:** Flat `--surface` containers with `1px solid var(--border)` (`0.625rem` radius for supporting repos `rfs-brand`, `rfs-themes`, and `rfs.tools`, strengthening to `--border-strong` on hover).

### Inputs / Fields
- **Catalog Search Input (`input-search`):** Small radius (`0.375rem`), `min-block-size: 2.45rem`, `min-inline-size: min(16rem, 62vw)`, `1px solid var(--border-strong)` on `--surface`, `0.9rem` `Albert Sans` copy with `--ink-muted` placeholder (`7.90:1`–`9.56:1`) and `--accent-beacon` caret, paired with an uppercase `Albert Sans` `<label>`.
- **Cyclorama Horizon Fader:** Custom-styled `<input type="range" min="0" max="5" step="1">` inside the `.horizon-desk` console strip (`0.625rem` radius). Its `0.5rem` pill track renders the full lighting continuum (`linear-gradient(90deg var(--in-oklab), #080c10 0%, #1d4d70 30%, #d9561a 60%, #f5a670 80%, #ffffff 100%)`) under a crisp `1.5rem × 1.15rem` white mechanical fader thumb (`0.25rem` radius, `2px solid #05070a`, `box-shadow: 0 2px 8px rgba(0, 0, 0, 0.45)`), announcing human-readable phases via `aria-valuetext`. Reverts to native `appearance: auto` under `forced-colors: active`.

### Navigation
- **Stage Left Rail:** Sticky `15rem × 100dvh` matte column (`--rail`, `1px solid var(--border)` inline-end edge) carrying the pure `RFS` stencil wordmark (no icon box, grounded by a `2px` Steel-to-Beacon bottom beam), 4 vertical anchor rows (`min-block-size: 2.6rem`, `0.375rem` radius, `16px` `1.5px`-stroke SVGs, tabular `Azeret Mono` section counts `06`/`17`/`04` for Horizon, Cue Sheet, Principles, plus GitHub), live active `LX` cue + tool readout, and the Daylight / Night Cue toggle.
- **States & Scrollspy:** Hover fills `color-mix(in oklab, var(--ink) 6%, transparent)` with `1px solid var(--border)`. Active section (`aria-current="page"` / `.is-active`, updated via `IntersectionObserver` with `rootMargin: "-20% 0px -55% 0px"`) locks to `color-mix(in oklab, var(--cyc-steel-fill) 22%, transparent)` and `color-mix(in oklab, var(--cyc-beacon) 56%, var(--border))`. Collapses to a static two-row top bar at `≤ 960px`.

### Cyclorama Horizon Desk & Stepped Phase Strip
- **Anatomy:** Signature interactive control uniting six full-bleed `.cyc-curtain` hero washes, the Horizon Fader range input, and six stepped `.phase-tile` swatch buttons (`min-block-size: 9.85rem`, `0.625rem` radius). Each tile renders a vertical horizon-banded swatch (`0%` sky → `74%–78%` wash → `100%` stage floor), tabular `LX` code + language header, `Big Shoulders Stencil` tool name, one-line job summary, and a 6-dot cue progress strip (`1`–`6` lit dots).
- **Behavior:** Scrubbing the fader or clicking any tile crossfades the hero curtain (`480ms var(--ease-expo)`), switches the global document color scheme when crossing between `LX 389 Maritime Flame` (dark) and `LX 455 Warm Frost` (light), syncs the paired tool into the Proof Desk, persists `rfs-cyc-cue` and `color-scheme` to `localStorage`, and updates deep-linkable hash state (`#cue=lx-389&tool=carify`). With JavaScript disabled, CSS defaults automatically to `LX 263 Beacon Horizon` under `prefers-color-scheme: dark` and `LX 512 Alabaster Day` under light mode.

### Tabular Cue Sheet
- **Anatomy:** Full semantic HTML `<table>` inside a bordered `--surface` frame (`0.625rem` radius, `overflow-x: auto`) with a live-count `<caption>` (`17 of 17 shown`), 5 columns (`No.`, `Repository & Job`, `Stack`, `IN -> OUT Proof`, `Links`), and accessible `<button class="tool-select-btn">` triggers in every row.
- **States:** Row hover adds `color-mix(in oklab, var(--ink) 5%, transparent)` (`140ms ease`); selected row (`.is-selected`, `aria-pressed="true"`) highlights in `color-mix(in oklab, var(--cyc-steel-fill) 20%, transparent)`. Filtering and search toggle native `[hidden]` rows and reveal a centered empty state with a keyboard-focus-restoring "Reset filters" control.

## Do's and Don'ts

### Do:
- **Do** keep dark page architecture strictly neutral matte black (`#050507` ground, `#070709` rail, `#0c0c10` surface) so projected Glacial Steel (`#1f547a`) and Maritime Beacon Orange (`#f06e2b`) stage light carries all chromatic drama (**The Neutral Blackout Rule**).
- **Do** guard every lit cyclorama wash with its directional readability scrim and use theme-shifted accent ink tokens (`#74b8e8`/`#ff9254` dark; `#164669`/`#ad3d0a` light) to hold `≥ 4.5:1` contrast (**The Scrim-Guarded Wash Rule**).
- **Do** interpolate opposing Steel-to-Beacon gradients in `oklab` (`--in-oklab`) so cool steel and warm orange transition cleanly across neutral twilight without hue drift (**The Steel-to-Beacon Polarity Rule**).
- **Do** self-host `Big Shoulders Stencil`, `Albert Sans`, and `Azeret Mono` as variable WOFF2 files, setting `Big Shoulders Stencil` at weight `700` with `0.055em` tracking for headings (**The Open Stencil Bridge Rule**).
- **Do** reserve `Azeret Mono` with `font-variant-numeric: tabular-nums` strictly for cue indices, repository slugs, `IN -> OUT` traces, and shell commands while keeping buttons, labels, and navigation in `Albert Sans` (**The Honest Voice Split Rule**).
- **Do** wrap all `<pre>` code blocks and command rows by default (`white-space: pre-wrap; overflow-wrap: anywhere; word-break: normal; tab-size: 2`) via `rfs.css` so long commands never trigger horizontal scrollbars, reserving `.rfs-code-scroll` strictly for column-aligned logs or ASCII art (**The Wrapped-by-Default Code Rule**).
- **Do** separate resting containers with full-perimeter `1px` hairlines (`--border`, `--border-strong`) and restrict soft shadows to the primary CTA, active horizon tile, fader thumb, and sticky proof desk (**The Hairline-First Depth Rule**).
- **Do** ship full progressive enhancement: No-JS dark/light parity via `light-dark()` + `prefers-color-scheme`, instant snap transitions under `prefers-reduced-motion: reduce`, `3px solid var(--focus)` keyboard rings, and `@media (forced-colors: active)` system-color overrides.
- **Do** extend Cyclorama Dawn across `rfs-brand`, `rfs.tools`, docs sites, and `1280×640` repo covers using these exact Steel & Beacon Orange CSS custom properties, the pure `RFS` stencil mark with its `2px` Steel-to-Beacon beam, the `RFS` favicon badge, and real `IN -> OUT` proofs.

### Don't:
- **Don't** tint dark grounds into blue-slate (`#0f172a`, `#111827`) or fall back to flat warm-charcoal themes; keep dark architecture strictly neutral matte black (`#050507`) and drop zero un-scrimmed copy onto lit washes.
- **Don't** introduce unrelated accent hues outside the Glacial Steel and Maritime Beacon Orange polarity (**The Steel-to-Beacon Polarity Rule**).
- **Don't** place kickers or eyebrows above headings, or render gradient fills on display or body text.
- **Don't** add one-sided colored accent bars to rounded cards or apply hard zero-blur offset shadows (`box-shadow: 4px 4px 0`) anywhere in the system.
- **Don't** use `Azeret Mono` on general buttons, navigation links, or prose descriptions, or substitute system display fonts (`Impact`, `Arial Black`) for self-hosted `Big Shoulders Stencil` in page CSS.
- **Don't** substitute Unicode glyphs or emoji for icons; draw every UI icon as an inline `1.5px`–`1.75px` stroke SVG in `currentColor`.
- **Don't** add decorative `backdrop-filter` blur cards, scattered entrance animations across every section, third-party CDN scripts/fonts, or invented metrics/badges.

## Interaction & Kit Contracts (v2.0)

- **Scrollbars Never Reach the Top Bar:** Use `.rfs-shell` (`100dvh`, `overflow: hidden`) + `.rfs-shell-header` + `.rfs-scroll-region` so vertical scrollbars start strictly below top navigation chrome.
- **Zero Native Browser Popups:** `window.alert()`, `window.confirm()`, and `window.prompt()` are forbidden. Use branded native `<dialog class="rfs-dialog">` modals and non-blocking `popover="manual"` `.rfs-toast-region` notifications.
- **Destructive Confirmations:** Delete, clear, reset, and overwrite actions must prompt with `<dialog class="rfs-dialog is-destructive">`, naming the target, placing `autofocus` on **Cancel**, and styling confirmation with `.rfs-btn-fault`.
- **Iconography:** Use the 60-icon Cyclorama Precision Silkscreen library (`brand/icons/rfs-icons.svg`, `24×24`, `1.75px`, `square` caps, `miter` joins).
