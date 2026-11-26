<!--
  RFS REPO README — ULTRA-MINIMAL TEMPLATE (40–60 lines target, BRAND.md §14)
  Section order is fixed. Delete empty sections; never reorder or rename.
  Voice: Plain · Specific · Dry · Honest. No emoji, no hype words, no exclamation marks.
  Move detailed CLI references, config schemas, examples, tested matrices, known issues,
  troubleshooting, and build guides into versioned Markdown under docs/ (e.g. docs/USAGE.md).
  Delete all HTML comments before committing.
  No RFS lockup above the title: the org mark lives on the cover (BRAND.md §7).
-->

# repo-name

<!--
  ONE sentence, <= 60 characters, no period. Identical to the GitHub repo description.
-->
What it does, for whom

<!--
  Cover: generated from docs/assets/cover.toml via rfs-brand/tools/make-cover.py.
-->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/cover-dark.svg">
  <img alt="repo-name: what the cover panel shows" src="docs/assets/cover-light.svg" width="100%">
</picture>

<!--
  Shortest real path to install or run locally. No accounts, no tracking.
-->
```powershell
git clone https://github.com/Real-Fruit-Snacks/repo-name.git
```

<!--
  3–5 short, specific bullets: what goes in, what comes out locally, key platform notes.
-->
- **Local-first:** Runs directly on your machine with zero accounts or telemetry.
- **Input -> Output:** Plainly state what goes in and what comes out.
- **Platforms:** State tested OS/runtime versions plainly.

## Documentation

<!-- Link only the docs/*.md files this repo actually ships (and live site if published). -->
- [Usage & CLI reference](docs/USAGE.md)
- [Configuration](docs/CONFIGURATION.md)
- [Development & testing](docs/DEVELOPMENT.md)

## License

MIT
