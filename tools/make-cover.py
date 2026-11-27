#!/usr/bin/env python3
"""Generate an RFS Cyclorama Dawn repo cover and GitHub social preview from cover.toml.

usage:
    python3 make-cover.py <path/to/cover.toml> [--out DIR] [--preview FILE] [--layout v1|v2]

Writes (next to cover.toml unless --out is given):
    cover-dark.svg   cover-light.svg     1200x560  README header (<picture>), animated once
    cover-dark.png   cover-light.png     1200x560  docs site og:image (finished frame)
    social-dark.png  social-light.png    1280x640  GitHub Settings > Social preview

World: Cyclorama Dawn (Steel & Beacon Orange).
Typography: Big Shoulders Stencil (display), Albert Sans (UI/prose), Azeret Mono (code/meta).
All glyphs are outlined from self-hosted variable .woff2 files in tools/fonts/, so SVGs
render identically on GitHub, browsers, and image viewers with zero font dependencies.

Requires Python 3.11+, fonttools, brotli, resvg-py (or cairosvg), and pillow (for --preview).
"""
import argparse, base64, io, json, math, os, re, struct, sys, tempfile, tomllib
from xml.sax.saxutils import escape

try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
except ImportError as e:  # pragma: no cover
    sys.exit(f"missing dependency ({e.name}): pip install fonttools brotli resvg-py")


def render_png(svg, path, width=None):
    """SVG -> PNG via resvg-py (preferred) or cairosvg."""
    try:
        import resvg_py
        kw = {"width": width} if width else {}
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(bytes(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True, **kw)))
        return
    except ImportError:
        pass
    try:
        import cairosvg
    except ImportError:
        sys.exit("no PNG renderer: pip install resvg-py  (or cairosvg)")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=path, output_width=width)


HERE = os.path.dirname(os.path.abspath(__file__))
FONT_SPECS = {
    "display": ("big-shoulders-stencil-latin.woff2", 800),
    "display-bold": ("big-shoulders-stencil-latin.woff2", 700),
    "sans": ("albert-sans-latin.woff2", 450),
    "sans-semibold": ("albert-sans-latin.woff2", 650),
    "mono": ("azeret-mono-latin.woff2", 400),
    "mono-semibold": ("azeret-mono-latin.woff2", 600),
}
_raw_fonts = {}
_glyph_sets = {}


def font_face(name):
    """Return (TTFont, GlyphSet) instantiated at the spec's variable wght."""
    if name not in FONT_SPECS:
        sys.exit(f"unknown font '{name}' (use {', '.join(FONT_SPECS)})")
    fname, wght = FONT_SPECS[name]
    if fname not in _raw_fonts:
        p = os.path.join(HERE, "fonts", fname)
        if not os.path.exists(p):
            sys.exit(f"missing font file: {p}")
        _raw_fonts[fname] = TTFont(p)
    if name not in _glyph_sets:
        f = _raw_fonts[fname]
        _glyph_sets[name] = f.getGlyphSet(location={"wght": wght}) if "fvar" in f else f.getGlyphSet()
    return _raw_fonts[fname], _glyph_sets[name]


# Brand tokens loaded from brand/tokens/rfs.tokens.json.
THEMES = {
    "dark": {
        "tile": "#18496B",
        "tile-end": "#F06E2B",
        "tile-fg": "#FFFFFF",
        "on-ember": "#050507",
        "desk": "#0C0C10",
        "window": "#1C1E26",
        "stage": "#07070B",
        "scrim": "rgba(5,5,7,0.68)",
        "wash-steel": "#1F547A",
        "wash-beacon": "#F06E2B",
        "wash-op": "0.56",
        "frame-stroke": "rgba(255,255,255,0.14)",
        "grid-stroke": "rgba(116,184,232,0.06)",
        "panel-grid": "rgba(116,184,232,0.065)",
        "reg-stroke": "rgba(116,184,232,0.36)",
        "steel-border": "rgba(116,184,232,0.42)",
        "steel-tint": "rgba(31,84,122,0.22)",
        "beacon-border": "rgba(255,146,84,0.58)",
        "beacon-tint": "rgba(240,110,43,0.14)",
        "mint-border": "rgba(61,220,151,0.44)",
        "mint-tint": "rgba(61,220,151,0.12)",
        "panel-shadow": "rgba(0,0,0,0.62)",
        "lx-code": "LX 263",
        "lx-title": "LX 263 · BEACON HORIZON",
        "tile-bg": "#050507",
        "tile-wash-op": "0.78",
        "tile-stroke": "rgba(255,255,255,0.22)",
        "tile-ink": "#F4F5F8",
        "tile-rule-id": "rfs-tile-rule",
        "lx263-ink": "#FF9254",
        "lx512-ink": "#B3B5C0",
    },
    "light": {
        "tile": "#FFFFFF",
        "tile-end": "#F5F7F9",
        "tile-fg": "#0D1016",
        "on-ember": "#FFFFFF",
        "desk": "#FFFFFF",
        "window": "#FFFFFF",
        "stage": "#F6F8FB",
        "scrim": "rgba(13,16,22,0.42)",
        "wash-steel": "#1F547A",
        "wash-beacon": "#F06E2B",
        "wash-op": "0.32",
        "frame-stroke": "rgba(13,16,22,0.16)",
        "grid-stroke": "rgba(22,70,105,0.055)",
        "panel-grid": "rgba(22,70,105,0.055)",
        "reg-stroke": "rgba(22,70,105,0.30)",
        "steel-border": "rgba(22,70,105,0.38)",
        "steel-tint": "rgba(22,70,105,0.08)",
        "beacon-border": "rgba(173,61,10,0.48)",
        "beacon-tint": "rgba(240,110,43,0.09)",
        "mint-border": "rgba(18,114,71,0.40)",
        "mint-tint": "rgba(18,114,71,0.08)",
        "panel-shadow": "rgba(13,16,22,0.14)",
        "lx-code": "LX 512",
        "lx-title": "LX 512 · ALABASTER DAY",
        "tile-bg": "#FFFFFF",
        "tile-wash-op": "0.36",
        "tile-stroke": "#CFD5DC",
        "tile-ink": "#0D1016",
        "tile-rule-id": "rfs-rule",
        "lx263-ink": "#474D59",
        "lx512-ink": "#AD3D0A",
    },
}

TOKENS = os.path.join(HERE, "..", "brand", "tokens", "rfs.tokens.json")
ALIASES = {"primary": "ember", "accent": "amber", "signal": "mint"}
try:
    with open(TOKENS, encoding="utf-8") as fh:
        _alltok = json.load(fh)
    _tok = _alltok["color"]
except (OSError, KeyError, ValueError) as e:
    sys.exit(f"can't read brand tokens from {TOKENS}: {e}")

for _theme in ("dark", "light"):
    src = _tok.get(_theme) or _tok["nightshift" if _theme == "dark" else "dayshift"]
    for k, v in src.items():
        THEMES[_theme][k] = v
        if k in ALIASES:
            THEMES[_theme][ALIASES[k]] = v

# Annotation inks (shared across both themes for UI/screenshot overlays)
INKS = {
    "ink-red": "#FF6E7A",
    "ink-blue": "#74B8E8",
    "ink-green": "#3DDC97",
    "ink-yellow": "#FFC247",
    "ink-mauve": "#B78CFF",
    "ink-on": "#050507",
}
for _t in THEMES.values():
    _t.update(INKS)

_mot = _alltok.get("motion", {})
EASE = _mot.get("ease", "cubic-bezier(0.16, 1, 0.3, 1)").replace(" ", "")
DUR_SLOW = float(_mot.get("dur-slow", "520ms").rstrip("ms")) / 1000
TYPE_RATE = float(_mot.get("type-rate", "45ms").rstrip("ms")) / 1000
LINE_GAP = 0.15
BLINK = 0.25
COVER_MOTION_MAX = 3.5

W, H = 1200, 560
SW, SH = 1280, 640
LEFT, COL_W = 88, 500
PX, PY, PW, PH = 640, 96, 480, 368


# ---------------------------------------------------------------- text & glyph metrics
def glyphs(fname, text):
    f, _ = font_face(fname)
    cmap = f.getBestCmap()
    missing = [ch for ch in text if ord(ch) not in cmap]
    if missing:
        sys.exit(f"font {fname} has no glyph for {''.join(missing)!r} in {text!r}")
    return [cmap[ord(ch)] for ch in text]


def advance(fname, text, size, ls=0.0):
    f, gs = font_face(fname)
    k = size / f["head"].unitsPerEm
    names = glyphs(fname, text)
    return sum(gs[n].width * k for n in names) + ls * max(len(names) - 1, 0)


def text_path(fname, text, x, y, size, ls=0.0, anchor="start"):
    """SVG path data for `text` with baseline at `y`."""
    f, gs = font_face(fname)
    k = size / f["head"].unitsPerEm
    names = glyphs(fname, text)
    total = advance(fname, text, size, ls)
    px = {"start": x, "middle": x - total / 2, "end": x - total}[anchor]
    out = []
    for n in names:
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, px, y)))
        cmd = pen.getCommands()
        if cmd:
            out.append(cmd)
        px += gs[n].width * k + ls
    return " ".join(out)


def text_el(fname, text, x, y, size, fill, ls=0.0, anchor="start"):
    d = text_path(fname, text, x, y, size, ls, anchor)
    return f'<path d="{d}" fill="{fill}"/>' if d else ""


def ink_box(fname, text, size, ls=0.0):
    """(left, top, right, bottom) of inked glyphs relative to origin on baseline."""
    f, gs = font_face(fname)
    k = size / f["head"].unitsPerEm
    px, box = 0.0, None
    for n in glyphs(fname, text):
        bp = BoundsPen(gs)
        gs[n].draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            b = (px + x0 * k, -y1 * k, px + x1 * k, -y0 * k)
            box = b if box is None else (
                min(box[0], b[0]),
                min(box[1], b[1]),
                max(box[2], b[2]),
                max(box[3], b[3]),
            )
        px += gs[n].width * k + ls
    return box or (0.0, 0.0, 0.0, 0.0)


def ink_extent(text, size, ls, fname="display"):
    b = ink_box(fname, text, size, ls)
    return b[0], b[2]


def descender(size, fname="mono-semibold"):
    f, gs = font_face(fname)
    bp = BoundsPen(gs)
    gs[f.getBestCmap()[ord("p")]].draw(bp)
    return -bp.bounds[1] * size / f["head"].unitsPerEm


def wrap(fname, text, size, width, max_lines, what):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if advance(fname, trial, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines or any(advance(fname, l, size) > width for l in lines):
        sys.exit(f"{what} doesn't fit in {max_lines} line(s) of {width}px: {text!r}")
    return lines


def wrap_balanced(fname, text, size, width, what):
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


# ---------------------------------------------------------------- Cyclorama Dawn shared visual helpers
def cyclorama_defs(c, w, h, rx, theme="dark", panel_box=None):
    """Linear Glacial Steel -> Maritime Beacon Orange cyclorama horizon defs + CAD blueprint patterns."""
    rule_start = c["steel-ink"] if theme == "dark" else c["steel-fill"]
    rule_end = c["beacon"] if theme == "dark" else c["beacon-ink"]
    mint_end = c["mint"]
    clip_panel = ""
    if panel_box:
        pw, ph, prx = panel_box
        clip_panel = f'<clipPath id="m"><rect width="{pw}" height="{ph:g}" rx="{prx}"/></clipPath>'
    return (
        f'<pattern id="cyc-grid" width="36" height="36" patternUnits="userSpaceOnUse">'
        f'<path d="M36 0V36H0" fill="none" stroke="{c["grid-stroke"]}" stroke-width="1"/>'
        f'</pattern>'
        f'<pattern id="panel-grid" width="20" height="20" patternUnits="userSpaceOnUse">'
        f'<path d="M20 0V20H0" fill="none" stroke="{c["panel-grid"]}" stroke-width="1"/>'
        f'</pattern>'
        f'<linearGradient id="cyc-grid-fade" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85"/>'
        f'<stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.35"/>'
        f'<stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.9"/>'
        f'</linearGradient>'
        f'<mask id="cyc-grid-mask"><rect width="{w}" height="{h}" fill="url(#cyc-grid-fade)"/></mask>'
        f'<linearGradient id="cyc-h" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="#133954"/>'
        f'<stop offset="44%" stop-color="{c["wash-steel"]}"/>'
        f'<stop offset="76%" stop-color="#CC5016"/>'
        f'<stop offset="100%" stop-color="{c["wash-beacon"]}"/>'
        f'</linearGradient>'
        f'<linearGradient id="cyc-fade" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>'
        f'<stop offset="36%" stop-color="#FFFFFF" stop-opacity="0.07"/>'
        f'<stop offset="72%" stop-color="#FFFFFF" stop-opacity="0.48"/>'
        f'<stop offset="100%" stop-color="#FFFFFF" stop-opacity="1"/>'
        f'</linearGradient>'
        f'<mask id="cyc-mask"><rect width="{w}" height="{h}" fill="url(#cyc-fade)"/></mask>'
        f'<linearGradient id="rfs-rule" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="{rule_start}"/>'
        f'<stop offset="52%" stop-color="{c["steel"] if theme == "light" else "#509AD0"}"/>'
        f'<stop offset="100%" stop-color="{rule_end}"/>'
        f'</linearGradient>'
        f'<linearGradient id="rfs-rule-v1" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{rule_start}"/>'
        f'<stop offset="100%" stop-color="{rule_end}"/>'
        f'</linearGradient>'
        f'<linearGradient id="rfs-rule-v2" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{rule_end}"/>'
        f'<stop offset="100%" stop-color="{mint_end}"/>'
        f'</linearGradient>'
        f'<linearGradient id="rfs-rule-v" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{rule_start}"/>'
        f'<stop offset="100%" stop-color="{rule_end}"/>'
        f'</linearGradient>'
        f'<radialGradient id="flow-glow-in" cx="50%" cy="18%" r="58%">'
        f'<stop offset="0%" stop-color="{c["steel"]}" stop-opacity="{"0.26" if theme == "dark" else "0.09"}"/>'
        f'<stop offset="100%" stop-color="{c["steel"]}" stop-opacity="0"/>'
        f'</radialGradient>'
        f'<radialGradient id="flow-glow-out" cx="50%" cy="82%" r="58%">'
        f'<stop offset="0%" stop-color="{c["mint"]}" stop-opacity="{"0.16" if theme == "dark" else "0.08"}"/>'
        f'<stop offset="100%" stop-color="{c["mint"]}" stop-opacity="0"/>'
        f'</radialGradient>'
        f'<linearGradient id="rfs-tile-f" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>'
        f'<stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.08"/>'
        f'<stop offset="74%" stop-color="#FFFFFF" stop-opacity="0.58"/>'
        f'<stop offset="100%" stop-color="#FFFFFF" stop-opacity="1"/>'
        f'</linearGradient>'
        f'<mask id="rfs-tile-m" maskContentUnits="objectBoundingBox">'
        f'<rect width="1" height="1" fill="url(#rfs-tile-f)"/>'
        f'</mask>'
        f'<linearGradient id="rfs-tile-rule" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="#74B8E8"/>'
        f'<stop offset="52%" stop-color="#3B85B8"/>'
        f'<stop offset="100%" stop-color="#F06E2B"/>'
        f'</linearGradient>'
        f'<linearGradient id="spec-spectrum" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="#0A141E"/>'
        f'<stop offset="28%" stop-color="#1F547A"/>'
        f'<stop offset="52%" stop-color="#74B8E8"/>'
        f'<stop offset="76%" stop-color="#F06E2B"/>'
        f'<stop offset="100%" stop-color="#F5F7F9"/>'
        f'</linearGradient>'
        f'<clipPath id="c"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
        + clip_panel
    )


def cyclorama_field(c, w, h, rx, theme="dark"):
    """Matte cyclorama ground + subtle CAD drafting grid + linear Steel->Beacon horizon floor wash + registration marks."""
    grid = f'<rect width="{w}" height="{h}" fill="url(#cyc-grid)" mask="url(#cyc-grid-mask)"/>'
    wash = (
        f'<rect width="{w}" height="{h}" fill="url(#cyc-h)" opacity="{c["wash-op"]}" mask="url(#cyc-mask)"/>'
    )
    beam_h = 4
    beam = f'<rect x="0" y="{h - beam_h}" width="{w}" height="{beam_h}" fill="url(#rfs-rule)"/>'
    m, t = 22, 10
    reg = (
        f'<g fill="none" stroke="{c["reg-stroke"]}" stroke-width="1.25">'
        f'<path d="M{m} {m + t} V{m} H{m + t}"/>'
        f'<path d="M{w - m - t} {m} H{w - m} V{m + t}"/>'
        f'<path d="M{m} {h - m - t} V{h - m} H{m + t}"/>'
        f'<path d="M{w - m - t} {h - m} H{w - m} V{h - m - t}"/>'
        f'</g>'
    )
    frame = (
        f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" '
        f'rx="{max(0, rx - 0.75):g}" fill="none" stroke="{c["frame-stroke"]}" stroke-width="1.5"/>'
        if rx > 0 else ""
    )
    return f'<rect width="{w}" height="{h}" fill="{c["bg"]}"/>{grid}{wash}{reg}{beam}{frame}'


def corner_mark(c, theme, tx, ty, ts=40):
    """Understated word-only REAL-FRUIT-SNACKS brand signature with Horizon accent pip."""
    y = ty + ts - 12
    pip = f'<rect x="{tx}" y="{y - 6.5:.1f}" width="18" height="3.5" rx="1.75" fill="url(#rfs-rule)"/>'
    return pip + text_el("mono-semibold", "REAL-FRUIT-SNACKS", tx + 26, y, 12.5, c["mute"], 1.8)


# ---------------------------------------------------------------- panels (v1 & art)
def panel_terminal(cfg, c):
    title = cfg.get("title", "") or "shell"
    lines = cfg.get("lines") or []
    if len(lines) > 12:
        sys.exit("terminal panel: at most 12 lines")
    tok_txt = f"[{title}]"
    tok_w = advance("mono-semibold", tok_txt, 11.5) + 16
    o = [
        f'<rect width="{PW}" height="{PH}" fill="{c["code-bg"]}"/>',
        f'<rect width="{PW}" height="38" fill="{c["surface"]}"/>',
        f'<rect width="{PW}" height="3" fill="url(#rfs-rule)"/>',
        f'<rect y="38" width="{PW}" height="1" fill="{c["line"]}"/>',
        f'<rect x="18" y="9" width="{tok_w:.1f}" height="22" rx="4" fill="{c["code-bg"]}" stroke="{c["line"]}"/>',
        text_el("mono-semibold", tok_txt, 26, 23.5, 11.5, c["steel-ink"]),
        text_el("mono", "LOCAL SHELL", PW - 18, 23.5, 10, c["mute"], 0.9, "end"),
    ]
    size, lh, x, y = 13.5, 26, 24, 74
    maxw = PW - 2 * x
    for ln in lines:
        if ln.startswith("$ "):
            o.append(text_el("mono-semibold", "$", x, y, size, c["beacon-ink"]))
            body, fill, fname, bx = ln[2:], c["text"], "mono", x + advance("mono", "$ ", size)
        elif ln.startswith("ok "):
            o.append(text_el("mono-semibold", "[ok]", x, y, size, c["mint"]))
            body, fill, fname, bx = ln[3:], c["text"], "mono", x + advance("mono-semibold", "[ok] ", size)
        elif ln.startswith("! "):
            o.append(text_el("mono-semibold", "[!]", x, y, size, c["amber"]))
            body, fill, fname, bx = ln[2:], c["text"], "mono", x + advance("mono-semibold", "[!] ", size)
        elif ln.startswith("x "):
            o.append(text_el("mono-semibold", "[x]", x, y, size, c["fault"]))
            body, fill, fname, bx = ln[2:], c["text"], "mono", x + advance("mono-semibold", "[x] ", size)
        else:
            body, fill, fname, bx = ln, c["mute"], "mono", x
        if advance(fname, body, size) > maxw - (bx - x):
            sys.exit(f"terminal line too long for the panel: {ln!r}")
        if body:
            o.append(text_el(fname, body, bx, y, size, fill))
        y += lh
    o.append(f'<rect x="{x}" y="{y - 13}" width="8" height="16" fill="{c["beacon"]}"/>')
    return "\n".join(o), ""


RFS_TEXT = re.compile(r"<rfs-text\b([^>]*)>(.*?)</rfs-text>", re.S)
ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def panel_art(cfg, c, base):
    p = os.path.join(base, cfg.get("file", "cover-art.svg"))
    try:
        with open(p, encoding="utf-8") as fh:
            src = fh.read()
    except OSError as e:
        sys.exit(f"art file: {e}")
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)

    def rt(m):
        a = dict(ATTR.findall(m.group(1)))
        fill = a.get("fill", "{text}")
        return text_el(
            a.get("font", "mono"),
            m.group(2).strip("\r\n"),
            float(a.get("x", 0)),
            float(a.get("y", 0)),
            float(a.get("size", 12)),
            fill,
            float(a.get("ls", 0)),
            a.get("anchor", "start"),
        )

    def tok(m):
        k = m.group(1)
        if k not in c:
            sys.exit(f"art file: unknown colour token {{{k}}} (have: {', '.join(sorted(c))})")
        return c[k]

    src = re.sub(r"\{([a-z][a-z0-9-]*)\}", tok, src)
    src = RFS_TEXT.sub(rt, src)
    clipped, _, top = src.partition("<rfs-unclip/>")
    return clipped.strip(), top.strip()


def panel_screenshot(cfg, theme, base):
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
    return (
        f'<image href="{uri}" x="0" y="0" width="{PW}" height="{PH}" '
        f'preserveAspectRatio="xMidYMin slice"/>'
    ), ""


# ---------------------------------------------------------------- v1 layout
def compose_v1(cfg, theme, base, social=False):
    c = THEMES[theme]
    name = cfg["name"]
    desc = cfg["description"]
    bullets = cfg.get("bullets", [])
    if len(bullets) > 4:
        sys.exit("at most 4 bullets")
    o = []

    disp_name = name.upper()
    size = 86
    while advance("display", disp_name, size, 0.045 * size) > COL_W and size > 48:
        size -= 2
    if advance("display", disp_name, size, 0.045 * size) > COL_W:
        sys.exit(f"name too long for the cover: {name!r}")
    col = []
    bx0, by0, bx1, _ = ink_box("display", disp_name, size, 0.045 * size)
    col.append(text_el("display", disp_name, LEFT - bx0, 0, size, c["text"], 0.045 * size))
    rule_y = 14.0
    col.append(f'<rect x="{LEFT}" y="{rule_y:g}" width="{bx1 - bx0:.1f}" height="5" rx="2.5" fill="url(#rfs-rule)"/>')
    y = 58.0
    for ln in wrap("sans-semibold", desc, 24, 430, 2, "description"):
        col.append(text_el("sans-semibold", ln, LEFT, y, 24, c["text"]))
        y += 32
    bottom = y - 32 + 6
    y += 18
    for b in bullets:
        if advance("sans", b, 15) > COL_W - 16:
            sys.exit(f"bullet too long: {b!r}")
        col.append(f'<rect x="{LEFT}" y="{y - 9}" width="6" height="6" rx="1" fill="{c["beacon"]}"/>')
        col.append(text_el("sans", b, LEFT + 16, y, 15, c["mute"]))
        bottom = y + 4
        y += 26
    shift = PY + PH / 2 - (by0 + bottom) / 2
    o.append(f'<g transform="translate(0 {shift:.1f})">' + "\n".join(col) + "</g>")

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
    o.append(f'<rect x="{PX + 0.5}" y="{PY + 0.5}" width="{PW - 1}" height="{PH - 1}" rx="9.5" fill="none" stroke="{c["line"]}"/>')

    fw, fh = (SW, SH) if social else (W, H)
    dx, dy = ((SW - W) / 2, (SH - H) / 2) if social else (0, 0)
    rx = 0 if social else 12
    label = escape(f"{name}: {desc.rstrip('.')}", {'"': "&quot;"})
    defs = f"<defs>{cyclorama_defs(c, fw, fh, rx, theme, (PW, PH, 10))}</defs>"
    field = cyclorama_field(c, fw, fh, rx, theme)
    m = 40 if social else 32
    mark = corner_mark(c, theme, dx + V2_LEFT, fh - m - 28, 40)
    body = "\n".join(x for x in o if x)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fw} {fh}" width="{fw}" height="{fh}" '
        f'role="img" aria-label="{label}">\n{defs}\n<g clip-path="url(#c)">{field}\n'
        f'<g transform="translate({dx} {dy})">\n{body}\n</g>\n{mark}</g></svg>\n'
    )


# ---------------------------------------------------------------- v2 layout
V2_LEFT, V2_COL = 72, 480
V2_PX, V2_PY, V2_PW, V2_PH = 600, 56, 528, 448
NAME_MAX = 136
NAME_BREAK = 90
NAME_MIN = 60
TRACK_DISPLAY = 0.045
DESC_SIZE, DESC_LH = 28, 36
TONES = ("text", "mute", "steel-ink", "beacon-ink", "amber", "mint", "fault")


class Motion:
    def __init__(self):
        self.rules = []
        self.end = 0.0

    def _cls(self):
        return f"m{len(self.rules)}"

    def draw(self, axis, start, dur=None):
        dur = DUR_SLOW if dur is None else dur
        cls = self._cls()
        origin = "0 50%" if axis == "x" else "50% 0"
        self.rules.append(
            f".{cls}{{transform-box:fill-box;transform-origin:{origin};"
            f"animation:rfs-draw-{axis} {dur:g}s {EASE} {start:g}s both}}"
        )
        self.end = max(self.end, start + dur)
        return cls

    def appear(self, at):
        cls = self._cls()
        self.rules.append(f".{cls}{{animation:rfs-hidden {at:.3f}s step-end}}")
        self.end = max(self.end, at)
        return cls

    def typing_cursor(self, shown, hidden, move_at, steps, dist):
        cls = self._cls()
        kf = f"rfs-mv{len(self.rules)}"
        self.rules.append(
            f"@keyframes {kf}{{to{{transform:translateX({dist:.2f}px)}}}}"
            f".{cls}{{animation:rfs-shown {hidden - shown:.3f}s step-end {shown:.3f}s,"
            f"{kf} {steps * TYPE_RATE:.3f}s steps({steps},end) {move_at:.3f}s both}}"
        )
        self.end = max(self.end, hidden)
        return cls

    def cursor_blinks(self, at):
        cls = self._cls()
        self.rules.append(
            f".{cls}{{animation:rfs-hidden {at:.3f}s step-end,"
            f"rfs-blink {2 * BLINK:g}s step-end {at:.3f}s 2}}"
        )
        self.end = max(self.end, at + 4 * BLINK)
        return cls

    def css(self):
        if not self.rules:
            return ""
        return (
            "<style>@media (prefers-reduced-motion:no-preference){"
            "@keyframes rfs-draw-x{from{transform:scaleX(0)}}"
            "@keyframes rfs-draw-y{from{transform:scaleY(0)}}"
            "@keyframes rfs-hidden{from,to{opacity:0}}"
            "@keyframes rfs-shown{from,to{opacity:1}}"
            "@keyframes rfs-blink{0%{opacity:1}50%{opacity:0}}"
            + "".join(self.rules)
            + "}</style>"
        )


def name_lines(name):
    up = name.upper()

    def unit(lines):
        return max(advance("display", l, 1, TRACK_DISPLAY) for l in lines)

    best = ([up], min(NAME_MAX, V2_COL / unit([up])))
    if best[1] < NAME_BREAK and "-" in up.strip("-"):
        for i, ch in enumerate(up):
            if ch == "-" and 0 < i < len(up) - 1:
                ls = [up[: i + 1], up[i + 1 :]]
                s = min(NAME_MAX, V2_COL / unit(ls))
                if s > best[1] * 1.1:
                    best = (ls, s) if len(best[0]) == 1 or s > best[1] else best
    lines, size = best
    size = math.floor(size)
    if size < NAME_MIN:
        sys.exit(f"name too long for the cover even on two lines: {name!r}")
    return lines, size


def status_token(ln, c):
    """Parse status prefix into (bracket_tag, tag_color, body_text, body_color)."""
    for pre, tag, key in (("ok ", "[ok]", "mint"), ("! ", "[!]", "amber"), ("x ", "[x]", "fault")):
        if ln.startswith(pre):
            return tag, c[key], ln[len(pre) :], c["text"]
    return "", c["mute"], ln, c["mute"]


FL_LABEL, FL_NOTE, FL_VALUE, FL_CHIP, FL_TOOL = 21, 16, 46, 17, 17.5
FL_INSET = 30
FL_GAP = 10


def flow_end(node, c, cx, y, w, which, below=False):
    label, note = node.get("label", ""), node.get("note", "")
    value, chips = node.get("value"), node.get("chips")
    tone = node.get("tone", "text")
    if not label:
        sys.exit(f"flow panel: {which} needs a label")
    if tone not in TONES:
        sys.exit(f"flow panel: {which} tone must be one of {', '.join(TONES)}, not {tone!r}")
    if (value is None) == (chips is None):
        sys.exit(f"flow panel: {which} needs a value or chips (one of them)")
    is_in = which == "input"
    fill, room = c[tone], w - 2 * FL_INSET - 44
    lw = advance("sans-semibold", label, FL_LABEL)
    nw = advance("mono", note, FL_NOTE) if note else 0
    gap = 10 if note else 0
    if lw + gap + nw > room:
        sys.exit(f"flow panel: {which} label and note too long for one line: {label!r} {note!r}")
    cap = 0.70 * FL_LABEL
    head_h = cap + 0.22 * FL_LABEL

    def head(y_top):
        hx, L = cx - (lw + gap + nw) / 2, y_top + cap
        return (
            text_el("sans-semibold", label, hx, L, FL_LABEL, c["text"])
            + (text_el("mono", note, hx + lw + gap, L, FL_NOTE, c["mute"]) if note else "")
        )

    chip_border = c["steel-border"] if is_in else c["mint-border"]
    chip_bg = c["steel-tint"] if is_in else c["mint-tint"]

    if value is not None:
        size = FL_VALUE
        while advance("mono-semibold", value, size) > room and size > 30:
            size -= 2
        if advance("mono-semibold", value, size) > room:
            sys.exit(f"flow panel: {which} value too long: {value!r}")
        body_h = 0.698 * size

        def body(y_top):
            return text_el("mono-semibold", value, cx, y_top + body_h, size, fill, 0, "middle")
    else:
        if not 1 <= len(chips) <= 3:
            sys.exit(f"flow panel: {which} takes 1-3 chips")
        pad, cg, body_h = 11, 9, 35
        ws = [advance("mono-semibold", t, FL_CHIP) + 2 * pad for t in chips]
        total = sum(ws) + cg * (len(ws) - 1)
        if total > room + 24:
            sys.exit(f"flow panel: {which} chips too wide ({total:.0f}px of {room + 24}): {chips!r}")

        def body(y_top):
            out, x = [], cx - total / 2
            for t, cw in zip(chips, ws):
                out.append(
                    f'<rect x="{x + 0.6:.2f}" y="{y_top + 0.6:.1f}" width="{cw - 1.2:.2f}" height="{body_h - 1.2}" '
                    f'rx="4" fill="{chip_bg}" stroke="{chip_border}" stroke-width="1.2"/>'
                )
                out.append(text_el("mono-semibold", t, x + cw / 2, y_top + body_h / 2 + 5.8, FL_CHIP, fill, 0, "middle"))
                x += cw + cg
            return "".join(out)

    content_h = head_h + FL_GAP + body_h - (0 if below else 0.22 * FL_LABEL)
    pad_y = 14
    box_h = content_h + 2 * pad_y
    box_x, box_w = 22, w - 44
    tag_txt = "[in]" if is_in else "[out]"
    idx_txt = "01" if is_in else "02"
    accent = c["steel-ink"] if is_in else c["mint"]
    border = c["steel-border"] if is_in else c["mint-border"]
    tint = c["steel-tint"] if is_in else c["mint-tint"]
    tag_w = advance("mono-semibold", tag_txt, 10.5) + 12
    frame = (
        f'<rect x="{box_x}" y="{y:.1f}" width="{box_w}" height="{box_h:.1f}" rx="8" fill="{c["code-bg"]}" stroke="{border}" stroke-width="1.25"/>'
        f'<rect x="{box_x + 0.75}" y="{y + 10:.1f}" width="3.5" height="{box_h - 20:.1f}" rx="1.75" fill="{accent}"/>'
        f'<rect x="{box_x + 12}" y="{y + 9:.1f}" width="{tag_w:.1f}" height="19" rx="3.5" fill="{tint}" stroke="{border}" stroke-width="0.9"/>'
        + text_el("mono-semibold", tag_txt, box_x + 18, y + 22, 10.5, accent)
        + text_el("mono", idx_txt, box_x + box_w - 13, y + 21.5, 10, c["mute"], 0.6, "end")
    )
    inner_y = y + pad_y
    if below:
        svg = frame + body(inner_y) + head(inner_y + body_h + FL_GAP)
    else:
        svg = frame + head(inner_y) + body(inner_y + head_h + FL_GAP - 0.22 * FL_LABEL)
    return svg, box_h


def panel_flow(cfg, c, mo, t0):
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
    hdr_h = 38
    st_lh = 28
    strip = 20 + st_lh * len(status) if status else 0
    stage_h = h - hdr_h - strip
    tok_hdr = "[flow]"
    tok_hdr_w = advance("mono-semibold", tok_hdr, 11.5) + 14
    o = [
        f'<rect width="{w}" height="{h}" fill="{c["stage"]}"/>',
        f'<rect y="{hdr_h}" width="{w}" height="{stage_h}" fill="url(#panel-grid)"/>',
        f'<rect y="{hdr_h}" width="{w}" height="{stage_h}" fill="url(#flow-glow-in)"/>',
        f'<rect y="{hdr_h}" width="{w}" height="{stage_h}" fill="url(#flow-glow-out)"/>',
        f'<rect width="{w}" height="{hdr_h}" fill="{c["surface"]}"/>',
        f'<rect width="{w}" height="3" fill="url(#rfs-rule)"/>',
        f'<rect y="{hdr_h}" width="{w}" height="1" fill="{c["line"]}"/>',
        f'<rect x="18" y="9" width="{tok_hdr_w:.1f}" height="21" rx="4" fill="{c["code-bg"]}" stroke="{c["line"]}"/>',
        text_el("mono-semibold", tok_hdr, 25, 23, 11.5, c["steel-ink"]),
        text_el("mono", "DATA PIPELINE", 25 + tok_hdr_w + 2, 23, 10.5, c["mute"], 0.9),
        text_el("mono", "LOCAL · ZERO CLOUD", w - 18, 23, 10, c["mute"], 0.9, "end"),
    ]
    _, h_in = flow_end(cfg["input"], c, cx, 0, w, "input")
    _, h_out = flow_end(cfg["output"], c, cx, 0, w, "output", below=True)
    tok_h, edge = 40, 16
    mid = stage_h - 2 * edge - h_in - h_out
    if mid < tok_h + 2 * 18:
        sys.exit("flow panel: too much in it; drop a status line or use a value instead of chips")
    y_in = hdr_h + edge
    y_out = y_in + h_in + mid

    # D · Terminal Token active processor core in Beacon Orange
    tl, tn = tool.get("label", ""), tool.get("note", "")
    if not tl:
        sys.exit("flow panel: [panel.tool] needs a label")
    tl_tok = f"[{tl}]"
    lw = advance("mono-semibold", tl_tok, FL_TOOL)
    nw = advance("mono", tn, FL_NOTE) if tn else 0
    g = 11 if tn else 0
    pw = 34 + lw + g + nw
    if pw > w - 2 * FL_INSET:
        sys.exit(f"flow panel: tool label and note too long: {tl!r} {tn!r}")
    y0, y1 = y_in + h_in + 2, y_out - 2
    head_w, head_h, bar_w = 14, 10, 3.5
    px0, py0 = cx - pw / 2, (y0 + y1 - head_h) / 2 - tok_h / 2
    py1 = py0 + tok_h

    # Two-stage matched conduit: Steel -> Beacon (upper), Beacon -> Mint (lower)
    o.append(
        f'<rect class="{mo.draw("y", t0, DUR_SLOW * 0.55)}" x="{cx - bar_w / 2}" y="{y0:.1f}" width="{bar_w}" '
        f'height="{max(4, py0 - y0):.1f}" fill="url(#rfs-rule-v1)"/>'
    )
    o.append(
        f'<rect class="{mo.draw("y", t0 + DUR_SLOW * 0.45, DUR_SLOW * 0.55)}" x="{cx - bar_w / 2}" y="{py1:.1f}" width="{bar_w}" '
        f'height="{max(4, y1 - head_h + 1 - py1):.1f}" fill="url(#rfs-rule-v2)"/>'
    )
    o.append(
        f'<path class="{mo.appear(t0 + DUR_SLOW * 0.9)}" d="M{cx - head_w / 2} {y1 - head_h:.1f} '
        f'H{cx + head_w / 2} L{cx} {y1:.1f} Z" fill="{c["mint"]}"/>'
    )
    o.append(flow_end(cfg["input"], c, cx, y_in, w, "input")[0])
    o.append(flow_end(cfg["output"], c, cx, y_out, w, "output", below=True)[0])

    # Terminal port docks on [in] bottom and [tool] top/bottom
    o.append(f'<circle cx="{cx}" cy="{y_in + h_in:.1f}" r="4" fill="{c["code-bg"]}" stroke="{c["steel-ink"]}" stroke-width="1.8"/>')
    o.append(f'<circle cx="{cx}" cy="{py0:.1f}" r="3.5" fill="{c["code-bg"]}" stroke="{c["beacon-ink"]}" stroke-width="1.6"/>')
    o.append(f'<circle cx="{cx}" cy="{py1:.1f}" r="3.5" fill="{c["code-bg"]}" stroke="{c["beacon-ink"]}" stroke-width="1.6"/>')

    # Beacon-framed active processor block
    o.append(
        f'<rect x="{px0:.2f}" y="{py0:.1f}" width="{pw:.2f}" height="{tok_h}" rx="6" fill="{c["code-bg"]}"/>'
        f'<rect x="{px0 + 0.75:.2f}" y="{py0 + 0.75:.1f}" width="{pw - 1.5:.2f}" height="{tok_h - 1.5}" '
        f'rx="5.25" fill="{c["beacon-tint"]}" stroke="{c["beacon-border"]}" stroke-width="1.5"/>'
        f'<line x1="{px0 - 8:.1f}" y1="{py0 + tok_h / 2:.1f}" x2="{px0:.1f}" y2="{py0 + tok_h / 2:.1f}" stroke="{c["beacon-border"]}" stroke-width="1.2"/>'
        f'<line x1="{px0 + pw:.1f}" y1="{py0 + tok_h / 2:.1f}" x2="{px0 + pw + 8:.1f}" y2="{py0 + tok_h / 2:.1f}" stroke="{c["beacon-border"]}" stroke-width="1.2"/>'
    )
    o.append(text_el("mono-semibold", tl_tok, px0 + 17, py0 + tok_h / 2 + 6, FL_TOOL, c["beacon-ink"]))
    if tn:
        o.append(text_el("mono", tn, px0 + 17 + lw + g, py0 + tok_h / 2 + 6, FL_NOTE, c["text"]))

    if status:
        o.append(
            f'<rect y="{h - strip}" width="{w}" height="{strip}" fill="{c["code-bg"]}"/>'
            f'<rect y="{h - strip}" width="{w}" height="1" fill="{c["line"]}"/>'
        )
        parsed = [status_token(ln, c) for ln in status]
        room = w - 2 * 22
        ss = 15.5
        while ss > 12.0 and max(advance("mono", (f"{tag} " if tag else "") + body, ss) for tag, _, body, _ in parsed) > room:
            ss -= 0.5
        sy, at = h - strip + 10 + 19.5, t0 + DUR_SLOW + 0.15
        for tag, tag_col, body, body_col in parsed:
            row_svg = ""
            bx = 22.0
            if tag:
                row_svg += text_el("mono-semibold", tag, bx, sy, ss, tag_col)
                bx += advance("mono-semibold", tag + " ", ss)
            row_svg += text_el("mono", body, bx, sy, ss, body_col)
            o.append(f'<g class="{mo.appear(at)}">{row_svg}</g>')
            sy += st_lh
            at += LINE_GAP
    return "\n".join(o), ""


TM_SIZES = (19, 18, 17, 16, 15, 14.5)
TM_MAX_LINES = 6


def _cmd_char_fills(body, c):
    """Per-character syntax highlight color map for a shell command string."""
    fills = [c["text"]] * len(body)
    token_idx = 0
    for m in re.finditer(r"\S+", body):
        tok = m.group(0)
        if token_idx == 0:
            col = c["steel-ink"]
        elif tok.startswith("-"):
            col = c["amber"]
        elif "/" in tok or "\\" in tok or tok.startswith(("'", '"', "~")):
            col = c["amber"]
        else:
            col = c["text"]
        for i in range(m.start(), m.end()):
            fills[i] = col
        token_idx += 1
    return fills


def panel_terminal_v2(cfg, c, mo, t0):
    title = cfg.get("title", "") or "shell"
    lines = cfg.get("lines") or []
    if not lines:
        sys.exit("terminal panel: needs lines")
    if len(lines) > TM_MAX_LINES:
        sys.exit(f"terminal panel (v2): at most {TM_MAX_LINES} lines")
    w = V2_PW
    win_h = V2_PH
    gutter_w = 48
    pad_l = gutter_w + 18
    pad_r = 22
    room = w - pad_l - pad_r
    rows = []
    for ln in lines:
        if ln.startswith("$ "):
            rows.append(("cmd", "", "", ln[2:], c["text"]))
        else:
            tag, tag_col, body, body_col = status_token(ln, c)
            rows.append(("out", tag, tag_col, body, body_col))

    def row_str(k, tag, b):
        if k == "cmd":
            return "$ " + b
        return (tag + " " + b) if tag else b

    def widest(size):
        return max(advance("mono", row_str(k, tag, b), size) for k, tag, _, b, _ in rows)

    size = next((s for s in TM_SIZES if widest(s) <= room), None)
    if size is None:
        sys.exit(f"terminal line too long at {TM_SIZES[-1]}px")
    lh = round(size * 2.05)
    bar = 44
    foot_h = 42
    body_h = win_h - bar - foot_h
    cw = advance("mono", "M", size)
    tok_txt = f"[{title}]"
    tok_w = advance("mono-semibold", tok_txt, 12.5) + 16
    exit_tok = "[ok]"
    exit_w = advance("mono-semibold", exit_tok, 11.5) + 12

    o = [
        f'<rect width="{w}" height="{win_h}" fill="{c["code-bg"]}"/>',
        f'<rect y="{bar}" width="{w}" height="{body_h}" fill="url(#panel-grid)" opacity="0.55"/>',
        f'<rect y="{bar}" width="{gutter_w}" height="{body_h}" fill="{c["surface"]}" opacity="0.55"/>',
        f'<line x1="{gutter_w}" y1="{bar}" x2="{gutter_w}" y2="{win_h - foot_h}" stroke="{c["line"]}" stroke-width="1"/>',
        # Console Header Bar
        f'<rect width="{w}" height="{bar}" fill="{c["surface"]}"/>',
        f'<rect width="{w}" height="3" fill="url(#rfs-rule)"/>',
        f'<rect y="{bar}" width="{w}" height="1" fill="{c["line"]}"/>',
        f'<rect x="18" y="10" width="{tok_w:.1f}" height="24" rx="4" fill="{c["code-bg"]}" stroke="{c["steel-border"]}" stroke-width="1"/>',
        text_el("mono-semibold", tok_txt, 26, 26.5, 12.5, c["steel-ink"]),
        text_el("mono", "TTY · LOCAL SHELL", w - 18, 26, 10.5, c["mute"], 1.0, "end"),
    ]
    cur_h, cur_w = round(size * 1.15), round(cw * 0.85, 1)

    def cursor(x, base, cls, hidden=False):
        extra = ' opacity="0"' if hidden else ""
        return (
            f'<rect class="{cls}" x="{x:.2f}" y="{base - 0.86 * size:.1f}" width="{cur_w}" height="{cur_h}" '
            f'fill="{c["beacon"]}"{extra}/>'
        )

    t, first = t0, True
    total_rows = len(rows) + 1
    y_start = bar + 24
    y = y_start + 0.72 * lh

    # Line numbers starting cleanly from top of console down to footer
    max_visible_lines = max(total_rows, int((body_h - 32) // lh))
    for ln_i in range(max_visible_lines):
        ly = y_start + 0.72 * lh + ln_i * lh
        if ly > win_h - foot_h - 14:
            break
        num_op = "0.78" if ln_i < total_rows else "0.28"
        o.append(f'<g opacity="{num_op}">{text_el("mono", f"{ln_i + 1:02d}", gutter_w - 12, ly, 11.5, c["mute"], 0, "end")}</g>')

    for kind, tag, tag_col, body, fill in rows:
        if kind == "cmd":
            shown = 0.0 if first else t
            typing = t0 if first else t + 0.2
            p = text_el("mono-semibold", "$", pad_l, y, size, c["beacon-ink"])
            o.append(p if first else f'<g class="{mo.appear(t)}">{p}</g>')
            bx = pad_l + advance("mono", "$ ", size)
            char_fills = _cmd_char_fills(body, c)
            for i, ch in enumerate(body):
                if ch == " ":
                    continue
                fn = "mono-semibold" if char_fills[i] == c["steel-ink"] else "mono"
                d = text_path(fn, ch, bx + advance("mono", body[:i], size), y, size)
                if d:
                    o.append(f'<path class="{mo.appear(typing + (i + 1) * TYPE_RATE)}" d="{d}" fill="{char_fills[i]}"/>')
            done = typing + len(body) * TYPE_RATE
            o.append(cursor(bx, y, mo.typing_cursor(shown, done + 0.2, typing, len(body), len(body) * cw), hidden=True))
            t, first = done + 0.25, False
        else:
            row_svg = ""
            if tag in ("[ok]", "[!]", "[x]"):
                strip_fill = c["mint-tint"] if tag == "[ok]" else c["beacon-tint"]
                row_svg += (
                    f'<rect x="{gutter_w + 1}" y="{y - size * 0.98:.1f}" width="{w - gutter_w - 1}" '
                    f'height="{size * 1.48:.1f}" fill="{strip_fill}" opacity="0.62"/>'
                )
            bx = float(pad_l)
            if tag:
                row_svg += text_el("mono-semibold", tag, bx, y, size, tag_col)
                bx += advance("mono-semibold", tag + " ", size)
            if body:
                row_svg += text_el("mono", body, bx, y, size, fill)
            if row_svg:
                o.append(f'<g class="{mo.appear(t)}">{row_svg}</g>')
            t += LINE_GAP
        y += lh
    o.append(cursor(pad_l, y, mo.cursor_blinks(t - LINE_GAP + 0.1)))

    # Bottom Console Telemetry Footer Bar
    fy = win_h - foot_h
    o.extend([
        f'<rect y="{fy}" width="{w}" height="{foot_h}" fill="{c["surface"]}"/>',
        f'<rect y="{fy}" width="{w}" height="1" fill="{c["line"]}"/>',
        f'<rect x="18" y="{fy + 10}" width="{exit_w:.1f}" height="21" rx="4" fill="{c["mint-tint"]}" stroke="{c["mint-border"]}" stroke-width="0.9"/>',
        text_el("mono-semibold", exit_tok, 24, fy + 24.5, 11.5, c["mint"]),
        text_el("mono", "exit 0", 24 + exit_w + 2, fy + 24.5, 11.5, c["text"]),
        text_el("mono", "NO_COLOR SAFE · LOCAL ONLY", w - 18, fy + 24.5, 10, c["mute"], 0.9, "end"),
    ])
    return "\n".join(o), "", win_h


def panel_art_v2(cfg, c, base):
    inner, top = panel_art(cfg, c, base)
    vb = cfg.get("viewbox")
    if vb:
        try:
            x, y, w, h = (float(v) for v in str(vb).replace(",", " ").split())
        except ValueError:
            sys.exit(f"art panel: viewbox must be four numbers, not {vb!r}")
        s = min(V2_PW / w, V2_PH / h)
        tf = f'translate({(V2_PW - w * s) / 2 - x * s:.2f} {(V2_PH - h * s) / 2 - y * s:.2f}) scale({s:.4f})'
        inner = f'<g transform="{tf}">{inner}</g>'
        top = f'<g transform="{tf}">{top}</g>' if top else ""
    return inner, top


def image_size(data, name):
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            break
        marker, seg = data[i + 1], struct.unpack(">H", data[i + 2 : i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            hh, ww = struct.unpack(">HH", data[i + 5 : i + 9])
            return ww, hh
        i += 2 + seg
    sys.exit(f"screenshot: can't read the size of {name}")


def panel_screenshot_v2(cfg, theme, base, c):
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
        cx, cy, cw, ch, par = 0, 0, iw, ih, "xMidYMin slice"
    else:
        if len(crop) != 4 or any(not isinstance(v, (int, float)) for v in crop):
            sys.exit("screenshot: crop is [x, y, width, height] in image pixels")
        cx, cy, cw, ch = crop
        if cx < 0 or cy < 0 or cw <= 0 or ch <= 0 or cx + cw > iw or cy + ch > ih:
            sys.exit(f"screenshot: crop {crop} is outside {name} ({iw}x{ih})")
        par = "xMidYMid slice"
    fit = cfg.get("fit", "cover")
    if fit not in ("cover", "contain"):
        sys.exit(f"screenshot: fit is 'cover' or 'contain', not {fit!r}")
    uri = f"data:{mime};base64,{base64.b64encode(data).decode()}"
    img = f'<image href="{uri}" width="{iw}" height="{ih}"/>'
    if fit == "contain":
        s = min(V2_PW / cw, V2_PH / ch)
        return (
            f'<rect width="{V2_PW}" height="{V2_PH}" fill="{c["bg"]}"/>'
            f'<svg x="{(V2_PW - cw * s) / 2:.2f}" y="{(V2_PH - ch * s) / 2:.2f}" '
            f'width="{cw * s:.2f}" height="{ch * s:.2f}" viewBox="{cx:g} {cy:g} {cw:g} {ch:g}">{img}</svg>'
        ), ""
    return (
        f'<svg width="{V2_PW}" height="{V2_PH}" viewBox="{cx:g} {cy:g} {cw:g} {ch:g}" preserveAspectRatio="{par}">'
        f"{img}</svg>"
    ), ""


def compose_v2(cfg, theme, base, social=False):
    c = THEMES[theme]
    name = cfg["name"]
    desc = cfg["description"]
    if cfg.get("bullets"):
        print(f"note: {name}: bullets are not drawn in layout v2 (they live in the README)", file=sys.stderr)
    mo = Motion()
    o = []

    lines, size = name_lines(name)
    ls = TRACK_DISPLAY * size
    pitch = round(size * 0.94)
    col = []
    widest = 0.0
    top = None
    for i, ln in enumerate(lines):
        bx0, by0, bx1, _ = ink_box("display", ln, size, ls)
        col.append(text_el("display", ln, V2_LEFT - bx0, i * pitch, size, c["text"], ls))
        widest = max(widest, bx1 - bx0)
        top = by0 if top is None else top

    # Top monospaced eyebrow kicker above the Stencil title
    kicker_txt = cfg.get("kicker") or "LOCAL-FIRST · OPEN SOURCE"
    ktok = "[rfs]"
    ktok_w = advance("mono-semibold", ktok, 12.5) + 14
    ky = top - 28
    col.insert(
        0,
        f'<rect x="{V2_LEFT}" y="{ky - 16:.1f}" width="{ktok_w:.1f}" height="23" rx="4" '
        f'fill="{c["code-bg"]}" stroke="{c["steel-border"]}" stroke-width="1"/>'
        + text_el("mono-semibold", ktok, V2_LEFT + 7, ky, 12.5, c["steel-ink"])
        + text_el("mono-semibold", kicker_txt.upper(), V2_LEFT + ktok_w + 12, ky, 12, c["steel-ink"], 1.5),
    )
    top = ky - 16

    last = (len(lines) - 1) * pitch
    rule_h = max(6, round(size * 0.055))
    rule_y = round(last + 18, 1)
    rule_cls = mo.draw("x", 0.1)
    col.append(
        f'<rect class="{rule_cls}" x="{V2_LEFT}" y="{rule_y:g}" width="{widest:.1f}" height="{rule_h}" '
        f'rx="{rule_h / 2:g}" fill="url(#rfs-rule)"/>'
    )
    y = rule_y + rule_h + 30 + 0.70 * DESC_SIZE
    dlines = wrap_balanced("sans-semibold", desc, DESC_SIZE, V2_COL, "description")
    for ln in dlines:
        dx0 = ink_box("sans-semibold", ln, DESC_SIZE)[0]
        col.append(text_el("sans-semibold", ln, V2_LEFT - dx0, y, DESC_SIZE, c["text"]))
        y += DESC_LH
    bottom = y - DESC_LH + 0.22 * DESC_SIZE
    shift = V2_PY + V2_PH / 2 - (top + bottom) / 2 - 8
    o.append(f'<g transform="translate(0 {shift:.1f})">' + "\n".join(col) + "</g>")

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
        sys.exit(
            f"{name}: entrance runs {mo.end:.2f} s; cover motion must end by {COVER_MOTION_MAX:g} s "
            f"(BRAND.md section 8)."
        )
    py = V2_PY + (V2_PH - ph) / 2
    o.append(f'<rect x="{V2_PX + 2}" y="{py + 8:g}" width="{V2_PW - 4}" height="{ph:g}" rx="14" fill="{c["panel-shadow"]}"/>')
    o.append(f'<rect x="{V2_PX}" y="{py:g}" width="{V2_PW}" height="{ph:g}" rx="12" fill="{c["desk"]}"/>')
    o.append(f'<g transform="translate({V2_PX} {py:g})"><g clip-path="url(#m)">{inner}</g>{ontop}</g>')
    o.append(
        f'<rect x="{V2_PX + 0.75}" y="{py + 0.75:g}" width="{V2_PW - 1.5}" height="{ph - 1.5:g}" rx="11.25" '
        f'fill="none" stroke="{c["line-strong"]}" stroke-opacity="0.55" stroke-width="1.5"/>'
    )

    fw, fh = (SW, SH) if social else (W, H)
    dx, dy = ((SW - W) / 2, (SH - H) / 2) if social else (0, 0)
    rx = 0 if social else 12
    label = escape(f"{name}: {desc.rstrip('.')}", {'"': "&quot;"})
    defs = f"<defs>{cyclorama_defs(c, fw, fh, rx, theme, (V2_PW, ph, 12))}</defs>"
    field = cyclorama_field(c, fw, fh, rx, theme)
    m = 40 if social else 32
    mark = corner_mark(c, theme, dx + V2_LEFT, fh - m - 28, 40)
    body = "\n".join(x for x in o if x)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fw} {fh}" width="{fw}" height="{fh}" '
        f'role="img" aria-label="{label}">\n{mo.css()}\n{defs}\n<g clip-path="url(#c)">{field}\n'
        f'<g transform="translate({dx} {dy})">\n{body}\n</g>\n{mark}</g></svg>\n'
    )


def compose(cfg, theme, base, social=False):
    if cfg.get("layout", "v2") == "v1":
        return compose_v1(cfg, theme, base, social)
    return compose_v2(cfg, theme, base, social)


# ---------------------------------------------------------------- preview sheet
def preview(cfg, base, path):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("--preview needs pillow: pip install pillow")

    def render(svg, width):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "p.png")
            render_png(svg, p, width)
            return Image.open(io.BytesIO(open(p, "rb").read())).convert("RGB")

    pad, gap, head = 40, 28, 28
    rows = []
    for theme in ("dark", "light"):
        svg, soc = compose(cfg, theme, base), compose(cfg, theme, base, social=True)
        rows.append((theme, render(svg, 1200), render(svg, 830), render(svg, 400), render(soc, 400)))
    sw = pad * 2 + max(1200, 830 + gap + 400)
    block = head + 560 + gap + head + 387 + gap
    sheet = Image.new("RGB", (sw, pad + 2 * block + pad), "#14161D")
    d = ImageDraw.Draw(sheet)
    y = pad
    for theme, full, mid, small, soc in rows:
        tn = "LX 263 Dark" if theme == "dark" else "LX 512 Light"
        d.text((pad, y + 6), f"{cfg['name']}  |  {tn}  |  1200px cover PNG", fill="#D2D6E0")
        sheet.paste(full, (pad, y + head))
        y += head + 560 + gap
        d.text((pad, y + 6), "830px (README column)", fill="#D2D6E0")
        d.text((pad + 830 + gap, y + 6), "400px (cover, then social card)", fill="#D2D6E0")
        sheet.paste(mid, (pad, y + head))
        sheet.paste(small, (pad + 830 + gap, y + head))
        sheet.paste(soc, (pad + 830 + gap, y + head + small.height + 14))
        y += head + max(mid.height, small.height + 14 + soc.height) + gap
    sheet = sheet.crop((0, 0, sw, y + pad - gap))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    sheet.save(path, optimize=True)


def main():
    ap = argparse.ArgumentParser(description="RFS Cyclorama Dawn cover + social preview generator")
    ap.add_argument("config", help="path to cover.toml")
    ap.add_argument("--out", help="output directory (default: next to cover.toml)")
    ap.add_argument("--preview", metavar="FILE", help="also write a preview sheet PNG")
    ap.add_argument("--layout", choices=("v1", "v2"), help="override cover.toml's layout")
    a = ap.parse_args()
    try:
        with open(a.config, "rb") as fh:
            cfg = tomllib.load(fh)
    except (OSError, tomllib.TOMLDecodeError) as e:
        sys.exit(f"{a.config}: {e}")
    if a.layout:
        cfg["layout"] = a.layout
    if cfg.get("layout", "v2") not in ("v1", "v2"):
        sys.exit(f"layout must be 'v1' or 'v2', not {cfg['layout']!r}")
    base = os.path.dirname(os.path.abspath(a.config))
    for k in ("name", "description"):
        if not isinstance(cfg.get(k), str) or not cfg[k].strip():
            sys.exit(f"cover.toml needs {k} = \"...\"")
    out = a.out or base
    os.makedirs(out, exist_ok=True)
    for theme in ("dark", "light"):
        svg = compose(cfg, theme, base)
        p = os.path.join(out, f"cover-{theme}.svg")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(svg)
        render_png(svg, os.path.join(out, f"cover-{theme}.png"))
        render_png(compose(cfg, theme, base, social=True), os.path.join(out, f"social-{theme}.png"))
    for f in (
        "cover-dark.svg",
        "cover-light.svg",
        "cover-dark.png",
        "cover-light.png",
        "social-dark.png",
        "social-light.png",
    ):
        print("wrote", os.path.join(out, f))
    if a.preview:
        preview(cfg, base, a.preview)
        print("wrote", a.preview)


if __name__ == "__main__":
    main()
