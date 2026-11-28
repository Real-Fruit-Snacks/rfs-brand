---
name: rfs-brand
description: Apply and audit the Real-Fruit-Snacks (RFS) Cyclorama Dawn (Steel & Beacon Orange) brand system across web UIs, GitHub Pages, CLIs, TUIs, Windows desktop apps, READMEs, and SVG covers. Use whenever building, styling, writing docs for, or reviewing any Real-Fruit-Snacks repository or branded asset.
license: MIT
metadata:
  author: Real-Fruit-Snacks
  version: "2.3.2"
  palette: Cyclorama Dawn — Steel & Beacon Orange
  manual: https://real-fruit-snacks.github.io/rfs-brand/
---

# RFS Brand Skill — Cyclorama Dawn (v2.3.2)

Self-contained agent skill for **Real-Fruit-Snacks** (**RFS**) — tagline **Built local-first.**  
World: **Cyclorama Dawn** · Palette: **Glacial Steel & Maritime Beacon Orange**  
Modes: **Beacon Horizon (`LX 263`, dark default)** · **Alabaster Day (`LX 512`, light opt-in)**

## 3-Step Execution Workflow

1. **Route & Choose Archetype:** Read only the reference doc(s) matching the task below. For web pages, pick 1 of the 5 bespoke archetypes in `references/page-archetypes.md` (never clone one template blindly) and start from `assets/starter-page.html` if creating a new page.
2. **Build with Cyclorama Dawn Primitives:** Load `rfs.css` -> `rfs-components.css` -> `rfs-motion.js` (or `rfs-tailwind.css` / `rfs-tokens.ts`). Use `--rfs-ease-detent` hardware controls, the 4 upgraded `<progress>` loaders, `D · Terminal Token` 4px badges, `.rfs-shell` scroll locks, branded `<dialog>` modals, and opt-in `.rfs-icon-live` part-level icon motion from `references/motion-and-icons.md`.
3. **Self-Critique & Run Bundled Auditor:** Reject AI-slop clichés (blue-slate darks, `in oklch` mud, Inter/Roboto CDN fonts, `99px` pill badges, fake macOS dots, raw `alert()`/`confirm()`, neon glows) and run the bundled standalone verifier before finishing:
   ```sh
   python scripts/verify-brand.py --repo <path-to-repo>
   ```
   Exit codes: `0` pass, `1` brand violation found, `2` invalid arguments. Add `--json` for machine-readable output.

## Non-Negotiable Invariants

1. **Dark Default, Light Opt-In, Motion On:** Declare `<meta name="color-scheme" content="dark">` (`#050507`, neutral matte black with zero blue-slate tint) as explicit default; `#F5F7F9` (`LX 512`) is an opt-in user toggle. Keep CSS transitions, mechanical detents (`--rfs-ease-detent`), and View Transitions enabled by default while keeping SVG DOM static-first outside `@media (prefers-reduced-motion: no-preference)`.
2. **Two Chromatic Poles + Cartesian `in oklab` Only:** Glacial Steel (`#1F547A` / `#18496B` fill / `#74B8E8` dark ink / `#164669` light ink) and Maritime Beacon Orange (`#F06E2B` / `#FF9254` dark ink / `#AD3D0A` light ink). Always interpolate gradients with `in oklab` (`--rfs-horizon-gradient`, `--rfs-horizon-rule`)—never polar `in oklch`. Pair status colors with words: Mint `[ok]` (`#3DDC97` / `#127247`), Amber `[!]` (`#FFC247` / `#885800`), Signal Crimson `[x]` (`#FF5C6C` / `#B91C2E`, fill `#C92438` / `#B91C2E` with `#FFFFFF`).
3. **Self-Hosted Variable Typography (Zero External CDNs):** `Big Shoulders Stencil` (`700–900`, uppercase, `+0.055em`), `Albert Sans` (`400–700`, UI/prose), and `Azeret Mono` (`400–600`, code/CLI/slugs, `tabular-nums`).
4. **Hardware Chrome, Badges, Code & 60 Icons:**
   - `D · Terminal Token` badges only (`4px` radius, `--rfs-code-bg`, `1px` `--rfs-line`, colored `[tag]` `.k` + neutral label). Zero `99px` pills, status dots, or macOS traffic lights.
   - Wrapped `.rfs-code-card` blocks with explicit language header and `.rfs-tok-*` syntax roles (`.rfs-code-scroll` opt-in for ASCII art).
   - 60 Precision Silkscreen icons (`24×24`, `1.75px` `square`/`miter`, `>= 44×44px` tap targets, opt-in `.rfs-icon-live` + bespoke `part-*` motion verbs)—zero emoji or third-party rounded icon packs.
   - 4 upgraded loaders (`.rfs-progress-dmx-shell`, `.rfs-progress`, `.rfs-led-ladder`, `.rfs-progress-ring` with `background-image:` so `border-area` stays hollow).
5. **App-Shell Scrollbars & Zero Native Popups:** Isolate top headers in `.rfs-shell` -> `.rfs-shell-header` above `.rfs-scroll-region`. Strictly forbid `window.alert()`, `window.confirm()`, and `window.prompt()`; destructive actions MUST open `<dialog class="rfs-dialog is-destructive">` naming the target, `autofocus` on **Cancel**, and `.rfs-btn-fault` confirm.
6. **CAD Geometry (`[dwg] rfs-01`–`rfs-05`) & Minimal README:** Never stretch or hand-edit marks (`64×64u rx 14`, `14u` clear space; `405×64u` lockup collapses to tile `< 160px`; `1200×560` / `1280×640` covers use `0.32` light wash). Keep `README.md` at 40–60 lines with a `<= 60`-char no-period summary and adaptive `<picture>` covers; put full docs in `docs/*.md` (never GitHub Wiki).

## Progressive Disclosure Routing

Read **only** the reference doc(s) matching the current task:

| Task | Read First | Bundled / Hosted Artifact |
|---|---|---|
| Choosing a GitHub Pages or web app layout (preventing clones) | `references/page-archetypes.md` | 5 bespoke RFS archetypes + `assets/starter-page.html` |
| Building buttons, badges, controls, loaders, dialogs, toasts, charts | `references/web-ui-components.md` | `rfs.css`, `rfs-components.css`, `rfs-motion.js`, Tailwind v4, TS, DTCG |
| Using `--rfs-ease-detent`, 60 icon names & `part-*` verbs, CAD geometry | `references/motion-and-icons.md` | Full 60-icon verb table + 5 CAD sheets (`rfs-01`–`rfs-05`) |
| Writing READMEs, CLI errors, microcopy, release notes, screenshots | `references/voice-and-docs.md` | 40–60 line `README.md` + `docs/*.md` + redaction rules |
| Building Rust, Go, Python, PowerShell, or C# CLIs / Windows apps | `references/cli-tui-native.md` | `NO_COLOR` CLI grammar, exit `0/1/2`, Win32 DWM |
| Reviewing or auditing any RFS repository before commit/release | `references/audit-rubric.md` | Bundled `scripts/verify-brand.py --repo <path>` |

## Standalone Asset Fetch (When `rfs-brand` Repo Is Not Cloned Locally)

```sh
curl -LO https://real-fruit-snacks.github.io/rfs-brand/assets/rfs.css
curl -LO https://real-fruit-snacks.github.io/rfs-brand/assets/rfs-components.css
curl -LO https://real-fruit-snacks.github.io/rfs-brand/assets/rfs-motion.js
curl -LO https://real-fruit-snacks.github.io/rfs-brand/assets/rfs-icons.svg
```

- **Full kit & generators:** `https://real-fruit-snacks.github.io/rfs-brand/llms.txt` · `tools/make-cover.py` (covers) · `tools/make-tokens.py` (DTCG/Tailwind/TS) · `tools/make-icons.py` (60 icons).
