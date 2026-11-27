#!/usr/bin/env python3
"""Generate org-level Cyclorama Dawn studio art: profile banner, org social card, social header.

usage:
    python3 make-org-art.py

Reads brand/org.toml and writes:
    assets/rfs-banner-{dark,light}.svg                1200x400  static standard (zero keyframes)
    assets/rfs-banner-{dark,light}-animated.svg       1200x400  animated one-shot (1.22s DMX bring-up)
    brand/lockup/rfs-banner-{dark,light}-1600.png     1600x533  static raster export
    brand/social/rfs-social-org-{dark,light}.svg      1280x640  static social card
    brand/social/rfs-social-org-{dark,light}-1280x640.png
    brand/social/rfs-header-{dark,light}-1500x500.png 1500x500  static profile header

Art direction: Cyclorama Dawn Six-Channel Lighting Rig (LX 001 -> LX 512)
paired with monumental Big Shoulders Stencil RFS typography—zero fake terminal chrome.
Static standard ships zero <style> keyframes; animated one-shot wraps all CSS @keyframes
inside @media (prefers-reduced-motion: no-preference) and settles onto the exact static frame.
"""
import importlib.util, os, shutil, tomllib
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
_spec = importlib.util.spec_from_file_location("make_cover", os.path.join(HERE, "make-cover.py"))
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)
T = mc.text_el


# Six physical Cyclorama Dawn channels (LX 001 -> LX 512) with ascending dawn fader heights (0=bottom, 1=top)
CHANNELS = [
    ("001", "BLACKOUT", "#07080C", "#0D1017", "#192230", 0.14, False, "dark"),
    ("127", "STEEL",    "#09131C", "#133954", "#1F547A", 0.34, False, "dark"),
    ("263", "HORIZON",  "#122F46", "#1F547A", "#F06E2B", 0.54, True,  "dark"),
    ("389", "FLAME",    "#1A0A06", "#8B2F0B", "#F06E2B", 0.70, False, "dark"),
    ("455", "FROST",    "#DCE5ED", "#EFE4DB", "#FDF8F5", 0.84, False, "light"),
    ("512", "DAYLIGHT", "#EAEEF2", "#F5F7F9", "#FFFFFF", 0.94, False, "light"),
]


def channel_defs():
    """Vertical linear gradients for the 6 sculptural Cyclorama light columns."""
    out = []
    for i, (code, _, top_c, mid_c, bot_c, _, _, _) in enumerate(CHANNELS):
        out.append(
            f'<linearGradient id="ch-{i}" x1="0%" y1="0%" x2="0%" y2="100%">'
            f'<stop offset="0%" stop-color="{top_c}"/>'
            f'<stop offset="56%" stop-color="{mid_c}"/>'
            f'<stop offset="100%" stop-color="{bot_c}"/>'
            f'</linearGradient>'
        )
    return "".join(out)


def cyclorama_rig(c, theme, x, y, rw, rh, animated=False):
    """Sculptural 6-channel Cyclorama Dawn light-wall with precision DMX fader curve.

    When animated=True, emits class hooks and CSS keyframes (gated inside
    prefers-reduced-motion: no-preference) that bring the 6 hardware faders up from
    blackout baseline, draw the connecting curve, and lock LX 263 in <= 1.22s, settling
    onto the exact pixel coordinates of the static master.
    """
    o = []
    kf = []
    rules = []
    # Subtle architectural deck backplate
    deck_fill = "rgba(12,12,16,0.82)" if theme == "dark" else "rgba(255,255,255,0.88)"
    o.append(f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}" rx="12" fill="{deck_fill}" stroke="{c["line"]}" stroke-width="1.2"/>')

    # Top calibration strip
    pad_x = 22
    top_y = y + 26
    o.append(T("mono-semibold", "CYCLORAMA DAWN", x + pad_x, top_y, 10.5, c["steel-ink"], 1.3))
    o.append(T("mono", "LX 001 — 512", x + rw - pad_x, top_y, 10.5, c["mute"], 1.1, "end"))
    o.append(f'<rect x="{x + pad_x}" y="{y + 38}" width="{rw - 2 * pad_x}" height="1" fill="{c["line"]}"/>')

    # 6 vertical gel-lit architectural light columns
    n = len(CHANNELS)
    gap = 10
    cols_x = x + pad_x
    cols_w = rw - 2 * pad_x
    col_w = (cols_w - gap * (n - 1)) / n
    col_top = y + 52
    col_h = rh - 86
    col_bot = col_top + col_h

    # Precompute fader cap center positions for subtle connecting tension curve
    pts = []
    slot_top = col_top + 18
    slot_bot = col_bot - 18
    for i, (code, name, _, _, _, level, active, polarity) in enumerate(CHANNELS):
        cx = cols_x + i * (col_w + gap)
        mid_x = cx + col_w / 2.0
        # Base column fill + neutral hairline
        o.append(
            f'<rect x="{cx:.1f}" y="{col_top:.1f}" width="{col_w:.1f}" height="{col_h:.1f}" '
            f'rx="6" fill="url(#ch-{i})" stroke="{c["line"]}" stroke-width="1"/>'
        )
        # Subtle vertical fader slot inside each channel
        slot_stroke = "rgba(255,255,255,0.22)" if polarity == "dark" else "rgba(13,16,22,0.18)"
        o.append(f'<line x1="{mid_x:.1f}" y1="{slot_top:.1f}" x2="{mid_x:.1f}" y2="{slot_bot:.1f}" stroke="{slot_stroke}" stroke-width="1.5" stroke-linecap="round"/>')
        # Micro calibration ticks along slot
        for step in (0.25, 0.5, 0.75):
            ty = slot_bot - step * (slot_bot - slot_top)
            o.append(f'<line x1="{mid_x - 5:.1f}" y1="{ty:.1f}" x2="{mid_x + 5:.1f}" y2="{ty:.1f}" stroke="{slot_stroke}" stroke-width="1"/>')

        fy = slot_bot - level * (slot_bot - slot_top)
        pts.append((mid_x, fy))

        # Active LX 263 Beacon Orange frame + top lock bar
        if active:
            cls = ' class="rfs-lock"' if animated else ""
            o.append(
                f'<g{cls}>'
                f'<rect x="{cx:.1f}" y="{col_top:.1f}" width="{col_w:.1f}" height="{col_h:.1f}" '
                f'rx="6" fill="none" stroke="{c["beacon"]}" stroke-width="2"/>'
                f'<rect x="{cx + 8:.1f}" y="{col_top + 6:.1f}" width="{col_w - 16:.1f}" height="3" rx="1.5" fill="#FFFFFF"/>'
                f'</g>'
            )

        # Channel number underneath
        lbl_col = c["beacon-ink"] if active else c["mute"]
        lbl_font = "mono-semibold" if active else "mono"
        o.append(T(lbl_font, code, mid_x, col_bot + 20, 10.5, lbl_col, 0.8, "middle"))

    # Smooth connecting horizon curve linking the 6 DMX fader positions
    path_d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for k in range(len(pts) - 1):
        x0, y0 = pts[k]
        x1, y1 = pts[k + 1]
        mx = (x0 + x1) / 2.0
        path_d += f" C {mx:.1f} {y0:.1f} {mx:.1f} {y1:.1f} {x1:.1f} {y1:.1f}"
    if animated:
        o.append(f'<path class="rfs-curve" pathLength="100" d="{path_d}" fill="none" stroke="url(#rfs-rule)" stroke-width="2" opacity="0.85"/>')
        kf.append("@keyframes rfs-curve-draw{0%{stroke-dashoffset:100;opacity:0.15}100%{stroke-dashoffset:0;opacity:0.85}}")
        rules.append(f".rfs-curve{{stroke-dasharray:100;animation:rfs-curve-draw 780ms {mc.EASE} 240ms both}}")
        kf.append("@keyframes rfs-lock{0%{opacity:0.18}100%{opacity:1}}")
        rules.append(f".rfs-lock{{animation:rfs-lock 480ms {mc.EASE} 740ms both}}")
    else:
        o.append(f'<path d="{path_d}" fill="none" stroke="url(#rfs-rule)" stroke-width="2" opacity="0.85"/>')

    # Draw crisp physical hardware fader caps on top of curve
    for i, (mid_x, fy) in enumerate(pts):
        active = CHANNELS[i][6]
        cap_w = col_w * 0.54
        cap_h = 11 if active else 9
        cap_fill = "#FFFFFF" if active else ("#F4F5F8" if CHANNELS[i][7] == "dark" else "#0D1016")
        cap_stroke = "#050507" if cap_fill != "#0D1016" else "#FFFFFF"
        cap_el = (
            f'<rect x="{mid_x - cap_w / 2:.1f}" y="{fy - cap_h / 2:.1f}" width="{cap_w:.1f}" height="{cap_h}" '
            f'rx="2.5" fill="{cap_fill}" stroke="{cap_stroke}" stroke-width="1.2"/>'
            f'<line x1="{mid_x - cap_w / 2 + 4:.1f}" y1="{fy:.1f}" x2="{mid_x + cap_w / 2 - 4:.1f}" y2="{fy:.1f}" '
            f'stroke="{c["beacon"] if active else cap_stroke}" stroke-width="1.5"/>'
        )
        if animated:
            dy = max(8.0, slot_bot - fy)
            delay = 90 + i * 65
            o.append(f'<g class="rfs-cap rfs-cap-{i}">{cap_el}</g>')
            kf.append(
                f"@keyframes rfs-cap-in-{i}{{0%{{transform:translateY({dy:.1f}px);opacity:0.3}}"
                f"100%{{transform:translateY(0);opacity:1}}}}"
            )
            rules.append(f".rfs-cap-{i}{{animation:rfs-cap-in-{i} 680ms {mc.EASE} {delay}ms both}}")
        else:
            o.append(cap_el)

    rig_svg = "".join(o)
    if animated:
        return rig_svg, "".join(kf) + "".join(rules)
    return rig_svg


def wordmark(c, x, base, size, rule_h, animated=False):
    """Big Shoulders Stencil 'RFS' with Steel->Beacon horizon rule under the ink."""
    ls = 0.055 * size
    bx0, by0, bx1, _ = mc.ink_box("display", "RFS", size, ls)
    ox = x - bx0
    w = bx1 - bx0
    ry = base + 0.12 * size
    r_cls = ' class="rfs-hrule"' if animated else ""
    el = (
        T("display", "RFS", ox, base, size, c["text"], ls)
        + f'<rect{r_cls} x="{x:.1f}" y="{ry:.1f}" width="{w:.1f}" height="{rule_h}" rx="{rule_h / 2}" fill="url(#rfs-rule)"/>'
    )
    return el, x + w, ry + rule_h, by0


def text_block(c, tagline, x, cy, size, animated=False):
    tsz = round(size * 0.25)
    word, _, rule_b, top = wordmark(c, x, 0, size, max(5, round(size / 22)), animated=animated)
    t_base = rule_b + 0.34 * size
    o_base = t_base + 0.22 * size
    s_base = o_base + 0.16 * size
    bottom = s_base
    g = (
        word
        + T("sans-semibold", tagline, x, t_base, tsz, c["text"])
        + T("mono", "REAL-FRUIT-SNACKS  ·  RFS.TOOLS", x, o_base, 12.5, c["steel-ink"], 1.1)
        + T("mono", "17 OPEN-SOURCE TOOLS  ·  ZERO ACCOUNTS", x, s_base, 11.0, c["mute"], 0.9)
    )
    return f'<g transform="translate(0 {cy - (top + bottom) / 2:.1f})">{g}</g>'


def wrap_svg(w, h, label, defs, body, style=""):
    st = f"<style>{style}</style>\n" if style else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(label, {chr(34): "&quot;"})}">\n'
        f'{st}<defs>{defs}</defs>\n<g clip-path="url(#c)">{body}</g></svg>\n'
    )


def banner(c, cfg, theme, animated=False):
    w, h = 1200, 400
    defs = mc.cyclorama_defs(c, w, h, 12, theme) + channel_defs()
    tb = text_block(c, cfg["tagline"], 78, h / 2, 134, animated=animated)
    if animated:
        rig_svg, rig_css = cyclorama_rig(c, theme, 588, 44, 548, 312, animated=True)
        hrule_css = (
            f"@keyframes rfs-sweep{{0%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}"
            f".rfs-hrule{{transform-origin:78px 0;animation:rfs-sweep 520ms {mc.EASE} 40ms both}}"
        )
        style = f"@media (prefers-reduced-motion:no-preference){{{hrule_css}{rig_css}}}"
    else:
        rig_svg = cyclorama_rig(c, theme, 588, 44, 548, 312, animated=False)
        style = ""
    body = mc.cyclorama_field(c, w, h, 12, theme) + tb + rig_svg
    suffix = " (Animated One-Shot)" if animated else ""
    return wrap_svg(w, h, f"RFS: {cfg['tagline']} — Cyclorama Dawn{suffix}", defs, body, style=style)


def social(c, cfg, theme):
    w, h = 1280, 640
    defs = mc.cyclorama_defs(c, w, h, 0, theme) + channel_defs()
    body = (
        mc.cyclorama_field(c, w, h, 0, theme)
        + text_block(c, cfg["tagline"], 96, h / 2 - 14, 152)
        + cyclorama_rig(c, theme, 634, 134, 566, 368)
        + mc.corner_mark(c, theme, 96, h - 68, 40)
    )
    return wrap_svg(w, h, f"RFS: {cfg['tagline']} — Cyclorama Dawn", defs, body)


def header(c, cfg, theme):
    w, h = 1500, 500
    defs = mc.cyclorama_defs(c, w, h, 0, theme) + channel_defs()
    size = 148
    word, wr, rule_b, top = wordmark(c, 0, 0, size, 6)
    gap = 54
    tw = max(
        mc.advance("sans-semibold", cfg["tagline"], 44),
        mc.advance("mono", "REAL-FRUIT-SNACKS  ·  RFS.TOOLS", 14, 1.4),
    )
    # Compact 6-bar Cyclorama spectrum motif on right of lockup (clear of phone & avatar crop)
    bar_w, bar_gap = 12, 6
    bars_total = 6 * bar_w + 5 * bar_gap
    total = wr + gap + 1.5 + gap + tw + gap + bars_total
    x0 = (w - total) / 2.0
    mid = (top + rule_b) / 2.0
    right = (
        T("sans-semibold", cfg["tagline"], wr + 2 * gap + 1.5, mid + 2, 44, c["text"])
        + T("mono", "REAL-FRUIT-SNACKS  ·  RFS.TOOLS", wr + 2 * gap + 1.5, mid + 38, 14, c["mute"], 1.4)
    )
    div = f'<rect x="{wr + gap:.1f}" y="{top:.1f}" width="1.5" height="{rule_b - top:.1f}" fill="{c["line"]}"/>'
    bx_start = wr + 2 * gap + 1.5 + tw + gap
    bar_h = rule_b - top
    bars = []
    for i, (_, _, _, _, _, _, active, _) in enumerate(CHANNELS):
        bx = bx_start + i * (bar_w + bar_gap)
        stroke = c["beacon"] if active else c["line"]
        bars.append(
            f'<rect x="{bx:.1f}" y="{top:.1f}" width="{bar_w}" height="{bar_h:.1f}" rx="3" '
            f'fill="url(#ch-{i})" stroke="{stroke}" stroke-width="{1.5 if active else 0.8}"/>'
        )
    body = (
        mc.cyclorama_field(c, w, h, 0, theme)
        + f'<g transform="translate({x0:.1f} {h / 2 - mid:.1f})">{word}{div}{right}{"".join(bars)}</g>'
    )
    return wrap_svg(w, h, f"RFS: {cfg['tagline']} — Cyclorama Dawn", defs, body)


def main():
    with open(os.path.join(ROOT, "brand", "org.toml"), "rb") as fh:
        cfg = tomllib.load(fh)
    from PIL import Image
    out = []

    def write(rel, data):
        p = os.path.normpath(os.path.join(ROOT, rel))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)
        out.append(p)

    def png(rel, s, scale=None):
        p = os.path.normpath(os.path.join(ROOT, rel))
        if scale:
            mc.render_png(s, p, width=scale[0] * 2)
            Image.open(p).convert("RGB").resize(scale, Image.LANCZOS).save(p, optimize=True)
        else:
            mc.render_png(s, p)
        out.append(p)

    for theme in ("dark", "light"):
        c = mc.THEMES[theme]
        b = banner(c, cfg, theme, animated=False)
        b_anim = banner(c, cfg, theme, animated=True)
        write(f"assets/rfs-banner-{theme}.svg", b)
        write(f"assets/rfs-banner-{theme}-animated.svg", b_anim)
        write(f"docs/assets/rfs-banner-{theme}.svg", b)
        write(f"docs/assets/rfs-banner-{theme}-animated.svg", b_anim)
        png(f"brand/lockup/rfs-banner-{theme}-1600.png", b, (1600, 533))
        s = social(c, cfg, theme)
        write(f"brand/social/rfs-social-org-{theme}.svg", s)
        png(f"brand/social/rfs-social-org-{theme}-1280x640.png", s)
        png(f"brand/social/rfs-header-{theme}-1500x500.png", header(c, cfg, theme))
        for fname in (f"rfs-social-org-{theme}-1280x640.png", f"rfs-header-{theme}-1500x500.png"):
            src = os.path.join(ROOT, "brand", "social", fname)
            dst = os.path.join(ROOT, "docs", "assets", fname)
            shutil.copy2(src, dst)
            out.append(dst)

    for p in out:
        print("wrote", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
