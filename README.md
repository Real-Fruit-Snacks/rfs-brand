# rfs-brand

RFS brand system, profile art, and repository templates.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/cover-dark.svg">
  <img alt="rfs-brand: Cyclorama Dawn Steel and Beacon Orange mark, Big Shoulders Stencil, Albert Sans and Azeret Mono specimens, and core palette swatches" src="docs/assets/cover-light.svg" width="100%">
</picture>

Org-wide design system and asset generators for **Real-Fruit-Snacks** (**RFS**) in the **Cyclorama Dawn — Steel & Beacon Orange** identity. Default dark mode is **Beacon Horizon (`LX 263`)** on matte cyclorama black (`#050507`); light mode is **Alabaster Day (`LX 512`, `#F5F7F9`)**. Asset filenames keep `-dark` / `-light` suffixes so paths stay stable everywhere.

| Path | What it is | Who reads it |
|---|---|---|
| [`assets/`](assets/) | Canonical banners, lockups, and marks | Profile README, external docs |
| [`brand/`](brand/) | Full asset kit — marks, lockups, social previews, web icons, CSS/JSON tokens, component stylesheet, and `BRAND-RULES.md` | Any repo or site in the org |
| [`templates/repo/`](templates/repo/) | Repo README template, `cover.toml` starter, and settings checklist | Starting or updating a repository |
| [`tools/`](tools/) | `make-marks.py`, `make-icons.py`, `make-cover.py`, `make-org-art.py`, and `make-avatar.py` | Regenerating all vector, icon, and raster brand art |
| [`BRAND.md`](BRAND.md) | Authoritative guide: color, typography, mark, principles, covers, motion | Anyone touching the brand |

## Get the kit

Each GitHub release ships the full kit zip alongside the standalone CSS and JSON token files:

| File | Link |
|---|---|
| Full brand kit | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-brand.zip |
| CSS variables | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs.css |
| Component kit CSS | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-components.css |
| Icon sprite (60 SVGs) | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-icons.svg |
| Design tokens (JSON) | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs.tokens.json |
| Agent brand rules | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/BRAND-RULES.md |

```powershell
curl.exe -LO https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-brand.zip
```

## Regenerating assets

All scripts use Python 3.11+, `fonttools`, `brotli`, `resvg-py`, and `pillow`. Every SVG outlines its glyphs from the self-hosted `.woff2` variable fonts in `tools/fonts/`, so assets render identically on GitHub, browsers, and image viewers with zero font dependencies.

```powershell
python -m pip install fonttools brotli resvg-py pillow
python tools/make-marks.py
python tools/make-icons.py
python tools/make-avatar.py
python tools/make-org-art.py
python tools/make-cover.py docs/assets/cover.toml
```

## Starting a new repo

1. Copy `templates/repo/README.md`, fill it in, and remove HTML comments.
2. Check off `templates/repo/SETTINGS-CHECKLIST.md`.
3. Copy `templates/repo/cover.toml` to `<repo>/docs/assets/cover.toml`, then run `python tools/make-cover.py ../<repo>/docs/assets/cover.toml`. Commit `cover-*` and upload `social-dark.png` in GitHub Settings → Social preview.

## Licenses

Code in `tools/` is MIT. Fonts in `tools/fonts/` (`Big Shoulders Stencil`, `Albert Sans`, and `Azeret Mono`) are licensed under the SIL Open Font License 1.1 (`tools/fonts/OFL.txt`). The RFS mark and name are not licensed for reuse.
