# Changelog

Each release publishes `rfs-brand.zip` (everything below except `.github/` and `docs/`), `rfs.css` and `rfs.tokens.json`.

## Unreleased

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
