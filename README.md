# rfs-brand

RFS brand, profile art and repo templates.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/cover-dark.svg">
  <img alt="rfs-brand: a miniature repo cover, the Ember, Amber and Mint colour swatches, and IBM Plex Sans and Mono specimens" src="docs/assets/cover-light.svg" width="100%">
</picture>

Org-wide defaults and the RFS identity. Themes are **Nightshift** (dark, default) and **Dayshift** (light); asset filenames keep plain `-dark` / `-light` suffixes so they stay self-describing. Everything that makes the repos under `Real-Fruit-Snacks` look and read like one org lives here.

| Path | What it is | Who reads it |
|---|---|---|
| [`assets/`](assets/) | The profile banner and the mark, loaded by raw URL | The profile page, [`Real-Fruit-Snacks/Real-Fruit-Snacks`](https://github.com/Real-Fruit-Snacks/Real-Fruit-Snacks) |
| [`brand/`](brand/) | The full asset set — mark, lockups, social, web icons, design tokens | You, when you need a file |
| [`templates/repo/`](templates/repo/) | README template and per-repo settings checklist | You, when starting or cleaning up a repo |
| [`tools/`](tools/) | `make-cover.py` renders a repo's README cover and social preview from its `docs/assets/cover.toml`; `make-org-art.py` renders the profile banner, org social preview and X header from `brand/org.toml`; `make-avatar.py` renders the profile picture | You, once per repo and after a description or tool-list change |
| [`BRAND.md`](BRAND.md) | The identity guide: color, type, mark, voice, naming | Anyone touching the brand |

## Get the kit

Each release has the whole kit as one zip, plus the two token files on their own. These links always point at the newest release:

| File | Link |
|---|---|
| Everything (guide, assets, tokens, tools, templates) | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-brand.zip |
| CSS variables | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs.css |
| Design tokens (JSON) | https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs.tokens.json |

```powershell
curl.exe -LO https://github.com/Real-Fruit-Snacks/rfs-brand/releases/latest/download/rfs-brand.zip
```

To publish a release: add a `## X.Y.Z (date)` section to `CHANGELOG.md`, commit, then `git tag vX.Y.Z` and `git push origin vX.Y.Z`. The release workflow checks that the committed SVGs match what the tools generate, builds the zip and publishes it, titled with the tag.

## Starting a new repo

1. Copy `templates/repo/README.md`, fill it in, delete the HTML comments.
2. Work through `templates/repo/SETTINGS-CHECKLIST.md`.
3. Copy `templates/repo/cover.toml` to the repo's `docs/assets/`, fill it in, then `python3 tools/make-cover.py ../<repo>/docs/assets/cover.toml` (from this repo, with the clones side by side). Commit the `cover-*` files; upload `social-dark.png` as the social preview.

## Changing the brand

Edit `BRAND.md` first, then regenerate assets. Assets are derived; the guide is the source. The profile page loads its banner from `assets/` by raw URL, so a change there is live on the next page load. Repo covers are committed in each repo, so they only change when you re-run `make-cover.py` there.

When a tool is added, renamed or archived, update `brand/org.toml`, the README in `Real-Fruit-Snacks/Real-Fruit-Snacks` and `tools.json` in the site repo, then run `python3 tools/make-org-art.py`.

Real-Fruit-Snacks is a personal account, so GitHub shows the profile README from the `Real-Fruit-Snacks/Real-Fruit-Snacks` repo; a `profile/` folder here would only work for an organization.

## Licenses

Code in `tools/` is MIT. Fonts in `tools/fonts/` are IBM Plex, SIL Open Font License (`OFL.txt`). The RFS mark and name are not licensed for reuse.
