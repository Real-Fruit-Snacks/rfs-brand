# RFS Brand Guide

**Real-Fruit-Snacks** · short form **RFS** · tagline **Built local-first.**  
World: **Cyclorama Dawn** · Palette: **Steel & Beacon Orange**  
Modes: **Beacon Horizon (`LX 263`, dark default)** · **Alabaster Day (`LX 512`, light)**

This file is the source of truth. If an asset in `brand/` or `assets/` disagrees with `BRAND.md`, update the generator and regenerate.

---

## 1. Color — *Steel & Beacon Orange*

Two canonical modes built on a neutral matte cyclorama ground (**Blackout `#050507`**, explicit default on every RFS page via `<meta name="color-scheme" content="dark">`) and an opt-in **Alabaster Day (`#F5F7F9`)** daylight paper. Two calibrated chromatic poles — **Glacial Steel** and **Maritime Beacon Orange** — sweep across horizon washes, lighting rules, and focus states. Every text pairing passes WCAG AA (≥ 4.5:1) and every interactive control border passes WCAG 1.4.11 (≥ 3:1).

| Token | Dark (`LX 263`) | Light (`LX 512`) | Role |
|---|---|---|---|
| `bg` | `#050507` | `#F5F7F9` | Page ground. Neutral matte cyclorama black (zero blue-slate drift) or alabaster paper. |
| `rail` | `#070709` | `#EAEEF2` | Navigation rail and secondary structural chrome. |
| `surface` | `#0C0C10` | `#FFFFFF` | Cards, panels, proof desk, and terminal frames. |
| `raised` | `#14141A` | `#E3E8EE` | Inputs, chips, pills, and nested elements. |
| `line` | `rgba(255,255,255,0.14)` (`#27272E`) | `rgba(13,16,22,0.16)` (`#CFD5DC`) | Hairlines and structural dividers. |
| `line-strong` | `#62646D` | `#6E7682` | Control borders (≥ 3.1:1 against `bg`, `surface`, `raised`, and `code-bg`). |
| `text` | `#F4F5F8` | `#0D1016` | Primary copy and headlines. |
| `mute` | `#B3B5C0` | `#474D59` | Secondary copy, metadata, captions (≥ 7:1 dark / ≥ 7.9:1 light). |
| `steel` | `#1F547A` | `#1F547A` | Glacial Steel physical cyclorama wash pole. |
| `steel-fill` | `#18496B` | `#18496B` | Primary Steel fill (`#FFFFFF` text ≥ 9.5:1). |
| `steel-ink` | `#74B8E8` | `#164669` | Text-safe Glacial Steel for labels, counts, and cue indices. |
| `beacon` | `#F06E2B` | `#F06E2B` | Maritime Beacon Orange physical cyclorama wash pole (`#CC5016` deep wash). |
| `beacon-ink` | `#FF9254` | `#AD3D0A` | Text-safe Maritime Beacon Orange for links, active indicators, and focus rings. |
| `primary` | `#F06E2B` | `#AD3D0A` | Single-color brand accent (dark graphic/beacon; light accessible ink/fill). |
| `on-primary` | `#050507` | `#FFFFFF` | Foreground on solid `primary` fills (≥ 7.5:1 dark / ≥ 6.7:1 light). |
| `accent` · Amber | `#FFC247` | `#885800` | Terminal warnings (`!`), highlights, secondary tags. |
| `signal` · Mint | `#3DDC97` | `#127247` | Terminal success (`ok`). Only ever means "succeeded". |
| `fault` · Signal Crimson | `#FF5C6C` | `#B91C2E` | Error/failure ink (`x`), borders, `[fail]` tags, diff deletions. Distinct from Beacon Orange (`26°` separation). |
| `fault-fill` | `#C92438` | `#B91C2E` | Destructive button fill (`#FFFFFF` text ≥ 5.54:1 dark / ≥ 6.43:1 light; hover `#E02E44` / `#991525`). |
| `code-bg` | `#08080B` | `#EEF2F5` | Terminal and code block surface. |

Machine-readable tokens & drop-in kit: [`brand/tokens/rfs.css`](brand/tokens/rfs.css), [`brand/tokens/rfs-components.css`](brand/tokens/rfs-components.css), [`brand/tokens/rfs.tokens.json`](brand/tokens/rfs.tokens.json), and [`brand/BRAND-RULES.md`](brand/BRAND-RULES.md).

### Six-Phase Cyclorama Scale (`LX 001` – `LX 512`)

Full web surfaces (`real-fruit-snacks.github.io`) support six lighting cues driven by a horizontal cyclorama crossfade:

- `LX 001` **Blackout** (dark) — `#06070A` → `#090B10` → `#131922`
- `LX 127` **Glacial Steel** (dark) — `#070A0E` → `#133954` → `#1F547A`
- `LX 263` **Beacon Horizon** (dark default) — `#07090D` → `#1E5078` → `#F06E2B`
- `LX 389` **Maritime Flame** (dark) — `#0B0707` → `#7A2A0A` → `#CC5016`
- `LX 455` **Warm Frost** (light) — `#FDF8F5` → `#F0E6DE` → `#DCE5ED`
- `LX 512` **Alabaster Day** (light default) — `#F5F7F9` → `#F0F4F8` → `#FDF5F0`

### Color Rules

- **Status always carries words.** Mint (`ok`), Amber (`warn`), and Signal Crimson (`fail`) never stand alone without explicit text (WCAG 1.4.1).
- **Focus indicator:** 2px solid `focus` (`#FF9254` dark / `#AD3D0A` light) with 3px `outline-offset` on `:focus-visible`.
- **Horizon wash, never neon glow.** Use clean multi-stop linear washes sweeping Steel (`#18496B` / `#1F547A`) into Beacon Orange (`#CC5016` / `#F06E2B`). Do not add radial neon halos or blue-tinted drop shadows on cards.
- **Forced Colors Mode:** Always provide `@media (forced-colors: active)` system color fallbacks (`Canvas`, `CanvasText`, `Highlight`, `LinkText`, `GrayText`).

---

## 2. Typography

Three self-hosted variable SIL OFL families (zero external CDN calls):

- **Display / Wordmark / Headlines:** **Big Shoulders Stencil** (`700–900`, uppercase condensed theatrical stencil, tracking `+0.055em`)
- **UI & Prose:** **Albert Sans** (`400–700`)
- **Code, Repo Slugs & Telemetry:** **Azeret Mono** (`400–600`)

```css
--rfs-font-display: "Big Shoulders Stencil", "Arial Narrow", sans-serif;
--rfs-font-sans: "Albert Sans", system-ui, -apple-system, sans-serif;
--rfs-font-mono: "Azeret Mono", ui-monospace, "Cascadia Code", Consolas, monospace;
```

| Role | Size / Line | Family · Weight | Tracking |
|---|---|---|---|
| Display | `clamp(2.55rem, 1.4rem + 3.4vw, 4.95rem)` / `0.96` | Big Shoulders Stencil 800 | `+0.055em` |
| Headline | `clamp(2rem, 1.4rem + 2vw, 3.15rem)` / `1.0` | Big Shoulders Stencil 700 | `+0.055em` |
| Title | `1.65rem` / `1.05` | Big Shoulders Stencil 700 | `+0.055em` |
| Body | `1rem` / `1.55` | Albert Sans 400 | `0` |
| Label | `0.78rem` / `1.2` | Albert Sans 600 · uppercase | `+0.08em` |
| Code | `0.84rem` / `1.6` | Azeret Mono 400 | `0` |

**Space:** 4px grid (`--rfs-space-1` through `--rfs-space-9`: 4, 8, 12, 16, 24, 32, 48, 64, 96px).

---

## 3. Mark — *Cyclorama Monogram Tile*

`RFS` set in **Big Shoulders Stencil** ExtraBold (outlined vector paths, zero font dependency) above a Steel → Beacon Orange horizontal bar on a 64×64 rounded tile (`rx="14"`), optically centered as one unified group across every surface:

- **Master / Dark (`rfs-mark-dark.svg`):** Matte `#050507` cyclorama ground with a rising lower-edge **Glacial Steel → Maritime Beacon Orange** horizon wash (`#133954 → #1F547A → #CC5016 → #F06E2B`), crisp `rgba(255,255,255,0.16)` hairline border, `#F4F5F8` stencil `RFS`, and a Steel→Beacon bar underneath—matching the 1024px profile avatar and every org banner.
- **Light (`rfs-mark-light.svg`):** Crisp Alabaster `#FFFFFF` tile with 1.5px `#CFD5DC` hairline border, `#0D1016` stencil `RFS`, and the identical Steel→Beacon horizon bar underneath.
- **Full-bleed square (`rfs-mark-*-square.svg`):** Same geometry without rounded corners for iOS `apple-touch-icon` and maskable icons.
- **Single-color (`rfs-mark-mono-{white,ink}.svg`):** 3.5-unit stroked tile + solid stencil `RFS` + monochrome bar for stickers, print, and etching.
- **Lockups (`brand/lockup/`):** Horizontal and stacked lockups pairing the unified tile with `REAL-FRUIT-SNACKS` in Big Shoulders Stencil and a Steel→Beacon horizon bar.

All SVG masters are generated by `tools/make-marks.py`. Never hand-edit paths.

---

## 4. Principles & Voice

Four core commitments held across every active public Real-Fruit-Snacks repository:

1. **01 / LOCAL — Local-first by default:** Software runs on your machine against your own files, certs, and processes—not behind a cloud sync service.
2. **02 / PRIVACY — No accounts or tracking:** Zero signups, zero telemetry beacons, and zero third-party analytics scripts.
3. **03 / OPEN — Source-first on GitHub:** Every active project is public, inspectable, and documented plainly alongside its inputs and outputs.
4. **04 / DIRECT — Direct downloads & reproducible setups:** Releases, source builds, and scripted setups stay straightforward and reproducible without extra lock-in.

Voice: **Plain**, **Specific**, **Dry**, **Honest**. No emoji, no hype words ("blazing", "seamless", "powerful", "supercharge"), no exclamation marks in headlines or README one-liners.

---

## 5. Naming

| Thing | Rule | Example |
|---|---|---|
| Repo | `thing-it-does`, lowercase, hyphens, 2–3 words | `port-sync` |
| Description | ≤ 60 chars, sentence case, no trailing period, matches README line 1 | `Keeps qBittorrent's port synced to Proton VPN` |
| Topics | Max 6; ≥ 1 language tag + ≥ 1 domain tag | `rust` `networking` `windows` |
| CLI | One binary per repo, named after the repo | `port-sync` |
| Releases | SemVer `vX.Y.Z`, release title equals tag, no codenames | `v1.4.0` |
| Retiring | Archive on GitHub, mark read-only, move into `retired` in `tools.json` | `forge-framework` |
| Deep docs | Versioned Markdown in `docs/*.md` (keep `README.md` 40–60 lines) | `docs/USAGE.md` |
| Account / Org | `Real-Fruit-Snacks` in URLs; **RFS** in marks and compact badges | `Real-Fruit-Snacks` |

---

## 6. Where Each Asset Goes — Static vs. Animated Standards

Org artwork is governed by **three explicit art standards** rather than treating static and animated SVGs interchangeably. Every animated asset must satisfy the **Static-First Invariant**: its base SVG DOM (outside `@media (prefers-reduced-motion: no-preference)`) is byte-for-byte visually identical to the finished still frame so static rasterizers (`resvg`), social scrapers, and reduced-motion viewers never see blank or half-drawn art.

| Standard | Canonical Files | Motion Budget & Loop | Technical Rules | Allowed Surfaces |
|---|---|---|---|---|
| **Static Standard** | `rfs-banner-{dark,light}.svg`, `rfs-banner-*-1600.png`, `rfs-social-org-*-1280x640.png`, `rfs-header-*-1500x500.png`, `rfs-avatar-*-1024.png`, `brand/mark/*` | **0ms / None** (zero `<style>` keyframes) | Outlined `<path>` glyphs only; full legibility at `400px` thumbnail width; deterministic `resvg` PNG export | Open Graph previews, social headers, profile avatars, print/stickers, link cards, reduced-motion fallbacks |
| **Animated One-Shot** | `assets/rfs-banner-{dark,light}-animated.svg`, `<repo>/docs/assets/cover-{dark,light}.svg` | **≤ 1.4s** banners (`1.22s` DMX fader bring-up), **≤ 3.5s** typed covers; **plays once** (`fill-mode: both`, zero infinite loop) | Pure inline CSS `@keyframes` inside `@media (prefers-reduced-motion: no-preference)`; compositor `transform` / `opacity` + single `pathLength` curve draw; zero JS or SMIL (GitHub `camo` safe) | Org & repo README heroes, live documentation headers |
| **Ambient Showcase** | `Real-Fruit-Snacks/assets/board-{dark,light}.svg` | **3.2s dwell / item** (`35.2s` full 11-tool cycle); `step-end` index changes, **0 flashes/sec** | Reserved strictly for multi-item data showcases; base SVG attributes leave `#01` completely readable (`opacity="0"` on wipe masks); web embeds running `> 5s` must expose a keyboard-accessible **Pause / Play** control (WCAG 2.2.2) | GitHub profile README cue board, interactive brand manual preview |

| Need | File | Generator |
|---|---|---|
| GitHub profile avatar (`1024×1024` circular-safe, static) | `brand/social/rfs-avatar-dark-1024.png` (and 512, 256, SVG) | `tools/make-avatar.py` |
| Favicons & PWA web icons (static) | `brand/web/*` (`icon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192/512/maskable-512.png`, `manifest.webmanifest`, `head.html`) | `tools/make-marks.py` |
| Brand marks & lockups (static) | `brand/mark/*`, `brand/lockup/*`, `assets/rfs-mark-*.svg` | `tools/make-marks.py` |
| Precision silkscreen icon library (60 SVGs + sprite) | `brand/icons/*.svg`, `brand/icons/rfs-icons.svg`, `brand/icons/icons.json` | `tools/make-icons.py` |
| Org banner — Static (`1200×400` / `1600×533`) | `assets/rfs-banner-{dark,light}.svg`, `brand/lockup/rfs-banner-*-1600.png` | `tools/make-org-art.py` |
| Org banner — Animated One-Shot (`1200×400`) | `assets/rfs-banner-{dark,light}-animated.svg` | `tools/make-org-art.py` |
| Org social preview (static `1280×640`) | `brand/social/rfs-social-org-{dark,light}-1280x640.png` | `tools/make-org-art.py` |
| Social header (static `1500×500`) | `brand/social/rfs-header-{dark,light}-1500x500.png` | `tools/make-org-art.py` |
| GitHub profile cue board (ambient showcase) | `Real-Fruit-Snacks/assets/board-{dark,light}.svg` | `art/make-board.py` |
| Per-repo README cover (one-shot SVG) & social PNG | `<repo>/docs/assets/cover-{dark,light}.{svg,png}`, `social-{dark,light}.png` | `tools/make-cover.py` |
| CSS tokens, component kit & JSON | `brand/tokens/rfs.css`, `brand/tokens/rfs-components.css`, `brand/tokens/rfs.tokens.json` | Hand-maintained source |
| Machine-readable agent brand contract | `brand/BRAND-RULES.md` | Hand-maintained source |

---

## 7. Repo Covers

Every active tool repository generates its README cover (`1200×560`, 12px radius) and GitHub social preview (`1280×640`, square) from one `docs/assets/cover.toml` via `tools/make-cover.py`:

- **Field:** Matte `#050507` cyclorama ground (dark) with a calibrated lower-edge **Glacial Steel → Maritime Beacon Orange** horizon wash and crisp structural frame; Alabaster `#F5F7F9` (light) with a soft cool-to-warm horizon tint.
- **Left column:** Repo name set bold in **Big Shoulders Stencil** (uppercase condensed, breaking at a hyphen onto two lines when needed), an animated **Steel → Beacon Orange** horizon rule underneath, and the README one-liner in **Albert Sans** SemiBold. Bottom-left carries the understated `REAL-FRUIT-SNACKS` word signature in **Azeret Mono**.
- **Right panel (`528×448`):** Supports `flow` (Terminal Token transform on Steel→Beacon conduit + recessed status log), `terminal` (Cyclorama console bar with `[shell]` Terminal Token—zero macOS traffic lights), `art`, and `screenshot` kinds (`cover.toml` layout `v2`, plus backward-compatible `layout = "v1"`).
- **Zero font dependency:** Every glyph is converted to SVG `<path>` outlines via `fontTools`.

---

## 8. Motion

- **Curves:**
  - `--rfs-ease: cubic-bezier(0.16, 1, 0.3, 1)` — **Expo Out** (primary entrances, DMX fader lifts, rule draws).
  - `--rfs-ease-in-out: cubic-bezier(0.65, 0, 0.35, 1)` — **Console Crossfade** (cyclorama washes, symmetric state swaps).
  - `--rfs-ease-exit: cubic-bezier(0.7, 0, 0.84, 0)` — **Crisp Exit** (dismissals, closing overlays, fading notices).
  - `--rfs-ease-linear: linear` — **Dwell / Telemetry** (constant-rate progress sweeps).
- **Durations:** `--rfs-dur-fast: 150ms`, `--rfs-dur-base: 250ms`, `--rfs-dur-slow: 520ms`, `--rfs-type-rate: 45ms`.
- **Rules:**
  - **Enabled by Default on Web UIs:** Browser animations, transitions, and circular View Transitions stay **enabled by default** across all RFS pages (never silently turned off by default). Still keep the un-animated base DOM complete so static rasterizers and instant-fallback environments always show finished content (never stranded at `opacity: 0`).
  - **One-shot vs. Ambient:** Banners (`≤ 1.4s`) and repo covers (`≤ 3.5s`) play once and lock onto the static frame. Looping ambient motion is restricted to multi-item showcases (`board-{dark,light}.svg`) and includes a Pause/Play control whenever embedded on web pages (`> 5s`, WCAG 2.2.2).
  - **Safety:** Compositor-only (`transform`, `opacity`), strictly `≤ 3` flashes/sec (target `0`, WCAG 2.3.1), zero JS or SMIL in SVG assets.

---

## 9. Terminal & Code

**Code blocks always display a language header + syntax coloring and wrap by default.** Wrap every framed multi-line snippet in `.rfs-code-card` with a `.rfs-code-head` language badge (`[rust]`, `[python]`, `[toml]`, `[css]`, `[shell]`) and syntax highlighting via `.rfs-tok-*` (`--rfs-syn-*`). Every `<pre>`, command row, and terminal block automatically inherits `white-space: pre-wrap; overflow-wrap: anywhere; word-break: normal; tab-size: 2` from `brand/tokens/rfs.css` so long commands, flags, and URLs remain readable without horizontal scrollbars at any viewport width (WCAG 1.4.10 Reflow). Reserve horizontal scrolling strictly as an opt-in via `.rfs-code-scroll` (or `[data-code-scroll]`) for column-aligned logs or ASCII diagrams.

| Prefix in `cover.toml` | Token | Dark | Light | Meaning |
|---|---|---|---|---|
| `$ ` | `beacon-ink` + `text` | `#FF9254` / `#F4F5F8` | `#AD3D0A` / `#0D1016` | Shell prompt and command |
| `ok ` | `signal` (Mint) | `#3DDC97` | `#127247` | Success (pair with a word stating what succeeded) |
| `! ` | `accent` (Amber) | `#FFC247` | `#885800` | Warning |
| `x ` | `fault` (Signal Crimson) | `#FF5C6C` | `#B91C2E` | Failure |
| *(none)* | `mute` | `#B3B5C0` | `#474D59` | Standard output |

---

## 10. Iconography, Syntax Highlighting & Diagrams

- **Precision Silkscreen Icons (`.rfs-icon`, 60-Icon Colorable Library):** Generated deterministically by `tools/make-icons.py` into `brand/icons/<name>.svg`, `brand/icons/rfs-icons.svg` (`<symbol id="rfs-i-<name>">` + `#rfs-icon-grad-horizon`), and `brand/icons/icons.json`. Vector stroke SVGs on a strict `24×24` optical grid (`2px` inset): `fill="none"`, `stroke="currentColor"`, `stroke-width="1.75"`, crisp industrial `stroke-linecap="square"` and `stroke-linejoin="miter"`. Standard sizes: `16px` (`.rfs-icon-sm`), `20px` (`.rfs-icon`), `24px` (`.rfs-icon-lg`), and `32px` (`.rfs-icon-xl`). Recolor cleanly using semantic classes `.rfs-icon-{text,mute,steel,beacon,ok,warn,fail}` or the Steel→Beacon gradient `.rfs-icon-horizon`. Organized into 6 categories (UI & Navigation, Actions & Controls, Files & Code, Security & System, Network/Media & Tools, Status/Theme & Time). Never use emoji or third-party rounded icon packs in UI, READMEs, or CLI output.
- **Code Syntax Highlighting:** Derived directly from the WCAG-calibrated semantic inks in `brand/tokens/rfs.css` so dark (`LX 263`) and light (`LX 512`) code blocks stay consistent with zero third-party themes:
  - `--rfs-syn-kw` (`.rfs-tok-kw`): `steel-ink` — keywords, types, storage modifiers (`fn`, `pub`, `const`)
  - `--rfs-syn-fn` (`.rfs-tok-fn`): `beacon-ink` — functions, commands, macros (`sync_port`, `println!`)
  - `--rfs-syn-str` (`.rfs-tok-str`): `accent` (Amber) — string literals, paths, URLs
  - `--rfs-syn-num` (`.rfs-tok-num`): `signal` (Mint) — numbers, ports, booleans
  - `--rfs-syn-com` (`.rfs-tok-com`): `mute` — comments and annotations
  - `--rfs-syn-add` / `--rfs-syn-del`: `signal` (`+`) / `fault` (`-`) — unified diff additions and deletions
- **Architecture Diagrams & Mermaid Theme:** Diagrams use `surface` (`#0C0C10` / `#FFFFFF`) nodes, `1px` `line-strong` borders, `steel` (`#1F547A`) primary inputs, `beacon` (`#F06E2B`) active transforms, `signal` (`#3DDC97`) verified outputs, and `Albert Sans` / `Azeret Mono` labels (Mermaid `base` theme with `primaryColor: #14141A`, `primaryBorderColor: #74B8E8`, `lineColor: #FF9254`, `primaryTextColor: #F4F5F8`).

---

## 11. CLI & Terminal Output Standard

Every Real-Fruit-Snacks CLI speaks the same plain, scannable console grammar—matching the `D · Terminal Token` badge aesthetic on the web:

| Prefix | Token | Truecolor Dark | Truecolor Light | 16-Color ANSI | `NO_COLOR` / Pipe |
|---|---|---|---|---|---|
| `[ok]` | `signal` | `#3DDC97` | `#127247` | Green (`32`) | `[ok]` plain text |
| `[!]` | `accent` | `#FFC247` | `#885800` | Yellow (`33`) | `[!]` plain text |
| `[x]` | `fault` | `#FF5C6C` | `#B91C2E` | Red (`31`) | `[x]` plain text |
| `[i]` | `steel-ink` | `#74B8E8` | `#164669` | Cyan (`36`) | `[i]` plain text |
| `$` | `beacon-ink` | `#FF9254` | `#AD3D0A` | Bright Red (`91`) | `$` plain text |

- **`NO_COLOR` & Non-TTY:** Always strip ANSI escape codes when `NO_COLOR` is set (any non-empty value), `TERM=dumb`, or stdout is not a TTY. Because every line starts with a bracketed ASCII tag (`[ok]`, `[!]`, `[x]`, `[i]`), meaning never depends on color.
- **Standard Flags & Exit Codes:** Support `--help`, `--version` (`<tool> vX.Y.Z`), and `--json` for machine-readable output where practical. Exit `0` on success, `1` on runtime failure, and `2` on invalid usage/arguments.

---

## 12. UI States, Layer Scale & Print / Transparency

- **Component Kit (`brand/tokens/rfs-components.css`):** Load directly after `rfs.css` for standardized `.rfs-btn*` (including `.rfs-btn-fault` for destructive confirmations), `.rfs-badge` (`D · Terminal Token`), `.rfs-shell` / `.rfs-scroll-region`, `.rfs-dialog`, `.rfs-link-*`, `.rfs-mark-*`, `.rfs-kbd`, `.rfs-callout`, `.rfs-input`, `.rfs-progress`, and `.rfs-state-box`.
- **Scrollbar Placement (App-Shell Rule):** The vertical scrollbar must **never** extend to the top of the screen alongside a top header or navigation bar. Use `.rfs-shell` (`height: 100dvh; overflow: hidden; display: flex; flex-direction: column`) with the header in `.rfs-shell-header` and all scrollable content inside `.rfs-scroll-region` (`flex: 1; min-height: 0; overflow-y: auto`) so the scrollbar begins cleanly at the header's bottom hairline. Style scrollbars with `scrollbar-width: thin` and `scrollbar-color: var(--rfs-sb-thumb) var(--rfs-sb-track)` (≥ 3:1 thumb contrast, high-contrast override under `prefers-contrast: more`, WebKit fallback inside `@supports not (scrollbar-color: auto)`, and `overflow: visible` reset in `@media print`).
- **Zero Native Browser Modals or Popups:** Never use `window.alert()`, `window.confirm()`, or `window.prompt()` in any RFS web app or tool. All dialogs must be branded Cyclorama Dawn HTML `<dialog class="rfs-dialog">` modals opened via `command="show-modal"` / `showModal()` (with `overscroll-behavior: contain` on both `dialog:modal` and `dialog::backdrop`, `overflow: hidden` on `::backdrop`, and `@starting-style` + `transition-behavior: allow-discrete` transitions).
- **Destructive Action Confirmation:** Whenever a user triggers a destructive or irreversible action (deleting a file/record/item, clearing local data, resetting config, overwriting exports), prompt them with a branded `<dialog class="rfs-dialog is-destructive">` asking if they are sure—naming the exact item affected, stating whether it can be undone, placing `autofocus` on the safe **Cancel** button, and styling the confirm action with `.rfs-btn-fault` (Signal Crimson).
- **Standard UI States:**
  - **Empty (`.rfs-state-box.is-empty`):** Dashed `line-strong` border, `[empty]` Steel Terminal Token, plain explanation of what is missing, and one direct next action.
  - **Loading (`.rfs-progress`):** Real semantic `<progress>` paired with `<label>`. Styled with Steel→Beacon fill (`--rfs-horizon-rule`), separate `::-webkit-progress-value` and `::-moz-progress-bar` rules, and a `10s` reduced-motion cadence on `:indeterminate` (never `animation: none`, which collapses fill width in Chromium).
  - **Error (`.rfs-state-box.is-error`):** Subtle Signal Crimson border mix, `[x]` Fault Terminal Token, plain failure cause, and an immediate recovery action.
- **Z-Index Layer Scale:** `--rfs-z-base: 0`, `--rfs-z-sticky: 20`, `--rfs-z-nav: 40`, `--rfs-z-popover: 60`, `--rfs-z-modal: 80`, `--rfs-z-toast: 100`. Never invent arbitrary values like `9999`.
- **Breakpoints:** `--rfs-bp-sm: 36em` (`576px`), `--rfs-bp-md: 56em` (`896px`), `--rfs-bp-lg: 72em` (`1152px`).
- **Reduced Transparency & Print:** `rfs.css` automatically disables glass `backdrop-filter` under `@media (prefers-reduced-transparency: reduce)` (falling back to solid `--rfs-rail`) and forces clean `#FFFFFF` paper ground, `#0D1016` ink, and `break-inside: avoid` blocks under `@media print`.
- **Drop-In App Primitives (`brand/tokens/rfs-components.css`):** Beyond buttons, badges, and states, the kit standardizes `.rfs-code-card` (language header + syntax-highlighted wrapped code), `.rfs-chip` (4px filter chips—zero 99px capsules), `.rfs-toast-region`/`.rfs-toast.is-{ok,warn,fail,info}` (bottom-right `popover="manual"` semantic colored notifications), `.rfs-popover-panel` (viewport-aware anchored action menus with `.is-fault` destructive items), `.rfs-tooltip` (`popover="hint"`), `.rfs-tabs`, native `<details>` `.rfs-accordion`, customizable `base-select` `.rfs-select`, `.rfs-switch`, `.rfs-card`, `.rfs-kv`, and `.rfs-skeleton`.
- **Agent Contract (`brand/BRAND-RULES.md`):** Drop directly into any repo's `AGENTS.md` (or copy `templates/repo/AGENTS.md`) to enforce all Cyclorama Dawn rules automatically.

---

## 13. Native Desktop & TUI Mapping

Non-web tools (Rust desktop utilities, C# Windows apps, PowerShell & Python/Kali CLIs) inherit the exact same **Cyclorama Dawn** tokens:

- **Windows Window Chrome & Icons:**
  - Enable dark titlebars via `DWMWA_USE_IMMERSIVE_DARK_MODE` (`20`) and set `DWMWA_CAPTION_COLOR` (`35`) to `0x00070505` (BGR for `#050507`) in dark mode or `0x00F2EEEA` (`#EAEEF2`) in light mode.
  - Package multi-size `.ico` executables (`16`, `32`, `48`, `256px`) directly from `brand/mark/rfs-mark-dark.png` / `brand/web/favicon.ico` (never rasterize blurry stretched icons).
- **Rust Terminal Palette (`anstyle` / Truecolor ANSI):**
  - Prompt `$`: `RgbColor(255, 146, 84)` (`#FF9254`) · Info `[i]`: `RgbColor(116, 184, 232)` (`#74B8E8`) · OK `[ok]`: `RgbColor(61, 220, 151)` (`#3DDC97`) · Warn `[!]`: `RgbColor(255, 194, 71)` (`#FFC247`) · Fail `[x]`: `RgbColor(255, 92, 108)` (`#FF5C6C`) · Mute: `RgbColor(179, 181, 192)` (`#B3B5C0`). Strip ANSI whenever `NO_COLOR` is set or `!stdout.is_terminal()`.
- **Python TUI (`rich.theme.Theme`):**
  ```python
  from rich.theme import Theme
  RFS_THEME = Theme({
      "prompt": "bold #FF9254", "info": "bold #74B8E8",
      "ok": "bold #3DDC97", "warn": "bold #FFC247",
      "fail": "bold #FF5C6C", "mute": "#B3B5C0",
  })
  ```
- **Automated Brand Verification (`tools/verify-brand.py`):** Run before every release (and in `.github/workflows/release.yml`) to check JSON validity, byte-sync across `brand/` and `docs/assets/`, zero `in oklch` gradients, zero `window.alert/confirm/prompt`, `CHANGELOG.md` version coverage, and active-tool parity across `tools.json`, `make-board.py`, and `_repo-covers`.

---

## 14. README & Documentation Standard

Every public repository keeps its `README.md` ultra-minimal (**40–60 lines target**) and moves deeper reference material into versioned in-repo Markdown files under `docs/`.

- **What stays in `README.md` (fixed order, 40–60 lines):**
  1. Title (`# repo-name`) and one-line summary (`≤ 60` chars, sentence case, no period, matching the GitHub repo description).
  2. Adaptive cover (`<picture>` referencing `docs/assets/cover-dark.svg` and `docs/assets/cover-light.svg`).
  3. Shortest real install or run snippet (one concise fenced block).
  4. **3–5 concise bullets** describing what the tool does, what goes in, and what comes out locally.
  5. `## Documentation` with direct relative links to `docs/*.md` (and the live project page if published).
  6. `## License` (short license line).
- **What moves to `docs/*.md`:** Complete CLI flag tables, configuration schemas, architecture notes, examples, tested-platform matrices, known limitations, troubleshooting, and development/build-from-source guides. Prefer clean uppercase filenames such as `docs/USAGE.md`, `docs/CONFIGURATION.md`, `docs/ARCHITECTURE.md`, `docs/TROUBLESHOOTING.md`, and `docs/DEVELOPMENT.md`.
- **Coexistence with GitHub Pages:** Repositories that publish GitHub Pages from `docs/` keep `docs/.nojekyll`, `docs/index.html`, and `docs/assets/` alongside `docs/*.md`. GitHub renders Markdown natively in the repository view while `.nojekyll` leaves `.md` files untouched on Pages.
- **No GitHub Wiki:** Disable the separate GitHub Wiki tab in repository settings (`Settings -> General -> Features -> Wikis`). Keeping all documentation inside `docs/` keeps it local-first in `git clone`, versioned with release tags, reviewable in pull requests, and verifiable by CI link checks.

---

*Cyclorama Dawn — Steel & Beacon Orange (`v2.1`). Edit this guide and `brand/tokens/rfs.tokens.json` first; regenerate derived assets second.*
