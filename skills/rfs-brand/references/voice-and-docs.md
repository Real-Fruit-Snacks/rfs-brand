# RFS Voice, Microcopy, Documentation & Media Standards

Four voice tests govern all copy: **Plain** (actionable at 2 am), **Specific** (replace adjectives with measured facts/flags), **Dry** (zero hype or exclamation marks in titles), and **Honest** (state platform caveats early).

## Voice & Microcopy Before / After Matrix

| Surface | Avoid (`[x]`) | Use (`[ok]`) |
|---|---|---|
| **README one-liner** | *"A blazing-fast, modern Rust screenshot tool!"* | `Screenshot capture and annotation in pure Rust` |
| **CLI error** | `Error: Something went wrong connecting.` | `[x] qBittorrent refused 127.0.0.1:8080 — enable Web UI and retry` |
| **Empty state** | *"Nothing here yet! Let's get started!"* | `[empty] 0 targets staged — run pwn-broker add <ip> to add one.` |
| **Destructive CTA** | `Are you sure? [Yes] [No]` | `Delete 2026-11-16_htb_forest.tar.gz? [Cancel] [Delete Archive]` |
| **Toast notice** | *"Awesome! Copied successfully!"* | `[ok] Copied git clone URL.` |
| **Release note** | *"Supercharged performance and seamless UX improvements."* | `Reduced full-world redraw from 18ms to 4ms on 4K displays.` |

**Banned words:** `blazing`, `powerful`, `modern`, `seamless`, `supercharge`, `awesome`, `Welcome!`, `coming soon`, all emoji, and exclamation marks in headings or descriptions.

## Ultra-Minimal `README.md` Contract (40–60 Lines)

Keep every repository `README.md` scannable in this fixed order:
1. `# repo-name`
2. One-line summary (`<= 60` chars, sentence case, no trailing period, matches GitHub repo description).
3. Adaptive `<picture>` cover referencing `docs/assets/cover-dark.svg` and `docs/assets/cover-light.svg`.
4. Shortest real install or run snippet (1 concise code block).
5. 3–5 concrete bullets (what goes in, what runs locally, what comes out).
6. `## Documentation` linking to `docs/*.md` and the published Pages URL.
7. `## License`.

**Strict Documentation Rules:**
- **No shields.io badge walls:** Never stack colorful third-party status badges under the README heading. Let the cover, one-liner, and CI handle signal.
- **Overflow goes in `docs/*.md` (never GitHub Wiki):** Put full CLI flags, config references, architecture notes, tested matrices, troubleshooting, and dev/build instructions in `docs/USAGE.md`, `docs/CONFIGURATION.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`. Disable the GitHub Wiki tab in repo settings.

## Screenshots, Demo Recordings & Redaction Rules

- **Themes:** Capture dark-mode (`LX 263`) screenshots by default; provide paired light (`LX 512`) captures when documenting dual-theme web apps.
- **Framing:** Keep clean `16px`–`24px` outer breathing room or native window edges—never add fake macOS traffic-light dots onto Linux/Windows terminal captures.
- **Redaction (mandatory):** Never commit real usernames (`C:\Users\<realname>`), private IPs from real engagements, real hostnames, tokens, or private repo names. Always use RFC 5737 / lab-safe placeholders (`10.10.14.5`, `10.0.0.1-2`, `dc1`, `htb_forest`, `example.invalid`).
- **Alt text:** Describe what the screenshot or cover proves (real inputs/outputs/UI state), never `"screenshot"` or `"banner"`.
