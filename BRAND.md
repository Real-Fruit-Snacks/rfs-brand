# RFS brand guide

Real-Fruit-Snacks · short form **RFS** · tagline **Real tools. No filler.**
Themes: **Nightshift** (dark, default) · **Dayshift** (light) · accent **Ember**

This is the source of truth. If an asset in `brand/` disagrees with this file, the asset is wrong.

---

## 1. Color — *Nightshift* / *Dayshift*

Two themes. **Nightshift** (dark) is the default; **Dayshift** (light) is derived from it. The accent color is **Ember**. Same structure, same hues, values shifted until every accent passes WCAG AA (≥ 4.5:1) as text on its background.

| Token | Nightshift | Dayshift | Rule |
|---|---|---|---|
| `bg` | `#0C0D10` | `#F6F5F2` | Page. Never pure black or pure white. |
| `surface` | `#13151A` | `#FFFFFF` | Cards, panels. One step up from bg. |
| `raised` | `#1A1D24` | `#ECEAE4` | Inputs, chips, nested cards. |
| `line` | `#262A33` | `#D6D3CB` | All borders. Borders replace shadows (Dayshift may add a 1px hairline shadow on cards). |
| `text` | `#E8E6E1` | `#1A1B1E` | Body. Never `#FFF` for body copy. |
| `mute` | `#8A8F99` | `#6B6F78` | Secondary text, captions. |
| `primary` · Ember | `#FF6A3D` | `#C43F11` | The brand. One per screen. Glow allowed in Nightshift only. |
| `accent` · Amber | `#FFC247` | `#9A6700` | Warnings, second category, prompts. |
| `signal` · Mint | `#3DDC97` | `#167A4E` | Success / running. Only ever means "OK". |
| `code-bg` | `#070809` | `#FFFFFF` | Code blocks follow the theme. Nightshift: one step darker than bg. Dayshift: surface white with ink text. |

Machine-readable: `brand/tokens/rfs.css`, `brand/tokens/rfs.tokens.json`.

**Don't:** use Mint decoratively · use Ember for errors (Ember is brand, not danger) · add a third accent · use gradients anywhere.

## 2. Type

**IBM Plex Sans** for UI and prose. **IBM Plex Mono** for code, labels, and the wordmark. One superfamily so prose and code look designed together. Both are OFL and on Google Fonts.

```
--rfs-font-sans: "IBM Plex Sans", Inter, system-ui, sans-serif;
--rfs-font-mono: "IBM Plex Mono", "JetBrains Mono", ui-monospace, monospace;
```

| Role | Size / line | Face · weight | Tracking |
|---|---|---|---|
| display | 48 / 1.05 | Sans 700 | −0.03em |
| h1 | 32 / 1.1 | Sans 700 | −0.02em |
| h2 | 22 / 1.2 | Sans 600 | −0.01em |
| body | 15 / 1.6 | Sans 400 | 0 |
| small | 13 / 1.5 | Sans 400 · mute | 0 |
| label | 11 / 1 | Mono 500 · caps | +0.08em |
| code | 13 / 1.7 | Mono 400 | 0 |
| wordmark | — | Mono 600 | −0.05em |

## 3. Mark — *Caps Tile*

`RFS` in Plex Mono SemiBold, centered on a rounded tile, Ember rule beneath.

- Tile: 64-unit grid, corner radius 14 (0.219 × side). Fill `#1A1D24` in Nightshift, `#1A1B1E` in Dayshift.
- Letters: 28 units, tracking −1.5, baseline at 43. Always white.
- Rule: 36 × 4 units, radius 2, at y = 48. Ember (theme value).
- Clear space: one corner radius on every side. Minimum size: 16 px.
- Lockup: tile + wordmark, gap = 0.3 × tile side, wordmark cap-height ≈ 0.55 × tile side.
- Single-color: tile becomes a 3-unit outline; letters and rule take the one color. For print, etching, stickers.

**Don't:** rotate · outline the color version · recolor the letters · put the mark on Ember (use the single-color white version instead) · bake the glow into an asset — glow is a CSS effect in Nightshift UI only.

Masters: `brand/mark/rfs-mark-{dark,light}.svg`. All text is outlined; no font is required to render any asset.

## 4. Voice

Four traits, each with a test:

| Trait | Means | Test |
|---|---|---|
| **Plain** | Short sentences. Concrete nouns. The reader is busy and competent. | Could a tired admin at 2 am act on it? |
| **Specific** | Versions, OS names, command names, numbers. | Is every adjective replaceable with a fact? |
| **Dry** | Humor lives in details — a flag name, a commit message — never in the headline. | Still funny with the emoji removed? (There are no emoji.) |
| **Honest** | Say what it doesn't do. "Tested on" is a list. Known issues above the fold. | Is the first limitation visible without scrolling? |

Banned: emoji · "blazing", "powerful", "modern", "seamless", "supercharge", "awesome" · "Welcome!" · "coming soon" · exclamation marks.
First person singular is correct for one maintainer. Sentence case everywhere, including headings.

README order (fixed): one-liner → install → context → what's in it → tested on → known issues → configuration → license. Template: `templates/repo/README.md`.

## 5. Naming

| Thing | Rule | Example |
|---|---|---|
| Repo | `thing-it-does`, lowercase, hyphens, 2–3 words. No `awesome-`, `my-`, `-tool`. | `port-sync` |
| Description | ≤ 60 chars, sentence case, no period, no emoji. Identical to README line 1. | `Keeps a forwarded VPN port and qBittorrent in sync` |
| Topics | Max 6. ≥ 1 language tag + ≥ 1 domain tag. | `python` `networking` `self-hosted` |
| PowerShell | Approved `Verb-Noun`. `Rfs` prefix only on the entry point. | `Get-RfsHelp`, `Rotate-Cert` |
| CLI | One binary per repo, named after the repo. Subcommands are verbs. | `port-sync check` |
| Install line | One canonical form per platform, first thing in the README, from the repo's raw URL (until rfs.sh exists). | `irm https://raw.githubusercontent.com/Real-Fruit-Snacks/<repo>/main/install.ps1 \| iex` · `curl -fsSL https://raw.githubusercontent.com/Real-Fruit-Snacks/<repo>/main/install.sh \| sh` |
| Releases | SemVer, tag `vX.Y.Z`, title = tag. No codenames. | `v1.4.0` |
| Retiring | Replace README with `Superseded by [repo](link).` then archive. Never delete, never rename history. | — |
| The org | `Real-Fruit-Snacks` in URLs. **RFS** everywhere else. Never "Real Fruit Snacks", never lowercase `rfs`. | — |

## 6. Where each asset goes

| Need | File |
|---|---|
| GitHub org avatar, and any square or circular avatar (Discord, X, Mastodon) | `brand/social/rfs-avatar-dark-1024.png` (also 512, 256, SVG), from `tools/make-avatar.py`: the cover look (dot grid, Ember glow, full-width rule), full bleed, safe for a circle crop |
| App icons, favicons, small marks | `brand/mark/rfs-mark-dark-*.png` (the Caps Tile) |
| README header | None. The README starts with `# repo-name`; the org mark is on the cover (§7). Never put the lockup above the title. |
| Org profile header | `assets/rfs-banner-{dark,light}.svg` (1200×400; PNG at `brand/lockup/rfs-banner-*-1600.png`), from `tools/make-org-art.py` and `brand/org.toml`: the cover layout with "RFS" for the name, the tagline for the description, and a terminal listing the tools. Place with `width="100%"` at the top of the README in `Real-Fruit-Snacks/Real-Fruit-Snacks` (the profile page); never box it. |
| Org social card (links to the org, the site's `og:image`) | `brand/social/rfs-social-org-dark-1280x640.png`, from `tools/make-org-art.py`. This repo's own social preview is its cover, like any repo (`docs/assets/social-dark.png`) |
| Per-repo README cover + social preview | `tools/make-cover.py <repo>/docs/assets/cover.toml` — see section 7 |
| X / Mastodon / Bluesky header | `brand/social/rfs-header-dark-1500x500.png`, from `tools/make-org-art.py`: one centred line, clear of the avatar and of the phone crop |
| Website | copy `brand/web/*` to site root; paste `brand/web/head.html` into `<head>` |
| CSS variables | `brand/tokens/rfs.css` |
| Print / stickers / etching | `brand/mark/rfs-mark-mono-{white,ink}.svg` |

## 7. Repo cover

Every tool repo gets one cover. It is the image under the README one-liner, the docs site's `og:image`, and the GitHub social preview, all from one `docs/assets/cover.toml` rendered by `tools/make-cover.py`. Don't draw covers by hand; change the tool and re-run it.

| Part | Rule |
|---|---|
| Size | 1200×560 cover (rounded 12px), 1280×640 social preview (same cover centred, square corners) |
| Field | `bg`, 26px dot grid, Ember glow from the lower right (Nightshift only) |
| Text column | Name, rule, description and bullets as one block at x 88, centred vertically on the panel |
| Repo name | Plex Mono 600, 70px, −0.05em; shrinks to 44px for long names, never wraps |
| Rule | Ember, 5px, exactly as wide as the name's ink, 7px below the descender line (same height on every cover) |
| Description | The README one-liner, Plex Sans 600 24/32, two lines at most |
| Bullets | 0–4 facts, Plex Sans 15, `mute`, Ember square markers. Facts, not adjectives |
| Org | RFS tile (40px) + `REAL-FRUIT-SNACKS` in Plex Mono 11 caps, in the image's bottom-left corner (32px margin; 40px on the social preview) |
| Panel | 480×368, right side. Default: a terminal showing the install line and a real run. A tool with a UI draws itself instead (`kind = "art"`, an SVG fragment using colour tokens; `screen-mark` is the reference) |
| Not on it | URLs, version numbers, star counts, screenshots of other people's software |

Outputs: `cover-{dark,light}.svg` (README, via `<picture>`), `cover-{dark,light}.png` (site `og:image`, 1200×560), `social-{dark,light}.png` (upload `social-dark.png` in Settings → Social preview). All text is outlined, so nothing depends on installed fonts.

---

*Decided October 2026. Change this file first; regenerate assets second.*
