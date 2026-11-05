# Design: the rfs-brand site (docs/)

BRAND.md is the design system. This file only records decisions specific to this page.

## Concept

The first screen is this repo's cover (BRAND.md §7, layout v2) at full size, drawn live. The name, the Ember rule and the README one-liner sit on the left, with the download and BRAND.md links under them, which the cover doesn't have. On the right is the cover's art panel (`assets/cover-art.svg`) built in HTML: the Caps Tile, the two type families and the four colours with a job. Each swatch also shows its value in the live theme. Behind them is the 26px dot grid with the Nightshift glow from the lower right. Below it, the page walks BRAND.md in order, §1 to §9. Each section's number hangs in the left margin and links to that section of the guide. The kit download comes first, and "Starting a repo" comes last.

## Wow moment

The four motions in BRAND.md §8, and nothing else:

- The Ember rule draws in under `rfs-brand` on load, at `--rfs-dur-slow`. It's the only motion in this repo's cover SVG, so the hero's entrance is the cover's.
- In Nightshift, with a fine pointer, the dot grid warms to Ember around the pointer.
- The theme switch sweeps the new theme in a circle from the control (View Transitions), at `--rfs-dur-slow`. Because the panel is live, the sweep redraws the cover as it passes: the tile's rule, the swatches and their values turn to Dayshift.

A terminal typing is demonstrated in §8, not in the hero: this repo's cover has no terminal. With no JS, the hero is complete. With reduced motion, the page is the still frame. On a phone there is no pointer warmth.

## Files

- `assets/rfs.css`: a verbatim copy of `brand/tokens/rfs.css`. Don't edit it; copy it again when the tokens change.
- `assets/site.css`, `assets/site.js`: the shared tool-page base, updated to 1.2.0. Every 1.1 class is kept, so a tool page can take both files unchanged.
- `assets/brand.css`: this page only.

## Page-only values

- `--wrap: 1120px` (the shared base is 1040px).
- Section titles run from 32px on phones to 48px (BRAND's h1 to display sizes). The repo name is `clamp(52px, …, 108px)`, and never wider than its column (`20cqi`), like the cover's name.
- The hero columns are the cover's, 480 : 528. The panel is sized in units of the cover's 528px panel (`--u`), so it keeps the cover's proportions at any width; the specimen labels and swatch values stop at 12px.
- The hero dots (`#1E222B` / `#DDD9D1`) and the glow (`rgba(255,106,61,.18)` at 78% 110%, radius 70%) are the cover's own values from `tools/make-cover.py` (THEMES).
- Text at 11px on the theme switch, the copy buttons and the labels is BRAND's label role. shoot.mjs warns about text under 12px; that warning is expected.

## When the brand changes, update by hand

- `index.html` §1: the token table (hex values and the "was" values) and the 42 contrast ratios in the two panes. Ratios use the WCAG 2 relative-luminance formula, two decimals.
- `brand.css`: `.p-night` / `.p-day` (the panes show both themes at once, so they carry their own copies), `.k-tile`, `--dots`.
- `index.html`, the hero: the swatch values (`.v-n` / `.v-d`), and the panel itself if `assets/cover-art.svg` changes.
- `index.html` §3: the construction drawing inlines the letter outlines from `brand/mark/rfs-mark-dark.svg`.
- `index.html`, the kit section: the "New in 1.2.0" box. Replace it each release.
- `assets/` copies from `brand/`: `rfs-mark-*-16.png`, `rfs-mark-small-*-16.png`, `rfs-avatar-dark-512.png`, `rfs-social-org-*-1280x640.png`, `rfs-header-*-1500x500.png`, `icon-192/512.png`, `icon-maskable-512.png`, `manifest.webmanifest`. From `assets/`: the banner, lockup and mark SVGs. Copy them again after running `make-org-art.py` or `make-avatar.py`.
- Never edit `assets/cover-*` or `social-*` by hand. The release workflow checks that the cover SVGs match `make-cover.py`.

## Alternatives considered

- The org banner's composition: RFS and the tagline on the left, a `gh repo list` terminal on the right, with `rfs-brand` as a smaller title. It reads as the org's front door, not the brand kit's.
- A theme-first opener: the first screen split down the middle, Nightshift on the left and Dayshift on the right, the same cover in both, with the switch on the seam.
