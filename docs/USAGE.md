# Using & Regenerating rfs-brand

Complete download links, repository layout, asset regeneration commands, and new-repository onboarding steps for **Real-Fruit-Snacks** (`rfs-brand`).

## Repository Layout

| Path | What it is | Who reads it |
|---|---|---|
| [`assets/`](../assets/) | Canonical banners, lockups, and marks | Profile README, external docs |
| [`brand/`](../brand/) | Full asset kit — marks, lockups, social previews, web icons, CSS/DTCG/Tailwind/TS/JSON tokens, component stylesheet, and `BRAND-RULES.md` | Any repo or site in the org |
| [`skills/rfs-brand/`](../skills/rfs-brand/) | Installable `agentskills.io` skill (`SKILL.md` + 5 progressive-disclosure `references/`) | Claude Code, Codex, Cursor, Antigravity |
| [`templates/repo/`](../templates/repo/) | Ultra-minimal README template, `AGENTS.md`, `cover.toml` starter, `SECURITY.md`, GitHub templates, and settings checklist | Starting or updating a repository |
| [`tools/`](../tools/) | `make-marks.py`, `make-icons.py`, `make-cover.py`, `make-org-art.py`, `make-avatar.py`, `make-tokens.py`, and `verify-brand.py` | Regenerating and verifying all vector, icon, token, and raster brand art |
| [`BRAND.md`](../BRAND.md) | Authoritative guide: color, typography, mark, principles, covers, motion, data viz, and README/docs rules | Anyone touching the brand |

## Release Downloads

Each GitHub release ships the full kit zip alongside the standalone CSS, DTCG/Tailwind/TypeScript exports, icon sprite, JSON tokens, and agent rules:

| File | Link |
|---|---|
| Full brand kit | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-brand.zip |
| CSS variables | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs.css |
| Component kit CSS | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-components.css |
| Icon sprite (60 SVGs) | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-icons.svg |
| Design tokens (JSON) | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs.tokens.json |
| W3C DTCG tokens | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs.dtcg.json |
| Tailwind CSS v4 `@theme` | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-tailwind.css |
| TypeScript tokens | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-tokens.ts |
| Agent brand rules | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/BRAND-RULES.md |
| Hosted agent index (`llms.txt`) | https://real-fruit-snacks.github.io/rfs-brand/llms.txt |

```powershell
curl.exe -LO https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-brand.zip
npx skills add Real-Fruit-Snacks/rfs-brand
```

## Regenerating Assets

All scripts use Python 3.11+, `fonttools`, `brotli`, `resvg-py`, and `pillow`. Every SVG outlines its glyphs from the self-hosted `.woff2` variable fonts in `tools/fonts/`, so assets render identically on GitHub, browsers, and image viewers with zero font dependencies.

```powershell
python -m pip install fonttools brotli resvg-py pillow
python tools/make-marks.py
python tools/make-icons.py
python tools/make-avatar.py
python tools/make-org-art.py
python tools/make-cover.py docs/assets/cover.toml
python tools/make-tokens.py
python tools/verify-brand.py
python tools/verify-brand.py --repo ../<target-repo> --json
```

## Starting a New Repo

1. Copy [`templates/repo/README.md`](../templates/repo/README.md), keep `README.md` at 40–60 lines, move deeper reference material into `docs/*.md`, and remove HTML comments.
2. Copy [`templates/repo/AGENTS.md`](../templates/repo/AGENTS.md) and [`templates/repo/SECURITY.md`](../templates/repo/SECURITY.md).
3. Check off [`templates/repo/SETTINGS-CHECKLIST.md`](../templates/repo/SETTINGS-CHECKLIST.md) (including disabling GitHub Wiki).
4. Copy [`templates/repo/cover.toml`](../templates/repo/cover.toml) to `<repo>/docs/assets/cover.toml`, run `python tools/make-cover.py ../<repo>/docs/assets/cover.toml`, commit `cover-*`, and upload `social-dark.png` in GitHub Settings -> Social preview.
