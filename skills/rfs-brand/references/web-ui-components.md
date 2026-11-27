# RFS Web UI Components, Data Visualization & Framework Bridges

Load stylesheets in strict order: `rfs.css` first, `rfs-components.css` second, page-specific CSS third.

## 1. Document Head & App-Shell Skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <script>
    try {
      var s = localStorage.getItem("rfs-theme") || localStorage.getItem("color-scheme");
      if (s === "light" || s === "dark") document.querySelector('meta[name="color-scheme"]').content = s;
    } catch (e) {}
  </script>
  <link rel="stylesheet" href="assets/rfs.css">
  <link rel="stylesheet" href="assets/rfs-components.css">
</head>
<body class="rfs-shell">
  <header class="rfs-shell-header"><!-- brand mark, nav, theme toggle --></header>
  <div class="rfs-scroll-region" id="page-scroll">
    <main><!-- page content --></main>
  </div>
</body>
</html>
```

## 2. Canonical Component Patterns

### Buttons & `D · Terminal Token` Badges
```html
<div class="btn-rack">
  <button class="rfs-btn rfs-btn-horizon" type="button">Primary CTA</button>
  <button class="rfs-btn rfs-btn-steel" type="button">Steel Action</button>
  <button class="rfs-btn rfs-btn-outline" type="button">Secondary</button>
  <button class="rfs-btn rfs-btn-fault" type="button" command="show-modal" commandfor="confirm-del">Delete…</button>
</div>

<span class="rfs-badge b-ok"><span class="k">[ok]</span> synced</span>
<span class="rfs-badge b-warn"><span class="k">[!]</span> ffmpeg missing</span>
<span class="rfs-badge b-fail"><span class="k">[x]</span> connection refused</span>
<span class="rfs-badge b-steel"><span class="k">[rust]</span> local binary</span>
```

### Framed Code Card (Language Header + Wrapped by Default)
```html
<div class="rfs-code-card">
  <div class="rfs-code-head">
    <span class="rfs-badge b-steel"><span class="k">[shell]</span></span>
    <span class="copy-wrap">
      <button class="copy-btn" type="button" command="--copy" commandfor="cmd-install">Copy<span class="visually-hidden"> install command</span></button>
      <span class="copy-tip" role="status"></span>
    </span>
  </div>
  <pre class="rfs-code-block"><code id="cmd-install"><span class="rfs-tok-fn">port-sync</span> <span class="rfs-tok-kw">check</span> <span class="rfs-tok-str">--verbose</span></code></pre>
</div>
```

### Destructive Confirmation Modal (Zero Native `confirm()`)
```html
<dialog id="confirm-del" class="rfs-dialog is-destructive" closedby="any" aria-labelledby="del-h" aria-describedby="del-p">
  <div class="rfs-dialog-bar" aria-hidden="true"></div>
  <form class="rfs-dialog-body" method="dialog">
    <span class="rfs-badge b-fail"><span class="k">[!]</span> destructive action</span>
    <h1 class="rfs-dialog-title" id="del-h">Delete archive.tar.gz?</h1>
    <p class="rfs-dialog-copy" id="del-p">Are you sure you want to permanently remove <code>archive.tar.gz</code>? This cannot be undone.</p>
    <div class="rfs-dialog-actions">
      <button class="rfs-btn rfs-btn-outline" value="cancel" autofocus>Cancel</button>
      <button class="rfs-btn rfs-btn-fault" value="delete">Delete Archive</button>
    </div>
  </form>
</dialog>
```

### Semantic UI States, Hardware Controls, Upgraded Loaders & Opt-In Icon Motion
Load `<script src="assets/rfs-motion.js"></script>` to auto-wire jumping radios, faders, armed latches, LED ladders, progress rings, and clickable icons:

```html
<!-- Custom checkboxes, switches & jumping radios -->
<label class="rfs-check-label"><input type="checkbox" class="rfs-check" checked><span>Ink Draw</span></label>
<label class="rfs-switch-label"><input type="checkbox" switch class="rfs-switch-breaker" checked><span>Breaker Rocker</span></label>
<div class="rfs-radio-group" data-rfs-radio-jump="reticle" role="radiogroup" aria-label="Preset">
  <label class="rfs-radio-label"><input type="radio" name="p" class="rfs-radio" checked><span>Low</span></label>
  <label class="rfs-radio-label"><input type="radio" name="p" class="rfs-radio"><span>Max</span></label>
</div>
<input class="rfs-fader" type="range" min="0" max="100" value="64" data-rfs-fader>

<!-- 4 upgraded loaders (DMX Cue Meter, Alive Trace, 20-Cell LED Ladder, Precision Ring) -->
<div class="rfs-progress-dmx-shell"><progress class="rfs-progress-dmx" value="68" max="100" aria-label="Build"></progress></div>
<progress class="rfs-progress" value="68" max="100" aria-label="Sync"></progress>
<div class="rfs-led-ladder" data-rfs-led-ladder data-rfs-led-value="68" role="progressbar" aria-valuemin="0" aria-valuemax="100"></div>
<div class="rfs-ring-wrap"><progress class="rfs-progress-ring" value="68" max="100" aria-label="Ring"></progress><span class="rfs-ring-label" aria-hidden="true">68%</span></div>

<!-- Opt-in click motion on any of the 60 RFS Silkscreen icons (calm by default) -->
<button class="rfs-btn rfs-btn-outline rfs-icon-live" type="button" data-rfs-motion="part-lid" data-rfs-icon-click>
  <svg class="rfs-icon" viewBox="0 0 24 24" aria-hidden="true"><!-- brand/icons/trash.svg inner --></svg>
  <span>Delete</span>
</button>
```

## 3. Data Visualization Palette (`--rfs-viz-1` through `--rfs-viz-6`)

Use the 6 ordered categorical series from `rfs.css` / `rfs.tokens.json`. Every series passes WCAG AA (>= 5.8:1) in both Dark (`LX 263`) and Light (`LX 512`):

| Series | Token | Dark (`LX 263`) | Light (`LX 512`) | Recommended Role |
|---|---|---|---|---|
| 1 | `--rfs-viz-1` | `#74B8E8` | `#164669` | Primary baseline / input series |
| 2 | `--rfs-viz-2` | `#FF9254` | `#AD3D0A` | Primary comparison / active series |
| 3 | `--rfs-viz-3` | `#3DDC97` | `#127247` | Verified / passing / completed series |
| 4 | `--rfs-viz-4` | `#FFC247` | `#885800` | Warning / threshold / latency series |
| 5 | `--rfs-viz-5` | `#FF5C6C` | `#B91C2E` | Error / rejected / fault series |
| 6 | `--rfs-viz-6` | `#B3B5C0` | `#474D59` | Background / historical / reference series |

**Chart Rules:**
- Pair color with direct text labels or distinct dash patterns (`stroke-dasharray`) so plots never rely on color alone (WCAG 1.4.1).
- Set numeric axes and callouts in `Azeret Mono` with `font-variant-numeric: tabular-nums`.
- Use `--rfs-viz-grid` (`1px`) for faint structural gridlines; never add 3D extrusions, neon glows, or default rainbow chart palettes.

## 4. Tailwind CSS v4, TypeScript & W3C DTCG Exports

- **Tailwind CSS v4:** Import `rfs.css` and `rfs-tailwind.css` right after `@import "tailwindcss";` to unlock `bg-rfs-bg`, `bg-rfs-surface`, `text-rfs-steel-ink`, `text-rfs-beacon-ink`, `border-rfs-line`, `font-display`, `font-sans`, `font-mono`, and `rounded-rfs-token`.
- **TypeScript / Canvas / WebGL:** Import `RFS_COLORS`, `RFS_DATAVIZ`, `RFS_MOTION`, `RFS_SPACE`, or `RFS_CLI` from `brand/tokens/rfs-tokens.ts`.
- **W3C DTCG (Figma / Style Dictionary):** Import `brand/tokens/rfs.dtcg.json` (`$type` / `$value` / `$description`).
