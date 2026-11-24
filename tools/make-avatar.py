#!/usr/bin/env python3
"""Generate the RFS Cyclorama Dawn profile avatar (GitHub, Discord, X, Mastodon).

usage:
    python3 make-avatar.py [--out DIR]

Writes (default DIR: brand/social/):
    rfs-avatar-dark.svg           outlined, 1024x1024
    rfs-avatar-dark-1024.png      upload to GitHub (Settings > Profile picture)
    rfs-avatar-dark-512.png
    rfs-avatar-dark-256.png
    rfs-avatar-light.svg
    rfs-avatar-light-512.png

Full-bleed square, zero transparent corners, optically centered Big Shoulders
Stencil "RFS" + Steel-to-Beacon horizon rule comfortably inside the inscribed
circle so circular avatar crops never clip the mark.
"""
import argparse, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("make_cover", os.path.join(HERE, "make-cover.py"))
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)

N = 1024


def avatar(theme="dark"):
    c = mc.THEMES[theme]
    size = 460
    ls = size * 0.055
    bx0, by0, bx1, by1 = mc.ink_box("display", "RFS", size, ls)
    rule_h = 34
    gap = 46
    total_h = (by1 - by0) + gap + rule_h
    top = (N - total_h) / 2
    base = top - by0
    x = N / 2 - (bx0 + bx1) / 2
    rule_w = bx1 - bx0
    rule_x = N / 2 - rule_w / 2
    rule_y = base + gap

    wash_op = "0.72" if theme == "dark" else "0.18"
    rule_start = "#74B8E8" if theme == "dark" else "#18496B"
    rule_mid = "#3B85B8" if theme == "dark" else "#1F547A"
    rule_end = "#F06E2B" if theme == "dark" else "#AD3D0A"

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}" width="{N}" height="{N}" '
        f'role="img" aria-label="RFS">'
        f'<defs>'
        f'<linearGradient id="cyc-h" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="#133954"/>'
        f'<stop offset="44%" stop-color="#1F547A"/>'
        f'<stop offset="76%" stop-color="#CC5016"/>'
        f'<stop offset="100%" stop-color="#F06E2B"/>'
        f'</linearGradient>'
        f'<linearGradient id="cyc-fade" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>'
        f'<stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.08"/>'
        f'<stop offset="74%" stop-color="#FFFFFF" stop-opacity="0.58"/>'
        f'<stop offset="100%" stop-color="#FFFFFF" stop-opacity="1"/>'
        f'</linearGradient>'
        f'<mask id="cyc-m"><rect width="{N}" height="{N}" fill="url(#cyc-fade)"/></mask>'
        f'<linearGradient id="rule" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="{rule_start}"/>'
        f'<stop offset="50%" stop-color="{rule_mid}"/>'
        f'<stop offset="100%" stop-color="{rule_end}"/>'
        f'</linearGradient>'
        f'</defs>'
        f'<rect width="{N}" height="{N}" fill="{c["bg"]}"/>'
        f'<rect width="{N}" height="{N}" fill="url(#cyc-h)" opacity="{wash_op}" mask="url(#cyc-m)"/>'
        f'<path d="{mc.text_path("display", "RFS", x, base, size, ls)}" fill="{c["text"]}"/>'
        f'<rect x="{rule_x:.1f}" y="{rule_y:.1f}" width="{rule_w:.1f}" height="{rule_h}" '
        f'rx="{rule_h / 2}" fill="url(#rule)"/>'
        f'</svg>\n'
    )


def main():
    ap = argparse.ArgumentParser(description="RFS Cyclorama Dawn profile avatar generator")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "brand", "social"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    for theme, sizes in (("dark", (1024, 512, 256)), ("light", (512,))):
        svg = avatar(theme)
        svg_path = os.path.join(a.out, f"rfs-avatar-{theme}.svg")
        with open(svg_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(svg)
        print("wrote", svg_path)
        for sz in sizes:
            png_path = os.path.join(a.out, f"rfs-avatar-{theme}-{sz}.png")
            mc.render_png(svg, png_path, width=sz)
            print("wrote", png_path)


if __name__ == "__main__":
    main()
