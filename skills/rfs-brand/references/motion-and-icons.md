# RFS Motion Choreography, 60-Icon Verb Table & CAD Geometry

Canonical reference for `--rfs-ease-detent` hardware controls, the 4 upgraded native `<progress>` loaders, all 60 Precision Silkscreen icons with their bespoke `part-*` click verbs, the 5 CAD geometric drawings (`[dwg] rfs-01`–`rfs-05`), and the 3-tier SVG art motion contract.

## 1. Mechanical Detent Curves & Timing Tokens

| Token | Value | Use |
|---|---|---|
| `--rfs-ease` | `cubic-bezier(0.16, 1, 0.3, 1)` | Standard exits/entrances, fades, panel glides |
| `--rfs-ease-detent` | `linear(0, 0.35 12%, 0.78 28%, 1.015 48%, 1.035 58%, 1.01 76%, 1)` | Tactile 3.5% mechanical seat settle (checkboxes, switches, icon detents; pairs with `--rfs-ease-detent-fallback`) |
| `--rfs-ease-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Symmetrical loops, meridian spin, loader beams |
| `--rfs-ease-exit` | `cubic-bezier(0.7, 0, 0.84, 0)` | Dismissals, drawer close |
| `--rfs-dur-fast` / `base` | `150ms` / `250ms` | Hover states, badge feedback, focus transitions |
| `--rfs-dur-detent` / `jump` | `340ms` / `360ms` | Hardware control locks & ballistic radio jumps |
| `--rfs-dur-slow` | `520ms` | Hero horizon rule draw, view transitions |

## 2. `rfs-motion.js` Controller Attributes & 4 Upgraded Loaders

Load `<script src="assets/rfs-motion.js"></script>` (zero dependencies) to auto-enhance:
- `[data-rfs-radio-jump="reticle|aperture"]` — 60fps compositor ballistic arc between 2–4 compact radio options.
- `[data-rfs-segmented]` — sliding segmented cue carriage with arrow-key support.
- `.rfs-fader` (`[data-rfs-fader]`) — syncs `--control-value`, `--attr-min`, `--attr-max`, and `aria-valuetext`.
- `[data-rfs-arm]` — two-stage destructive confirmation latch (`idle` -> `armed` -> `done`, auto-disarms after 3s).
- `[data-rfs-led-ladder]` — 20-cell hardware Patch-Bay LED progress bar (`window.RFS.setLadder(el, pct | null)`).
- `progress.rfs-progress-ring` — hollow conic ring via `background-clip: border-area`. **Gotcha:** always override indeterminate/100% fills with `background-image:` (never `background:` shorthand, which resets `background-clip` and fills the center solid).
- `[data-rfs-icon-click]` — triggers zero-reflow `.is-anim-a` / `.is-anim-b` part-level animations (plus stateful toggle/ratchet for `part-shackle`, `part-faders`, `part-ratchet`, `part-copy`).

## 3. Canonical 60-Icon Library & Bespoke `part-*` Verbs

Every icon lives in `rfs-icons.svg` (`#rfs-i-<name>`) and `brand/icons/<name>.svg` on a `24×24u` optical grid (`2u` inset, `1.75px` `square`/`miter`). Calm by default; opt in with `.rfs-icon-live` + `data-rfs-motion="<verb>"` + `data-rfs-icon-click`.

### UI & Navigation (10)
| Icon (`name`) | Motion Verb (`data-rfs-motion`) | Search Tags |
|---|---|---|
| `arrow-right` | `part-arrow-r` | next, forward, go, direction |
| `arrow-left` | `part-arrow-l` | back, previous, return, direction |
| `arrow-up-right` | `part-launch` | external, open, link, launch |
| `chevron-down` | `part-chev-d` | expand, dropdown, accordion, more |
| `chevron-right` | `part-chev-r` | next, breadcrumb, disclosure, step |
| `menu` | `part-menu` | hamburger, nav, drawer, lines |
| `close` | `part-close` | x, dismiss, cancel, clear |
| `search` | `part-scan` | find, filter, lookup, magnifier |
| `filter` | `part-funnel` | funnel, sort, query, refine |
| `sliders` | `part-faders` | dmx, faders, controls, console, tune |

### Actions & Controls (10)
| Icon (`name`) | Motion Verb (`data-rfs-motion`) | Search Tags |
|---|---|---|
| `plus` | `part-plus` | add, new, create, insert |
| `minus` | `part-compress` | remove, subtract, collapse |
| `edit` | `part-write` | pencil, write, rename, modify |
| `trash` | `part-lid` | delete, remove, destroy, confirm |
| `copy` | `part-copy` | clipboard, duplicate, clone |
| `check` | `part-draw-ok` | ok, done, confirm, valid |
| `refresh` | `part-spin` | sync, reload, retry, port-sync |
| `download` | `part-plunge` | save, export, install, fetch |
| `upload` | `part-upload` | import, push, publish, send |
| `share` | `part-share` | export, forward, distribute |

### Files & Code (10)
| Icon (`name`) | Motion Verb (`data-rfs-motion`) | Search Tags |
|---|---|---|
| `file` | `part-page` | document, note, markdown, page |
| `file-code` | `part-brackets` | source, script, toml, json, config |
| `folder` | `part-folder` | directory, workspace, path, project |
| `archive` | `part-box-lid` | zip, tar, retired, box, bundle |
| `terminal` | `part-prompt` | cli, shell, console, pwsh, zsh |
| `code` | `part-code` | brackets, syntax, html, dev |
| `git-branch` | `part-branch` | repo, branch, version, vcs |
| `diff` | `part-diff` | compare, patch, changes, plus-minus |
| `package` | `part-crate` | release, crate, pwn-shop, artifact |
| `book` | `part-book` | docs, manual, playbook, guide |

### Security & System (10)
| Icon (`name`) | Motion Verb (`data-rfs-motion`) | Search Tags |
|---|---|---|
| `shield` | `part-armor` | privacy, local, protect, firewall |
| `shield-check` | `part-verify` | verified, sha256, signed, trusted |
| `lock` | `part-shackle` | private, encrypted, mtls, secure |
| `unlock` | `part-unlatch` | open, public, access |
| `key` | `part-key-turn` | token, auth, credentials, passphrase |
| `certificate` | `part-seal` | certapi, x509, store, badge |
| `eye` | `part-blink` | view, preview, visible, inspect |
| `eye-off` | `part-slash` | hide, mask, redact, secret |
| `cpu` | `part-cpu` | hardware, local, rust, native, chip |
| `settings` | `part-ratchet` | gear, config, preferences, options |

### Network, Media & Tools (10)
| Icon (`name`) | Motion Verb (`data-rfs-motion`) | Search Tags |
|---|---|---|
| `globe` | `part-globe` | web, browser, offline, dns |
| `wifi` | `part-arcs` | network, signal, vpn, port |
| `server` | `part-rack` | daemon, localhost, host, node |
| `link` | `part-link` | url, chain, connect, anchor |
| `capture` | `part-shutter` | screenshot, screen-mark, crop, crosshair |
| `image` | `part-photo` | png, svg, photo, cover, artwork |
| `video` | `part-rec` | carify, ffmpeg, usb, media, encode |
| `play` | `part-play` | start, run, replay, motion |
| `pause` | `part-pause` | stop, freeze, wcag, board |
| `volume` | `part-waves` | audio, aac, sound, speaker |

### Status, Theme & Time (10)
| Icon (`name`) | Motion Verb (`data-rfs-motion`) | Search Tags |
|---|---|---|
| `check-circle` | `part-draw-ok` | ok, success, synced, pass |
| `alert-triangle` | `part-warn` | warn, warning, caution, destructive |
| `x-circle` | `part-draw-x` | error, fail, fault, blocked |
| `info` | `part-info` | note, help, details, stdout |
| `sun` | `part-sun` | light, day, lx512, alabaster |
| `moon` | `part-moon` | dark, night, lx263, blackout |
| `clock` | `part-clock` | time, timer, dwell, schedule, interval |
| `calendar` | `part-cal` | date, changelog, release, orders |
| `bell` | `part-chime` | notify, alert, webhook, status |
| `pin` | `part-pin` | featured, fixed, bookmark, lock |

## 4. Five CAD Engineering Drawings (`[dwg] rfs-01`–`rfs-05`)

| Sheet | Subject | Locked Dimensions | Clear Space / Safe Rule |
|---|---|---|---|
| **`[dwg] rfs-01`** | Monogram Tile | `64×64u`, `rx 14` (`21.9%`), `14.9u` V / `9.82u` H symmetry, `3.8u` Horizon bar | `>= 14u` (`1×rx`) all 4 sides; zero stretch or outer glow |
| **`[dwg] rfs-02`** | Horizontal Lockup | `405×64u` (`6.33:1`), `64u` tile + `18u` gap + `312.6u` Stencil wordmark & `3u` rule | `>= 16u` (`0.25×H`) perimeter; `< 160px` width -> collapse to `rfs-01` tile |
| **`[dwg] rfs-03`** | Silkscreen Icon Grid | `24×24u` (`2u` inset = `20×20u` live), `1.75px` `square`/`miter`, `17u` sq/Ø keylines | `>= 44×44px` minimum touch target (`10px` tap apron per side) |
| **`[dwg] rfs-04`** | Repo Cover v2 | `1200×560` README (`rx 12`), `480px` text col, `48px` gap, `528×448` panel, `0.32` light wash | `1280×640` (`2:1`) Social OG adds `+40px` bleed; must read at `400px` card width |
| **`[dwg] rfs-05`** | App-Shell & Controls | `100dvh` `.rfs-shell`, `64px` `.rfs-shell-header`, `4px` token badge, `2px` focus + `3px` offset | Scrollbar begins strictly at `y = 64px` (`scrollbar-gutter: stable`); `>= 44×44px` coarse target |

## 5. Three-Tier SVG Art Motion Contract (Static-First Invariant)

1. **Static Standard (`0ms`, zero `<style>` keyframes):** social previews (`social-*.png`), avatars, favicons, print.
2. **Animated One-Shot (`<= 1.4s` banners, `<= 3.5s` repo covers, plays once):** README covers and headers.
3. **Ambient Showcase (`board-{dark,light}.svg` only):** multi-item cue boards with `0` flashes/sec and a keyboard-accessible **Pause / Play** button (WCAG 2.2.2).
- **Static-First Rule:** Base SVG DOM outside `@media (prefers-reduced-motion: no-preference)` must always render the complete finished still frame.
