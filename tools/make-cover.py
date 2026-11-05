#!/usr/bin/env python3
"""Generate an RFS repo cover and GitHub social preview from one cover.toml.

usage:
    python3 make-cover.py <path/to/cover.toml> [--out DIR] [--preview FILE] [--layout v1|v2]

Writes, next to cover.toml unless --out is given:
    cover-dark.svg   cover-light.svg     1200x560  README header (<picture>), animated once
    cover-dark.png   cover-light.png     1200x560  docs site og:image (the finished frame)
    social-dark.png  social-light.png    1280x640  Settings > Social preview
--preview FILE also writes one PNG that shows the cover at 1200, 830 and 400 px
wide in both themes, plus the social card at 400: the sizes people actually
see it at (README, Slack/Discord/X cards). Judge covers there, not at 1200.

Layout v2 (the default; BRAND.md section 7), built to be read at 400 px wide:
    left   the repo name, as big as the column allows (Plex Mono 600, up to
           120 px; long hyphenated names break at a hyphen onto two lines),
           the Ember rule, and the README one-liner (Plex Sans 600 30/38, up
           to two lines). No bullets: they don't survive a social card.
    right  the panel, 528x448: the one thing that shows what the tool does.
    bottom-left corner  RFS tile + REAL-FRUIT-SNACKS label
Layout v1 (layout = "v1" in cover.toml, or --layout v1) is the old cover:
name, rule, description, up to 4 bullets, and a 480x368 panel. It renders
exactly as before, so a repo can move to v2 when its cover.toml does.

Motion (BRAND.md section 8). The SVGs play once on load: the Ember rule
draws in under the name (every cover), a flow's connector draws in the same
way and its status lines print, and a terminal types its command at the type
rate, prints its lines 150 ms apart, and its cursor blinks twice and stays.
A flow takes 1.2 s; a cover may take up to 3.5 s, and the tool refuses one
that runs longer. All of it sits inside
@media (prefers-reduced-motion: no-preference), but browsers don't always
apply that query to an SVG shown through <img>, so the motion is kept safe
without it: one shot, nothing loops or flashes, nothing large moves. The
styles outside the media query are the finished frame, which is what the PNGs,
the social preview and any static renderer show.

All text is converted to outlines, so the SVGs render the same on GitHub,
in browsers and in image viewers without the fonts installed.

Requires Python 3.11+, fonttools and resvg-py (pip install fonttools resvg-py;
cairosvg also works for the cover PNGs), pillow for --preview, and the four
IBM Plex files in tools/fonts/ (OFL, see fonts/OFL.txt).

cover.toml (v2):

    name        = "port-sync"                          # repo name, as on GitHub
    description = "Keeps qBittorrent's port synced to Proton VPN"   # README line 1

    [panel]
    kind   = "flow"                                    # input -> the tool -> output
    status = ["ok listening port updated: 49160 -> 48213"]   # 0-2 lines, as in a terminal

    [panel.input]                                      # what goes in
    label = "Proton VPN"                               # Plex Sans 600
    note  = "forwarded port"                           # optional, muted mono
    value = "48213"                                    # big mono value, or:
    # chips = ["HEVC 10-bit", "1080p", "AC3 5.1"]      #   up to 3 short chips
    tone  = "amber"                                    # text | mute | amber | mint | fault

    [panel.tool]                                       # the repo's tool, on the connector
    label = "port-sync"
    note  = "every 15 s"

    [panel.output]                                     # what comes out; same keys as input
    label = "qBittorrent"
    note  = "listening port"
    value = "48213"
    tone  = "mint"

    # or a short terminal: the command and the lines that matter, 6 at most
    [panel]
    kind  = "terminal"                                 # the default
    title = "pwsh"                                     # optional window title
    lines = ["$ .\\scripts\\install-windows.ps1", "ok done. open a new terminal"]

    # or the tool's own drawing
    [panel]
    kind = "art"
    file = "cover-art.svg"                             # see "Art files" below
    # viewbox = "0 0 480 368"                          # scale an older drawing to fit

    # or a screenshot per theme, cropped to the part that reads at 400px
    [panel]
    kind = "screenshot"
    file = "cover-shot-{theme}.png"                    # {theme} is dark or light; PNG or JPEG
    crop = [4, 182, 546, 532]                          # x, y, width, height in image pixels
    fit  = "contain"                                   # or "cover" (the default: fill, trim)

Status and terminal lines: the prefix picks the colour and isn't drawn, so the
words must say what happened (BRAND.md section 9): "$ " a command (Ember
prompt), "ok " Mint, "! " Amber, "x " Raspberry (a failure), anything else
muted output. Mint is only ever "it worked"; pair it with a word that says so.
A terminal sizes its type from 26 down to 22px to fit the longest line
(about 35 characters, prompt included); a real line isn't reworded to fit.

templates/repo/cover.toml documents every field. Layout v1's fields (bullets,
and a 12-line terminal) still work with layout = "v1".

Art files: plain SVG elements (no <svg> wrapper) drawn in a 528x448 box (v1:
480x368) with its origin at the panel's top-left corner; they are clipped to
the panel's rounded rectangle. Write colours as {token} and they are filled in per theme
(tokens: every key in brand/tokens/rfs.tokens.json, with primary/accent/signal
 also as ember/amber/mint, plus tile, dots, desk, window, scrim, on-ember and
 the annotation inks ink-red, ink-blue, ink-green, ink-yellow, ink-mauve, ink-on).
Text goes in <rfs-text> and is outlined:
    <rfs-text font="mono" size="12" x="40" y="20" anchor="start" fill="{text}">300 x 186</rfs-text>
    font: mono | mono-semibold | sans | sans-semibold;  anchor: start | middle | end
    optional ls="1.5" (letter spacing, px). Elements after a <rfs-unclip/> line
    are drawn on top without the panel clip (selection handles that overhang).
"""
import argparse, json, math, os, re, sys, tomllib
from xml.sax.saxutils import escape

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
except ImportError as e:  # pragma: no cover
    sys.exit(f"missing dependency ({e.name}): pip install fonttools resvg-py")


def render_png(svg, path, width=None):
    """SVG -> PNG. resvg-py has wheels for Windows/macOS/Linux with no system
    libraries; cairosvg is used if that's what's installed."""
    try:
        import resvg_py
        kw = {"width": width} if width else {}
        open(path, "wb").write(bytes(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True, **kw)))
        return
    except ImportError:
        pass
    try:
        import cairosvg
    except ImportError:
        sys.exit("no PNG renderer: pip install resvg-py  (or cairosvg)")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path, output_width=width)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_FILES = {
    "mono": "IBMPlexMono-Regular.ttf",
    "mono-semibold": "IBMPlexMono-SemiBold.ttf",
    "sans": "IBMPlexSans-Regular.ttf",
    "sans-semibold": "IBMPlexSans-SemiBold.ttf",
}
_fonts = {}


def font(name):
    if name not in _fonts:
        if name not in FONT_FILES:
            sys.exit(f"unknown font '{name}' (use {', '.join(FONT_FILES)})")
        _fonts[name] = TTFont(os.path.join(HERE, "fonts", FONT_FILES[name]))
    return _fonts[name]


# Brand colours come from brand/tokens/rfs.tokens.json (BRAND.md section 2), so
# a palette change there reaches every cover on the next run. The entries below
# are the cover's own: tile, dot grid, glow, and the panel's desktop/window/scrim.
THEMES = {
    "dark": {
        "tile": "#1A1D24", "tile-fg": "#FFFFFF", "on-ember": "#0C0D10",
        "dots": "#1E222B", "glow": "rgba(255,106,61,.18)",
        "desk": "#2A2F38", "window": "#3A4050", "scrim": "rgba(12,13,16,.62)",
    },
    "light": {
        "tile": "#1A1B1E", "tile-fg": "#FFFFFF", "on-ember": "#FFFFFF",
        "dots": "#DDD9D1", "glow": "rgba(0,0,0,0)",   # glow is Nightshift-only
        "desk": "#DDD9D1", "window": "#FFFFFF", "scrim": "rgba(26,27,30,.42)",
    },
}
TOKENS = os.path.join(HERE, "..", "brand", "tokens", "rfs.tokens.json")
ALIASES = {"primary": "ember", "accent": "amber", "signal": "mint"}
try:
    _alltok = json.load(open(TOKENS, encoding="utf-8"))
    _tok = _alltok["color"]
except (OSError, KeyError, ValueError) as e:
    sys.exit(f"can't read brand colours from {TOKENS}: {e}")
for _theme, _shift in (("dark", "nightshift"), ("light", "dayshift")):
    for k, v in _tok[_shift].items():
        THEMES[_theme][k] = v
        if k in ALIASES:
            THEMES[_theme][ALIASES[k]] = v
# Annotation inks are the same in both themes (they're drawn on a capture).
INKS = {"ink-red": "#FF6E7A", "ink-blue": "#5CB8FF", "ink-green": "#3DDC97",
        "ink-yellow": "#FFC247", "ink-mauve": "#B78CFF", "ink-on": "#0C0D10"}
for t in THEMES.values():
    t.update(INKS)

# Motion tokens (BRAND.md section 8), read from the same file.
_mot = _alltok.get("motion", {})
EASE = _mot.get("ease", "cubic-bezier(.2, .7, .2, 1)").replace(" ", "")
DUR_SLOW = float(_mot.get("dur-slow", "600ms").rstrip("ms")) / 1000
TYPE_RATE = float(_mot.get("type-rate", "45ms").rstrip("ms")) / 1000
LINE_GAP = 0.15             # s between printed lines (BRAND: 100-200ms)
BLINK = 0.25                # s per half blink: two blinks take 1 s, 2 flashes a second
COVER_MOTION_MAX = 3.5      # s; a cover's whole entrance (BRAND.md section 8)

W, H = 1200, 560            # cover
SW, SH = 1280, 640          # social preview; cover is centred in it
# v1 layout
LEFT = 88                   # left column x
COL_W = 500                 # left column width (panel starts at 640)
PX, PY, PW, PH = 640, 96, 480, 368   # panel


# ---------------------------------------------------------------- text
def glyphs(f, text):
    cmap = f.getBestCmap()
    missing = [ch for ch in text if ord(ch) not in cmap]
    if missing:
        sys.exit(f"font {f['name'].getDebugName(4)} has no glyph for {''.join(missing)!r} in {text!r}")
    return [cmap[ord(ch)] for ch in text]


def advance(fname, text, size, ls=0.0):
    f = font(fname); gs = f.getGlyphSet(); k = size / f["head"].unitsPerEm
    names = glyphs(f, text)
    return sum(gs[n].width * k for n in names) + ls * max(len(names) - 1, 0)


def text_path(fname, text, x, y, size, ls=0.0, anchor="start"):
    """SVG path data for text with its baseline at y."""
    f = font(fname); gs = f.getGlyphSet(); k = size / f["head"].unitsPerEm
    names = glyphs(f, text)
    total = advance(fname, text, size, ls)
    px = {"start": x, "middle": x - total / 2, "end": x - total}[anchor]
    out = []
    for n in names:
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, px, y)))
        out.append(pen.getCommands())
        px += gs[n].width * k + ls
    return " ".join(c for c in out if c)


def text_el(fname, text, x, y, size, fill, ls=0.0, anchor="start"):
    d = text_path(fname, text, x, y, size, ls, anchor)
    return f'<path d="{d}" fill="{fill}"/>' if d else ""


def ink_extent(text, size, ls):
    """Left and right edges of the inked part of `text` in Mono 600, relative to
    the text origin (side bearings excluded)."""
    f = font("mono-semibold"); gs = f.getGlyphSet(); k = size / f["head"].unitsPerEm
    px, left, right = 0.0, None, 0.0
    for n in glyphs(f, text):
        bp = BoundsPen(gs); gs[n].draw(bp)
        if bp.bounds:
            if left is None:
                left = px + bp.bounds[0] * k
            right = px + bp.bounds[2] * k
        px += gs[n].width * k + ls
    return left or 0.0, right


def ink_box(fname, text, size, ls=0.0):
    """(left, top, right, bottom) of the inked part of `text`, relative to its
    origin on the baseline; y grows downward, so top is negative."""
    f = font(fname); gs = f.getGlyphSet(); k = size / f["head"].unitsPerEm
    px, box = 0.0, None
    for n in glyphs(f, text):
        bp = BoundsPen(gs); gs[n].draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            b = (px + x0 * k, -y1 * k, px + x1 * k, -y0 * k)
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]),
                                         max(box[2], b[2]), max(box[3], b[3]))
        px += gs[n].width * k + ls
    return box or (0.0, 0.0, 0.0, 0.0)


def descender(size):
    """Depth of Plex Mono 600's descenders (the 'p') at this size."""
    f = font("mono-semibold"); gs = f.getGlyphSet()
    bp = BoundsPen(gs); gs[f.getBestCmap()[ord("p")]].draw(bp)
    return -bp.bounds[1] * size / f["head"].unitsPerEm


def wrap(fname, text, size, width, max_lines, what):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if advance(fname, trial, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines or any(advance(fname, l, size) > width for l in lines):
        sys.exit(f"{what} doesn't fit in {max_lines} line(s) of {width}px: {text!r}")
    return lines


def wrap_balanced(fname, text, size, width, what):
    """One line if it fits; otherwise the two-line break with the most even
    lines, so the second line is never a lone word or two."""
    if advance(fname, text, size) <= width:
        return [text]
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wa, wb = advance(fname, a, size), advance(fname, b, size)
        if max(wa, wb) <= width and (best is None or max(wa, wb) < best[0]):
            best = (max(wa, wb), [a, b])
    if best is None:
        sys.exit(f"{what} doesn't fit in 2 lines of {width}px: {text!r}")
    return best[1]


# ---------------------------------------------------------------- panels
def panel_terminal(cfg, c):
    title = cfg.get("title", "")
    lines = cfg.get("lines") or []
    if len(lines) > 12:
        sys.exit("terminal panel: at most 12 lines")
    o = [f'<rect width="{PW}" height="{PH}" fill="{c["code-bg"]}"/>',
         f'<rect width="{PW}" height="34" fill="{c["surface"]}"/>',
         f'<rect y="34" width="{PW}" height="1" fill="{c["line"]}"/>']
    for i in range(3):
        o.append(f'<circle cx="{20 + i * 16}" cy="17" r="4.5" fill="{c["line"]}"/>')
    if title:
        o.append(text_el("mono", title, PW / 2, 21.5, 12, c["mute"], 0.5, "middle"))
    size, lh, x, y = 14, 26, 24, 70
    maxw = PW - 2 * x
    for ln in lines:
        if ln.startswith("$ "):
            o.append(text_el("mono-semibold", "$", x, y, size, c["ember"]))
            body, fill, fname, bx = ln[2:], c["text"], "mono", x + advance("mono", "$ ", size)
        elif ln.startswith("ok "):
            body, fill, fname, bx = ln[3:], c["mint"], "mono", x
        elif ln.startswith("! "):
            body, fill, fname, bx = ln[2:], c["amber"], "mono", x
        elif ln.startswith("x "):
            body, fill, fname, bx = ln[2:], c["fault"], "mono", x
        else:
            body, fill, fname, bx = ln, c["mute"], "mono", x
        if advance(fname, body, size) > maxw - (bx - x):
            sys.exit(f"terminal line too long for the panel (max ~{int(maxw / 8.4)} chars): {ln!r}")
        if body:
            o.append(text_el(fname, body, bx, y, size, fill))
        y += lh
    # cursor after the last line
    o.append(f'<rect x="{x}" y="{y - 13}" width="8" height="16" fill="{c["ember"]}"/>')
    return "\n".join(o), ""


RFS_TEXT = re.compile(r"<rfs-text\b([^>]*)>(.*?)</rfs-text>", re.S)
ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def panel_art(cfg, c, base):
    p = os.path.join(base, cfg.get("file", "cover-art.svg"))
    try:
        src = open(p, encoding="utf-8").read()
    except OSError as e:
        sys.exit(f"art file: {e}")
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)

    def rt(m):
        a = dict(ATTR.findall(m.group(1)))
        fill = a.get("fill", "{text}")
        return text_el(a.get("font", "mono"), m.group(2).strip("\r\n"), float(a.get("x", 0)),
                       float(a.get("y", 0)), float(a.get("size", 12)), fill,
                       float(a.get("ls", 0)), a.get("anchor", "start"))
    src = RFS_TEXT.sub(rt, src)

    def tok(m):
        k = m.group(1)
        if k not in c:
            sys.exit(f"art file: unknown colour token {{{k}}} (have: {', '.join(sorted(c))})")
        return c[k]
    src = re.sub(r"\{([a-z][a-z0-9-]*)\}", tok, src)
    clipped, _, top = src.partition("<rfs-unclip/>")
    return clipped.strip(), top.strip()


def panel_screenshot(cfg, theme, base):
    import base64
    name = cfg.get("file", "cover-shot-{theme}.png").replace("{theme}", theme)
    p = os.path.join(base, name)
    try:
        data = open(p, "rb").read()
    except OSError as e:
        sys.exit(f"screenshot: {e}")
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        mime = "image/png"
    elif data[:3] == b"\xff\xd8\xff":
        mime = "image/jpeg"
    else:
        sys.exit(f"screenshot: {name} is not a PNG or JPEG")
    uri = f"data:{mime};base64,{base64.b64encode(data).decode()}"
    return (f'<image href="{uri}" x="0" y="0" width="{PW}" height="{PH}" '
            f'preserveAspectRatio="xMidYMin slice"/>'), ""


# ---------------------------------------------------------------- compose (v1)
def compose_v1(cfg, theme, base, social=False):
    c = THEMES[theme]
    name = cfg["name"]; desc = cfg["description"]; bullets = cfg.get("bullets", [])
    if len(bullets) > 4:
        sys.exit("at most 4 bullets")
    o = []

    # repo name: Mono 600, 70px, -0.05em; shrinks (to 44px) before it refuses
    size = 70
    while advance("mono-semibold", name, size, -0.05 * size) > COL_W and size > 44:
        size -= 2
    if advance("mono-semibold", name, size, -0.05 * size) > COL_W:
        sys.exit(f"name too long for the cover: {name!r}")
    # left column, built from baseline 0, then centred on the panel's middle
    col = []
    top = -0.74 * size                       # cap/ascender height of Plex Mono
    col.append(text_el("mono-semibold", name, LEFT, 0, size, c["text"], -0.05 * size))
    # Ember rule under the whole name, 7px below the descender line, so it sits
    # at the same height on every cover whether or not the name has descenders
    il, ir = ink_extent(name, size, -0.05 * size)
    rule_y = round(descender(size) + 7, 1)
    col.append(f'<rect x="{LEFT + il:.1f}" y="{rule_y:g}" width="{ir - il:.1f}" height="5" rx="2.5" fill="{c["ember"]}"/>')
    y = 64 + (rule_y - 17)
    for ln in wrap("sans-semibold", desc, 24, 410, 2, "description"):
        col.append(text_el("sans-semibold", ln, LEFT, y, 24, c["text"])); y += 32
    bottom = y - 32 + 6                      # descenders of the last line
    y += 18
    for b in bullets:
        if advance("sans", b, 15) > COL_W - 16:
            sys.exit(f"bullet too long: {b!r}")
        col.append(f'<rect x="{LEFT}" y="{y - 9}" width="6" height="6" rx="1" fill="{c["ember"]}"/>')
        col.append(text_el("sans", b, LEFT + 16, y, 15, c["mute"])); bottom = y + 4; y += 26
    shift = PY + PH / 2 - (top + bottom) / 2
    o.append(f'<g transform="translate(0 {shift:.1f})">' + "\n".join(col) + "</g>")

    # panel
    pcfg = cfg.get("panel", {})
    kind = pcfg.get("kind", "terminal")
    if kind == "terminal":
        inner, top = panel_terminal(pcfg, c)
    elif kind == "art":
        inner, top = panel_art(pcfg, c, base)
    elif kind == "screenshot":
        inner, top = panel_screenshot(pcfg, theme, base)
    else:
        sys.exit(f"panel kind must be 'terminal', 'art' or 'screenshot', not {kind!r}")
    o.append(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="10" fill="{c["desk"]}"/>')
    o.append(f'<g transform="translate({PX} {PY})"><g clip-path="url(#m)">{inner}</g>{top}</g>')
    o.append(f'<rect x="{PX + .5}" y="{PY + .5}" width="{PW - 1}" height="{PH - 1}" rx="9.5" fill="none" stroke="{c["line"]}"/>')

    fw, fh = (SW, SH) if social else (W, H)
    dx, dy = ((SW - W) / 2, (SH - H) / 2) if social else (0, 0)
    label = escape(f"{name}: {desc.rstrip('.')}", {'"': "&quot;"})
    defs = (f'<defs><pattern id="g" width="26" height="26" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.2" cy="1.2" r="1.2" fill="{c["dots"]}"/></pattern>'
            f'<radialGradient id="r" cx="78%" cy="110%" r="70%"><stop offset="0" stop-color="{c["glow"]}"/>'
            f'<stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient>'
            f'<clipPath id="c"><rect width="{fw}" height="{fh}" rx="{0 if social else 12}"/></clipPath>'
            f'<clipPath id="m"><rect width="{PW}" height="{PH}" rx="10"/></clipPath></defs>')
    field = (f'<rect width="{fw}" height="{fh}" fill="{c["bg"]}"/><rect width="{fw}" height="{fh}" fill="url(#g)"/>'
             f'<rect width="{fw}" height="{fh}" fill="url(#r)"/>')
    # RFS tile + org label in the frame's bottom-left corner. The social preview
    # keeps a 40px margin (GitHub crops previews in some places); the cover 32px.
    m = 40 if social else 32
    ts = 40; k = ts / 56; tx, ty = m, fh - m - ts
    mark = (f'<rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="{14 * ts / 64:.2f}" fill="{c["tile"]}"/>'
            + text_el("mono-semibold", "RFS", tx + ts / 2, ty + 37.3 * k, 24.5 * k, c["tile-fg"], -1.17 * k, "middle")
            + f'<rect x="{tx + 12.25 * k:.2f}" y="{ty + 42 * k:.2f}" width="{31.5 * k:.2f}" height="{3.5 * k:.2f}" rx="{1.75 * k:.2f}" fill="{c["ember"]}"/>'
            + text_el("mono", "REAL-FRUIT-SNACKS", tx + ts + 14, ty + ts / 2 + 4, 11, c["mute"], 1.3))
    body = "\n".join(x for x in o if x)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fw} {fh}" width="{fw}" height="{fh}" '
            f'role="img" aria-label="{label}">\n{defs}\n<g clip-path="url(#c)">{field}\n'
            f'<g transform="translate({dx} {dy})">\n{body}\n</g>\n{mark}</g></svg>\n')


# ---------------------------------------------------------------- v2 layout
# One grid for every cover: 72px side margins, a 480px text column, a 48px
# gutter and a 528x448 panel area, centred vertically.
V2_LEFT, V2_COL = 72, 480
V2_PX, V2_PY, V2_PW, V2_PH = 600, 56, 528, 448
NAME_MAX = 120              # px; short names stop growing here
NAME_BREAK = 80             # one-line names smaller than this break at a hyphen
NAME_MIN = 56               # smallest name, one line or two
TRACK = -0.05               # wordmark tracking, em
DESC_SIZE, DESC_LH = 30, 38
TONES = ("text", "mute", "amber", "mint", "fault")


class Motion:
    """Collects the cover's one-shot entrance as CSS. Every rule is emitted
    inside @media (prefers-reduced-motion: no-preference); nothing outside it
    hides or moves anything, so without the query the SVG is the finished
    frame. Each element gets its own class with absolute times, which keeps
    the whole timeline readable in one place."""

    def __init__(self):
        self.rules = []
        self.end = 0.0

    def _cls(self):
        return f"m{len(self.rules)}"

    def draw(self, axis, start, dur=None):
        """Grow an element from its left (x) or top (y) edge, like the rule."""
        dur = DUR_SLOW if dur is None else dur
        cls = self._cls()
        origin = "0 50%" if axis == "x" else "50% 0"
        self.rules.append(f".{cls}{{transform-box:fill-box;transform-origin:{origin};"
                          f"animation:rfs-draw-{axis} {dur:g}s {EASE} {start:g}s both}}")
        self.end = max(self.end, start + dur)
        return cls

    def appear(self, at):
        """Hidden until `at` seconds, then shown at once: a printed line, or a
        typed character."""
        cls = self._cls()
        self.rules.append(f".{cls}{{animation:rfs-hidden {at:.3f}s step-end}}")
        self.end = max(self.end, at)
        return cls

    def typing_cursor(self, shown, hidden, move_at, steps, dist):
        """The cursor while a command types. Its base style is opacity 0 (it
        isn't in the finished frame); here it shows from `shown` to `hidden`
        and steps right one character per type-rate tick from `move_at`."""
        cls = self._cls()
        kf = f"rfs-mv{len(self.rules)}"
        self.rules.append(f"@keyframes {kf}{{to{{transform:translateX({dist:.2f}px)}}}}"
                          f".{cls}{{animation:rfs-shown {hidden - shown:.3f}s step-end {shown:.3f}s,"
                          f"{kf} {steps * TYPE_RATE:.3f}s steps({steps},end) {move_at:.3f}s both}}")
        self.end = max(self.end, hidden)
        return cls

    def cursor_blinks(self, at):
        """The last cursor: appears at `at`, blinks twice, then stays."""
        cls = self._cls()
        self.rules.append(f".{cls}{{animation:rfs-hidden {at:.3f}s step-end,"
                          f"rfs-blink {2 * BLINK:g}s step-end {at:.3f}s 2}}")
        self.end = max(self.end, at + 4 * BLINK)
        return cls

    def css(self):
        if not self.rules:
            return ""
        return ("<style>@media (prefers-reduced-motion:no-preference){"
                "@keyframes rfs-draw-x{from{transform:scaleX(0)}}"
                "@keyframes rfs-draw-y{from{transform:scaleY(0)}}"
                "@keyframes rfs-hidden{from,to{opacity:0}}"
                "@keyframes rfs-shown{from,to{opacity:1}}"
                "@keyframes rfs-blink{0%{opacity:1}50%{opacity:0}}"
                + "".join(self.rules) + "}</style>")


def name_lines(name):
    """Pick one line, or two broken after a hyphen, and the size that fills the
    column. Returns (lines, size)."""
    def unit(lines):   # width of the widest line at 1px, tracking included
        return max(advance("mono-semibold", l, 1, TRACK) for l in lines)
    best = ([name], min(NAME_MAX, V2_COL / unit([name])))
    if best[1] < NAME_BREAK and "-" in name.strip("-"):
        for i, ch in enumerate(name):
            if ch == "-" and 0 < i < len(name) - 1:
                ls = [name[:i + 1], name[i + 1:]]
                s = min(NAME_MAX, V2_COL / unit(ls))
                if s > best[1] * 1.1:
                    best = (ls, s) if len(best[0]) == 1 or s > best[1] else best
    lines, size = best
    size = math.floor(size)
    if size < NAME_MIN:
        sys.exit(f"name too long for the cover even on two lines: {name!r}")
    return lines, size


def status_line(ln, c):
    """A terminal line's colour and body (BRAND.md section 9)."""
    for pre, key in (("ok ", "mint"), ("! ", "amber"), ("x ", "fault")):
        if ln.startswith(pre):
            return ln[len(pre):], c[key]
    return ln, c["mute"]


# Flow panel type, sized so every word still reads with the cover 400px wide
# (a third of these sizes): labels 26, notes 22, tool 24, values 64, status 20-22.
FL_LABEL, FL_NOTE, FL_VALUE, FL_CHIP, FL_TOOL = 26, 22, 64, 22, 24
FL_INSET = 32               # side padding inside the panel
FL_GAP = 16                 # label line to value (or chips)


def flow_end(node, c, cx, y, w, which, below=False):
    """The input or output of a flow: label and note centred on one line, and
    the value (or chips) big. The input reads label then value; the output is
    mirrored, value then label (below=True), so the two values face each
    other across the connector. Drawn from y = its top edge; returns
    (svg, height)."""
    label, note = node.get("label", ""), node.get("note", "")
    value, chips = node.get("value"), node.get("chips")
    tone = node.get("tone", "text")
    if not label:
        sys.exit(f"flow panel: {which} needs a label")
    if tone not in TONES:
        sys.exit(f"flow panel: {which} tone must be one of {', '.join(TONES)}, not {tone!r}")
    if (value is None) == (chips is None):
        sys.exit(f"flow panel: {which} needs a value or chips (one of them)")
    fill, room = c[tone], w - 2 * FL_INSET
    lw = advance("sans-semibold", label, FL_LABEL)
    nw = advance("mono", note, FL_NOTE) if note else 0
    gap = 16 if note else 0
    if lw + gap + nw > room:
        sys.exit(f"flow panel: {which} label and note too long for one line: {label!r} {note!r}")
    cap = 0.698 * FL_LABEL
    head_h = cap + 0.22 * FL_LABEL          # cap height + descenders (the q in qBittorrent)

    def head(y_top):
        hx, L = cx - (lw + gap + nw) / 2, y_top + cap
        return (text_el("sans-semibold", label, hx, L, FL_LABEL, c["text"])
                + (text_el("mono", note, hx + lw + gap, L, FL_NOTE, c["mute"]) if note else ""))

    if value is not None:
        size = FL_VALUE
        while advance("mono-semibold", value, size) > room and size > 40:
            size -= 2
        if advance("mono-semibold", value, size) > room:
            sys.exit(f"flow panel: {which} value too long: {value!r}")
        body_h = 0.698 * size                # figures: cap height, no descenders

        def body(y_top):
            return text_el("mono-semibold", value, cx, y_top + body_h, size, fill, 0, "middle")
    else:
        if not 1 <= len(chips) <= 3:
            sys.exit(f"flow panel: {which} takes 1-3 chips")
        pad, cg, body_h = 14, 10, 44
        ws = [advance("mono", t, FL_CHIP) + 2 * pad for t in chips]
        total = sum(ws) + cg * (len(ws) - 1)
        if total > room:
            sys.exit(f"flow panel: {which} chips too wide ({total:.0f}px of {room}): {chips!r}")

        def body(y_top):
            out, x = [], cx - total / 2
            for t, cw in zip(chips, ws):
                out.append(f'<rect x="{x + .75:.2f}" y="{y_top + .75:.1f}" width="{cw - 1.5:.2f}" height="{body_h - 1.5}" '
                           f'rx="6" fill="{c["raised"]}" stroke="{fill}" stroke-width="1.5"/>')
                out.append(text_el("mono", t, x + cw / 2, y_top + body_h / 2 + 7.5, FL_CHIP, fill, 0, "middle"))
                x += cw + cg
            return "".join(out)
    if below:   # value first, label under it
        svg = body(y) + head(y + body_h + FL_GAP)
    else:
        svg = head(y) + body(y + head_h + FL_GAP - 0.22 * FL_LABEL)
    return svg, head_h + FL_GAP + body_h - (0 if below else 0.22 * FL_LABEL)


def panel_flow(cfg, c, mo, t0):
    """input -> the tool -> output, top to bottom, in one panel. The Ember
    connector runs down the middle behind the tool's pill and draws in like
    the rule; the status lines sit in a log strip along the panel's foot and
    print once the connector arrives. Returns (inner, top) like the v1
    panels, in panel coordinates."""
    for k in ("input", "tool", "output"):
        if not isinstance(cfg.get(k), dict):
            sys.exit(f"flow panel needs a [panel.{k}] table")
    status = cfg.get("status") or []
    if isinstance(status, str):
        status = [status]
    if len(status) > 2:
        sys.exit("flow panel: at most 2 status lines")
    tool = cfg["tool"]
    w, h = V2_PW, V2_PH
    cx = w / 2
    st_lh = 34
    strip = 26 + st_lh * len(status) if status else 0
    o = [f'<rect width="{w}" height="{h}" fill="{c["surface"]}"/>']
    # measure both ends, then share the space above the strip out: equal room
    # above the input and below the output, the rest for the connector
    _, h_in = flow_end(cfg["input"], c, cx, 0, w, "input")
    _, h_out = flow_end(cfg["output"], c, cx, 0, w, "output", below=True)
    pill_h, edge = 46, 28          # tool pill; room above the input / below the output
    mid = (h - strip) - 2 * edge - h_in - h_out
    if mid < pill_h + 2 * 36:
        sys.exit("flow panel: too much in it; drop a status line or use a value instead of chips")
    y_in = edge
    y_out = y_in + h_in + mid
    # connector: one bar from under the input to the arrowhead over the output
    bar_w, head_w, head_h = 4, 18, 13
    y0, y1 = y_in + h_in + 14, y_out - 12
    o.append(f'<rect class="{mo.draw("y", t0)}" x="{cx - bar_w / 2}" y="{y0:.1f}" width="{bar_w}" '
             f'height="{y1 - head_h + 1 - y0:.1f}" fill="{c["ember"]}"/>')
    o.append(f'<path class="{mo.appear(t0 + DUR_SLOW * 0.8)}" d="M{cx - head_w / 2} {y1 - head_h:.1f} '
             f'H{cx + head_w / 2} L{cx} {y1:.1f} Z" fill="{c["ember"]}"/>')
    o.append(flow_end(cfg["input"], c, cx, y_in, w, "input")[0])
    o.append(flow_end(cfg["output"], c, cx, y_out, w, "output", below=True)[0])
    # the tool: a pill on the connector, name and note
    tl, tn = tool.get("label", ""), tool.get("note", "")
    if not tl:
        sys.exit("flow panel: [panel.tool] needs a label")
    lw = advance("mono-semibold", tl, FL_TOOL)
    nw = advance("mono", tn, FL_NOTE) if tn else 0
    g = 16 if tn else 0
    pw = 40 + lw + g + nw
    if pw > w - 2 * FL_INSET:
        sys.exit(f"flow panel: tool label and note too long: {tl!r} {tn!r}")
    px0, py0 = cx - pw / 2, (y0 + y1 - head_h) / 2 - pill_h / 2
    o.append(f'<rect x="{px0 + 1:.2f}" y="{py0 + 1:.1f}" width="{pw - 2:.2f}" height="{pill_h - 2}" '
             f'rx="{(pill_h - 2) / 2:g}" fill="{c["raised"]}" stroke="{c["line-strong"]}" stroke-width="2"/>')
    o.append(text_el("mono-semibold", tl, px0 + 20, py0 + pill_h / 2 + 8.4, FL_TOOL, c["text"]))
    if tn:
        o.append(text_el("mono", tn, px0 + 20 + lw + g, py0 + pill_h / 2 + 7.7, FL_NOTE, c["mute"]))
    # the log strip: status lines in terminal colours, printed one at a time
    if status:
        o.append(f'<rect y="{h - strip}" width="{w}" height="{strip}" fill="{c["code-bg"]}"/>'
                 f'<rect y="{h - strip}" width="{w}" height="1" fill="{c["line"]}"/>')
        # real log lines aren't reworded to fit: the size steps down to 20px
        # (a 40-character line), and past that the line has to be shorter
        bodies = [status_line(ln, c) for ln in status]
        room = w - 2 * 28
        ss = FL_NOTE
        while ss > 20 and max(advance("mono", b, ss) for b, _ in bodies) > room:
            ss -= 0.5
        for (body, _), ln in zip(bodies, status):
            if advance("mono", body, ss) > room:
                sys.exit(f"flow panel: status line too long (max {int(room / (0.6 * ss))} chars): {ln!r}")
        sy, at = h - strip + 13 + 24, t0 + DUR_SLOW + 0.15
        for body, fill in bodies:
            o.append(f'<g class="{mo.appear(at)}">{text_el("mono", body, 28, sy, ss, fill)}</g>')
            sy += st_lh; at += LINE_GAP
    return "\n".join(o), ""


TM_SIZES = (26, 25, 24, 23, 22)   # terminal type, largest first; 22px is 7px on a card
TM_MAX_LINES = 6


def panel_terminal_v2(cfg, c, mo, t0):
    """A short terminal: the command and the one or two lines that matter.
    The window is as tall as its lines and centred in the panel area. The
    command types at the type rate, its output prints a line at a time, and
    the cursor on the last row blinks twice and stays. Returns (inner, top,
    window height)."""
    title = cfg.get("title", "")
    lines = cfg.get("lines") or []
    if not lines:
        sys.exit("terminal panel: needs lines")
    if len(lines) > TM_MAX_LINES:
        sys.exit(f"terminal panel (v2): at most {TM_MAX_LINES} lines; show the moment that matters, not the log")
    w, pad = V2_PW, 28
    room = w - 2 * pad
    rows = []
    for ln in lines:
        if ln.startswith("$ "):
            rows.append(("cmd", ln[2:], c["text"]))
        else:
            rows.append(("out", *status_line(ln, c)))

    def widest(size):
        return max(advance("mono", ("$ " + b) if k == "cmd" else b, size) for k, b, _ in rows)
    size = next((s for s in TM_SIZES if widest(s) <= room), None)
    if size is None:
        sys.exit(f"terminal line too long: at most {int(room / (0.6 * TM_SIZES[-1]))} characters, "
                 f"prompt included, at {TM_SIZES[-1]}px")
    lh, bar = round(size * 1.7), 48
    cw = advance("mono", "M", size)
    win_h = bar + 24 + (len(rows) + 1) * lh + 16
    o = [f'<rect width="{w}" height="{win_h}" fill="{c["code-bg"]}"/>',
         f'<rect width="{w}" height="{bar}" fill="{c["surface"]}"/>',
         f'<rect y="{bar}" width="{w}" height="1" fill="{c["line"]}"/>']
    for i in range(3):
        o.append(f'<circle cx="{26 + i * 20}" cy="{bar / 2}" r="6" fill="{c["line"]}"/>')
    if title:
        o.append(text_el("mono", title, w / 2, bar / 2 + 6, 17, c["mute"], 0.5, "middle"))
    cur_h, cur_w = round(size * 1.12), round(cw * 0.9, 1)

    def cursor(x, base, cls, hidden=False):
        extra = ' opacity="0"' if hidden else ""
        return (f'<rect class="{cls}" x="{x:.2f}" y="{base - 0.86 * size:.1f}" width="{cur_w}" height="{cur_h}" '
                f'fill="{c["ember"]}"{extra}/>')
    t, first = t0, True
    y = bar + 24 + 0.72 * lh
    for kind, body, fill in rows:
        if kind == "cmd":
            # the prompt is there from the start (later prompts once the
            # output above them has printed); then each character types
            shown = 0.0 if first else t
            typing = t0 if first else t + 0.2
            p = text_el("mono-semibold", "$", pad, y, size, c["ember"])
            o.append(p if first else f'<g class="{mo.appear(t)}">{p}</g>')
            bx = pad + advance("mono", "$ ", size)
            for i, ch in enumerate(body):
                if ch == " ":
                    continue
                d = text_path("mono", ch, bx + advance("mono", body[:i], size), y, size)
                if d:
                    o.append(f'<path class="{mo.appear(typing + (i + 1) * TYPE_RATE)}" d="{d}" fill="{fill}"/>')
            done = typing + len(body) * TYPE_RATE
            o.append(cursor(bx, y, mo.typing_cursor(shown, done + 0.2, typing, len(body), len(body) * cw), hidden=True))
            t, first = done + 0.25, False
        else:
            if body:
                o.append(f'<g class="{mo.appear(t)}">{text_el("mono", body, pad, y, size, fill)}</g>')
            t += LINE_GAP
        y += lh
    # the last row: the cursor, back at the start of a fresh line
    o.append(cursor(pad, y, mo.cursor_blinks(t - LINE_GAP + 0.1)))
    return "\n".join(o), "", win_h


def panel_art_v2(cfg, c, base):
    """The tool's own drawing. Art files for v2 are drawn in a 528x448 box;
    `viewbox = "0 0 480 368"` scales an older (v1) drawing to fit instead."""
    inner, top = panel_art(cfg, c, base)
    vb = cfg.get("viewbox")
    if vb:
        try:
            x, y, w, h = (float(v) for v in str(vb).replace(",", " ").split())
        except ValueError:
            sys.exit(f"art panel: viewbox must be four numbers, \"x y width height\", not {vb!r}")
        s = min(V2_PW / w, V2_PH / h)
        tf = f'translate({(V2_PW - w * s) / 2 - x * s:.2f} {(V2_PH - h * s) / 2 - y * s:.2f}) scale({s:.4f})'
        inner = f'<g transform="{tf}">{inner}</g>'
        top = f'<g transform="{tf}">{top}</g>' if top else ""
    return inner, top


def image_size(data, name):
    """Pixel size of a PNG or JPEG, read from its header."""
    import struct
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            break
        marker, seg = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            hh, ww = struct.unpack(">HH", data[i + 5:i + 9])
            return ww, hh
        i += 2 + seg
    sys.exit(f"screenshot: can't read the size of {name}")


def panel_screenshot_v2(cfg, theme, base, c):
    """A screenshot per theme, filling the panel. `crop = [x, y, w, h]` (image
    pixels) picks the part that still reads at 400px; it is scaled to cover
    the panel and centred, so give it about the panel's shape, 528:448.
    `fit = "contain"` shows all of the crop instead, centred on the theme's
    bg colour: seamless when the app's page uses the brand bg."""
    import base64
    name = cfg.get("file", "cover-shot-{theme}.png").replace("{theme}", theme)
    try:
        data = open(os.path.join(base, name), "rb").read()
    except OSError as e:
        sys.exit(f"screenshot: {e}")
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        mime = "image/png"
    elif data[:3] == b"\xff\xd8\xff":
        mime = "image/jpeg"
    else:
        sys.exit(f"screenshot: {name} is not a PNG or JPEG")
    iw, ih = image_size(data, name)
    crop = cfg.get("crop")
    if crop is None:
        cx, cy, cw, ch, par = 0, 0, iw, ih, "xMidYMin slice"     # v1 behaviour: fill, anchored top-centre
    else:
        if len(crop) != 4 or any(not isinstance(v, (int, float)) for v in crop):
            sys.exit("screenshot: crop is [x, y, width, height] in image pixels")
        cx, cy, cw, ch = crop
        if cx < 0 or cy < 0 or cw <= 0 or ch <= 0 or cx + cw > iw or cy + ch > ih:
            sys.exit(f"screenshot: crop {crop} is outside {name} ({iw}x{ih})")
        par = "xMidYMid slice"
    fit = cfg.get("fit", "cover")
    if fit not in ("cover", "contain"):
        sys.exit(f"screenshot: fit is \"cover\" or \"contain\", not {fit!r}")
    uri = f"data:{mime};base64,{base64.b64encode(data).decode()}"
    img = f'<image href="{uri}" width="{iw}" height="{ih}"/>'
    if fit == "contain":
        # a nested viewport exactly the crop's shape, so nothing outside the
        # crop shows; the theme's bg fills the rest of the panel
        s = min(V2_PW / cw, V2_PH / ch)
        return (f'<rect width="{V2_PW}" height="{V2_PH}" fill="{c["bg"]}"/>'
                f'<svg x="{(V2_PW - cw * s) / 2:.2f}" y="{(V2_PH - ch * s) / 2:.2f}" '
                f'width="{cw * s:.2f}" height="{ch * s:.2f}" viewBox="{cx:g} {cy:g} {cw:g} {ch:g}">{img}</svg>'), ""
    return (f'<svg width="{V2_PW}" height="{V2_PH}" viewBox="{cx:g} {cy:g} {cw:g} {ch:g}" preserveAspectRatio="{par}">'
            f'{img}</svg>'), ""


def compose_v2(cfg, theme, base, social=False):
    c = THEMES[theme]
    name = cfg["name"]; desc = cfg["description"]
    if cfg.get("bullets"):
        print(f"note: {name}: bullets are not drawn in layout v2 (they're in the README)", file=sys.stderr)
    mo = Motion()
    o = []

    # left column, built from baseline 0 of the first name line, then centred
    lines, size = name_lines(name)
    ls = TRACK * size
    pitch = round(size * 1.02)
    col = []
    widest = 0.0
    top = None
    for i, ln in enumerate(lines):
        bx0, by0, bx1, _ = ink_box("mono-semibold", ln, size, ls)
        # optical alignment: each line's ink starts exactly at the column edge
        col.append(text_el("mono-semibold", ln, V2_LEFT - bx0, i * pitch, size, c["text"], ls))
        widest = max(widest, bx1 - bx0)
        top = by0 if top is None else top
    last = (len(lines) - 1) * pitch
    # Ember rule under the name, as wide as its widest line's ink, below the
    # descender line, so it sits the same on names with and without descenders
    rule_h = max(5, round(size * 0.06))
    rule_y = round(last + descender(size) + 0.1 * size, 1)
    rule_cls = mo.draw("x", 0.1)
    col.append(f'<rect class="{rule_cls}" x="{V2_LEFT}" y="{rule_y:g}" width="{widest:.1f}" height="{rule_h}" '
               f'rx="{rule_h / 2:g}" fill="{c["ember"]}"/>')
    y = rule_y + rule_h + 32 + 0.698 * DESC_SIZE
    dlines = wrap_balanced("sans-semibold", desc, DESC_SIZE, V2_COL, "description")
    for ln in dlines:
        dx0 = ink_box("sans-semibold", ln, DESC_SIZE)[0]
        col.append(text_el("sans-semibold", ln, V2_LEFT - dx0, y, DESC_SIZE, c["text"])); y += DESC_LH
    bottom = y - DESC_LH + 0.22 * DESC_SIZE
    shift = V2_PY + V2_PH / 2 - (top + bottom) / 2
    o.append(f'<g transform="translate(0 {shift:.1f})">' + "\n".join(col) + "</g>")

    # panel
    pcfg = cfg.get("panel", {})
    kind = pcfg.get("kind", "terminal")
    ph = V2_PH
    if kind == "flow":
        inner, ontop = panel_flow(pcfg, c, mo, 0.45)
    elif kind == "terminal":
        inner, ontop, ph = panel_terminal_v2(pcfg, c, mo, 0.3)
    elif kind == "art":
        inner, ontop = panel_art_v2(pcfg, c, base)
    elif kind == "screenshot":
        inner, ontop = panel_screenshot_v2(pcfg, theme, base, c)
    else:
        sys.exit(f"panel kind must be 'flow', 'terminal', 'art' or 'screenshot', not {kind!r}")
    if mo.end > COVER_MOTION_MAX + 1e-9:
        sys.exit(f"{name}: the entrance runs {mo.end:.2f} s; a cover's motion ends by {COVER_MOTION_MAX:g} s "
                 f"(BRAND.md section 8). Shorten the command or drop a line.")
    py = V2_PY + (V2_PH - ph) / 2
    o.append(f'<rect x="{V2_PX}" y="{py:g}" width="{V2_PW}" height="{ph:g}" rx="12" fill="{c["desk"]}"/>')
    o.append(f'<g transform="translate({V2_PX} {py:g})"><g clip-path="url(#m)">{inner}</g>{ontop}</g>')
    o.append(f'<rect x="{V2_PX + .75}" y="{py + .75:g}" width="{V2_PW - 1.5}" height="{ph - 1.5:g}" rx="11.25" '
             f'fill="none" stroke="{c["line"]}" stroke-width="1.5"/>')

    fw, fh = (SW, SH) if social else (W, H)
    dx, dy = ((SW - W) / 2, (SH - H) / 2) if social else (0, 0)
    label = escape(f"{name}: {desc.rstrip('.')}", {'"': "&quot;"})
    defs = (f'<defs><pattern id="g" width="26" height="26" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.2" cy="1.2" r="1.2" fill="{c["dots"]}"/></pattern>'
            f'<radialGradient id="r" cx="78%" cy="110%" r="70%"><stop offset="0" stop-color="{c["glow"]}"/>'
            f'<stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient>'
            f'<clipPath id="c"><rect width="{fw}" height="{fh}" rx="{0 if social else 12}"/></clipPath>'
            f'<clipPath id="m"><rect width="{V2_PW}" height="{ph:g}" rx="12"/></clipPath></defs>')
    field = (f'<rect width="{fw}" height="{fh}" fill="{c["bg"]}"/><rect width="{fw}" height="{fh}" fill="url(#g)"/>'
             f'<rect width="{fw}" height="{fh}" fill="url(#r)"/>')
    # RFS tile + org label in the frame's bottom-left corner, as in v1. The
    # social preview keeps a 40px margin (GitHub crops previews); the cover 32px.
    m = 40 if social else 32
    ts = 40; k = ts / 56; tx, ty = m, fh - m - ts
    mark = (f'<rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="{14 * ts / 64:.2f}" fill="{c["tile"]}"/>'
            + text_el("mono-semibold", "RFS", tx + ts / 2, ty + 37.3 * k, 24.5 * k, c["tile-fg"], -1.17 * k, "middle")
            + f'<rect x="{tx + 12.25 * k:.2f}" y="{ty + 42 * k:.2f}" width="{31.5 * k:.2f}" height="{3.5 * k:.2f}" rx="{1.75 * k:.2f}" fill="{c["ember"]}"/>'
            + text_el("mono", "REAL-FRUIT-SNACKS", tx + ts + 14, ty + ts / 2 + 4, 11, c["mute"], 1.3))
    body = "\n".join(x for x in o if x)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fw} {fh}" width="{fw}" height="{fh}" '
            f'role="img" aria-label="{label}">\n{mo.css()}\n{defs}\n<g clip-path="url(#c)">{field}\n'
            f'<g transform="translate({dx} {dy})">\n{body}\n</g>\n{mark}</g></svg>\n')


def compose(cfg, theme, base, social=False):
    if cfg.get("layout", "v2") == "v1":
        return compose_v1(cfg, theme, base, social)
    return compose_v2(cfg, theme, base, social)


# ---------------------------------------------------------------- preview
def preview(cfg, base, path):
    """One sheet with the cover at the sizes it is seen at: 1200 (the PNG),
    830 (a README column), 400 (a Slack/Discord/X card), for both themes, and
    the social preview at 400."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("--preview needs pillow: pip install pillow")
    import io, tempfile
    def render(svg, width):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "p.png")
            render_png(svg, p, width)
            return Image.open(io.BytesIO(open(p, "rb").read())).convert("RGB")
    lab = ImageFont.truetype(os.path.join(HERE, "fonts", FONT_FILES["mono"]), 15)
    pad, gap, head = 40, 28, 34
    rows = []
    for theme in ("dark", "light"):
        svg, soc = compose(cfg, theme, base), compose(cfg, theme, base, social=True)
        rows.append((theme, render(svg, 1200), render(svg, 830), render(svg, 400), render(soc, 400)))
    sw = pad * 2 + max(1200, 830 + gap + 400)
    block = head + 560 + gap + head + 387 + gap
    sheet = Image.new("RGB", (sw, pad + 2 * block + pad), "#2B2E35")
    d = ImageDraw.Draw(sheet)
    y = pad
    for theme, full, mid, small, soc in rows:
        tn = "Nightshift" if theme == "dark" else "Dayshift"
        d.text((pad, y), f"{cfg['name']}  {tn}  1200 px (cover PNG)", font=lab, fill="#C9CCD3")
        sheet.paste(full, (pad, y + head)); y += head + 560 + gap
        d.text((pad, y), "830 px (README column)", font=lab, fill="#C9CCD3")
        d.text((pad + 830 + gap, y), "400 px (cover, then social card)", font=lab, fill="#C9CCD3")
        sheet.paste(mid, (pad, y + head))
        sheet.paste(small, (pad + 830 + gap, y + head))
        sheet.paste(soc, (pad + 830 + gap, y + head + small.height + 14))
        y += head + max(mid.height, small.height + 14 + soc.height) + gap
    sheet = sheet.crop((0, 0, sw, y + pad - gap))
    sheet.save(path, optimize=True)


def main():
    ap = argparse.ArgumentParser(description="RFS cover + social preview generator")
    ap.add_argument("config", help="path to cover.toml")
    ap.add_argument("--out", help="output directory (default: next to cover.toml)")
    ap.add_argument("--preview", metavar="FILE", help="also write a PNG of the cover at 1200, 830 and 400 px")
    ap.add_argument("--layout", choices=("v1", "v2"), help="override cover.toml's layout")
    a = ap.parse_args()
    try:
        cfg = tomllib.load(open(a.config, "rb"))
    except (OSError, tomllib.TOMLDecodeError) as e:
        sys.exit(f"{a.config}: {e}")
    if a.layout:
        cfg["layout"] = a.layout
    if cfg.get("layout", "v2") not in ("v1", "v2"):
        sys.exit(f"layout must be \"v1\" or \"v2\", not {cfg['layout']!r}")
    base = os.path.dirname(os.path.abspath(a.config))
    for k in ("name", "description"):
        if not isinstance(cfg.get(k), str) or not cfg[k].strip():
            sys.exit(f"cover.toml needs {k} = \"...\"")
    out = a.out or base
    os.makedirs(out, exist_ok=True)
    for theme in ("dark", "light"):
        svg = compose(cfg, theme, base)
        p = os.path.join(out, f"cover-{theme}.svg")
        open(p, "w", encoding="utf-8", newline="\n").write(svg)
        render_png(svg, os.path.join(out, f"cover-{theme}.png"))
        render_png(compose(cfg, theme, base, social=True), os.path.join(out, f"social-{theme}.png"))
    for f in ("cover-dark.svg", "cover-light.svg", "cover-dark.png", "cover-light.png",
              "social-dark.png", "social-light.png"):
        print("wrote", os.path.join(out, f))
    if a.preview:
        preview(cfg, base, a.preview)
        print("wrote", a.preview)


if __name__ == "__main__":
    main()
