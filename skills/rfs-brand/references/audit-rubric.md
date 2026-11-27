# RFS Brand Audit Rubric & Verification Workflow

Run the automated verifier against any repository before pushing, then review the priority rubric below.

## Automated Audit Command

```sh
# Audit any single RFS tool repo
python <rfs-brand>/tools/verify-brand.py --repo <path-to-repo>

# Machine-readable JSON output
python <rfs-brand>/tools/verify-brand.py --repo <path-to-repo> --json

# Audit rfs-brand itself + sibling org repos
python <rfs-brand>/tools/verify-brand.py --workspace <staging-parent-dir>
```

## Priority Review Rubric

### CRITICAL (Must Fail Build / Block Push)
- **Polar `in oklch` gradients:** Any `gradient(... in oklch ...)` causes hue drift between Glacial Steel and Beacon Orange. Replace with Cartesian `in oklab` (`var(--rfs-in-oklab)`).
- **Native browser popups:** Any `window.alert()`, `window.confirm()`, or `window.prompt()` in app JS (vendored WASM/third-party engines excluded). Replace with `<dialog class="rfs-dialog">`.
- **External CDN font/script calls:** Zero `fonts.googleapis.com`, `cdn.jsdelivr.net`, or analytics beacons. Self-host WOFF2 fonts locally.
- **Wrong default color scheme:** Web pages must declare `<meta name="color-scheme" content="dark">` (`#050507`) as the explicit default.
- **Private repo leaks or unredacted personal data:** Zero references to private repositories, real local user directories, or live secrets.
- **Missing destructive confirmation:** Any delete, clear, reset, or irreversible overwrite must open `<dialog class="rfs-dialog is-destructive">` with `autofocus` on **Cancel** and `.rfs-btn-fault` confirm.

### HIGH (Fix Before Shipping)
- **Outdated covers or missing motion guard:** `docs/assets/cover-light.svg` must use the `0.32` Cyclorama floor wash (not legacy `0.14`) and wrap animations inside `@media (prefers-reduced-motion:no-preference)`. Regenerate via `tools/make-cover.py`.
- **Top-clipping scrollbars:** Pages with top navigation chrome must isolate scrolling inside `.rfs-scroll-region` / `.stage-main` below the header hairline.
- **Mobile horizontal overflow:** Verify `scrollWidth <= innerWidth` at `390×844` in both Dark and Light modes, and ensure interactive targets meet `44px` height on mobile.
- **Legacy icon strokes or fake OS chrome:** Replace `1.65` icon strokes with `1.75px` `square`/`miter` icons from `rfs-icons.svg`; strip any macOS traffic-light dots from terminal frames.
- **README drift:** Keep `README.md` at 40–60 lines, `<= 60`-char one-liner with no trailing period, `<picture>` dark/light covers, zero `shields.io` walls, and zero emoji or banned hype words.

### MEDIUM (Polish & Cohesion)
- **Visual distinction:** Confirm the tool's GitHub Pages layout uses the archetype best suited to its domain (see `references/page-archetypes.md`) rather than cloning another tool's page verbatim.
- **Light-mode visual parity:** Toggle to `LX 512 Light` and verify marks, covers, Mermaid configs, avatars, and charts all adapt cleanly with `>= 4.5:1` text contrast and `>= 3:1` border contrast.
- **Code block ergonomics:** Confirm framed snippets show a language header badge, syntax roles (`.rfs-tok-*`), wrap cleanly on mobile (`pre-wrap`), and expose an accessible Copy button with `role="status"` feedback.
