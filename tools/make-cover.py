#!/usr/bin/env python3
"""Generate an RFS repo cover and GitHub social preview from one cover.toml.

usage:
    python3 make-cover.py <path/to/cover.toml> [--out DIR]

Writes, next to cover.toml unless --out is given:
    cover-dark.svg   cover-light.svg     1200x560  README header (<picture>)
    cover-dark.png   cover-light.png     1200x560  docs site og:image
    social-dark.png  social-light.png    1280x640  Settings > Social preview

Layout (fixed, so every repo matches):
    left   repo name (Plex Mono 600) / Ember rule / description (Plex Sans 600,
           up to 2 lines) / up to 4 bullets (Plex Sans 400)
    bottom-left corner  RFS tile + REAL-FRUIT-SNACKS label
    right  480x368 panel: a terminal (default) or the repo's own art file

All text is converted to outlines, so the SVGs render the same on GitHub,
in browsers and in image viewers without the fonts installed.

Requires Python 3.11+, fonttools and resvg-py (pip install fonttools resvg-py;
cairosvg also works), and the four IBM Plex files in
tools/fonts/ (OFL, see fonts/OFL.txt).

cover.toml:

    name        = "screen-mark"                       # repo name, as on GitHub
    description = "Screenshot capture and annotation in pure Rust."
    bullets     = ["Region, window, or timed capture", "..."]   # 0-4

    [panel]
    kind  = "terminal"                                # default
    title = "pwsh"                                    # optional window title
    lines = ["$ irm rfs.sh/carify | iex",             # "$ " command (Ember prompt)
             "ok carify 1.1.0 installed",             # "ok " Mint
             "! no ffmpeg on PATH",                   # "! " Amber
             "plain output"]                          # anything else: mute

    # or, for a drawing of the tool itself:
    [panel]
    kind = "art"
    file = "cover-art.svg"     # SVG fragment, see "Art files" below

Art files: plain SVG elements (no <svg> wrapper) drawn in a 480x368 box with
its origin at the panel's top-left corner; they are clipped to the panel's
rounded rectangle. Write colours as {token} and they are filled in per theme
(tokens: every key in brand/tokens/rfs.tokens.json, with primary/accent/signal
 also as ember/amber/mint, plus tile, dots, desk, window, scrim, on-ember and
 the annotation inks ink-red, ink-blue, ink-green, ink-yellow, ink-mauve, ink-on).
Text goes in <rfs-text> and is outlined:
    <rfs-text font="mono" size="12" x="40" y="20" anchor="start" fill="{text}">300 x 186</rfs-text>
    font: mono | mono-semibold | sans | sans-semibold;  anchor: start | middle | end
    optional ls="1.5" (letter spacing, px). Elements after a <rfs-unclip/> line
    are drawn on top without the panel clip (selection handles that overhang).
"""
import argparse, json, os, re, sys, tomllib
from xml.sax.saxutils import escape

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
except ImportError as e:  # pragma: no cover
    sys.exit(f"missing dependency ({e.name}): pip install fonttools resvg-py")


def render_png(svg, path):
    """SVG -> PNG. resvg-py has wheels for Windows/macOS/Linux with no system
    libraries; cairosvg is used if that's what's installed."""
    try:
        import resvg_py
        open(path, "wb").write(bytes(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True)))
        return
    except ImportError:
        pass
    try:
        import cairosvg
    except ImportError:
        sys.exit("no PNG renderer: pip install resvg-py  (or cairosvg)")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path)

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
    _tok = json.load(open(TOKENS, encoding="utf-8"))["color"]
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

W, H = 1200, 560            # cover
SW, SH = 1280, 640          # social preview; cover is centred in it
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


# ---------------------------------------------------------------- compose
def compose(cfg, theme, base, social=False):
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
    else:
        sys.exit(f"panel kind must be 'terminal' or 'art', not {kind!r}")
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


def main():
    ap = argparse.ArgumentParser(description="RFS cover + social preview generator")
    ap.add_argument("config", help="path to cover.toml")
    ap.add_argument("--out", help="output directory (default: next to cover.toml)")
    a = ap.parse_args()
    try:
        cfg = tomllib.load(open(a.config, "rb"))
    except (OSError, tomllib.TOMLDecodeError) as e:
        sys.exit(f"{a.config}: {e}")
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


if __name__ == "__main__":
    main()
