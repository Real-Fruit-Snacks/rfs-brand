# Changelog

Each release publishes `rfs-brand.zip` (everything below except `.github/` and `docs/`), `rfs.css` and `rfs.tokens.json`.

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
