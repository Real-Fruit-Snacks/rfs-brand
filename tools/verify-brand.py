#!/usr/bin/env python3
"""Verify Real-Fruit-Snacks (RFS) Cyclorama Dawn brand kit integrity and cross-repo parity.

Usage:
    python tools/verify-brand.py [--workspace DIR]

Exit codes (RFS CLI standard):
    0  all checks passed
    1  one or more brand invariant checks failed
    2  invalid arguments
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR") and os.environ.get("TERM") != "dumb"
C_OK = "\033[38;2;61;220;151m" if USE_COLOR else ""
C_WARN = "\033[38;2;255;194;71m" if USE_COLOR else ""
C_FAIL = "\033[38;2;255;92;108m" if USE_COLOR else ""
C_INFO = "\033[38;2;116;184;232m" if USE_COLOR else ""
C_RST = "\033[0m" if USE_COLOR else ""


def log_ok(msg):
    print(f"{C_OK}[ok]{C_RST} {msg}")


def log_info(msg):
    print(f"{C_INFO}[i]{C_RST}  {msg}")


def log_fail(msg, errors):
    print(f"{C_FAIL}[x]{C_RST}  {msg}")
    errors.append(msg)


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Verify RFS Cyclorama Dawn brand kit & sibling parity.")
    ap.add_argument("--workspace", help="Optional parent folder containing sibling staged repos")
    args = ap.parse_args()

    errors = []

    # 1. Validate tokens JSON + CHANGELOG parity
    tok_path = os.path.join(ROOT, "brand", "tokens", "rfs.tokens.json")
    try:
        tokens = json.load(open(tok_path, encoding="utf-8"))
        version = tokens["meta"]["version"]
        log_ok(f"rfs.tokens.json valid (v{version})")
    except Exception as e:
        log_fail(f"rfs.tokens.json invalid: {e}", errors)
        version = None

    if version:
        cl_path = os.path.join(ROOT, "CHANGELOG.md")
        cl = open(cl_path, encoding="utf-8").read() if os.path.exists(cl_path) else ""
        if re.search(rf"^## {re.escape(version)} ", cl, re.M):
            log_ok(f"CHANGELOG.md contains '## {version} ' release section")
        else:
            log_fail(f"CHANGELOG.md is missing '## {version} ' section", errors)

    # 2. Validate 60-icon library completeness
    icons_json = os.path.join(ROOT, "brand", "icons", "icons.json")
    sprite_path = os.path.join(ROOT, "brand", "icons", "rfs-icons.svg")
    try:
        idata = json.load(open(icons_json, encoding="utf-8"))
        sprite = open(sprite_path, encoding="utf-8").read()
        missing = []
        for item in idata["icons"]:
            n = item["name"]
            if not os.path.exists(os.path.join(ROOT, "brand", "icons", f"{n}.svg")):
                missing.append(f"{n}.svg")
            if f'id="rfs-i-{n}"' not in sprite:
                missing.append(f"sprite:#rfs-i-{n}")
        if missing:
            log_fail(f"icon library incomplete: {', '.join(missing[:6])}", errors)
        else:
            log_ok(f"icon library complete ({len(idata['icons'])} standalone SVGs + sprite symbols)")
    except Exception as e:
        log_fail(f"icon library check failed: {e}", errors)

    # 3. Verify byte-sync between brand/ & assets/ and docs/assets/
    sync_pairs = [
        ("brand/tokens/rfs.css", "docs/assets/rfs.css"),
        ("brand/tokens/rfs-components.css", "docs/assets/rfs-components.css"),
        ("brand/tokens/rfs.tokens.json", "docs/assets/rfs.tokens.json"),
        ("brand/BRAND-RULES.md", "docs/assets/BRAND-RULES.md"),
        ("brand/icons/rfs-icons.svg", "docs/assets/rfs-icons.svg"),
        ("brand/icons/icons.json", "docs/assets/icons.json"),
        ("assets/rfs-banner-dark.svg", "docs/assets/rfs-banner-dark.svg"),
        ("assets/rfs-banner-light.svg", "docs/assets/rfs-banner-light.svg"),
        ("assets/rfs-banner-dark-animated.svg", "docs/assets/rfs-banner-dark-animated.svg"),
        ("assets/rfs-banner-light-animated.svg", "docs/assets/rfs-banner-light-animated.svg"),
        ("assets/rfs-mark-dark.svg", "docs/assets/rfs-mark-dark.svg"),
        ("assets/rfs-mark-light.svg", "docs/assets/rfs-mark-light.svg"),
        ("assets/rfs-lockup-dark.svg", "docs/assets/rfs-lockup-dark.svg"),
        ("assets/rfs-lockup-light.svg", "docs/assets/rfs-lockup-light.svg"),
    ]
    drift = []
    for src_rel, dst_rel in sync_pairs:
        src = os.path.join(ROOT, src_rel)
        dst = os.path.join(ROOT, dst_rel)
        if not os.path.exists(src) or not os.path.exists(dst):
            drift.append(f"missing {src_rel} or {dst_rel}")
        elif sha256(src) != sha256(dst):
            drift.append(f"{src_rel} != {dst_rel}")
    if drift:
        log_fail(f"asset drift detected: {'; '.join(drift)}", errors)
    else:
        log_ok(f"all {len(sync_pairs)} canonical brand <-> docs/assets pairs byte-synced")

    # 4. Scan code files for forbidden regressions
    scan_roots = [ROOT]
    if args.workspace:
        for sib in ("Real-Fruit-Snacks", "Real-Fruit-Snacks.github.io", "rfs.tools"):
            sp = os.path.join(args.workspace, sib)
            if os.path.isdir(sp):
                scan_roots.append(sp)

    rx_oklch = re.compile(r"gradient\([^)]*in oklch")
    rx_modal = re.compile(r"\b(?:window\.)?(?:alert|confirm|prompt)\s*\(")
    rx_private = re.compile(r"\b(?:pn-selfhost|Eddy)\b")
    rx_old_stroke = re.compile(r'stroke-width[:=]\s*["\']?1\.65')

    code_hits = []
    for sr in scan_roots:
        for r, dirs, files in os.walk(sr):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
            for fn in files:
                if fn == "verify-brand.py":
                    continue
                fp = os.path.join(r, fn)
                rel = os.path.relpath(fp, args.workspace or ROOT)
                if fn.endswith((".css", ".html", ".js")):
                    txt = open(fp, encoding="utf-8", errors="ignore").read()
                    if rx_oklch.search(txt):
                        code_hits.append(f"in oklch gradient in {rel}")
                    if fn.endswith(".js") and rx_modal.search(txt):
                        code_hits.append(f"native modal call in {rel}")
                    if rx_old_stroke.search(txt):
                        code_hits.append(f"legacy 1.65 stroke in {rel}")
                if fn.endswith((".html", ".js", ".json", ".toml", ".md", ".py")):
                    txt = open(fp, encoding="utf-8", errors="ignore").read()
                    if rx_private.search(txt):
                        code_hits.append(f"private repo reference in {rel}")

    if code_hits:
        for h in code_hits:
            log_fail(h, errors)
    else:
        log_ok(f"zero oklch gradients, native popups, 1.65 strokes, or private-repo leaks across {len(scan_roots)} repo(s)")

    # 5. Optional sibling active-tool catalog parity check
    if args.workspace:
        tools_json = os.path.join(args.workspace, "Real-Fruit-Snacks.github.io", "tools.json")
        board_py = os.path.join(args.workspace, "Real-Fruit-Snacks", "art", "make-board.py")
        covers_dir = os.path.join(args.workspace, "_repo-covers")
        if os.path.exists(tools_json) and os.path.exists(board_py):
            tj_repos = [t["repo"] for t in json.load(open(tools_json, encoding="utf-8"))["tools"]]
            board_src = open(board_py, encoding="utf-8").read()
            missing_board = [r for r in tj_repos if f'"{r}"' not in board_src]
            missing_covers = [
                r for r in tj_repos
                if os.path.isdir(covers_dir)
                and not os.path.exists(os.path.join(covers_dir, r, "docs", "assets", "cover-dark.svg"))
            ]
            if missing_board:
                log_fail(f"make-board.py missing tools: {missing_board}", errors)
            elif missing_covers:
                log_fail(f"_repo-covers missing covers: {missing_covers}", errors)
            else:
                log_ok(f"{len(tj_repos)}-tool parity verified across tools.json, make-board.py, and _repo-covers ({len(tj_repos)} tools)")

    if errors:
        log_info(f"verification finished with {len(errors)} failure(s)")
        sys.exit(1)
    log_ok("all Cyclorama Dawn brand checks passed")


if __name__ == "__main__":
    main()
