---
name: Real-Fruit-Snacks — Cyclorama Dawn
version: "2.3.2"
description: Brand-wide Cyclorama Dawn design system (Steel & Beacon Orange) with LX 263 Beacon Horizon dark default and LX 512 Alabaster Day light opt-in.
world: "stagecraft-theater-lighting-cyclorama-dawn"
default_theme: dark
colors:
  steel: "#1F547A"
  steel-fill: "#18496B"
  beacon: "#F06E2B"
  beacon-wash: "#CC5016"
  dark:
    bg: "#050507"
    rail: "#070709"
    surface: "#0C0C10"
    raised: "#14141A"
    code-bg: "#08080B"
    line: "rgba(255, 255, 255, 0.14)"
    line-strong: "#62646D"
    text: "#F4F5F8"
    mute: "#B3B5C0"
    steel-ink: "#74B8E8"
    beacon-ink: "#FF9254"
    primary: "#F06E2B"
    on-primary: "#050507"
    accent: "#FFC247"
    signal: "#3DDC97"
    fault: "#FF5C6C"
    fault-fill: "#C92438"
    on-fault: "#FFFFFF"
    focus: "#FF9254"
  light:
    bg: "#F5F7F9"
    rail: "#EAEEF2"
    surface: "#FFFFFF"
    raised: "#E3E8EE"
    code-bg: "#EEF2F5"
    line: "rgba(13, 16, 22, 0.16)"
    line-strong: "#6E7682"
    text: "#0D1016"
    mute: "#474D59"
    steel-ink: "#164669"
    beacon-ink: "#AD3D0A"
    primary: "#AD3D0A"
    on-primary: "#FFFFFF"
    accent: "#885800"
    signal: "#127247"
    fault: "#B91C2E"
    fault-fill: "#B91C2E"
    on-fault: "#FFFFFF"
    focus: "#AD3D0A"
  dataviz:
    dark: ["#74B8E8", "#FF9254", "#3DDC97", "#FFC247", "#FF5C6C", "#B3B5C0"]
    light: ["#164669", "#AD3D0A", "#127247", "#885800", "#B91C2E", "#474D59"]
typography:
  display:
    fontFamily: '"Big Shoulders Stencil", "Arial Narrow", sans-serif'
    fontSize: "clamp(2.55rem, 1.4rem + 3.4vw, 4.95rem)"
    fontWeight: 800
    lineHeight: 0.96
    letterSpacing: "0.055em"
  headline:
    fontFamily: '"Big Shoulders Stencil", "Arial Narrow", sans-serif'
    fontSize: "clamp(2rem, 1.4rem + 2vw, 3.15rem)"
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: "0.055em"
  body:
    fontFamily: '"Albert Sans", system-ui, -apple-system, sans-serif'
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: '"Albert Sans", system-ui, -apple-system, sans-serif'
    fontSize: "0.78rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.08em"
  mono:
    fontFamily: '"Azeret Mono", ui-monospace, "Cascadia Code", Consolas, monospace'
    fontSize: "0.84rem"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: '"tnum" 1'
radius:
  token: "4px"
  sm: "6px"
  md: "10px"
  tile: "14/64 (21.9%)"
space:
  base: "4px"
  scale: [4, 8, 12, 16, 24, 32, 48, 64, 96]
motion:
  ease: "cubic-bezier(0.16, 1, 0.3, 1)"
  ease-detent: "linear(0, 0.35 12%, 0.78 28%, 1.015 48%, 1.035 58%, 1.01 76%, 1)"
  ease-in-out: "cubic-bezier(0.65, 0, 0.35, 1)"
  ease-exit: "cubic-bezier(0.7, 0, 0.84, 0)"
  dur-fast: "150ms"
  dur-base: "250ms"
  dur-detent: "340ms"
  dur-jump: "360ms"
  dur-slow: "520ms"
z_index:
  base: 0
  sticky: 20
  nav: 40
  popover: 60
  modal: 80
  toast: 100
breakpoints:
  sm: "36em"
  md: "56em"
  lg: "72em"
---

# Design System: Real-Fruit-Snacks — Cyclorama Dawn (v2.3.2)

Authoritative `DESIGN.md` aligned with [`BRAND.md`](../BRAND.md), [`brand/BRAND-RULES.md`](../brand/BRAND-RULES.md), and [`skills/rfs-brand/SKILL.md`](../skills/rfs-brand/SKILL.md).

## 1. Visual Theme & Atmosphere

**Creative North Star: "The Lighting-Desk Cyclorama"**

Cyclorama Dawn frames Real-Fruit-Snacks (`RFS`) software as an architectural studio lighting console rather than a generic SaaS template or retro CRT terminal costume. Absorbent neutral matte black (`#050507`, zero blue-slate tint) holds dense technical content, while calibrated linear washes of **Glacial Steel** (`#1F547A`) sweeping into **Maritime Beacon Orange** (`#F06E2B`) establish depth and drive the six-cue lighting continuum from **LX 263 Beacon Horizon** (explicit dark default) to **LX 512 Alabaster Day** (opt-in light mode on `#F5F7F9`).

Every surface is engineered for solo-authored credibility: local-first execution, zero external CDN requests, self-hosted variable WOFF2 typography, WCAG AA/AAA text contrast in both modes, and explicit `IN -> OUT` proofs.

## 2. Color Palette & Roles

- **Explicit Dark Default:** Every page declares `<meta name="color-scheme" content="dark">` so Dark (`LX 263`) renders by default regardless of OS preference; Light (`LX 512`) is an explicit user toggle persisted under `rfs-theme` / `color-scheme`.
- **Cartesian `in oklab` Gradients Only:** Always interpolate Steel to Beacon using `linear-gradient(... var(--rfs-in-oklab), ...)` — never polar `in oklch`, which introduces violet/green hue drift between opposing poles.
- **Four Surface Tiers:** `--rfs-bg` (`#050507` / `#F5F7F9`) → `--rfs-rail` (`#070709` / `#EAEEF2`) → `--rfs-surface` (`#0C0C10` / `#FFFFFF`) → `--rfs-raised` (`#14141A` / `#E3E8EE`), plus recessed `--rfs-code-bg` (`#08080B` / `#EEF2F5`).
- **Semantic Status (Always Paired with Words, WCAG 1.4.1):**
  - Success `[ok]`: Mint `--rfs-signal` (`#3DDC97` / `#127247`)
  - Warning `[!]`: Amber `--rfs-accent` (`#FFC247` / `#885800`)
  - Failure / Destructive `[x]`: Signal Crimson `--rfs-fault` (`#FF5C6C` / `#B91C2E`) and `--rfs-fault-fill` (`#C92438` / `#B91C2E`, `#FFFFFF` text)
- **Data Visualization (`--rfs-viz-1` through `--rfs-viz-6`):** Ordered categorical sequence (`Steel` → `Beacon` → `Mint` → `Amber` → `Crimson` → `Slate`), passing `>= 5.8:1` in both Dark and Light.
- **Focus Ring:** `2px solid var(--rfs-focus)` (`#FF9254` dark / `#AD3D0A` light) with `3px` `outline-offset` on `:focus-visible`.

Machine-readable exports: [`brand/tokens/rfs.css`](../brand/tokens/rfs.css), [`brand/tokens/rfs.tokens.json`](../brand/tokens/rfs.tokens.json), [`brand/tokens/rfs.dtcg.json`](../brand/tokens/rfs.dtcg.json) (W3C DTCG), [`brand/tokens/rfs-tailwind.css`](../brand/tokens/rfs-tailwind.css) (Tailwind v4 `@theme`), and [`brand/tokens/rfs-tokens.ts`](../brand/tokens/rfs-tokens.ts).

## 3. Typography Rules

Three self-hosted variable SIL OFL families (zero external font CDNs):
- **Display / Wordmark / Section Headings:** `Big Shoulders Stencil` (`700–900`, uppercase, `+0.055em` tracking, line-height `0.96`–`1.05`).
- **UI Chrome & Running Prose:** `Albert Sans` (`400–700`, `1rem` / `1.55` body capped at `58ch`–`66ch`, `0.78rem` `600` uppercase `+0.08em` labels).
- **Code, CLI, Repo Slugs & Telemetry:** `Azeret Mono` (`400–600`, `tabular-nums`, strictly for real technical identifiers—never general nav links or paragraphs).

## 4. Component Stylings (`rfs-components.css` + `rfs-motion.js`)

Load `rfs.css`, then `rfs-components.css`, then optional zero-dependency `rfs-motion.js`:
- **Buttons & Armed Latches:** `.rfs-btn-horizon` (borderless `oklab` Steel→Beacon fill + shimmer sweep, `#FFFFFF` text), `.rfs-btn-beacon`, `.rfs-btn-steel`, `.rfs-btn-fault` / `.rfs-btn-fault-soft` / `.rfs-btn-fault-outline` (Signal Crimson destructive actions), `.rfs-btn-outline`, `.rfs-btn-ghost`, `.rfs-btn-copy-morph`, and `[data-rfs-arm]` two-stage destructive latch.
- **Hardware Controls (`--rfs-ease-detent`):** Checkboxes (`.rfs-check`, `.rfs-check-shutter`, `.rfs-check-token` with `:indeterminate`), semantic `<input type="checkbox" switch>` toggles (`.rfs-switch`, `.rfs-switch-breaker`, `.rfs-switch-patch`), ballistic Jumping Radios (`[data-rfs-radio-jump="reticle|aperture"]`), sliding `.rfs-segmented` cue bars, and `.rfs-fader` console sliders.
- **Upgraded Hardware Loaders (4 Native Systems):** `.rfs-progress-dmx-shell` (DMX Cue Meter with etched 10% ticks + Signal Mint `100%` lock), `.rfs-progress` (Horizon Alive Trace), `.rfs-led-ladder` (20-cell patch-bay LED bar), and `.rfs-progress-ring` / `.rfs-spinner` (hollow `border-area` conic ring using `background-image:` overrides).
- **Badges & Filter Chips (`D · Terminal Token` only):** `4px` radius, `--rfs-code-bg` surface, `1px solid var(--rfs-line)` full perimeter, colored bracketed `.k` prefix (`[ok]`, `[!]`, `[x]`, `[steel]`, `[beacon]`) + neutral `--rfs-text`. Zero `99px` capsule pills or status dots.
- **Framed Code Cards (`.rfs-code-card`):** Explicit language badge header + `.rfs-tok-*` syntax coloring + wrapped lines by default (`pre-wrap`, `overflow-wrap: anywhere`; `.rfs-code-scroll` opt-in for ASCII art/wide tables). Zero macOS traffic-light dots.
- **Callouts & Quotes:** `.rfs-callout.is-{note,tip,warn,fail}` and `.rfs-quote` use a `3.5px` inline-start semantic rail paired with `1px` `--rfs-line` borders and explicit uppercase tone labels.
- **Branded Native `<dialog class="rfs-dialog">` & Semantic Toasts:** Zero `window.alert()`, `window.confirm()`, or `window.prompt()`. Destructive actions use `<dialog class="rfs-dialog is-destructive">` naming the target, `autofocus` on **Cancel**, and `.rfs-btn-fault` confirm. Non-blocking `popover="manual"` toasts tint via `.rfs-toast.is-{ok,warn,fail,info}`.
- **Icons (`rfs-icons.svg` + `.rfs-icon-live`):** 60 monochrome `24×24` Precision Silkscreen stroke icons (`1.75px`, `square` caps, `miter` joins, `>= 44×44px` tap targets, recolorable via `.rfs-icon-*`). Calm by default; opt into bespoke part-level hover/click choreography on all 60 icons with `.rfs-icon-live` + `data-rfs-motion="part-*"` + `data-rfs-icon-click`.

## 5. Layout Principles & Page Archetypes

- **4px Base Spacing Scale:** `--rfs-space-1` (`4px`) through `--rfs-space-9` (`96px`).
- **App-Shell Scrollbars:** Top headers sit inside `.rfs-shell-header` above `.rfs-scroll-region` inside a `100dvh` `.rfs-shell` (`overflow: hidden`) so vertical scrollbars always start cleanly below top navigation chrome.
- **Five Bespoke Page Archetypes** (choose per tool domain; never clone one template blindly across distinct tools — full decision tree in `skills/rfs-brand/references/page-archetypes.md`):
  1. **Interactive Proof Console** (`rfs.tools`, `Real-Fruit-Snacks.github.io`, `port-sync`, `screen-mark`)
  2. **Safety Matrix & Protocol Spec** (`cred-spray`, `certapi`)
  3. **Topology & Signal Pipeline Workbench** (`shell-tunnel`, `ad-sweep`, `hash-bait`, `carify`, `amazon-order-sync`)
  4. **Editorial Handbook & Command Ledger** (`pwn-broker`, `pwn-playbooks`, `pwn-report`, `pwn-shop`, `powershell-toolbox`)
  5. **Full-Viewport Offline App** (`open-file`, `identity-gen`)

## 6. Depth, Elevation & Motion

- **Flat Hairline-First Architecture:** Separate resting planes using `1px` full-perimeter hairlines (`--rfs-line`, `--rfs-line-strong` >= 3.11:1) and matte luminance steps (`--rfs-bg` → `--rfs-surface` → `--rfs-raised`)—never neon glows, glassmorphic floating pills, or heavy card drop shadows.
- **Z-Index Scale:** `base: 0`, `sticky: 20`, `nav: 40`, `popover: 60`, `modal: 80`, `toast: 100`.
- **Motion & CAD Geometry (`[dwg] rfs-01`–`rfs-05`):** Enabled by default on web UIs (`--rfs-ease`, `--rfs-ease-detent` 3.5% mechanical settle, `--rfs-ease-in-out`, `--rfs-ease-exit`, `--rfs-dur-fast: 150ms`, `--rfs-dur-base: 250ms`, `--rfs-dur-detent: 340ms`, `--rfs-dur-jump: 360ms`, `--rfs-dur-slow: 520ms`). SVG assets strictly follow the Static-First Invariant with keyframes guarded inside `@media (prefers-reduced-motion: no-preference)`. Geometric clear-space rules: `14u` (`1×rx`) on `64×64u` tile (`rfs-01`), `16u` + `< 160px` collapse on `405×64u` lockup (`rfs-02`), `2u` inset + `44×44px` tap target on `24×24u` icons (`rfs-03`), `1200×560` + `40px` social bleed (`1280×640`) on Repo Cover v2 (`rfs-04`), and `64px` shell header scrollbar lock (`rfs-05`).

## 7. Do's and Don'ts

### Do
- Keep dark grounds strictly achromatic matte black (`#050507`) and interpolate all Steel→Beacon gradients in `in oklab`.
- Pair every status color with an explicit ASCII/word token (`[ok]`, `[!]`, `[x]`, `[i]`).
- Use self-hosted WOFF2 fonts, the 60-icon Precision Silkscreen sprite, wrapped `.rfs-code-card` snippets, `.rfs-shell` scrollbars, and branded `<dialog>` confirmations.
- Honor `prefers-reduced-transparency: reduce`, `prefers-contrast: more`, `forced-colors: active`, and `@media print`.
- Keep `README.md` ultra-minimal (40–60 lines) and verify repos with `python tools/verify-brand.py --repo <path>`.

### Don't
- Never tint dark surfaces into blue-slate (`#0f172a`, `#111827`), use `in oklch` gradients, or add neon outer glows.
- Never call `window.alert()`, `window.confirm()`, or `window.prompt()`.
- Never draw fake macOS traffic-light dots, `99px` capsule status pills, emoji, or `shields.io` badge walls.
- Never load fonts or scripts from external CDNs (`fonts.googleapis.com`, etc.).
- Never publish plain unwashed white Alabaster marks or light covers (`0.14` wash is deprecated; marks use `0.36` wash and covers/banners use `0.32`).

## 8. Responsive Behavior

- **Breakpoints:** `sm: 36em` (`576px`), `md: 56em` (`896px`), `lg: 72em` (`1152px`).
- **Zero Horizontal Overflow:** Maintain `scrollWidth <= innerWidth` down to `390px` viewport width (`min-width: 0` on all grid children; `.table-wrap` container queries for dense token tables).
- **Touch & Keyboard:** Maintain `>= 44px` tap targets on coarse pointers and visible `2px solid var(--rfs-focus)` (`3px` offset) keyboard focus rings across all interactive elements.

## 9. Agent Prompt Guide

```markdown
Read `rfs-brand/skills/rfs-brand/SKILL.md` (or `https://real-fruit-snacks.github.io/rfs-brand/llms.txt`) before authoring UI, CLI, docs, or covers for any Real-Fruit-Snacks repository.
- Load `rfs.css` then `rfs-components.css` (plus `rfs-tailwind.css` for Tailwind v4 or `rfs-tokens.ts` for TS).
- Dark LX 263 (`#050507`) is default; Light LX 512 (`#F5F7F9`) is opt-in toggle; Cartesian `in oklab` gradients only.
- Use `D · Terminal Token` 4px badges, `.rfs-shell` below-header scrollbars, and branded `<dialog>` modals (zero native popups).
- Audit every change with: `python rfs-brand/tools/verify-brand.py --repo <target-repo>`
```
