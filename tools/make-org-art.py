#!/usr/bin/env python3
"""Generate the org-level art: profile banner, org social preview, X header.

usage:
    python3 make-org-art.py

Reads brand/org.toml (tagline + the tool list shown in the panel) and writes:
    assets/rfs-banner-{dark,light}.svg                1200x400  org profile README header
    brand/lockup/rfs-banner-{dark,light}-1600.png     1600x533  same, as PNG
    brand/social/rfs-social-org-{dark,light}.svg      1280x640  GitHub social preview (.github repo, org links)
    brand/social/rfs-social-org-{dark,light}-1280x640.png
    brand/social/rfs-header-{dark,light}-1500x500.png  X / Mastodon / Bluesky header

Same look as the repo covers (BRAND.md section 7): bg, 26px dot grid, Ember glow
from the lower right (Nightshift only), "RFS" in Plex Mono 600 at -0.05em with an
Ember rule as wide as the word, the tagline in Plex Sans 600, REAL-FRUIT-SNACKS
in Plex Mono caps. The banner and social preview add the cover's terminal panel,
listing the tools from org.toml. The header has no panel: X puts the avatar over
its lower left and crops the top and bottom on phones, so it is one centred line.

Shares fonts, colour tokens and text outlining with make-cover.py.
Requires Python 3.11+, fonttools and resvg-py (or cairosvg).
"""
import importlib.util, os, sys, tomllib
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
_spec = importlib.util.spec_from_file_location("make_cover", os.path.join(HERE, "make-cover.py"))
mc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(mc)
T = mc.text_el


def field(c, w, h, rx, glow_cx="78%"):
    defs = (f'<pattern id="g" width="26" height="26" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.2" cy="1.2" r="1.2" fill="{c["dots"]}"/></pattern>'
            f'<radialGradient id="r" cx="{glow_cx}" cy="110%" r="70%"><stop offset="0" stop-color="{c["glow"]}"/>'
            f'<stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient>'
            f'<clipPath id="c"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    body = (f'<rect width="{w}" height="{h}" fill="{c["bg"]}"/><rect width="{w}" height="{h}" fill="url(#g)"/>'
            f'<rect width="{w}" height="{h}" fill="url(#r)"/>')
    return defs, body


def wordmark(c, x, base, size, rule_h):
    """'RFS' with its baseline at `base`, Ember rule under the ink. Returns
    (svg, ink right edge, rule bottom)."""
    ls = -0.05 * size
    il, ir = mc.ink_extent("RFS", size, ls)
    ry = base + 0.16 * size
    return (T("mono-semibold", "RFS", x, base, size, c["text"], ls)
            + f'<rect x="{x + il:.1f}" y="{ry:.1f}" width="{ir - il:.1f}" height="{rule_h}" '
              f'rx="{rule_h / 2}" fill="{c["ember"]}"/>'), x + ir, ry + rule_h


def panel(c, tools, x, y, pw, ph):
    """The cover's terminal panel, listing the org's tools."""
    if not 1 <= len(tools) <= 7:
        sys.exit("org.toml: 1-7 tools")
    size, lh, px = 14, 28, 24
    cw = mc.advance("mono", "m", size)                       # Plex Mono is monospaced
    cols = (max(len(t[0]) for t in tools) + 2, max(len(t[1]) for t in tools) + 2)
    o = [f'<rect width="{pw}" height="{ph}" fill="{c["code-bg"]}"/>',
         f'<rect width="{pw}" height="34" fill="{c["surface"]}"/>',
         f'<rect y="34" width="{pw}" height="1" fill="{c["line"]}"/>']
    o += [f'<circle cx="{20 + i * 16}" cy="17" r="4.5" fill="{c["line"]}"/>' for i in range(3)]
    o.append(T("mono", "pwsh", pw / 2, 21.5, 12, c["mute"], 0.5, "middle"))
    ty = 70                                                  # first line, as on the covers
    if ty + lh * len(tools) + 16 > ph:
        sys.exit("org.toml: too many tools for the panel")
    o.append(T("mono-semibold", "$", px, ty, size, c["ember"]))
    o.append(T("mono", "gh repo list Real-Fruit-Snacks", px + 2 * cw, ty, size, c["text"]))
    for name, lang, what in tools:
        ty += lh
        if (cols[0] + cols[1] + len(what)) * cw > pw - 2 * px:
            sys.exit(f"org.toml: row too wide for the panel: {name} / {what}")
        o.append(T("mono", name, px, ty, size, c["text"]))
        o.append(T("mono", lang, px + cols[0] * cw, ty, size, c["amber"]))
        o.append(T("mono", what, px + (cols[0] + cols[1]) * cw, ty, size, c["mute"]))
    o.append(f'<rect x="{px}" y="{ty + lh - 13}" width="8" height="16" fill="{c["ember"]}"/>')
    return (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="10" fill="{c["desk"]}"/>'
            f'<clipPath id="m"><rect width="{pw}" height="{ph}" rx="10"/></clipPath>'
            f'<g transform="translate({x} {y})"><g clip-path="url(#m)">{"".join(o)}</g></g>'
            f'<rect x="{x + .5}" y="{y + .5}" width="{pw - 1}" height="{ph - 1}" rx="9.5" fill="none" stroke="{c["line"]}"/>')


def text_block(c, tagline, x, cy, size):
    """Wordmark / tagline / org name, left-aligned at x, centred on cy."""
    cap = 0.698 * size
    tsz = round(size * 0.30)
    word, _, rule_b = wordmark(c, x, 0, size, max(5, round(size / 22)))
    t_base = rule_b + 0.62 * size
    o_base = t_base + 0.36 * size
    top, bottom = -cap, o_base
    g = (word + T("sans-semibold", tagline, x, t_base, tsz, c["text"])
         + T("mono", "REAL-FRUIT-SNACKS", x, o_base, 13, c["mute"], 1.6))
    return f'<g transform="translate(0 {cy - (top + bottom) / 2:.1f})">{g}</g>'


def svg(w, h, label, defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(label, {chr(34): "&quot;"})}">\n<defs>{defs}</defs>\n'
            f'<g clip-path="url(#c)">{body}</g></svg>\n')


def banner(c, cfg):
    w, h = 1200, 400
    defs, f = field(c, w, h, 12)
    body = f + text_block(c, cfg["tagline"], 88, h / 2, 120) + panel(c, cfg["tools"], 640, 52, 480, 296)
    return svg(w, h, f"RFS: {cfg['tagline']}", defs, body)


def social(c, cfg):
    w, h = 1280, 640
    defs, f = field(c, w, h, 0)
    body = f + text_block(c, cfg["tagline"], 112, h / 2, 140) + panel(c, cfg["tools"], 680, 172, 480, 296)
    return svg(w, h, f"RFS: {cfg['tagline']}", defs, body)


def header(c, cfg):
    """One line, centred: RFS + rule | tagline over REAL-FRUIT-SNACKS."""
    w, h = 1500, 500
    defs, f = field(c, w, h, 0, "50%")
    size = 128
    word, wr, rule_b = wordmark(c, 0, 0, size, 6)
    cap = 0.698 * size
    gap = 56
    tw = mc.advance("sans-semibold", cfg["tagline"], 44)
    total = wr + gap + 1 + gap + tw
    x0 = (w - total) / 2
    mid = (-cap + rule_b) / 2
    right = (T("sans-semibold", cfg["tagline"], wr + 2 * gap + 1, mid + 4, 44, c["text"])
             + T("mono", "REAL-FRUIT-SNACKS", wr + 2 * gap + 1, mid + 38, 14, c["mute"], 1.8))
    div = f'<rect x="{wr + gap:.1f}" y="{-cap:.1f}" width="1" height="{rule_b + cap:.1f}" fill="{c["line"]}"/>'
    body = f + f'<g transform="translate({x0:.1f} {h / 2 - mid:.1f})">{word}{div}{right}</g>'
    return svg(w, h, f"RFS: {cfg['tagline']}", defs, body)


def main():
    cfg = tomllib.load(open(os.path.join(ROOT, "brand", "org.toml"), "rb"))
    try:
        from PIL import Image
    except ImportError:
        Image = None
    out = []

    def write(rel, data):
        p = os.path.normpath(os.path.join(ROOT, rel))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write(data); out.append(p)

    def png(rel, s, scale=None):
        p = os.path.normpath(os.path.join(ROOT, rel))
        mc.render_png(s, p)
        if scale:
            if not Image:
                sys.exit("pillow is needed for the 1600px banner PNG: pip install pillow")
            # render at 2x and downsample: crisper than resvg at 1.33x
            mc.render_png(s.replace('width="1200" height="400"', 'width="2400" height="800"', 1), p)
            Image.open(p).convert("RGB").resize(scale, Image.LANCZOS).save(p, optimize=True)
        out.append(p)

    for theme in ("dark", "light"):
        c = mc.THEMES[theme]
        b = banner(c, cfg)
        write(f"assets/rfs-banner-{theme}.svg", b)
        png(f"brand/lockup/rfs-banner-{theme}-1600.png", b, (1600, 533))
        s = social(c, cfg)
        write(f"brand/social/rfs-social-org-{theme}.svg", s)
        png(f"brand/social/rfs-social-org-{theme}-1280x640.png", s)
        png(f"brand/social/rfs-header-{theme}-1500x500.png", header(c, cfg))
    for p in out:
        print("wrote", os.path.relpath(p, os.getcwd()))


if __name__ == "__main__":
    main()
