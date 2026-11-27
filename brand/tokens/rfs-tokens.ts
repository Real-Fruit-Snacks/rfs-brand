// RFS Cyclorama Dawn v2.2.0 — Typed TypeScript design tokens.
// Generated from brand/tokens/rfs.tokens.json by tools/make-tokens.py. Do not hand-edit.

export const RFS_META = {
  "name": "Real-Fruit-Snacks \u2014 Cyclorama Dawn",
  "short": "RFS",
  "palette": "Steel & Beacon Orange",
  "tagline": "Built local-first.",
  "world": "stagecraft-theater-lighting-cyclorama-dawn",
  "version": "2.2.0"
} as const;

export const RFS_COLORS = {
  "dark": {
    "bg": "#050507",
    "rail": "#070709",
    "surface": "#0C0C10",
    "raised": "#14141A",
    "line": "#27272E",
    "line-strong": "#62646D",
    "text": "#F4F5F8",
    "mute": "#B3B5C0",
    "steel": "#1F547A",
    "steel-fill": "#18496B",
    "steel-ink": "#74B8E8",
    "beacon": "#F06E2B",
    "beacon-wash": "#CC5016",
    "beacon-ink": "#FF9254",
    "primary": "#F06E2B",
    "primary-hover": "#FF8442",
    "primary-press": "#FFA06B",
    "on-primary": "#050507",
    "on-steel": "#FFFFFF",
    "accent": "#FFC247",
    "signal": "#3DDC97",
    "fault": "#FF5C6C",
    "fault-fill": "#C92438",
    "fault-fill-hover": "#E02E44",
    "on-fault": "#FFFFFF",
    "code-bg": "#08080B",
    "focus": "#FF9254"
  },
  "light": {
    "bg": "#F5F7F9",
    "rail": "#EAEEF2",
    "surface": "#FFFFFF",
    "raised": "#E3E8EE",
    "line": "#CFD5DC",
    "line-strong": "#6E7682",
    "text": "#0D1016",
    "mute": "#474D59",
    "steel": "#1F547A",
    "steel-fill": "#18496B",
    "steel-ink": "#164669",
    "beacon": "#F06E2B",
    "beacon-wash": "#CC5016",
    "beacon-ink": "#AD3D0A",
    "primary": "#AD3D0A",
    "primary-hover": "#943207",
    "primary-press": "#7B2905",
    "on-primary": "#FFFFFF",
    "on-steel": "#FFFFFF",
    "accent": "#885800",
    "signal": "#127247",
    "fault": "#B91C2E",
    "fault-fill": "#B91C2E",
    "fault-fill-hover": "#991525",
    "on-fault": "#FFFFFF",
    "code-bg": "#EEF2F5",
    "focus": "#AD3D0A"
  }
} as const;

export const RFS_DATAVIZ = {
  "categorical": [
    {
      "series": 1,
      "name": "Glacial Steel",
      "token": "steel-ink",
      "dark": "#74B8E8",
      "light": "#164669"
    },
    {
      "series": 2,
      "name": "Maritime Beacon",
      "token": "beacon-ink",
      "dark": "#FF9254",
      "light": "#AD3D0A"
    },
    {
      "series": 3,
      "name": "Mint Signal",
      "token": "signal",
      "dark": "#3DDC97",
      "light": "#127247"
    },
    {
      "series": 4,
      "name": "Amber",
      "token": "accent",
      "dark": "#FFC247",
      "light": "#885800"
    },
    {
      "series": 5,
      "name": "Signal Crimson",
      "token": "fault",
      "dark": "#FF5C6C",
      "light": "#B91C2E"
    },
    {
      "series": 6,
      "name": "Stage Slate",
      "token": "mute",
      "dark": "#B3B5C0",
      "light": "#474D59"
    }
  ],
  "sequential-steel": [
    "#070A0E",
    "#133954",
    "#1F547A",
    "#4F88B5",
    "#74B8E8"
  ],
  "diverging-oklab": [
    "#164669",
    "#74B8E8",
    "#B3B5C0",
    "#FF9254",
    "#AD3D0A"
  ],
  "gridline-dark": "rgba(255, 255, 255, 0.10)",
  "gridline-light": "rgba(13, 16, 22, 0.12)"
} as const;

export const RFS_CYCLORAMA = [
  {
    "cue": 0,
    "lx": "001",
    "name": "Blackout",
    "mode": "dark",
    "stops": [
      "#06070A",
      "#090B10",
      "#131922"
    ]
  },
  {
    "cue": 1,
    "lx": "127",
    "name": "Glacial Steel",
    "mode": "dark",
    "stops": [
      "#070A0E",
      "#133954",
      "#1F547A"
    ]
  },
  {
    "cue": 2,
    "lx": "263",
    "name": "Beacon Horizon",
    "mode": "dark",
    "stops": [
      "#07090D",
      "#1E5078",
      "#F06E2B"
    ]
  },
  {
    "cue": 3,
    "lx": "389",
    "name": "Maritime Flame",
    "mode": "dark",
    "stops": [
      "#0B0707",
      "#7A2A0A",
      "#CC5016"
    ]
  },
  {
    "cue": 4,
    "lx": "455",
    "name": "Warm Frost",
    "mode": "light",
    "stops": [
      "#FDF8F5",
      "#F0E6DE",
      "#DCE5ED"
    ]
  },
  {
    "cue": 5,
    "lx": "512",
    "name": "Alabaster Day",
    "mode": "light",
    "stops": [
      "#F5F7F9",
      "#F0F4F8",
      "#FDF5F0"
    ]
  }
] as const;

export const RFS_FONTS = {
  "display": "\"Big Shoulders Stencil\", \"Arial Narrow\", sans-serif",
  "sans": "\"Albert Sans\", system-ui, -apple-system, sans-serif",
  "mono": "\"Azeret Mono\", ui-monospace, \"Cascadia Code\", Consolas, monospace"
} as const;

export const RFS_SPACE = {
  "1": 4,
  "2": 8,
  "3": 12,
  "4": 16,
  "5": 24,
  "6": 32,
  "7": 48,
  "8": 64,
  "9": 96
} as const;

export const RFS_MOTION = {
  "ease": "cubic-bezier(0.16, 1, 0.3, 1)",
  "ease-in-out": "cubic-bezier(0.65, 0, 0.35, 1)",
  "ease-exit": "cubic-bezier(0.7, 0, 0.84, 0)",
  "ease-linear": "linear",
  "dur-fast": "150ms",
  "dur-base": "250ms",
  "dur-slow": "520ms",
  "type-rate": "45ms"
} as const;

export const RFS_Z_INDEX = {
  "base": 0,
  "sticky": 20,
  "nav": 40,
  "popover": 60,
  "modal": 80,
  "toast": 100
} as const;

export const RFS_BREAKPOINTS = {
  "sm": "36em",
  "md": "56em",
  "lg": "72em"
} as const;

export const RFS_CLI = {
  "ok": {
    "tag": "[ok]",
    "ansi16": "green",
    "dark": "#3DDC97",
    "light": "#127247"
  },
  "warn": {
    "tag": "[!]",
    "ansi16": "yellow",
    "dark": "#FFC247",
    "light": "#885800"
  },
  "fail": {
    "tag": "[x]",
    "ansi16": "red",
    "dark": "#FF5C6C",
    "light": "#B91C2E"
  },
  "prompt": {
    "tag": "$",
    "ansi16": "bright-red",
    "dark": "#FF9254",
    "light": "#AD3D0A"
  },
  "info": {
    "tag": "[i]",
    "ansi16": "cyan",
    "dark": "#74B8E8",
    "light": "#164669"
  },
  "no-color-env": "NO_COLOR",
  "exit-codes": {
    "ok": 0,
    "runtime-error": 1,
    "usage-error": 2
  }
} as const;

export type RfsThemeMode = keyof typeof RFS_COLORS;
export type RfsColorToken = keyof typeof RFS_COLORS.dark;
