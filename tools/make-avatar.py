#!/usr/bin/env python3
"""Generate the RFS profile picture (GitHub org avatar, other square avatars).

usage:
    python3 make-avatar.py [--out DIR]

Writes (default DIR: brand/social/):
    rfs-avatar-dark.svg           outlined, 1024x1024
    rfs-avatar-dark-1024.png      upload this one to GitHub (Settings > Profile picture)
    rfs-avatar-dark-512.png
    rfs-avatar-dark-256.png

Same look as the repo covers (BRAND.md section 7): Nightshift surface, dot grid,
Ember glow from the lower right (28%, stronger than the covers' so it shows at
40px), "RFS" in Plex Mono 600 at -0.05em, and an Ember rule exactly as wide as
the word. Full-bleed square, no inner tile and no
transparent corners: GitHub rounds or circles avatars itself. The word and rule
sit inside the inscribed circle, so a circular crop doesn't clip them.

Shares fonts, colour tokens and text outlining with make-cover.py.
Requires Python 3.11+, fonttools and resvg-py (or cairosvg).
"""
import argparse, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("make_cover", os.path.join(HERE, "make-cover.py"))
mc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(mc)

N = 1024


def avatar(theme="dark"):
    c = mc.THEMES[theme]
    size, rule_h = 440, 40
    ls = -0.05 * size
    il, ir = mc.ink_extent("RFS", size, ls)
    cap = 0.698 * size                       # Plex Mono cap height
    gap = 0.20 * size                        # baseline to rule
    top = (N - (cap + gap + rule_h)) / 2     # centre cap-top..rule-bottom
    base = top + cap
    x = N / 2 - (il + ir) / 2
    step, r = 48, 2.6
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}" width="{N}" height="{N}" '
            f'role="img" aria-label="RFS">'
            f'<defs><pattern id="g" width="{step}" height="{step}" patternUnits="userSpaceOnUse" x="{step/2}" y="{step/2}">'
            f'<circle cx="{r}" cy="{r}" r="{r}" fill="{c["line"]}"/></pattern>'
            f'<radialGradient id="r" cx="78%" cy="108%" r="80%">'
            f'<stop offset="0" stop-color="{c["ember"]}" stop-opacity="{0.28 if theme == "dark" else 0}"/>'
            f'<stop offset="1" stop-color="rgba(0,0,0,0)"/></radialGradient></defs>'
            f'<rect width="{N}" height="{N}" fill="{c["surface"]}"/>'
            f'<rect width="{N}" height="{N}" fill="url(#g)"/>'
            f'<rect width="{N}" height="{N}" fill="url(#r)"/>'
            f'<path d="{mc.text_path("mono-semibold", "RFS", x, base, size, ls)}" fill="{c["text"]}"/>'
            f'<rect x="{x + il:.1f}" y="{base + gap:.1f}" width="{ir - il:.1f}" height="{rule_h}" '
            f'rx="{rule_h / 2}" fill="{c["ember"]}"/></svg>\n')


def main():
    ap = argparse.ArgumentParser(description="RFS profile picture generator")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "brand", "social"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    svg = avatar("dark")
    p = os.path.join(a.out, "rfs-avatar-dark.svg")
    open(p, "w", encoding="utf-8", newline="\n").write(svg); print("wrote", p)
    big = os.path.join(a.out, "rfs-avatar-dark-1024.png")
    mc.render_png(svg, big); print("wrote", big)
    try:
        from PIL import Image
    except ImportError:
        print("pillow not installed: skipped the 512 and 256 PNGs"); return
    im = Image.open(big).convert("RGB")
    for s in (512, 256):
        q = os.path.join(a.out, f"rfs-avatar-dark-{s}.png")
        im.resize((s, s), Image.LANCZOS).save(q, optimize=True); print("wrote", q)


if __name__ == "__main__":
    main()
