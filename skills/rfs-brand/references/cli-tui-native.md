# RFS CLI, TUI & Native Desktop Mapping

Every Real-Fruit-Snacks binary (Rust, Go, Python, PowerShell, C#) speaks the same scannable console grammar as web `D · Terminal Token` badges.

## Console Status Grammar & Color Table

| Prefix | Token | Truecolor Dark | Truecolor Light | ANSI-16 Fallback | `NO_COLOR` / Non-TTY |
|---|---|---|---|---|---|
| `[ok]` | `signal` | `#3DDC97` | `#127247` | Green (`32`) | `[ok]` plain text |
| `[!]` | `accent` | `#FFC247` | `#885800` | Yellow (`33`) | `[!]` plain text |
| `[x]` | `fault` | `#FF5C6C` | `#B91C2E` | Red (`31`) | `[x]` plain text |
| `[i]` | `steel-ink` | `#74B8E8` | `#164669` | Cyan (`36`) | `[i]` plain text |
| `$` | `beacon-ink` | `#FF9254` | `#AD3D0A` | Bright Red (`91`) | `$` plain text |

## Required CLI Contracts

- **`NO_COLOR` & TTY detection:** Strip all ANSI escape sequences when `NO_COLOR` is set (any non-empty value), `TERM=dumb`, or stdout is not a TTY. Because every status starts with `[ok]`, `[!]`, `[x]`, or `[i]`, piped logs retain full meaning without color.
- **Standard flags:** Support `--help`, `--version` (prints `<tool> vX.Y.Z`), and `--json` for machine-readable output wherever commands emit structured data.
- **Exit codes:** `0` success, `1` runtime failure, `2` invalid arguments / usage error.
- **Actionable errors:** Name the failing target, cause, and recovery action on `stderr` prefixed with `[x]`.

## Language Presets

### Rust (`anstyle` / Truecolor)
```rust
const PROMPT: RgbColor = RgbColor(255, 146, 84);  // $    #FF9254
const INFO:   RgbColor = RgbColor(116, 184, 232); // [i]  #74B8E8
const OK:     RgbColor = RgbColor(61,  220, 151); // [ok] #3DDC97
const WARN:   RgbColor = RgbColor(255, 194, 71);  // [!]  #FFC247
const FAIL:   RgbColor = RgbColor(255, 92,  108); // [x]  #FF5C6C
```

### Go (ANSI Truecolor)
```go
const (
    Prompt = "\x1b[38;2;255;146;84m"
    Info   = "\x1b[38;2;116;184;232m"
    OK     = "\x1b[38;2;61;220;151m"
    Warn   = "\x1b[38;2;255;194;71m"
    Fail   = "\x1b[38;2;255;92;108m"
    Reset  = "\x1b[0m"
)
```

### Python (`rich.theme.Theme`)
```python
from rich.console import Console
from rich.theme import Theme

RFS_THEME = Theme({
    "prompt": "bold #FF9254", "info": "bold #74B8E8",
    "ok": "bold #3DDC97", "warn": "bold #FFC247",
    "fail": "bold #FF5C6C", "mute": "#B3B5C0",
})
console = Console(theme=RFS_THEME)  # honors NO_COLOR automatically
```

## Windows Native Desktop Chrome & Icons

- Enable immersive dark titlebars via `DWMWA_USE_IMMERSIVE_DARK_MODE` (`20`) and set `DWMWA_CAPTION_COLOR` (`35`) to `0x00070505` (BGR for `#050507`) in dark mode or `0x00F2EEEA` (`#EAEEF2`) in light mode.
- Embed multi-size `.ico` executables (`16`, `32`, `48`, `256px`) exported from `brand/mark/rfs-mark-dark.png` / `brand/web/favicon.ico`.
