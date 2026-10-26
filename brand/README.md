# RFS brand assets

Themes **Nightshift** (dark, default) / **Dayshift** (light) · accent **Ember** · type **IBM Plex Sans / Plex Mono** · mark **Caps Tile** · tagline *Real tools. No filler.*

| Need | Use |
|---|---|
| GitHub org avatar, circular avatars (Discord, X, Mastodon) | `social/rfs-avatar-dark-1024.png` (from `tools/make-avatar.py`) |
| README header | None; the RFS mark is on the repo cover (BRAND.md §7) |
| Org profile header | `lockup/rfs-banner-{dark,light}.svg` |
| GitHub social preview | `social/rfs-social-org-dark-1280x640.png` |
| X / Mastodon header | `social/rfs-header-dark-1500x500.png` |
| Website | copy `web/*` to site root, paste `web/head.html` into `<head>` |
| CSS variables | `tokens/rfs.css` |
| Print / stickers / etching | `mark/rfs-mark-mono-{white,ink}.svg` |

Rules: never rotate, outline, recolor, or add a gradient. Clear space = the tile's corner radius. Minimum 16 px.
All SVG text is outlined — no fonts needed to render. Fonts are only needed to *author* new material (IBM Plex, OFL).
