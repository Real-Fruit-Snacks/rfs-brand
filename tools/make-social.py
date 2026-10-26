#!/usr/bin/env python3
"""Generate a 1280x640 GitHub social-preview PNG for a repo.
usage: python3 make-social.py <repo-name> "<one-line description>" [dark|light]
Requires: cairosvg, fonttools, IBM Plex Mono SemiBold (fonts/IBMPlexMono-SemiBold.ttf) and IBM Plex Sans Regular (fonts/IBMPlexSans-Regular.ttf).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
MONO = TTFont(os.path.join(HERE, "fonts/IBMPlexMono-SemiBold.ttf"))
SANS = TTFont(os.path.join(HERE, "fonts/IBMPlexSans-Regular.ttf"))

def path(font, text, x, y, size, ls=0, anchor="start"):
    upm = font["head"].unitsPerEm; gs = font.getGlyphSet(); cmap = font.getBestCmap(); k = size/upm
    names = [cmap.get(ord(ch)) or cmap[ord("?")] for ch in text]
    total = sum(gs[n].width*k for n in names) + ls*(len(names)-1)
    px = x - total/2 if anchor == "middle" else x
    d = []
    for n in names:
        sp = SVGPathPen(gs); gs[n].draw(TransformPen(sp, (k,0,0,-k,px,y))); d.append(sp.getCommands()); px += gs[n].width*k + ls
    return " ".join(d)

T = {"dark": dict(bg="#0c0d10", tile="#1a1d24", fg="#fff", ember="#ff6a3d", text="#e8e6e1", mute="#8a8f99"),
     "light": dict(bg="#f6f5f2", tile="#1a1b1e", fg="#fff", ember="#c43f11", text="#1a1b1e", mute="#6b6f78")}

repo, desc = sys.argv[1], sys.argv[2]
theme = sys.argv[3] if len(sys.argv) > 3 else "dark"
c = T[theme]
s = 96; x0 = 120; y0 = 255   # lockup block (tile top to description) centred on the 640 height
tile = (f'<rect x="{x0}" y="{y0}" width="{s}" height="{s}" rx="{14*s/64}" fill="{c["tile"]}"/>'
        f'<path d="{path(MONO,"RFS",x0+s/2, y0+64, 42, -2, "middle")}" fill="{c["fg"]}"/>'
        f'<rect x="{x0+21}" y="{y0+72}" width="{54}" height="6" rx="3" fill="{c["ember"]}"/>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
<rect width="1280" height="640" fill="{c["bg"]}"/>{tile}
<path d="{path(MONO, repo, 248, y0+62, 56, -2)}" fill="{c["text"]}"/>
<path d="{path(SANS, desc, 248, y0+118, 26)}" fill="{c["mute"]}"/>
<path d="{path(MONO, "github.com/Real-Fruit-Snacks", 120, 560, 20)}" fill="{c["mute"]}"/>
</svg>'''
out = f"rfs-social-{repo}-{theme}.png"
cairosvg.svg2png(bytestring=svg.encode(), write_to=out, output_width=1280, output_height=640)
print("wrote", out)
