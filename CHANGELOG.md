# Changelog

Each release publishes `rfs-brand.zip` (everything below except `.github/` and `docs/`), `rfs.css`, `rfs-components.css`, `rfs-motion.js`, `rfs.tokens.json`, `rfs.dtcg.json`, `rfs-tailwind.css`, `rfs-tokens.ts`, `rfs-icons.svg`, and `BRAND-RULES.md`.

## 2.3.1 (2026-11-27)

Upgraded all 60 Cyclorama Precision Silkscreen icons from generic fallback motion verbs to bespoke, part-level hardware animations.

- **All 60 Icons with Bespoke Part-Level Choreography (`tools/make-icons.py`, `brand/tokens/rfs-components.css`, `docs/index.html`):** Replaced every remaining whole-icon fallback verb (including `seat`) with semantic `.rfs-p-*` SVG sub-parts and physically grounded `part-*` click/hover animations across all 6 categories—including `eye` lid blink, `eye-off` Crimson slash draw, `clock` 360° hand sweep, `globe` spinning meridian, `key` `-42°` turn, `unlock` shackle snap, `book` symmetric page fan, `code` `< / >` spread, `git-branch` Mint curve trace, `diff` Mint `+` / Crimson `-`, `cpu` core die + pin pulse, `server` alternating status LEDs, `link` chain lock, `image` mountain draw + sunrise, `volume` staggered sound arcs, `menu` 3-bar stagger, `close` 90° scissor swap, `sun` 8-ray 45° rotation, `calendar` ring lift + page flip, and exact path-length stroke draws (`check`, `check-circle`, `shield`, `shield-check`, `x-circle`, `share`).
- **Full-Grid Cascade (`docs/assets/brand.js`):** Upgraded the `§13A` `[live] Click Motion` `Cascade` trigger to ripple across all 60 visible icons (or the active filtered category).

## 2.3.0 (2026-11-27)

Added custom mechanical-detent hardware control animations, an official opt-in motion taxonomy across all 60 Precision Silkscreen icons, and 4 upgraded Cyclorama Dawn loading bar systems.

- **Mechanical Detent Token & Motion Controller (`rfs.css`, `rfs-components.css`, `rfs-motion.js`):** Added `--rfs-ease-detent` (`linear()` 3.5% seat settle with `cubic-bezier()` fallback), `--rfs-dur-detent` (`340ms`), and `--rfs-dur-jump` (`360ms`), plus a zero-dependency drop-in `rfs-motion.js` controller.
- **Custom Animated Hardware Controls (`§05 Controls`):**
  - Checkboxes: `.rfs-check` (Silkscreen Ink Draw), `.rfs-check-shutter` (Horizon Shutter Stamp), `.rfs-check-token` (`[x]` Bracket Latch), all supporting `:checked`, `:indeterminate`, and `44×44px` hit targets.
  - Switches: `.rfs-switch` (Cyclorama Cue Slide with etched `0`/`I`), `.rfs-switch-breaker` (square `5px` hardware Breaker Rocker), and `.rfs-switch-patch` (monochrome-safe `ON`/`OFF` Patch Shutter) on semantic `<input type="checkbox" switch>`.
  - Jumping Radios & Controls: `[data-rfs-radio-jump="reticle"]` (Reticle Jump ballistic arc + Steel lock), `[data-rfs-radio-jump="aperture"]` (Aperture Hop), `[data-rfs-segmented]` (Cue Carriage), `.rfs-btn-horizon` (Horizon Sweep), `.rfs-btn-copy-morph` (Copy-to-Check morph), `.rfs-btn-arm` (two-stage Armed Destructive Latch), and `.rfs-fader` (Console Fader).
- **Upgraded Hardware Loading Bars & Precision Ring:** Replaced plain progress styling with 4 native `<progress>` / hardware systems—**DMX Cue Meter** (`.rfs-progress-dmx-shell` etched 10% ticks + leading needle + Signal Mint `100%` lock), **Horizon Alive Trace** (`.rfs-progress` moving sheen + racing indeterminate beam), **20-Cell LED Ladder** (`.rfs-led-ladder`), and **Precision Progress Ring / Dawn Ring** (`.rfs-progress-ring` / `.rfs-spinner` using `background-image` so `background-clip: border-area` stays hollow across determinate, `100%`, and indeterminate states).
- **Opt-In 60-Icon Click Motion (`tools/make-icons.py`, `icons.json`, `§13A`):** Added canonical `motion` verbs for all 60 icons (calm by default; opt in with `.rfs-icon-live` + `data-rfs-motion` + `data-rfs-icon-click`), including 12 multi-part silkscreen icons (`trash`, `lock`, `bell`, `sliders`, `capture`, `download`, `copy`, `shield-check`, `refresh`, `wifi`, `terminal`, `settings`) and a live `[live] Click Motion` + `Cascade 12` mode in the brand manual icon browser.

## 2.2.0 (2026-11-27)

Upgraded `rfs-brand` into an installable agent brand skill with standards-compliant token exports, portable cross-repo auditing, and expanded visual/editorial specimens on the living manual.

- **Installable Agent Skill & `llms.txt`:** Added `skills/rfs-brand/SKILL.md` (`agentskills.io` / `npx skills add Real-Fruit-Snacks/rfs-brand` compatible) with 5 progressive-disclosure `references/` modules (`page-archetypes.md`, `web-ui-components.md`, `voice-and-docs.md`, `cli-tui-native.md`, `audit-rubric.md`), hosted `docs/llms.txt`, and rewrote `docs/DESIGN.md` to eliminate legacy `v2.0` drift.
- **W3C DTCG, Tailwind v4 & TypeScript Exports (`tools/make-tokens.py`):** Added deterministic generation of `brand/tokens/rfs.dtcg.json` (W3C DTCG `$type`/`$value`/`$description`), `brand/tokens/rfs-tailwind.css` (theme-reactive Tailwind CSS v4 `@theme inline`), and `brand/tokens/rfs-tokens.ts` (`as const` typed exports), plus 6 ordered WCAG-AA data visualization tokens (`--rfs-viz-1` through `--rfs-viz-6`).
- **Portable Repo Auditor (`tools/verify-brand.py --repo`):** Added `--repo <path>` and `--json` flags to audit any Real-Fruit-Snacks repository for README budget/summary, adaptive covers, `0.32` light wash, `prefers-reduced-motion`, explicit dark default, zero `in oklch`, zero native popups, zero external CDN fonts, zero `shields.io` badge walls, and zero private-repo leaks.
- **Living Manual Visual Upgrades (`docs/index.html`, `brand.css`):** Added the 6-series Data Visualization palette + live chart specimen in `§01`, expandable `View HTML` `<details>` copy disclosures on component cards (`§04`, `§05`, `§13`), a 4-part Visual Do vs. Don't & Anti-Patterns gallery in `§06`, a Voice Before/After microcopy matrix in `§07`, and `§13 H` Page Archetypes & Repo Audit.
- **Alabaster Light Parity:** Upgraded light marks (`0.36` wash), covers/banners/boards (`0.32` wash), theme-calibrated `rfs-brand` Light cover/avatar/Mermaid specimens, and mobile `390px` table wrapping.

## 2.1.0 (2026-11-24)

Replaced the Raspberry fault/error palette (`#F06292` / `#B0306A`) with **Signal Crimson** across tokens, components, CLI presets, and docs—introducing a dedicated destructive button fill role mirroring `--rfs-steel-fill`.

- **Signal Crimson Fault Tokens (`rfs.css`, `rfs.tokens.json`):**
  - Dark (`LX 263`): `--rfs-fault` `#FF5C6C` (≥ 6.11:1 across all four dark surfaces), `--rfs-fault-fill` `#C92438` (5.54:1 with `#FFFFFF`), `--rfs-fault-fill-hover` `#E02E44` (4.52:1), `--rfs-on-fault` `#FFFFFF`.
  - Light (`LX 512`): `--rfs-fault` / `--rfs-fault-fill` `#B91C2E` (≥ 5.21:1 text, 6.43:1 with `#FFFFFF`), `--rfs-fault-fill-hover` `#991525` (8.44:1), `--rfs-on-fault` `#FFFFFF`.
- **Destructive Button Variants (`rfs-components.css`):** Updated `.rfs-btn-fault` to use `--rfs-fault-fill` / `--rfs-fault-fill-hover` with white text, added `.rfs-btn-fault-soft` and `.rfs-btn-fault-outline`, and updated `.rfs-toast.is-fail` tinting.
- **CLI & TUI Standards:** Updated `[x]` fail truecolor to `#FF5C6C` / `#B91C2E` (`RgbColor(255, 92, 108)`) and ANSI-16 fallback to Red (`31`).

## 2.0.0 (2026-11-23)

Complete Cyclorama Dawn — **Steel & Beacon Orange** identity overhaul (`LX 263 Beacon Horizon` matte cyclorama dark default `#050507`, `LX 512 Alabaster Day` light `#F5F7F9`).

- **Typography:** Migrated to self-hosted variable **Big Shoulders Stencil** (`700–900`, display), **Albert Sans** (`400–700`, UI/prose), and **Azeret Mono** (`400–600`, code/CLI/telemetry) across web pages and outlined SVG generators (zero external CDN calls).
- **Color & Contrast:** Calibrated every text token ≥ 4.84:1 and every control border (`--rfs-line-strong`) ≥ 3.11:1 across all four surfaces in both modes; locked all Steel→Beacon gradients to Cartesian `in oklab` interpolation; added `--rfs-on-fault`, syntax roles (`--rfs-syn-*`), z-index scale, breakpoints, `prefers-reduced-transparency`, `prefers-contrast: more`, `forced-colors`, and `@media print`.
- **Marks, Org Art & Repo Covers:** Unified all dark marks, favicons, lockups, and avatar onto the matte `#050507` + lower Steel→Beacon wash + white `RFS` + bar tile; added 3 SVG art tiers (Static Standard, Animated One-Shot `rfs-banner-*-animated.svg`, Ambient Showcase `board-{dark,light}.svg` 11-channel DMX Console); updated `make-cover.py` to word-only `REAL-FRUIT-SNACKS` cover signatures, recessed `flow` patch bays, and zero-traffic-light Cyclorama terminals.
- **Drop-In Component Kit (`brand/tokens/rfs-components.css`):** Shipped reusable buttons (including `.rfs-btn-fault`), `D · Terminal Token` badges & filter chips, wrapped-by-default code blocks (`.rfs-code-scroll` opt-in), `.rfs-shell` below-header scrollbars, branded native `<dialog class="rfs-dialog">` confirmation modals (zero native `alert()`/`confirm()`/`prompt()`), non-blocking `.rfs-toast-region` notifications, viewport-aware `.rfs-popover-panel` action menus, `popover="hint"` `.rfs-tooltip`, `.rfs-tabs`, native `<details>` `.rfs-accordion`, `base-select` `.rfs-select`, `.rfs-switch`, native `<progress>`, UI states, cards, KV lists, and skeletons.
- **60-Icon Precision Silkscreen Library (`tools/make-icons.py`):** Added 60 monochrome `24×24` (`1.75px` `square`/`miter`) SVGs in `brand/icons/`, symbol sprite `rfs-icons.svg`, manifest `icons.json`, and an interactive searchable browser in `docs/`.
- **Agent Contract, Native/TUI & CI Linter:** Added `brand/BRAND-RULES.md`, expanded `templates/repo/` (`AGENTS.md`, `SECURITY.md`, GitHub issue/PR templates), documented Windows/Rust/Python TUI presets, and added `tools/verify-brand.py` to enforce sync and brand invariants in CI.

## 1.4.0 (2026-11-05)

Covers v2: repo covers are redesigned to be read where most people see them, as a 400–500px social card or an 830px README image. Each tool repo has to regenerate its cover; until it does, `layout = "v1"` in its `cover.toml` keeps the old one, byte for byte.

- BRAND.md §7 is rewritten for the new layout:
  - **Name and description.** The repo name is as large as its 480px column allows, up to 120px; long hyphenated names break onto two lines. The description is the README one-liner (Plex Sans 600 30/38, up to two even lines), and it drops a trailing period.
  - **No bullets.**
  - **The panel** is 528×448 (was 480×368) and shows the one thing the tool does, in four kinds: `flow` (new), `terminal`, `art` and `screenshot`.
- BRAND.md §8: covers are the one exception to the 1.2s entrance and may run up to 3.5s. Their motion must be safe even where a browser ignores `prefers-reduced-motion` in an `<img>`, as Chromium does. A flow's connector draws in like the rule.
- `make-cover.py`:
  - Layout v2 is the default; `layout = "v1"` in cover.toml, or `--layout v1`, renders the old cover exactly as before.
  - New `flow` panel: input, the tool on an Ember connector, then output, with up to two status lines in terminal colours.
  - `terminal` keeps to six lines at 22–26px and sizes its window to them.
  - `art` files are drawn in a 528×448 box; `viewbox` scales an older drawing to fit.
  - `screenshot` takes `crop = [x, y, w, h]` and `fit = "contain"`.
  - The README SVGs animate once with BRAND §8's motions: the rule and connector draw in, a terminal types its command at 45ms a character and prints its lines, the cursor blinks twice and stays, and status lines print. The styles outside the motion are the finished frame, so the PNGs and social previews are unchanged by it. A cover whose motion would run past 3.5s is refused.
  - `--preview FILE` writes the cover at 1200, 830 and 400px in both themes, plus the social card at 400.
  - Text that won't fit at a size that reads on a card is refused, not shrunk.
- `templates/repo/cover.toml` documents the v2 fields.
- This repo's own cover is v2: the Caps Tile, the two type families and the four colours with a job.
- The site's §7 section describes v2, and its gallery shows one cover of each panel kind.

## 1.3.0 (2026-11-04)

- New tokens `primary-hover` (`#FC7951` / `#AC370C`) and `primary-press` (`#F98864` / `#98330F`). Each mixes 12% or 24% of `text` into Ember, so a hovered or pressed button moves away from its `on-primary` text and gains contrast in both themes (7.4 / 6.4:1 hover, 8.1 / 7.5:1 pressed).
- BRAND.md §1 **States**: hover, pressed and disabled for Ember buttons, links and secondary controls. Hover sits inside `@media (hover: hover)`, and Ember is never changed with a `brightness()` filter, which in Dayshift moves it toward its white text.
- The site (docs/) is redesigned around the brand: the rfs-brand cover runs as the first screen, then BRAND.md §1–§9, with both themes' contrast measured on every surface and a demo of each §8 motion. It also links the manifest and app icons, and offers rfs.tokens.json as a download.
- BRAND.md §5: the PowerShell example is `Update-Cert` (was `Rotate-Cert`, and Rotate is not an approved verb).
- `templates/repo/cover.toml` documents the `x ` (Raspberry) terminal prefix.

## 1.2.0 (2026-11-04)

- Dayshift text colours now pass WCAG AA (4.5:1) on `bg`, `surface` and `raised`, as BRAND.md §1 promises. Before, Amber failed on `bg` (4.46:1), and on `raised` all four failed: `mute` `#6B6F78` → `#666A73`, Ember `#C43F11` → `#C03B0A`, Amber `#9A6700` → `#925F00`, Mint `#167A4E` → `#15794D`. The light marks, lockups, banner, social card, header and this repo's cover use the new values. Nightshift is unchanged.
- New tokens, in `rfs.css` and `rfs.tokens.json`:
  - `on-primary`, for text on Ember: `#0C0D10` / `#FFFFFF`. White on Nightshift Ember is 2.9:1.
  - `line-strong`, for inputs and borders that identify a control (3:1): `#636872` / `#89867F`.
  - `fault`, Raspberry, for errors: `#F06292` / `#B0306A`.
- Space scale (`--rfs-space-1` to `-9`, 4 to 96 px) and motion tokens (`--rfs-ease`, `--rfs-dur-fast` / `-base` / `-slow`, `--rfs-type-rate`).
- BRAND.md:
  - Status colours always come with a word (WCAG 1.4.1). Red–green colour-blind readers can't tell Dayshift Ember from Amber, or Mint from Raspberry.
  - The focus ring rule.
  - Body text is 16 px (was 15) and there is a line-length rule.
  - New sections: §8 Motion and §9 Terminal and code.
- `make-cover.py`: terminal lines starting with `x ` are drawn in Raspberry.

## 1.1.0 (2026-11-04)

- Small-size mark: `brand/mark/rfs-mark-small-{dark,light}.svg`, with PNGs at 16, 32 and 48 px. The Caps Tile with its letters drawn on the 16 px grid, for favicons and icon files at 48 px or less (BRAND.md §3). At 16 px the master's letters blurred into a grey bar.
- `brand/web/icon.svg`, `favicon.ico` and `favicon-{16,32,48}.png` use the small-size mark, and so do `docs/assets/icon.svg` and `favicon.ico`.
- `brand/web/apple-touch-icon.png` (and the copy in `docs/assets/`) is rendered from `rfs-mark-dark-square.svg`: full bleed and opaque. The old one had transparent rounded corners, which iOS fills with black.
- `brand/web/head.html` and `docs/index.html` link `favicon.ico` with `sizes="32x32"` (was `48x48`), the usual value next to an SVG favicon.
- `make-cover.py`: a third panel kind, `screenshot`, embeds one PNG or JPEG per theme (`file = "cover-shot-{theme}.png"`).
- The install line is the repo's raw URL until rfs.sh exists: BRAND.md, the README template and the cover template no longer show `irm rfs.sh/<repo> | iex`.

## 1.0.1 (2026-10-26)

- The repo is now `Real-Fruit-Snacks/rfs-brand` (was `Real-Fruit-Snacks/.github`). Old URLs redirect, but update links and clone paths: the tools are run as `rfs-brand/tools/...` from the folder holding your clones.

## 1.0.0 (2026-10-26)

First release of the RFS brand kit.

- `BRAND.md`: colour, type, mark, voice, naming, where each asset goes, and the repo cover rules.
- Themes Nightshift (dark) and Dayshift (light); accents Ember, Amber and Mint; IBM Plex Sans and Plex Mono.
- `brand/tokens/`: `rfs.css` (CSS variables) and `rfs.tokens.json`.
- `brand/mark/`, `brand/lockup/`, `brand/web/`: the Caps Tile mark, lockups, favicons and web app icons.
- `brand/social/`: profile picture, org social card and X header.
- `assets/`: the profile banner, loaded by the profile README.
- `tools/make-cover.py`: a repo's README cover and social preview from its `docs/assets/cover.toml`.
- `tools/make-org-art.py`: the profile banner, org social card and X header from `brand/org.toml`.
- `tools/make-avatar.py`: the profile picture.
- `templates/repo/`: README template, `cover.toml` template and settings checklist.
