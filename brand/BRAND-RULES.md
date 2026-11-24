# RFS Brand Rules — Cyclorama Dawn (Steel & Beacon Orange)

Drop-in brand contract for any **Real-Fruit-Snacks** (**RFS**) repository, web UI, CLI, or agent instruction file (`AGENTS.md` / `CLAUDE.md`).  
Source of truth: `rfs-brand/BRAND.md` · Tokens: `rfs.css` + `rfs-components.css` + `rfs.tokens.json`.

## 1. Visual Identity & Color
- **Modes & Motion (Default Rule):** Dark mode (**Beacon Horizon `LX 263`** on neutral matte `#050507`, zero blue-slate tint) is the **explicit default** on every RFS page (`<meta name="color-scheme" content="dark">`); Light (**Alabaster Day `LX 512`** on `#F5F7F9`) is an opt-in user toggle. Keep browser animations, motion transitions, and View Transitions **enabled by default**—never turn them off by default.
- **Two chromatic poles only:** Glacial Steel (`#1F547A` / `#18496B` fill / `#74B8E8` dark ink / `#164669` light ink) and Maritime Beacon Orange (`#F06E2B` / `#FF9254` dark ink / `#AD3D0A` light ink).
- **Cartesian `in oklab` gradients always:** Never interpolate Steel → Beacon in polar `in oklch` (introduces mud/green-pink drift). Use `--rfs-horizon-gradient` and `--rfs-horizon-rule`.
- **No neon glows or colored drop shadows:** Use calibrated horizon washes and 1px structural hairlines (`--rfs-line`, `--rfs-line-strong` ≥ 3:1).
- **Status always carries words (WCAG 1.4.1):** Mint (`#3DDC97` / `#127247`) = `[ok]`, Amber (`#FFC247` / `#885800`) = `[!]`, Raspberry (`#F06292` / `#B0306A`) = `[x]`.

## 2. Typography & Code Blocks
- **Self-hosted variable fonts only (zero external CDNs):**
  - Display / headings / repo titles: `Big Shoulders Stencil` (`700–900`, uppercase, `+0.055em` tracking).
  - UI & prose: `Albert Sans` (`400–700`).
  - Code, CLI, telemetry, repo slugs: `Azeret Mono` (`400–600`).
- **Code blocks show language + syntax coloring and wrap by default:** Wrap every framed code snippet in `.rfs-code-card` with a `.rfs-code-head` language badge (`[rust]`, `[python]`, `[toml]`, `[css]`, `[shell]`) and syntax highlighting via `.rfs-tok-*` (`--rfs-syn-*`). Inherit `white-space: pre-wrap; overflow-wrap: anywhere; word-break: normal; tab-size: 2` from `rfs.css`; only add `.rfs-code-scroll` (or `[data-code-scroll]`) for strictly column-aligned ASCII diagrams or wide tables.

## 3. Components & Chrome
- **Load both stylesheets in web tools:** `<link rel="stylesheet" href="rfs.css">` followed by `<link rel="stylesheet" href="rfs-components.css">`.
- **Badges = `D · Terminal Token` only:** `4px` radius, `var(--rfs-code-bg)` recessed surface, `1px` full-perimeter `var(--rfs-line)` border, colored bracketed `.k` prefix (`[ok]`, `[!]`, `[x]`, `[steel]`, `[beacon]`) + neutral `var(--rfs-text)` label. Zero status dots, zero thick left-edge stripes, zero `99px` capsule pills.
- **Zero fake OS chrome:** Never draw red/yellow/green macOS traffic-light dots on terminal frames; use a `3px` Steel→Beacon top edge and a `[shell]` Terminal Token header.
- **Zero AI clichés:** No emoji in UI/docs/CLI, no hype copy ("blazing", "seamless", "supercharge"), no exclamation marks in headings or repo descriptions, no floating glassmorphic pills.
- **Buttons:** `.rfs-btn-horizon` (borderless Steel→Beacon `oklab` fill, `#FFFFFF` text), `.rfs-btn-beacon`, `.rfs-btn-steel`, `.rfs-btn-fault` (destructive confirm), `.rfs-btn-outline`, `.rfs-btn-ghost`. Always keep `:focus-visible` at `2px solid var(--rfs-focus)` with `3px` offset.
- **Scrollbars never run to the top of the screen:** Keep top headers outside the scrolling container using `.rfs-shell` (`100dvh`, `overflow: hidden`, column flex) + `.rfs-shell-header` + `.rfs-scroll-region` (`flex: 1; min-height: 0; overflow-y: auto`) so the scrollbar always starts below the header hairline. Never animate `scrollbar-color`.
- **Zero native browser modals / popups:** Strictly forbid `window.alert()`, `window.confirm()`, and `window.prompt()`. Always render branded Cyclorama Dawn HTML `<dialog class="rfs-dialog">` modals via `command="show-modal"` or `showModal()` (with `overscroll-behavior: contain` on `dialog:modal` and `dialog::backdrop`, `overflow: hidden` on `::backdrop`, and `returnValue` reset on close).
- **Confirm all destructive actions:** Any delete, clear, reset, or irreversible overwrite MUST open a `<dialog class="rfs-dialog is-destructive">` asking if the user is sure, naming the exact target, putting `autofocus` on **Cancel**, and styling the confirm action with `.rfs-btn-fault`.
- **Semantic colored toasts:** Tint non-blocking `popover="manual"` toasts to match their status via `.rfs-toast.is-ok` (Mint green), `.is-warn` (Amber yellow), `.is-fail` (Fault raspberry), and `.is-info` (Glacial steel).

## 4. Marks, Art & Repo Covers
- **Unified dark tile:** Matte `#050507` + rising lower Steel→Beacon wash + white stencil `RFS` + Steel→Beacon bar (`brand/mark/rfs-mark-dark.svg`). Never hand-edit mark paths.
- **Repo covers (`docs/assets/cover.toml` → `tools/make-cover.py`):** Word-only `REAL-FRUIT-SNACKS` bottom-left signature (no redundant RFS icon box). Use `panel.kind = "flow"` or `"terminal"` (v2) with truthful commands/outputs—never invent CLI flags.
- **3 SVG Art Tiers + Static-First Invariant:**
  1. **Static Standard** (`0ms`, zero `<style>` keyframes): social previews, avatars, favicons, print.
  2. **Animated One-Shot** (`≤ 1.4s` banners, `≤ 3.5s` covers, plays once, zero infinite loop): README heroes.
  3. **Ambient Showcase** (`board-{dark,light}.svg` only): multi-item data displays with `0` flashes/sec and a keyboard-accessible **Pause / Play** button on web embeds (WCAG 2.2.2).
  - Base SVG DOM outside `@media (prefers-reduced-motion: no-preference)` must render the complete finished still frame.

## 5. Icons, Syntax, Diagrams & CLI
- **Icons (Colorable 60-Icon Library):** Use the canonical 60-icon Cyclorama Precision Silkscreen set (`brand/icons/rfs-icons.svg` / `brand/icons/*.svg`, generated by `tools/make-icons.py`): `24×24`, `fill="none"`, `stroke="currentColor"`, `stroke-width="1.75"`, `linecap="square"`, `linejoin="miter"`, sizes `16 / 20 / 24 / 32px`. Recolor cleanly with semantic classes `.rfs-icon-{text,mute,steel,beacon,ok,warn,fail}` or Steel→Beacon gradient `.rfs-icon-horizon` (`#rfs-icon-grad-horizon`). Zero emoji or mismatched third-party icon packs.
- **Syntax & Mermaid:** Map keywords → `--rfs-syn-kw` (`steel-ink`), functions → `--rfs-syn-fn` (`beacon-ink`), strings → `--rfs-syn-str` (`accent`), numbers/additions → `--rfs-syn-num`/`--rfs-syn-add` (`signal`), comments → `--rfs-syn-com` (`mute`), deletions → `--rfs-syn-del` (`fault`).
- **CLI Standard:** Support `--version`, `--help`, and `--json` where applicable. Respect `NO_COLOR` and non-TTY stdout by stripping ANSI escapes while preserving bracketed tags (`[ok]`, `[!]`, `[x]`, `[i]`). Standard exit codes: `0` ok, `1` runtime error, `2` usage/argument error.
- **Native Desktop & TUI:** Windows apps set `DWMWA_USE_IMMERSIVE_DARK_MODE` + `#050507` caption color and bundle `brand/web/favicon.ico` / `brand/mark/` `.ico` icons. Rust (`anstyle`) and Python (`rich`) CLIs map `[ok]` `#3DDC97`, `[!]` `#FFC247`, `[x]` `#F06292`, `[i]` `#74B8E8`, `$` `#FF9254`.

## 6. UI States, Layers & Accessibility
- **Standard states:** Use `.rfs-state-box.is-empty` (`[empty]` + next action), native `<progress class="rfs-progress">` (determinate & indeterminate), labeled `.rfs-skeleton` loading placeholders, and `.rfs-state-box.is-error` (`[x]` + recovery action).
- **Z-index scale:** `base: 0`, `sticky: 20`, `nav: 40`, `popover: 60`, `modal: 80`, `toast: 100`.
- **Breakpoints:** `sm: 36em` (576px), `md: 56em` (896px), `lg: 72em` (1152px).
- **Media contracts:** Keep UI animations enabled by default; honor `prefers-reduced-transparency: reduce` (disable blur/glass), `forced-colors: active` (system color tokens), and `@media print` (clean `#FFFFFF` ground, `#0D1016` ink, wrapped code).
