#!/usr/bin/env python3
"""Generate all RFS Cyclorama Dawn marks, lockups, favicons, and web icons.

usage:
    python3 make-marks.py

Writes:
    brand/mark/rfs-mark-{dark,light}.svg + PNGs (16..1024)
    brand/mark/rfs-mark-{dark,light}-square.svg + 1024 PNG
    brand/mark/rfs-mark-small-{dark,light}.svg + 16,32,48 PNGs
    brand/mark/rfs-mark-mono-{white,ink}.svg + 1024 PNG
    brand/lockup/rfs-lockup-{horizontal,stacked}-{dark,light}.svg + PNGs
    brand/web/{icon.svg, favicon-16/32/48.png, favicon.ico, apple-touch-icon.png,
               icon-192.png, icon-512.png, icon-maskable-512.png,
               manifest.webmanifest, head.html}
    assets/{rfs-mark-dark.svg, rfs-mark-light.svg, rfs-mark-dark-512.png,
            rfs-lockup-dark.svg, rfs-lockup-light.svg}
"""
import importlib.util, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
_spec = importlib.util.spec_from_file_location("make_cover", os.path.join(HERE, "make-cover.py"))
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)

SIZES = (16, 32, 48, 64, 96, 128, 180, 192, 256, 400, 512, 1024)


def tile_svg(theme="dark", rx=14, size=64, small=False, mono=None, pad_scale=1.0):
    """64-unit Cyclorama Dawn RFS Monogram Tile with exact ink-box optical centering.

    Dark master unifies with the Cyclorama Avatar style: matte #050507 ground,
    lower Glacial Steel -> Maritime Beacon Orange horizon wash, crisp hairline
    frame, white stencil RFS, and a Steel -> Beacon horizontal bar underneath.
    """
    c = mc.THEMES[theme]
    defs = (
        '<defs>'
        '<linearGradient id="cyc-h" x1="0%" y1="0%" x2="100%" y2="0%">'
        '<stop offset="0%" stop-color="#133954"/>'
        '<stop offset="44%" stop-color="#1F547A"/>'
        '<stop offset="76%" stop-color="#CC5016"/>'
        '<stop offset="100%" stop-color="#F06E2B"/>'
        '</linearGradient>'
        '<linearGradient id="cyc-f" x1="0%" y1="0%" x2="0%" y2="100%">'
        '<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.08"/>'
        '<stop offset="74%" stop-color="#FFFFFF" stop-opacity="0.58"/>'
        '<stop offset="100%" stop-color="#FFFFFF" stop-opacity="1"/>'
        '</linearGradient>'
        '<mask id="cyc-m" maskContentUnits="objectBoundingBox">'
        '<rect width="1" height="1" fill="url(#cyc-f)"/>'
        '</mask>'
        '<linearGradient id="rule-d" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="#74B8E8"/>'
        '<stop offset="52%" stop-color="#3B85B8"/>'
        '<stop offset="100%" stop-color="#F06E2B"/>'
        '</linearGradient>'
        '<linearGradient id="rule-l" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="#18496B"/>'
        '<stop offset="52%" stop-color="#1F547A"/>'
        '<stop offset="100%" stop-color="#AD3D0A"/>'
        '</linearGradient>'
        '</defs>'
    )

    if mono is not None:
        fg = "#FFFFFF" if mono == "white" else "#0D1016"
        draw_sz = 29.0 * pad_scale
        draw_ls = draw_sz * 0.05
        bx0, by0, bx1, by1 = mc.ink_box("display", "RFS", draw_sz, draw_ls)
        ink_w = bx1 - bx0
        ink_h = by1 - by0
        gap = 5.0 * pad_scale
        bar_h = 3.6 * pad_scale
        group_h = ink_h + gap + bar_h
        group_top = (64.0 - group_h) / 2.0
        cx = 32.0 - (bx0 + bx1) / 2.0
        cy = group_top - by0
        bar_y = group_top + ink_h + gap
        bg_el = (
            f'<rect x="2" y="2" width="60" height="60" rx="{max(0, rx - 1)}" '
            f'fill="none" stroke="{fg}" stroke-width="3.5"/>'
        )
        glyph = mc.text_el("display", "RFS", cx, cy, draw_sz, fg, draw_ls)
        bar = f'<rect x="{32.0 - ink_w / 2.0:.2f}" y="{bar_y:.2f}" width="{ink_w:.2f}" height="{bar_h:.2f}" rx="{bar_h / 2.0:.2f}" fill="{fg}"/>'
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}" height="{size}" '
            f'role="img" aria-label="RFS">{bg_el}{glyph}{bar}</svg>\n'
        )

    draw_sz = (34.0 if small else 31.0) * pad_scale
    draw_ls = draw_sz * (0.04 if small else 0.05)
    bx0, by0, bx1, by1 = mc.ink_box("display", "RFS", draw_sz, draw_ls)
    ink_w = bx1 - bx0
    ink_h = by1 - by0
    gap = (4.2 if small else 5.0) * pad_scale
    bar_h = (4.4 if small else 3.8) * pad_scale
    group_h = ink_h + gap + bar_h
    group_top = (64.0 - group_h) / 2.0
    cx = 32.0 - (bx0 + bx1) / 2.0
    cy = group_top - by0
    bar_y = group_top + ink_h + gap

    if theme == "dark":
        wash_op = "0.86" if small else "0.74"
        frame_stroke = "#3B3E4A" if small else "rgba(255,255,255,0.16)"
        frame = (
            f'<rect x="0.75" y="0.75" width="62.5" height="62.5" rx="{max(0, rx - 0.75):g}" '
            f'fill="none" stroke="{frame_stroke}" stroke-width="1.5"/>'
            if rx > 0 else ""
        )
        bg_el = (
            f'<rect width="64" height="64" rx="{rx}" fill="#050507"/>'
            f'<rect width="64" height="64" rx="{rx}" fill="url(#cyc-h)" opacity="{wash_op}" mask="url(#cyc-m)"/>'
            f'{frame}'
        )
        glyph = mc.text_el("display", "RFS", cx, cy, draw_sz, "#F4F5F8", draw_ls)
        bar = f'<rect x="{32.0 - ink_w / 2.0:.2f}" y="{bar_y:.2f}" width="{ink_w:.2f}" height="{bar_h:.2f}" rx="{bar_h / 2.0:.2f}" fill="url(#rule-d)"/>'
    else:
        inset = 0.75 if rx > 0 else 0
        box = (
            f'x="{inset}" y="{inset}" width="{64 - 2 * inset}" height="{64 - 2 * inset}" '
            f'rx="{max(0, rx - inset):g}"'
        )
        # Alabaster ground with the same lower Steel -> Beacon horizon wash as the dark
        # master, at the light-mode strength of the brand site's floor wash (0.36).
        bg_el = (
            f'<rect {box} fill="#FFFFFF"/>'
            f'<rect width="64" height="64" rx="{rx}" fill="url(#cyc-h)" opacity="0.36" mask="url(#cyc-m)"/>'
        )
        if rx > 0:
            bg_el += f'<rect {box} fill="none" stroke="{c["line"]}" stroke-width="1.5"/>'
        glyph = mc.text_el("display", "RFS", cx, cy, draw_sz, c["text"], draw_ls)
        bar = f'<rect x="{32.0 - ink_w / 2.0:.2f}" y="{bar_y:.2f}" width="{ink_w:.2f}" height="{bar_h:.2f}" rx="{bar_h / 2.0:.2f}" fill="url(#rule-l)"/>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}" height="{size}" '
        f'role="img" aria-label="RFS">{defs}{bg_el}{glyph}{bar}</svg>\n'
    )


def lockup_horizontal(theme="dark"):
    c = mc.THEMES[theme]
    tile_inner = tile_svg(theme, rx=14, size=64).split(">", 1)[1].rsplit("</svg>", 1)[0]
    word_sz = 36
    word_ls = word_sz * 0.055
    bx0, by0, bx1, by1 = mc.ink_box("display", "REAL-FRUIT-SNACKS", word_sz, word_ls)
    word_w = bx1 - bx0
    wx = 82 - bx0
    wy = 34.0
    w = int(round(82 + word_w + 10))
    h = 64
    word = mc.text_el("display", "REAL-FRUIT-SNACKS", wx, wy, word_sz, c["text"], word_ls)
    rule_id = "rule-d" if theme == "dark" else "rule-l"
    rule = f'<rect x="82" y="40.5" width="{word_w:.1f}" height="3" rx="1.5" fill="url(#{rule_id})"/>'
    sub_bx0 = mc.ink_box("mono", "BUILT LOCAL-FIRST.", 11.5, 1.1)[0]
    sub = mc.text_el("mono", "BUILT LOCAL-FIRST.", 82 - sub_bx0, 58.5, 11.5, c["mute"], 1.1)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Real-Fruit-Snacks">{tile_inner}{word}{rule}{sub}</svg>\n'
    )


def lockup_stacked(theme="dark"):
    c = mc.THEMES[theme]
    tile_inner = tile_svg(theme, rx=14, size=64).split(">", 1)[1].rsplit("</svg>", 1)[0]
    defs_part, body_part = tile_inner.split("</defs>", 1)
    defs_part += "</defs>"
    word_sz = 36
    word_ls = word_sz * 0.055
    bx0, by0, bx1, by1 = mc.ink_box("display", "REAL-FRUIT-SNACKS", word_sz, word_ls)
    word_w = bx1 - bx0
    w = max(296, int(round(word_w + 36)))
    h = 188
    wx = w / 2.0 - (bx0 + bx1) / 2.0
    wy = 140.0
    word = mc.text_el("display", "REAL-FRUIT-SNACKS", wx, wy, word_sz, c["text"], word_ls)
    rule_id = "rule-d" if theme == "dark" else "rule-l"
    rule = f'<rect x="{(w - word_w) / 2.0:.1f}" y="148" width="{word_w:.1f}" height="3" rx="1.5" fill="url(#{rule_id})"/>'
    sb0, _, sb1, _ = mc.ink_box("mono", "BUILT LOCAL-FIRST.", 11.0, 1.1)
    sub_x = w / 2.0 - (sb0 + sb1) / 2.0
    sub = mc.text_el("mono", "BUILT LOCAL-FIRST.", sub_x, 170, 11.0, c["mute"], 1.1)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Real-Fruit-Snacks">{defs_part}'
        f'<g transform="translate({(w - 84) / 2.0:.1f} 12) scale({84 / 64:.4f})">{body_part}</g>'
        f'{word}{rule}{sub}</svg>\n'
    )


def write_text(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    return p


def main():
    wrote = []

    for theme in ("dark", "light"):
        svg = tile_svg(theme, rx=14)
        wrote.append(write_text(f"brand/mark/rfs-mark-{theme}.svg", svg))
        wrote.append(write_text(f"assets/rfs-mark-{theme}.svg", svg))
        for sz in SIZES:
            p = os.path.join(ROOT, f"brand/mark/rfs-mark-{theme}-{sz}.png")
            mc.render_png(svg, p, width=sz)
            wrote.append(p)

        sq = tile_svg(theme, rx=0)
        wrote.append(write_text(f"brand/mark/rfs-mark-{theme}-square.svg", sq))
        p_sq = os.path.join(ROOT, f"brand/mark/rfs-mark-{theme}-square-1024.png")
        mc.render_png(sq, p_sq, width=1024)
        wrote.append(p_sq)

        sm = tile_svg(theme, rx=14, small=True)
        wrote.append(write_text(f"brand/mark/rfs-mark-small-{theme}.svg", sm))
        for sz in (16, 32, 48):
            p_sm = os.path.join(ROOT, f"brand/mark/rfs-mark-small-{theme}-{sz}.png")
            mc.render_png(sm, p_sm, width=sz)
            wrote.append(p_sm)

        lh = lockup_horizontal(theme)
        wrote.append(write_text(f"brand/lockup/rfs-lockup-horizontal-{theme}.svg", lh))
        wrote.append(write_text(f"assets/rfs-lockup-{theme}.svg", lh))
        p_lh = os.path.join(ROOT, f"brand/lockup/rfs-lockup-horizontal-{theme}-800.png")
        mc.render_png(lh, p_lh, width=800)
        wrote.append(p_lh)

        ls_svg = lockup_stacked(theme)
        wrote.append(write_text(f"brand/lockup/rfs-lockup-stacked-{theme}.svg", ls_svg))
        p_ls = os.path.join(ROOT, f"brand/lockup/rfs-lockup-stacked-{theme}-512.png")
        mc.render_png(ls_svg, p_ls, width=512)
        wrote.append(p_ls)

    for mono in ("white", "ink"):
        m_svg = tile_svg("dark" if mono == "white" else "light", rx=14, mono=mono)
        wrote.append(write_text(f"brand/mark/rfs-mark-mono-{mono}.svg", m_svg))
        p_m = os.path.join(ROOT, f"brand/mark/rfs-mark-mono-{mono}-1024.png")
        mc.render_png(m_svg, p_m, width=1024)
        wrote.append(p_m)

    # Top-level 512 PNG mark in assets/
    p_a512 = os.path.join(ROOT, "assets/rfs-mark-dark-512.png")
    mc.render_png(tile_svg("dark", rx=14), p_a512, width=512)
    wrote.append(p_a512)

    # Web icons & PWA bundle in brand/web/
    icon_svg = tile_svg("dark", rx=14, small=True)
    wrote.append(write_text("brand/web/icon.svg", icon_svg))
    ico_imgs = []
    for sz in (16, 32, 48):
        p = os.path.join(ROOT, f"brand/web/favicon-{sz}.png")
        mc.render_png(icon_svg, p, width=sz)
        wrote.append(p)
        ico_imgs.append(Image.open(p).convert("RGBA"))
    ico_path = os.path.join(ROOT, "brand/web/favicon.ico")
    ico_imgs[2].save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    wrote.append(ico_path)

    apple_svg = tile_svg("dark", rx=0, pad_scale=0.88)
    p_apple = os.path.join(ROOT, "brand/web/apple-touch-icon.png")
    mc.render_png(apple_svg, p_apple, width=180)
    wrote.append(p_apple)

    dark_master = tile_svg("dark", rx=14)
    for sz in (192, 512):
        p = os.path.join(ROOT, f"brand/web/icon-{sz}.png")
        mc.render_png(dark_master, p, width=sz)
        wrote.append(p)

    maskable_svg = tile_svg("dark", rx=0, pad_scale=0.72)
    p_mask = os.path.join(ROOT, "brand/web/icon-maskable-512.png")
    mc.render_png(maskable_svg, p_mask, width=512)
    wrote.append(p_mask)

    manifest = {
        "name": "Real-Fruit-Snacks",
        "short_name": "RFS",
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
        "theme_color": "#050507",
        "background_color": "#050507",
    }
    wrote.append(write_text("brand/web/manifest.webmanifest", json.dumps(manifest, indent=2) + "\n"))
    wrote.append(
        write_text(
            "brand/web/head.html",
            '<link rel="icon" href="/icon.svg" type="image/svg+xml">\n'
            '<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
            '<link rel="manifest" href="/manifest.webmanifest">\n'
            '<meta name="theme-color" content="#050507" media="(prefers-color-scheme: dark)">\n'
            '<meta name="theme-color" content="#f5f7f9" media="(prefers-color-scheme: light)">\n',
        )
    )
    print(f"make-marks.py wrote {len(wrote)} files.")


if __name__ == "__main__":
    main()
