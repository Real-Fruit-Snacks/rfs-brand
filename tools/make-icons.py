#!/usr/bin/env python3
"""Generate the canonical Real-Fruit-Snacks (RFS) Cyclorama Dawn Icon Library (60 icons).

Design grammar ("Cyclorama Precision Silkscreen"):
  - Strict 24x24 viewBox, 2px optical inset (2..22 live frame), pixel-aligned geometry.
  - Consistent 1.75px stroke weight, fill="none", stroke="currentColor".
  - Crisp industrial linecap="square" and linejoin="miter" (with 1.5px-2px geometric
    corner chamfers/radii where appropriate), matching Big Shoulders Stencil and
    DMX console hardware engraving rather than soft rounded cartoon icons.
  - Optical area balance: squares 16x16 (4..20), circles r=8.5, wide rects 18x14,
    tall rects 14x18 so every icon carries uniform visual weight at 16, 20, 24, and 32px.

Outputs (relative to repo root):
  brand/icons/<name>.svg         60 standalone SVGs
  brand/icons/rfs-icons.svg      All-in-one SVG <symbol> sprite (#rfs-i-<name>)
  brand/icons/icons.json         Manifest (name, category, tags, inner markup)

Optional:
  python tools/make-icons.py --preview DIR   Render high-res dark & light QA sheets
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "brand", "icons")

SVG_ATTRS = (
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.75" stroke-linecap="square" stroke-linejoin="miter"'
)

# 60 icons = 6 balanced categories x 10 icons each
# Each tuple: (name, category, tags, inner_svg_elements)
ICONS = [
    # ---- 1. UI & Navigation (10) ----
    (
        "arrow-right",
        "ui",
        ["next", "forward", "go", "direction"],
        '<path d="M4 12h15"/><path d="M13.5 6.5L19 12l-5.5 5.5"/>',
    ),
    (
        "arrow-left",
        "ui",
        ["back", "previous", "return", "direction"],
        '<path d="M20 12H5"/><path d="M10.5 6.5L5 12l5.5 5.5"/>',
    ),
    (
        "arrow-up-right",
        "ui",
        ["external", "open", "link", "launch"],
        '<path d="M6.5 17.5L17.5 6.5"/><path d="M9 6.5h8.5V15"/>',
    ),
    (
        "chevron-down",
        "ui",
        ["expand", "dropdown", "accordion", "more"],
        '<path d="M6 9.5l6 6 6-6"/>',
    ),
    (
        "chevron-right",
        "ui",
        ["next", "breadcrumb", "disclosure", "step"],
        '<path d="M9.5 6l6 6-6 6"/>',
    ),
    (
        "menu",
        "ui",
        ["hamburger", "nav", "drawer", "lines"],
        '<path d="M4 6.5h16"/><path d="M4 12h16"/><path d="M4 17.5h16"/>',
    ),
    (
        "close",
        "ui",
        ["x", "dismiss", "cancel", "clear"],
        '<path d="M6 6l12 12"/><path d="M18 6L6 18"/>',
    ),
    (
        "search",
        "ui",
        ["find", "filter", "lookup", "magnifier"],
        '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L20 20"/>',
    ),
    (
        "filter",
        "ui",
        ["funnel", "sort", "query", "refine"],
        '<path d="M3.5 5h17l-6.5 7.5V19l-4-2v-4.5L3.5 5z"/>',
    ),
    (
        "sliders",
        "ui",
        ["dmx", "faders", "controls", "console", "tune"],
        '<path d="M5 4v16"/><path d="M12 4v16"/><path d="M19 4v16"/>'
        '<rect x="3" y="8" width="4" height="3.5" fill="currentColor" stroke="none"/>'
        '<rect x="10" y="13.5" width="4" height="3.5" fill="currentColor" stroke="none"/>'
        '<rect x="17" y="6.5" width="4" height="3.5" fill="currentColor" stroke="none"/>',
    ),

    # ---- 2. Actions & Controls (10) ----
    (
        "plus",
        "actions",
        ["add", "new", "create", "insert"],
        '<path d="M12 5v14"/><path d="M5 12h14"/>',
    ),
    (
        "minus",
        "actions",
        ["remove", "subtract", "collapse"],
        '<path d="M5 12h14"/>',
    ),
    (
        "edit",
        "actions",
        ["pencil", "write", "rename", "modify"],
        '<path d="M4 20h4.5L19.5 9 15 4.5 4 15.5V20z"/><path d="M12.5 7l4.5 4.5"/>',
    ),
    (
        "trash",
        "actions",
        ["delete", "remove", "destroy", "confirm"],
        '<path d="M4 6.5h16"/><path d="M9 6.5V4h6v2.5"/>'
        '<path d="M6.5 6.5l1 13.5h9l1-13.5"/><path d="M10.25 10.5v6"/><path d="M13.75 10.5v6"/>',
    ),
    (
        "copy",
        "actions",
        ["clipboard", "duplicate", "clone"],
        '<rect x="8.5" y="8.5" width="11.5" height="11.5" rx="1"/>'
        '<path d="M15.5 8.5V4.5A0.5 0.5 0 0 0 15 4H4.5A0.5 0.5 0 0 0 4 4.5V15a0.5 0.5 0 0 0 0.5 0.5h4"/>',
    ),
    (
        "check",
        "actions",
        ["ok", "done", "confirm", "valid"],
        '<path d="M4.5 12.5L9.5 17.5L19.5 6.5"/>',
    ),
    (
        "refresh",
        "actions",
        ["sync", "reload", "retry", "port-sync"],
        '<path d="M19.5 10A7.5 7.5 0 0 0 6.2 7.2L4.5 9"/>'
        '<path d="M4.5 4.5V9H9"/>'
        '<path d="M4.5 14A7.5 7.5 0 0 0 17.8 16.8L19.5 15"/>'
        '<path d="M19.5 19.5V15H15"/>',
    ),
    (
        "download",
        "actions",
        ["save", "export", "install", "fetch"],
        '<path d="M12 4v11"/><path d="M7.5 10.5L12 15l4.5-4.5"/><path d="M4 19.5h16"/>',
    ),
    (
        "upload",
        "actions",
        ["import", "push", "publish", "send"],
        '<path d="M12 15.5V4.5"/><path d="M7.5 9L12 4.5 16.5 9"/><path d="M4 19.5h16"/>',
    ),
    (
        "share",
        "actions",
        ["export", "forward", "distribute"],
        '<circle cx="17.5" cy="5.5" r="2.25"/><circle cx="6.5" cy="12" r="2.25"/><circle cx="17.5" cy="18.5" r="2.25"/>'
        '<path d="M8.5 10.8l7-4.1"/><path d="M8.5 13.2l7 4.1"/>',
    ),

    # ---- 3. Files & Code (10) ----
    (
        "file",
        "code",
        ["document", "note", "markdown", "page"],
        '<path d="M5.5 3.5h8.5L18.5 8v12.5h-13V3.5z"/><path d="M13.5 3.5V8.5h5"/>',
    ),
    (
        "file-code",
        "code",
        ["source", "script", "toml", "json", "config"],
        '<path d="M4.5 3.5h9.5L19.5 9v11.5h-15V3.5z"/><path d="M14 3.5V9h5.5"/>'
        '<path d="M10.25 13L8.25 15l2 2"/><path d="M13.75 13l2 2-2 2"/>',
    ),
    (
        "folder",
        "code",
        ["directory", "workspace", "path", "project"],
        '<path d="M3.5 5.5h6l2 2.5h9v11h-17V5.5z"/>',
    ),
    (
        "archive",
        "code",
        ["zip", "tar", "retired", "box", "bundle"],
        '<rect x="3.5" y="4.5" width="17" height="4"/>'
        '<path d="M5 8.5v11h14v-11"/><path d="M9.5 13h5"/>',
    ),
    (
        "terminal",
        "code",
        ["cli", "shell", "console", "pwsh", "zsh"],
        '<rect x="3" y="4" width="18" height="16" rx="1"/>'
        '<path d="M7 9.5l3 2.5-3 2.5"/><path d="M12.5 14.5h4.5"/>',
    ),
    (
        "code",
        "code",
        ["brackets", "syntax", "html", "dev"],
        '<path d="M8 7.5L3.5 12 8 16.5"/><path d="M16 7.5L20.5 12 16 16.5"/><path d="M13.5 5.5l-3 13"/>',
    ),
    (
        "git-branch",
        "code",
        ["repo", "branch", "version", "vcs"],
        '<circle cx="7" cy="6" r="2.25"/><circle cx="7" cy="18" r="2.25"/><circle cx="17" cy="9" r="2.25"/>'
        '<path d="M7 8.5v7"/><path d="M17 11.5v1a4.5 4.5 0 0 1-4.5 4.5H9.5"/>',
    ),
    (
        "diff",
        "code",
        ["compare", "patch", "changes", "plus-minus"],
        '<rect x="3.5" y="3.5" width="17" height="17" rx="1"/>'
        '<path d="M12 7.25v4.5"/><path d="M9.75 9.5h4.5"/><path d="M9.75 15.75h4.5"/>',
    ),
    (
        "package",
        "code",
        ["release", "crate", "pwn-shop", "artifact"],
        '<path d="M12 3L20 7.5v9L12 21 4 16.5v-9L12 3z"/>'
        '<path d="M4 7.5L12 12l8-4.5"/><path d="M12 12v9"/><path d="M8 5.25l8 4.5"/>',
    ),
    (
        "book",
        "code",
        ["docs", "manual", "playbook", "guide"],
        '<path d="M3.5 5h6.5a2 2 0 0 1 2 2v12.5a1.5 1.5 0 0 0-1.5-1.5h-7V5z"/>'
        '<path d="M20.5 5H14a2 2 0 0 0-2 2v12.5a1.5 1.5 0 0 1 1.5-1.5h7V5z"/>',
    ),

    # ---- 4. Security & System (10) ----
    (
        "shield",
        "security",
        ["privacy", "local", "protect", "firewall"],
        '<path d="M12 3.25L19.5 6v6c0 4.6-3.1 7.7-7.5 9.25C7.6 19.7 4.5 16.6 4.5 12V6L12 3.25z"/>',
    ),
    (
        "shield-check",
        "security",
        ["verified", "sha256", "signed", "trusted"],
        '<path d="M12 3.25L19.5 6v6c0 4.6-3.1 7.7-7.5 9.25C7.6 19.7 4.5 16.6 4.5 12V6L12 3.25z"/>'
        '<path d="M8.75 12.25l2.25 2.25 4.5-4.75"/>',
    ),
    (
        "lock",
        "security",
        ["private", "encrypted", "mtls", "secure"],
        '<rect x="5" y="10.5" width="14" height="9.5" rx="1"/>'
        '<path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="M12 14v2.5"/>',
    ),
    (
        "unlock",
        "security",
        ["open", "public", "access"],
        '<rect x="5" y="10.5" width="14" height="9.5" rx="1"/>'
        '<path d="M8 10.5V7.5a4 4 0 0 1 7.7-1.5"/><path d="M12 14v2.5"/>',
    ),
    (
        "key",
        "security",
        ["token", "auth", "credentials", "passphrase"],
        '<circle cx="7.75" cy="12" r="3.75"/><path d="M11.5 12H20.5"/><path d="M17 12v3"/><path d="M20 12v2.25"/>',
    ),
    (
        "certificate",
        "security",
        ["certapi", "x509", "store", "badge"],
        '<path d="M12 16.5H3.5V4.5h17v6.25"/>'
        '<path d="M7 8.5h7.5"/><path d="M7 12h4"/>'
        '<circle cx="16.5" cy="14" r="2.75"/>'
        '<path d="M15 16.5V21l1.5-1.15L18 21v-4.5"/>',
    ),
    (
        "eye",
        "security",
        ["view", "preview", "visible", "inspect"],
        '<path d="M2.5 12S6 6.25 12 6.25 21.5 12 21.5 12 18 17.75 12 17.75 2.5 12 2.5 12z"/>'
        '<circle cx="12" cy="12" r="2.75"/>',
    ),
    (
        "eye-off",
        "security",
        ["hide", "mask", "redact", "secret"],
        '<path d="M3.5 3.5l17 17"/>'
        '<path d="M10.2 6.45A10 10 0 0 1 12 6.25C18 6.25 21.5 12 21.5 12a16.5 16.5 0 0 1-3.1 3.7"/>'
        '<path d="M6.4 8.2A16.5 16.5 0 0 0 2.5 12s3.5 5.75 9.5 5.75a10 10 0 0 0 3.7-.7"/>',
    ),
    (
        "cpu",
        "security",
        ["hardware", "local", "rust", "native", "chip"],
        '<rect x="6.5" y="6.5" width="11" height="11"/>'
        '<rect x="10" y="10" width="4" height="4"/>'
        '<path d="M9 3.5v3M15 3.5v3M9 17.5v3M15 17.5v3M3.5 9h3M3.5 15h3M17.5 9h3M17.5 15h3"/>',
    ),
    (
        "settings",
        "security",
        ["gear", "config", "preferences", "options"],
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M10.4 3.25h3.2l.55 2.1 1.65.7 1.85-1.05 2.25 2.25-1.05 1.85.7 1.65 2.1.55v3.2l-2.1.55-.7 1.65 1.05 1.85-2.25 2.25-1.85-1.05-1.65.7-.55 2.1h-3.2l-.55-2.1-1.65-.7-1.85 1.05-2.25-2.25 1.05-1.85-.7-1.65-2.1-.55v-3.2l2.1-.55.7-1.65-1.05-1.85 2.25-2.25 1.85 1.05 1.65-.7.55-2.1z"/>',
    ),

    # ---- 5. Network, Media & Tools (10) ----
    (
        "globe",
        "tools",
        ["web", "browser", "offline", "dns"],
        '<circle cx="12" cy="12" r="8.5"/>'
        '<ellipse cx="12" cy="12" rx="3.75" ry="8.5"/><path d="M3.75 12h16.5"/>',
    ),
    (
        "wifi",
        "tools",
        ["network", "signal", "vpn", "port"],
        '<path d="M3.5 9a12.5 12.5 0 0 1 17 0"/>'
        '<path d="M6.8 12.5a8 8 0 0 1 10.4 0"/>'
        '<path d="M10.1 16a3.2 3.2 0 0 1 3.8 0"/>'
        '<rect x="11.15" y="18.25" width="1.7" height="1.7" fill="currentColor" stroke="none"/>',
    ),
    (
        "server",
        "tools",
        ["daemon", "localhost", "host", "node"],
        '<rect x="3.5" y="4" width="17" height="6.5" rx="1"/>'
        '<rect x="3.5" y="13.5" width="17" height="6.5" rx="1"/>'
        '<rect x="6.25" y="6.35" width="1.8" height="1.8" fill="currentColor" stroke="none"/>'
        '<rect x="6.25" y="15.85" width="1.8" height="1.8" fill="currentColor" stroke="none"/>'
        '<path d="M11 7.25h6M11 16.75h6"/>',
    ),
    (
        "link",
        "tools",
        ["url", "chain", "connect", "anchor"],
        '<path d="M9.5 14.5l5-5"/>'
        '<path d="M11.5 7.5l1.75-1.75a3.5 3.5 0 0 1 5 5L16.5 12.5"/>'
        '<path d="M12.5 16.5l-1.75 1.75a3.5 3.5 0 0 1-5-5L7.5 11.5"/>',
    ),
    (
        "capture",
        "tools",
        ["screenshot", "screen-mark", "crop", "crosshair"],
        '<path d="M4 8.5V4h4.5M15.5 4H20v4.5M20 15.5V20h-4.5M8.5 20H4v-4.5"/>'
        '<circle cx="12" cy="12" r="2.75"/>',
    ),
    (
        "image",
        "tools",
        ["png", "svg", "photo", "cover", "artwork"],
        '<rect x="3.5" y="4.5" width="17" height="15" rx="1"/>'
        '<path d="M4 16.5l5-5 3.5 3.5 2.5-2.5 5 4"/>'
        '<circle cx="9" cy="9" r="1.25"/>',
    ),
    (
        "video",
        "tools",
        ["carify", "ffmpeg", "usb", "media", "encode"],
        '<rect x="3" y="6" width="13" height="12" rx="1"/>'
        '<path d="M16 10l5-3v10l-5-3"/>',
    ),
    (
        "play",
        "tools",
        ["start", "run", "replay", "motion"],
        '<path d="M7 5l12 7-12 7V5z"/>',
    ),
    (
        "pause",
        "tools",
        ["stop", "freeze", "wcag", "board"],
        '<rect x="6" y="5" width="4" height="14"/><rect x="14" y="5" width="4" height="14"/>',
    ),
    (
        "volume",
        "tools",
        ["audio", "aac", "sound", "speaker"],
        '<path d="M4 9.5h4l5-4.5v14l-5-4.5H4V9.5z"/>'
        '<path d="M16.5 9a4.5 4.5 0 0 1 0 6"/><path d="M19.2 6.5a8 8 0 0 1 0 11"/>',
    ),

    # ---- 6. Status, Theme & Time (10) ----
    (
        "check-circle",
        "status",
        ["ok", "success", "synced", "pass"],
        '<circle cx="12" cy="12" r="8.5"/><path d="M8.5 12.25l2.25 2.25 4.75-5"/>',
    ),
    (
        "alert-triangle",
        "status",
        ["warn", "warning", "caution", "destructive"],
        '<path d="M12 4L21 19.5H3L12 4z"/><path d="M12 10v4"/>'
        '<rect x="11.15" y="16" width="1.7" height="1.7" fill="currentColor" stroke="none"/>',
    ),
    (
        "x-circle",
        "status",
        ["error", "fail", "fault", "blocked"],
        '<circle cx="12" cy="12" r="8.5"/><path d="M9 9l6 6"/><path d="M15 9l-6 6"/>',
    ),
    (
        "info",
        "status",
        ["note", "help", "details", "stdout"],
        '<circle cx="12" cy="12" r="8.5"/><path d="M12 11.25V16"/>'
        '<rect x="11.15" y="7.75" width="1.7" height="1.7" fill="currentColor" stroke="none"/>',
    ),
    (
        "sun",
        "status",
        ["light", "day", "lx512", "alabaster"],
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M18.4 5.6L17 7M7 17l-1.4 1.4"/>',
    ),
    (
        "moon",
        "status",
        ["dark", "night", "lx263", "blackout"],
        '<path d="M19.5 14.25A7.75 7.75 0 0 1 9.75 4.5a8 8 0 1 0 9.75 9.75z"/>',
    ),
    (
        "clock",
        "status",
        ["time", "timer", "dwell", "schedule", "interval"],
        '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3.25 2"/>',
    ),
    (
        "calendar",
        "status",
        ["date", "changelog", "release", "orders"],
        '<rect x="3.5" y="5" width="17" height="15.5" rx="1"/>'
        '<path d="M3.5 9.5h17"/><path d="M8 3.25V6.5M16 3.25V6.5"/>',
    ),
    (
        "bell",
        "status",
        ["notify", "alert", "webhook", "status"],
        '<path d="M6 16.5V10a6 6 0 0 1 12 0v6.5L20 18.5H4l2-2z"/><path d="M10 18.5a2 2 0 0 0 4 0"/>',
    ),
    (
        "pin",
        "status",
        ["featured", "fixed", "bookmark", "lock"],
        '<path d="M8.5 4h7v2L14 7.75v3.5l2.75 2.75H7.25L10 11.25v-3.5L8.5 6V4z"/><path d="M12 14v6.25"/>',
    ),
]


def make_standalone_svg(inner):
    return f'<svg xmlns="http://www.w3.org/2000/svg" {SVG_ATTRS}>{inner}</svg>\n'


def build_sprite():
    grad = (
        '  <defs>\n'
        '    <linearGradient id="rfs-icon-grad-horizon" gradientUnits="userSpaceOnUse" x1="2" y1="22" x2="22" y2="2">\n'
        '      <stop offset="0%" stop-color="#74B8E8"/>\n'
        '      <stop offset="52%" stop-color="#1F547A"/>\n'
        '      <stop offset="100%" stop-color="#F06E2B"/>\n'
        '    </linearGradient>\n'
        '  </defs>\n'
    )
    symbols = []
    for name, _, _, inner in ICONS:
        symbols.append(f'  <symbol id="rfs-i-{name}" {SVG_ATTRS}>{inner}</symbol>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
        + grad
        + "\n".join(symbols)
        + "\n</svg>\n"
    )


def render_preview(preview_dir):
    try:
        import resvg_py
        from PIL import Image, ImageDraw
    except ImportError as e:
        sys.exit(f"preview requires resvg-py and pillow: {e}")

    os.makedirs(preview_dir, exist_ok=True)
    cols = 10
    rows = (len(ICONS) + cols - 1) // cols
    cell_w, cell_h = 136, 120
    pad = 24
    w = cols * cell_w + pad * 2
    h = rows * cell_h + pad * 2 + 40

    for mode, bg, card, border, ink, sub in (
        ("dark", (5, 5, 7), (12, 12, 16), (42, 43, 50), "#F4F5F8", (179, 181, 192)),
        ("light", (245, 247, 249), (255, 255, 255), (207, 213, 220), "#0D1016", (71, 77, 89)),
    ):
        sheet = Image.new("RGB", (w, h), bg)
        draw = ImageDraw.Draw(sheet)
        draw.text(
            (pad, 14),
            f"RFS Cyclorama Precision Silkscreen Icons ({len(ICONS)} icons · 24px grid · 1.75px stroke · {mode})",
            fill=sub,
        )
        for idx, (name, cat, _, inner) in enumerate(ICONS):
            r, c = divmod(idx, cols)
            x0 = pad + c * cell_w + 4
            y0 = pad + 32 + r * cell_h + 4
            x1 = x0 + cell_w - 8
            y1 = y0 + cell_h - 8
            draw.rounded_rectangle((x0, y0, x1, y1), radius=6, fill=card, outline=border, width=1)

            svg_str = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
                f'fill="none" stroke="{ink}" stroke-width="1.75" '
                f'stroke-linecap="square" stroke-linejoin="miter">{inner.replace("currentColor", ink)}</svg>'
            )
            # Render large 40px inspection + real-size 20px side-by-side
            big_bytes = bytes(resvg_py.svg_to_bytes(svg_string=svg_str, width=40, skip_system_fonts=True))
            sm_bytes = bytes(resvg_py.svg_to_bytes(svg_string=svg_str, width=20, skip_system_fonts=True))
            import io
            big_im = Image.open(io.BytesIO(big_bytes)).convert("RGBA")
            sm_im = Image.open(io.BytesIO(sm_bytes)).convert("RGBA")
            sheet.paste(big_im, (x0 + 22, y0 + 20), big_im)
            sheet.paste(sm_im, (x0 + 80, y0 + 30), sm_im)
            draw.text((x0 + 10, y1 - 24), name, fill=sub)

        out_path = os.path.join(preview_dir, f"rfs-icons-contact-{mode}.png")
        sheet.save(out_path)
        print(f"wrote preview {out_path}")


def main():
    ap = argparse.ArgumentParser(description="Generate the 60-icon RFS Cyclorama Dawn SVG library.")
    ap.add_argument("--preview", metavar="DIR", help="Render dark & light QA contact sheets into DIR")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    # Clean stale .svg files that are no longer in ICONS
    expected = {f"{n}.svg" for n, _, _, _ in ICONS} | {"rfs-icons.svg"}
    for fn in os.listdir(OUT_DIR):
        if fn.endswith(".svg") and fn not in expected:
            os.remove(os.path.join(OUT_DIR, fn))

    manifest = []
    for name, cat, tags, inner in ICONS:
        p = os.path.join(OUT_DIR, f"{name}.svg")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(make_standalone_svg(inner))
        manifest.append({"name": name, "category": cat, "tags": tags, "inner": inner})

    sprite_path = os.path.join(OUT_DIR, "rfs-icons.svg")
    with open(sprite_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build_sprite())

    json_path = os.path.join(OUT_DIR, "icons.json")
    with open(json_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(
            {
                "meta": {
                    "count": len(ICONS),
                    "grid": 24,
                    "strokeWidth": 1.75,
                    "linecap": "square",
                    "linejoin": "miter",
                },
                "icons": manifest,
            },
            fh,
            indent=2,
        )
        fh.write("\n")

    print(f"wrote {len(ICONS)} icons + rfs-icons.svg + icons.json -> {OUT_DIR}")
    if args.preview:
        render_preview(args.preview)


if __name__ == "__main__":
    main()
