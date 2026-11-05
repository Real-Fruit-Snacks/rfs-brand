# RFS brand guide

Real-Fruit-Snacks · short form **RFS** · tagline **Real tools. No filler.**
Themes: **Nightshift** (dark, default) · **Dayshift** (light) · accent **Ember**

This is the source of truth. If an asset in `brand/` disagrees with this file, the asset is wrong.

---

## 1. Color — *Nightshift* / *Dayshift*

Two themes. **Nightshift** (dark) is the default; **Dayshift** (light) is derived from it. The accent color is **Ember**. Same structure, same hues, values shifted until every text color passes WCAG AA (≥ 4.5:1) on `bg`, `surface` and `raised` in both themes.

| Token | Nightshift | Dayshift | Rule |
|---|---|---|---|
| `bg` | `#0C0D10` | `#F6F5F2` | Page. Never pure black or pure white. |
| `surface` | `#13151A` | `#FFFFFF` | Cards, panels. One step up from bg. |
| `raised` | `#1A1D24` | `#ECEAE4` | Inputs, chips, nested cards. |
| `line` | `#262A33` | `#D6D3CB` | Dividers and decorative borders. Borders replace shadows (Dayshift may add a 1px hairline shadow on cards). |
| `line-strong` | `#636872` | `#89867F` | Inputs and any border that identifies a control. ≥ 3:1 against `bg`, `surface` and `raised` (WCAG 1.4.11), which `line` is not. |
| `text` | `#E8E6E1` | `#1A1B1E` | Body. Never `#FFF` for body copy. |
| `mute` | `#8A8F99` | `#666A73` | Secondary text, captions. |
| `primary` · Ember | `#FF6A3D` | `#C03B0A` | The brand. One per screen. Glow allowed in Nightshift only. |
| `primary-hover` | `#FC7951` | `#AC370C` | Ember fill on hover: 12% of `text` mixed in, so it moves away from `on-primary` (7.4:1 / 6.4:1). |
| `primary-press` | `#F98864` | `#98330F` | Ember fill while pressed: 24% of `text` (8.1:1 / 7.5:1). |
| `on-primary` | `#0C0D10` | `#FFFFFF` | Text and icons on Ember fills (buttons). Dark in Nightshift: white on Ember is only 2.9:1. |
| `accent` · Amber | `#FFC247` | `#925F00` | Warnings, second category, prompts. |
| `signal` · Mint | `#3DDC97` | `#15794D` | Success / running. Only ever means "OK". |
| `fault` · Raspberry | `#F06292` | `#B0306A` | Errors and failures. Only ever means "failed". Raspberry, not red, so it can't be mistaken for Ember. |
| `code-bg` | `#070809` | `#FFFFFF` | Code blocks follow the theme. Nightshift: one step darker than bg. Dayshift: surface white with ink text. |

Machine-readable: `brand/tokens/rfs.css`, `brand/tokens/rfs.tokens.json`.

**Status always has a word.** Mint, Amber and Raspberry are never the only signal: pair them with `ok`, `warn` or `fail` (or a line that says what happened). To red–green colour-blind readers Dayshift Ember and Amber look the same, and Mint and Raspberry come close; the word carries the meaning (WCAG 1.4.1). Mint and Raspberry are status colors, not accents.

**Focus:** a 2px Ember outline with a 3px offset on every focusable element (≥ 4.9:1 against `bg` in both themes). Never remove it without a replacement that is at least as visible.

**States.** Every change takes `--rfs-dur-fast` with `--rfs-ease`, and hover styles sit inside `@media (hover: hover)` so they never stick on touch screens.

| Element | Hover | Pressed | Disabled |
|---|---|---|---|
| Ember button | fill `primary-hover`; may lift 1px | fill `primary-press`; no lift | — (don't disable the primary action; explain what's missing instead) |
| Link | underline turns Ember; the text color stays | — | — |
| Secondary control (outline button, toggle, copy) | text `mute` → `text`, border `line-strong` → `mute` | moves down 1px | text `mute`, border `line`, no hover, default cursor |

Never lighten or darken Ember with a filter: `brightness()` moves Dayshift Ember toward its white text and lowers the contrast. Hover colors never replace focus; a hovered control that has focus shows both.

**Don't:** use Mint or Raspberry decoratively · use Ember for errors (Ember is brand, not danger; errors are Raspberry) · add a third accent · use gradients anywhere.

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
| body | 16 / 1.6 | Sans 400 | 0 |
| small | 13 / 1.5 | Sans 400 · mute | 0 |
| label | 11 / 1 | Mono 500 · caps | +0.08em |
| code | 13 / 1.7 | Mono 400 | 0 |
| wordmark | — | Mono 600 | −0.05em |

Sizes are for the web at 1×; covers and banners keep their own sizes (§7). Keep prose to 60–75 characters per line.

**Space:** a 4px base. Steps `--rfs-space-1` to `--rfs-space-9` are 4, 8, 12, 16, 24, 32, 48, 64 and 96px. Use the steps, not one-off values: 8–12 inside a component, 16–24 between related blocks, 48–96 between sections.

## 3. Mark — *Caps Tile*

`RFS` in Plex Mono SemiBold, centered on a rounded tile, Ember rule beneath.

- Tile: 64-unit grid, corner radius 14 (0.219 × side). Fill `#1A1D24` in Nightshift, `#1A1B1E` in Dayshift.
- Letters: 28 units, tracking −1.5, baseline at 43. Always white.
- Rule: 36 × 4 units, radius 2, at y = 48. Ember (theme value).
- Clear space: one corner radius on every side. Minimum size: 16 px.
- Small sizes (favicons, icon files at 48 px or less): `brand/mark/rfs-mark-small-{dark,light}.svg`. Same tile, colors and rule; the letters are redrawn on the 16 px grid, because the master's blur into a grey bar at 16 px. Letters 16 × 24 units, 4-unit strokes and gaps, at x = 4 / 24 / 44, cap top 16, baseline 40. Rule 40 × 4 units, radius 2, at x = 12, y = 48. Stems and bars sit on multiples of 4, so they land on whole pixels at 16, 32 and 48 px.
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
| PowerShell | Approved `Verb-Noun`. `Rfs` prefix only on the entry point. | `Get-RfsHelp`, `Update-Cert` |
| CLI | One binary per repo, named after the repo. Subcommands are verbs. | `port-sync check` |
| Install line | One canonical form per platform, first thing in the README, from the repo's raw URL (until rfs.sh exists). | `irm https://raw.githubusercontent.com/Real-Fruit-Snacks/<repo>/main/install.ps1 \| iex` · `curl -fsSL https://raw.githubusercontent.com/Real-Fruit-Snacks/<repo>/main/install.sh \| sh` |
| Releases | SemVer, tag `vX.Y.Z`, title = tag. No codenames. | `v1.4.0` |
| Retiring | Replace README with `Superseded by [repo](link).` then archive. Never delete, never rename history. | — |
| The org | `Real-Fruit-Snacks` in URLs. **RFS** everywhere else. Never "Real Fruit Snacks", never lowercase `rfs`. | — |

## 6. Where each asset goes

| Need | File |
|---|---|
| GitHub org avatar, and any square or circular avatar (Discord, X, Mastodon) | `brand/social/rfs-avatar-dark-1024.png` (also 512, 256, SVG), from `tools/make-avatar.py`: the cover look (dot grid, Ember glow, full-width rule), full bleed, safe for a circle crop |
| Favicons and icons at 48 px or less | `brand/mark/rfs-mark-small-dark-{16,32,48}.png` (the small-size Caps Tile, §3) |
| App icons, larger marks | `brand/mark/rfs-mark-dark-*.png` (the Caps Tile). iOS home screen: `brand/web/apple-touch-icon.png`, full bleed from `rfs-mark-dark-square.svg` (iOS rounds the corners itself and shows transparent pixels as black) |
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

Most people see a cover as a social card, 400–500px wide in Slack, Discord or X, or at about 830px in a README. At 400px everything is a third of its size, so anything drawn under about 20px turns into a grey line. Design for the card: a big name, one sentence, and one panel that shows what the tool does. `make-cover.py --preview FILE` shows the cover at 1200, 830 and 400px in both themes; judge it there.

| Part | Rule |
|---|---|
| Size | 1200×560 cover (rounded 12px), 1280×640 social preview (same cover centred, square corners) |
| Field | `bg`, 26px dot grid, Ember glow from the lower right (Nightshift only) |
| Grid | Text column at x 72–552; panel at x 600–1128, y 56–504 (528×448). The column is centred on the panel |
| Repo name | Plex Mono 600, −0.05em, as large as the 480px column allows, up to 120px. A name that would be under 80px on one line breaks after a hyphen onto two lines (the hyphen stays on the first); each line's ink starts at the column edge |
| Rule | Ember, as wide as the name's widest line of ink, 0.06 × the name's size high, below the descender line. It draws in on load (§8) |
| Description | The README one-liner and nothing else: Plex Sans 600 30/38, one line, or two of even length. No trailing period, even if the README has one |
| Bullets | None. They are in the README, and they can't be read on a card |
| Org | RFS tile (40px) + `REAL-FRUIT-SNACKS` in Plex Mono 11 caps, in the image's bottom-left corner (32px margin; 40px on the social preview) |
| Panel | The one thing that shows what the tool does, at sizes that read at 400px. Four kinds, below |
| Not on it | URLs, version numbers, star counts, screenshots of other people's software, invented figures. Values come from a real run or the README's own examples |

The panel, in the order to consider the kinds:

| Kind | For | Rules |
|---|---|---|
| `flow` | A tool that turns one thing into another: a port, a file, a request | Input, the tool on an Ember connector, output, top to bottom. The output is mirrored (its value above its label), so the two values face each other across the connector. Each end has a label (Sans 600 26), an optional note (Mono 22, `mute`) and one big value (Mono 600 64) or up to three chips. Up to two status lines sit in a log strip along the panel's foot, in terminal colours (§9). The connector draws in and the status lines print (§8) |
| `terminal` | A tool whose moment is a command | The command and the lines that matter, six at most, at 22–26px: about 35 characters a line, prompt included. Real lines aren't reworded to fit; pick shorter ones. The window is as tall as its lines. The command types, the lines print, and the cursor blinks twice and stays (§8) |
| `art` | A tool with a UI | The tool draws itself: an SVG fragment in the 528×448 box, in colour tokens, with fewer and bigger parts than the real screen. `screen-mark` is the reference. It doesn't move |
| `screenshot` | A UI too detailed to redraw | One PNG or JPEG per theme, cropped to the part that still reads at 400px (`crop`; `fit = "contain"` sits it on `bg`, seamless when the app uses the brand `bg`). `open-file` is the reference. It doesn't move |

Mint and Raspberry in a panel are status, as everywhere (§1): a Mint value or chip means it worked, and a word beside it says so.

Outputs: `cover-{dark,light}.svg` (README, via `<picture>`; these move once, §8), `cover-{dark,light}.png` (site `og:image`, 1200×560, the finished frame), `social-{dark,light}.png` (upload `social-dark.png` in Settings → Social preview). All text is outlined, so nothing depends on installed fonts. A cover made before this layout keeps rendering, unchanged, with `layout = "v1"` in its `cover.toml`. `templates/repo/cover.toml` documents every field.

## 8. Motion

Motion brings the brand's own parts to life; it never decorates. Both themes move the same way, and only Nightshift glows.

| Token | Value | Use |
|---|---|---|
| `--rfs-ease` | `cubic-bezier(.2, .7, .2, 1)` | Everything. Fast start, soft landing. |
| `--rfs-dur-fast` | `150ms` | Hover, press, focus. |
| `--rfs-dur-base` | `250ms` | State changes: toggles, menus, copy confirmations. |
| `--rfs-dur-slow` | `600ms` | Entrances and the theme switch. |
| `--rfs-type-rate` | `45ms` per character | A terminal typing its command. |

The brand's motions (use these; don't invent others):

- The Ember rule draws in, left to right, under a name or the wordmark. Once, on load. On a repo cover, a flow's connector draws in the same way, top to bottom.
- A terminal types its command at `--rfs-type-rate`, then prints its output one line at a time, 100–200ms apart. The cursor blinks twice, then stays. A cover's status lines print the same way.
- In Nightshift, the dot grid warms to Ember around the pointer (fine pointers only). Dayshift has no glow.
- The theme switch sweeps the new theme in from the control, in a circle, at `--rfs-dur-slow`.

An entrance totals 1.2s at most and never delays reading the headline. Nothing loops except the cursor's two blinks. Every motion sits inside `prefers-reduced-motion: no-preference`; with reduced motion the page is the finished still frame. No parallax, no scroll-jacking.

**Repo covers** are the one exception to the 1.2s: a cover's SVG may run up to 3.5s, because a terminal types its command at the type rate. The name and the description are there from the first frame, so nothing waits on it, and `make-cover.py` refuses a cover that runs longer. Covers are shown through `<img>`, where a browser may not apply `prefers-reduced-motion` (Chromium doesn't), so their motion must be safe without that switch: once, on load; nothing flashes or loops beyond the cursor's two blinks; nothing larger than the rule, the connector or a line of type moves. The styles outside the media query are the finished frame, which is also what the PNGs show.

## 9. Terminal and code

Terminals on covers, sites and docs use one palette, the same one `tools/make-cover.py` draws:

| Line | Color | Example |
|---|---|---|
| prompt | Ember, Mono 600 | `$` |
| command after the prompt | `text` | `./install.sh` |
| success | Mint | `carify 1.1.0 installed` |
| warning | Amber | `no ffmpeg on PATH` |
| error | Raspberry | `port 51413 refused` |
| other output | `mute` | `listening on 0.0.0.0:8080` |

In `cover.toml`, a line's prefix picks its color: `$ `, `ok `, `! `, `x ` or none. The prefix isn't drawn, so the words themselves must say what happened (§1): "installed", "refused", not just a colored line. On sites, keep `ok` / `warn` / `fail` visible or write the line the same way.

Code blocks use `code-bg`, `text` for code, `mute` for comments and Amber for strings, and nothing else. Keywords stay in `text`. Mint and Raspberry never appear in code, only in output that reports a result.

---

*Decided October 2026. Change this file first; regenerate assets second.*
