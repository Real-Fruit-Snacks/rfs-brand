# RFS Page Archetypes & Layout Decision Tree

Different Real-Fruit-Snacks tools solve different problems and **must not** ship identical clone GitHub Pages sites. Every tool shares the same Cyclorama Dawn tokens, typography, header/shell discipline, and `D · Terminal Token` grammar, while choosing a layout archetype tailored to how the tool actually works.

## Decision Tree: Pick the Right Archetype

1. **Is the site itself a live interactive browser app (game, puzzle board, local generator)?**
   → **Archetype 5 — Full-Viewport Offline App** (e.g., `open-file`, `one-billion-pixels`, `identity-gen`).
2. **Is the tool a multi-command workflow, toolkit, or reference collection?**
   → **Archetype 4 — Editorial Handbook & Command Ledger** (e.g., `pwn-broker`, `pwn-playbooks`, `pwn-report`, `pwn-shop`, `powershell-toolbox`).
3. **Does the tool's core value hinge on safety bounds, exit/status codes, or protocol rules?**
   → **Archetype 2 — Safety Matrix & Protocol Spec** (e.g., `cred-spray`, `certapi`).
4. **Does the tool transform, bridge, route, or coerce traffic/files across stages or hosts?**
   → **Archetype 3 — Topology & Signal Pipeline Workbench** (e.g., `shell-tunnel`, `ad-sweep`, `hash-bait`, `carify`, `amazon-order-sync`).
5. **Does the tool watch one live state or serve as an org-wide directory/proof bay?**
   → **Archetype 1 — Interactive Proof Console** (e.g., `rfs.tools`, `Real-Fruit-Snacks.github.io`, `port-sync`, `screen-mark`).

## The Five Canonical Archetypes

| Archetype | Hero Signature | Primary Content Pattern | Max Content Width |
|---|---|---|---|
| **1. Interactive Proof Console** | Monumental stencil title + live `IN -> OUT` patch deck or DMX channel bay | Interactive selector / cue table + sticky proof inspector | `72rem` – `82rem` |
| **2. Safety Matrix & Protocol Spec** | Stencil title + lock-out / safety telemetry panel (threshold gauges, 7 explicit statuses) | Interactive protocol/status filter tabs + safety boundary tables | `74rem` |
| **3. Topology & Pipeline Workbench** | Stencil title + bespoke inline SVG architecture/stage diagram (`Steel -> Beacon -> Mint`) | Interactive mode switcher (e.g., bind vs. reverse, drop vs. clean, per-target stage cards) | `74rem` |
| **4. Editorial Handbook & Ledger** | Compact stencil masthead + direct install/run strip | Two-column TOC sidebar + scannable command/recipe reference ledger (`62ch` prose limit) | `76rem` |
| **5. Full-Viewport Offline App** | No marketing hero—opens directly into the working tool chrome | `100dvh` app shell (`.rfs-shell`), collapsible side panel, canvas/workspace stage | `100vw` |

## Shared Spatial & Responsive Rules

- **App-Shell Scrollbar:** Every site with a top header wraps the document in `<body class="rfs-shell">` -> `<header class="rfs-shell-header">` -> `<div class="rfs-scroll-region" id="page-scroll">` so vertical scrollbars begin strictly at the header's bottom hairline. Sidebar-rail apps (`Real-Fruit-Snacks.github.io`) use a `100dvh` grid where the main column scrolls independently and collapses into a top bar at `<= 960px`.
- **Breakpoints:** `--rfs-bp-sm: 36em` (`576px`), `--rfs-bp-md: 56em` (`896px`), `--rfs-bp-lg: 72em` (`1152px`).
- **Prose Measure:** Cap running descriptions at `58ch`–`66ch` (`text-wrap: pretty`; headings `text-wrap: balance`).
- **Touch Targets & Reflow:** Interactive buttons/tabs/inputs maintain `>= 44px` tap targets on coarse pointers and `0px` horizontal document overflow down to `390px` viewport width (`min-width: 0` on all CSS grid children).
- **Hidden Tabpanels:** When using `hidden="until-found"` in stacked grid cells, apply `pointer-events: none; z-index: 0;` to `[role="tabpanel"][hidden]` and `position: relative; z-index: 1;` to `:not([hidden])` so hidden panels never swallow clicks on active Copy buttons.
