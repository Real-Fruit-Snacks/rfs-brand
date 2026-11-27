---
name: rfs-brand
description: Apply and audit the Real-Fruit-Snacks (RFS) Cyclorama Dawn (Steel & Beacon Orange) brand system across web UIs, GitHub Pages, CLIs, TUIs, Windows desktop apps, READMEs, and SVG covers. Use whenever building, styling, writing docs for, or reviewing any Real-Fruit-Snacks repository or branded asset.
license: MIT
metadata:
  author: Real-Fruit-Snacks
  version: "2.2.0"
  palette: Cyclorama Dawn — Steel & Beacon Orange
  manual: https://real-fruit-snacks.github.io/rfs-brand/
---

# RFS Brand Skill — Cyclorama Dawn (v2.2.0)

Single-entry agent skill for **Real-Fruit-Snacks** (**RFS**) — tagline **Built local-first.**  
World: **Cyclorama Dawn** · Palette: **Glacial Steel & Maritime Beacon Orange**  
Modes: **Beacon Horizon (`LX 263`, dark default)** · **Alabaster Day (`LX 512`, light opt-in)**

## Non-Negotiable Invariants

1. **Dark Default, Light Opt-In, Motion On:** Every web surface sets `<meta name="color-scheme" content="dark">` (`#050507`, neutral matte black with zero blue-slate tint) as its explicit default, with `#F5F7F9` (`LX 512`) as a user toggle. Keep CSS transitions, animations, and View Transitions enabled by default (while preserving static-first SVG DOM outside `@media (prefers-reduced-motion: no-preference)`).
2. **Two Chromatic Poles Only:** Glacial Steel (`#1F547A` / `#18496B` fill / `#74B8E8` dark ink / `#164669` light ink) and Maritime Beacon Orange (`#F06E2B` / `#FF9254` dark ink / `#AD3D0A` light ink). Status always carries words: Mint `[ok]` (`#3DDC97` / `#127247`), Amber `[!]` (`#FFC247` / `#885800`), Signal Crimson `[x]` (`#FF5C6C` / `#B91C2E`, fill `#C92438` / `#B91C2E` with `#FFFFFF`).
3. **Cartesian `in oklab` Gradients Only:** Never interpolate Steel to Beacon in polar `in oklch` (causes violet/green hue drift). Use `--rfs-horizon-gradient` and `--rfs-horizon-rule`. Zero neon glows or decorative drop shadows.
4. **Self-Hosted Variable Typography:** Zero external CDN calls (`fonts.googleapis.com` is forbidden). Load self-hosted `Big Shoulders Stencil` (`700–900`, uppercase, `+0.055em` tracking), `Albert Sans` (`400–700`, UI & prose), and `Azeret Mono` (`400–600`, code, slugs, CLI, `tabular-nums`).
5. **Chrome, Badges & Code Blocks:**
   - Load `rfs.css` then `rfs-components.css` (plus `rfs-tailwind.css` for Tailwind v4 or `rfs-tokens.ts` for TS/Canvas apps).
   - Use `D · Terminal Token` badges only (`4px` radius, `--rfs-code-bg`, `1px` `--rfs-line`, colored `[tag]` `.k` + neutral label). Zero `99px` capsule pills, zero status dots, zero fake macOS traffic-light dots.
   - Wrap code in `.rfs-code-card` with a language header and `.rfs-tok-*` syntax classes; wrap lines by default (`pre-wrap`, `overflow-wrap: anywhere`; `.rfs-code-scroll` opt-in).
   - Use the 60-icon Precision Silkscreen library (`rfs-icons.svg`, `24×24`, `1.75px` `square`/`miter`)—zero emoji or third-party rounded icon packs.
6. **App-Shell Scrollbars & Zero Native Popups:**
   - Keep top headers outside the scroll region via `.rfs-shell` + `.rfs-shell-header` + `.rfs-scroll-region` so vertical scrollbars never run into the top header.
   - Strictly forbid `window.alert()`, `window.confirm()`, and `window.prompt()`. Use branded native `<dialog class="rfs-dialog">` modals; destructive actions (delete/clear/reset/overwrite) MUST use `<dialog class="rfs-dialog is-destructive">` naming the target, `autofocus` on **Cancel**, and `.rfs-btn-fault` confirm.
7. **Voice & Ultra-Minimal README:** Plain, specific, dry, honest. No emoji, no hype adjectives (`blazing`, `seamless`, `supercharge`), no exclamation marks in headings or descriptions, no `shields.io` rainbow badge walls. Keep `README.md` at 40–60 lines with a `<= 60`-char no-period summary and adaptive `<picture>` covers; put full docs in `docs/*.md` (never GitHub Wiki).

## Progressive Disclosure Routing

Read **only** the reference doc(s) matching the current task:

| Task | Read First | Key Output / Script |
|---|---|---|
| Choosing a GitHub Pages or web app layout (preventing lookalike pages) | `references/page-archetypes.md` | Pick 1 of 5 bespoke RFS archetypes |
| Building HTML/CSS/Tailwind/TS components, dialogs, toasts, or charts | `references/web-ui-components.md` | `brand/tokens/{rfs.css,rfs-components.css,rfs-tailwind.css,rfs-tokens.ts}` |
| Writing READMEs, CLI errors, microcopy, release notes, or framing screenshots | `references/voice-and-docs.md` | 40–60 line `README.md` + `docs/*.md` |
| Building Rust, Go, Python, PowerShell, or C# CLIs / Windows desktop apps | `references/cli-tui-native.md` | `NO_COLOR` CLI grammar, exit `0/1/2`, Win32 DWM |
| Reviewing or auditing any RFS repository before commit/release | `references/audit-rubric.md` | `python tools/verify-brand.py --repo <path>` |

## Generating Assets & Running Audits

- **Repo covers (`docs/assets/cover.toml`):** Always generate with `python <rfs-brand>/tools/make-cover.py <repo>/docs/assets/cover.toml` (produces `cover-{dark,light}.{svg,png}` and `social-{dark,light}.png` with `0.32` light wash and `@media (prefers-reduced-motion:no-preference)`). Never hand-edit mark paths.
- **Token exports:** Edit `brand/tokens/rfs.tokens.json`, then run `python tools/make-tokens.py` to regenerate `rfs.dtcg.json` (W3C DTCG), `rfs-tailwind.css` (Tailwind v4 `@theme`), and `rfs-tokens.ts`.
- **Portable repo audit (required before pushing):**
  ```sh
  python <rfs-brand>/tools/verify-brand.py --repo <path-to-repo>
  ```
  Exit codes: `0` pass, `1` brand violation found, `2` invalid arguments. Add `--json` for machine-readable output.
