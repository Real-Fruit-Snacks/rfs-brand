#!/usr/bin/env python3
"""Generate W3C DTCG JSON, Tailwind CSS v4 @theme, and TypeScript token exports from rfs.tokens.json.

Usage:
    python tools/make-tokens.py
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOKENS_DIR = os.path.join(ROOT, "brand", "tokens")
DOCS_ASSETS = os.path.join(ROOT, "docs", "assets")
SRC_PATH = os.path.join(TOKENS_DIR, "rfs.tokens.json")

COLOR_DESCRIPTIONS = {
    "bg": "Primary page canvas (matte cyclorama black in dark; alabaster paper in light).",
    "rail": "Navigation rail, table headers, and secondary structural chrome.",
    "surface": "Primary cards, panels, proof desk, and terminal frames.",
    "raised": "Nested inputs, chips, active rows, and elevated controls.",
    "line": "1px structural hairlines and table dividers.",
    "line-strong": "Interactive control borders (>= 3.11:1 against every surface).",
    "text": "Primary display and body ink (>= 15.4:1 contrast).",
    "mute": "Secondary copy, metadata, captions, and standard CLI output.",
    "steel": "Glacial Steel physical cyclorama wash pole.",
    "steel-fill": "Solid Glacial Steel fill for buttons and active chips (white text >= 9.5:1).",
    "steel-ink": "Text-safe Glacial Steel for labels, kickers, cue numbers, and [i] tags.",
    "beacon": "Maritime Beacon Orange physical cyclorama wash pole.",
    "beacon-wash": "Deep Maritime Beacon Orange wash stop for hero gradients.",
    "beacon-ink": "Text-safe Beacon Orange for links, active indicators, and focus rings.",
    "primary": "Single-color primary brand accent.",
    "primary-hover": "Primary accent hover state (increased contrast against foreground).",
    "primary-press": "Primary accent pressed state (highest contrast against foreground).",
    "on-primary": "Foreground text on solid primary fills.",
    "on-steel": "Foreground text on solid steel-fill surfaces.",
    "accent": "Amber warning ink ([!]) and syntax string literals.",
    "signal": "Mint success ink ([ok]) and diff additions.",
    "fault": "Signal Crimson failure ink ([x]), error borders, and diff deletions.",
    "fault-fill": "Solid Signal Crimson destructive button fill with white foreground.",
    "fault-fill-hover": "Hover state for Signal Crimson destructive fills.",
    "on-fault": "Foreground text on solid fault-fill surfaces.",
    "code-bg": "Recessed terminal, command row, badge, and code-block surface.",
    "focus": "Keyboard :focus-visible outline ring (2px solid, 3px offset).",
}


def parse_bezier(value: str):
    if value == "linear":
        return [0, 0, 1, 1]
    inner = value[value.index("(") + 1 : value.index(")")]
    return [float(x.strip()) for x in inner.split(",")]


def parse_font_stack(value: str):
    return [part.strip().strip('"').strip("'") for part in value.split(",")]


def build_dtcg(data: dict) -> dict:
    meta = data["meta"]
    dtcg = {
        "$schema": "https://tr.designtokens.org/format/",
        "$description": f"{meta['name']} ({meta['palette']}, v{meta['version']}) — W3C Design Tokens Community Group (DTCG) export.",
        "color": {
            "$type": "color",
            "dark": {
                "$description": "Beacon Horizon (LX 263) — explicit dark default.",
                **{
                    k: {
                        "$value": v,
                        "$description": COLOR_DESCRIPTIONS.get(k, f"Dark mode {k} color."),
                    }
                    for k, v in data["color"]["dark"].items()
                },
            },
            "light": {
                "$description": "Alabaster Day (LX 512) — opt-in light mode.",
                **{
                    k: {
                        "$value": v,
                        "$description": COLOR_DESCRIPTIONS.get(k, f"Light mode {k} color."),
                    }
                    for k, v in data["color"]["light"].items()
                },
            },
            "dataviz": {
                "$description": "Ordered 6-series categorical data visualization palette (WCAG AA >= 5.8:1 in both modes).",
                "dark": {
                    f"series-{item['series']}": {
                        "$value": item["dark"],
                        "$description": f"Series {item['series']} — {item['name']} (maps to --rfs-{item['token']}).",
                    }
                    for item in data["dataviz"]["categorical"]
                },
                "light": {
                    f"series-{item['series']}": {
                        "$value": item["light"],
                        "$description": f"Series {item['series']} — {item['name']} (maps to --rfs-{item['token']}).",
                    }
                    for item in data["dataviz"]["categorical"]
                },
            },
        },
        "fontFamily": {
            "$type": "fontFamily",
            **{
                k: {
                    "$value": parse_font_stack(v),
                    "$description": f"Self-hosted variable {k} stack.",
                }
                for k, v in data["font"].items()
            },
        },
        "space": {
            "$type": "dimension",
            **{
                k: {"$value": f"{v}px", "$description": f"4px base grid step {k}."}
                for k, v in data["space"].items()
            },
        },
        "radius": {
            "$type": "dimension",
            "token": {"$value": "4px", "$description": "D · Terminal Token badges, chips, and keycaps."},
            "sm": {"$value": data["radius"]["sm"], "$description": "Buttons, inputs, and compact controls."},
            "md": {"$value": data["radius"]["card"], "$description": "Cards, panels, and structural frames."},
        },
        "motion": {
            "easing": {
                "$type": "cubicBezier",
                **{
                    k: {"$value": parse_bezier(v), "$description": f"Motion curve --rfs-{k}."}
                    for k, v in data["motion"].items()
                    if k.startswith("ease")
                },
            },
            "duration": {
                "$type": "duration",
                **{
                    k: {"$value": v, "$description": f"Motion duration --rfs-{k}."}
                    for k, v in data["motion"].items()
                    if not k.startswith("ease")
                },
            },
        },
        "zIndex": {
            "$type": "number",
            **{
                k: {"$value": v, "$description": f"Layer elevation --rfs-z-{k}."}
                for k, v in data["z-index"].items()
            },
        },
        "breakpoint": {
            "$type": "dimension",
            **{
                k: {"$value": v, "$description": f"Responsive breakpoint --rfs-bp-{k}."}
                for k, v in data["breakpoints"].items()
            },
        },
    }
    return dtcg


def build_tailwind(data: dict) -> str:
    ver = data["meta"]["version"]
    color_keys = list(data["color"]["dark"].keys())
    lines = [
        f"/* RFS Cyclorama Dawn v{ver} — Tailwind CSS v4 @theme bridge.",
        "   Generated from brand/tokens/rfs.tokens.json by tools/make-tokens.py.",
        '   Import after `@import "tailwindcss";` and `rfs.css` so utilities stay theme-reactive across LX 263 Dark and LX 512 Light. */',
        "",
        "@theme inline {",
        "  /* Semantic & brand colors (resolve dynamically via rfs.css dark/light variables) */",
    ]
    for k in color_keys:
        lines.append(f"  --color-rfs-{k}: var(--rfs-{k});")
    lines.append("")
    lines.append("  /* Ordered 6-series data visualization palette */")
    for item in data["dataviz"]["categorical"]:
        lines.append(f"  --color-rfs-viz-{item['series']}: var(--rfs-viz-{item['series']});")
    lines.append("")
    lines.append("  /* Self-hosted variable typography */")
    lines.append("  --font-display: var(--rfs-font-display);")
    lines.append("  --font-sans: var(--rfs-font-sans);")
    lines.append("  --font-mono: var(--rfs-font-mono);")
    lines.append("")
    lines.append("  /* 4px spacing grid */")
    for k, v in data["space"].items():
        lines.append(f"  --spacing-rfs-{k}: {v}px;")
    lines.append("")
    lines.append("  /* Technical corner radii */")
    lines.append("  --radius-rfs-token: 4px;")
    lines.append(f"  --radius-rfs-sm: {data['radius']['sm']};")
    lines.append(f"  --radius-rfs-md: {data['radius']['card']};")
    lines.append("")
    lines.append("  /* Motion curves */")
    for k, v in data["motion"].items():
        if k.startswith("ease"):
            lines.append(f"  --ease-rfs-{k}: {v};")
    lines.append("")
    lines.append("  /* Breakpoints */")
    for k, v in data["breakpoints"].items():
        lines.append(f"  --breakpoint-rfs-{k}: {v};")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def build_ts(data: dict) -> str:
    ver = data["meta"]["version"]
    return "\n".join(
        [
            f"// RFS Cyclorama Dawn v{ver} — Typed TypeScript design tokens.",
            "// Generated from brand/tokens/rfs.tokens.json by tools/make-tokens.py. Do not hand-edit.",
            "",
            f"export const RFS_META = {json.dumps(data['meta'], indent=2)} as const;",
            "",
            f"export const RFS_COLORS = {json.dumps({'dark': data['color']['dark'], 'light': data['color']['light']}, indent=2)} as const;",
            "",
            f"export const RFS_DATAVIZ = {json.dumps(data['dataviz'], indent=2)} as const;",
            "",
            f"export const RFS_CYCLORAMA = {json.dumps(data['cyclorama'], indent=2)} as const;",
            "",
            f"export const RFS_FONTS = {json.dumps(data['font'], indent=2)} as const;",
            "",
            f"export const RFS_SPACE = {json.dumps(data['space'], indent=2)} as const;",
            "",
            f"export const RFS_MOTION = {json.dumps(data['motion'], indent=2)} as const;",
            "",
            f"export const RFS_Z_INDEX = {json.dumps(data['z-index'], indent=2)} as const;",
            "",
            f"export const RFS_BREAKPOINTS = {json.dumps(data['breakpoints'], indent=2)} as const;",
            "",
            f"export const RFS_CLI = {json.dumps(data['cli'], indent=2)} as const;",
            "",
            "export type RfsThemeMode = keyof typeof RFS_COLORS;",
            "export type RfsColorToken = keyof typeof RFS_COLORS.dark;",
            "",
        ]
    )


def write_synced(filename: str, content: str):
    src = os.path.join(TOKENS_DIR, filename)
    dst = os.path.join(DOCS_ASSETS, filename)
    with open(src, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    shutil.copy2(src, dst)
    print(f"wrote brand/tokens/{filename} + docs/assets/{filename}")


def main():
    with open(SRC_PATH, encoding="utf-8") as fh:
        data = json.load(fh)

    dtcg = json.dumps(build_dtcg(data), indent=2) + "\n"
    tailwind = build_tailwind(data)
    ts = build_ts(data)

    write_synced("rfs.dtcg.json", dtcg)
    write_synced("rfs-tailwind.css", tailwind)
    write_synced("rfs-tokens.ts", ts)

    # Also keep rfs.css and rfs.tokens.json byte-synced into docs/assets/
    for core in ("rfs.css", "rfs-components.css", "rfs.tokens.json"):
        shutil.copy2(os.path.join(TOKENS_DIR, core), os.path.join(DOCS_ASSETS, core))
        print(f"synced brand/tokens/{core} -> docs/assets/{core}")


if __name__ == "__main__":
    main()
