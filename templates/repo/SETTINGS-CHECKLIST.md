# Per-repo settings checklist (Settings -> General)

Run through this once per public repository so every active tool matches the Real-Fruit-Snacks brand system.

- [ ] **Description** — identical to README line 1. <= 60 chars, sentence case, no period, no emoji.
- [ ] **Website** — project page URL if published, otherwise blank.
- [ ] **Topics** (max 6) — at least one language tag and one domain tag (`rust`, `python`, `powershell`, `csharp`, `typescript`, `local-first`, `windows`, `kali`, `networking`, `cli`).
- [ ] **Cover + social preview** — fill in `docs/assets/cover.toml`, run `python3 ../rfs-brand/tools/make-cover.py docs/assets/cover.toml`, commit `cover-*`, and upload `docs/assets/social-dark.png` (1280x640).
- [ ] **Brand contract & templates** — copy `templates/repo/AGENTS.md` (with `BRAND-RULES.md`), `SECURITY.md`, and `.github/` issue/PR templates. For web UIs, load `rfs.css`, `rfs-components.css`, and `rfs-icons.svg`.
- [ ] **README & Docs** — keep `README.md` ultra-minimal (40–60 lines per `BRAND.md` §14), place detailed reference and guides in versioned `docs/*.md`, and **disable GitHub Wiki** (`Settings -> General -> Features -> Wikis` unchecked).
- [ ] **Catalog sync** — add or update the entry in `Real-Fruit-Snacks.github.io/tools.json` and `Real-Fruit-Snacks/art/make-board.py`.
- [ ] **Releases** — SemVer tag `vX.Y.Z`, release title equals tag, direct binaries/archives when applicable.
- [ ] **Retiring** — archive on GitHub (read-only) and move the repo into `retired` in `tools.json`.
- [ ] **Default branch** — `main`.
