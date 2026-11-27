#!/usr/bin/env python3
"""Verify Real-Fruit-Snacks (RFS) Cyclorama Dawn brand kit integrity, sibling parity, or any tool repo.

Usage:
    python tools/verify-brand.py [--workspace DIR] [--repo DIR ...] [--json]

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

RX_OKLCH = re.compile(r"gradient\([^)]*in oklch")
RX_MODAL = re.compile(r"\b(?:window\.)?(?:alert|confirm|prompt)\s*\(")
RX_PRIVATE = re.compile(r"\b(?:pn-selfhost|Eddy)\b")
RX_OLD_STROKE = re.compile(r'stroke-width[:=]\s*["\']?1\.65')
RX_CDN_FONTS = re.compile(r"fonts\.googleapis\.com|fonts\.gstatic\.com|use\.typekit\.net")
RX_BANNED_COPY = re.compile(r"\b(blazing|supercharge|seamless|awesome)\b", re.I)
RX_SHIELDS = re.compile(r"img\.shields\.io", re.I)
RX_EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")


class Reporter:
    def __init__(self, as_json: bool = False):
        self.as_json = as_json
        self.passed = []
        self.warnings = []
        self.errors = []

    def ok(self, msg: str):
        self.passed.append(msg)
        if not self.as_json:
            print(f"{C_OK}[ok]{C_RST} {msg}")

    def warn(self, msg: str):
        self.warnings.append(msg)
        if not self.as_json:
            print(f"{C_WARN}[!]{C_RST}  {msg}")

    def info(self, msg: str):
        if not self.as_json:
            print(f"{C_INFO}[i]{C_RST}  {msg}")

    def fail(self, msg: str):
        self.errors.append(msg)
        if not self.as_json:
            print(f"{C_FAIL}[x]{C_RST}  {msg}")

    def finish(self):
        if self.as_json:
            print(
                json.dumps(
                    {
                        "ok": len(self.errors) == 0,
                        "passed": self.passed,
                        "warnings": self.warnings,
                        "errors": self.errors,
                    },
                    indent=2,
                )
            )
        elif self.errors:
            self.info(f"verification finished with {len(self.errors)} failure(s)")
        else:
            self.ok("all Cyclorama Dawn brand checks passed")
        sys.exit(1 if self.errors else 0)


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def should_skip_file(rel_path: str) -> bool:
    norm = rel_path.replace("\\", "/").lower()
    if any(seg in norm.split("/") for seg in (".git", "node_modules", "dist", "target", ".venv", "__pycache__")):
        return True
    if "stockfish" in norm:
        return True
    if norm.startswith("tests/") or "/tests/" in norm or norm.endswith(".test.js") or norm.endswith(".test.ts"):
        return True
    return False


def audit_repo(repo_path: str, rep: Reporter):
    repo_dir = os.path.abspath(repo_path)
    name = os.path.basename(repo_dir)
    if not os.path.isdir(repo_dir):
        rep.fail(f"[{name}] repository path does not exist: {repo_dir}")
        return

    # 1. README checks (ultra-minimal landing page contract)
    readme_path = os.path.join(repo_dir, "README.md")
    if os.path.exists(readme_path):
        lines = open(readme_path, encoding="utf-8", errors="ignore").read().splitlines()
        body = "\n".join(lines)
        if len(lines) > 65:
            rep.warn(f"[{name}] README.md is {len(lines)} lines (target 40-60 lines; move deep docs to docs/*.md)")
        else:
            rep.ok(f"[{name}] README.md length within budget ({len(lines)} lines)")

        # One-line summary check (first non-empty line after H1)
        summary = ""
        saw_h1 = False
        for ln in lines:
            s = ln.strip()
            if not saw_h1 and s.startswith("# "):
                saw_h1 = True
                continue
            if saw_h1 and s and not s.startswith("<"):
                summary = s
                break
        if summary:
            if len(summary) > 60:
                rep.warn(f"[{name}] README summary is {len(summary)} chars (target <= 60): {summary!r}")
            if summary.endswith("."):
                rep.warn(f"[{name}] README summary ends with a trailing period: {summary!r}")
            if "!" in summary:
                rep.fail(f"[{name}] README summary contains exclamation mark: {summary!r}")

        if RX_SHIELDS.search(body):
            rep.fail(f"[{name}] README.md contains shields.io badge URL (forbidden)")
        if RX_BANNED_COPY.search(body):
            hit = RX_BANNED_COPY.search(body).group(1)
            rep.fail(f"[{name}] README.md contains banned hype word '{hit}'")
        if RX_EMOJI.search(body):
            rep.fail(f"[{name}] README.md contains emoji (forbidden)")

        # Check adaptive cover if cover.toml or cover-dark.svg exists
        cover_dark = os.path.join(repo_dir, "docs", "assets", "cover-dark.svg")
        cover_light = os.path.join(repo_dir, "docs", "assets", "cover-light.svg")
        if os.path.exists(cover_dark) or os.path.exists(cover_light):
            if "<picture>" not in body or "cover-dark.svg" not in body or "cover-light.svg" not in body:
                rep.fail(f"[{name}] README.md missing adaptive <picture> referencing cover-dark.svg & cover-light.svg")
            else:
                rep.ok(f"[{name}] README.md adaptive <picture> cover verified")
    else:
        rep.warn(f"[{name}] README.md not found")

    # 2. Cover SVG wash & reduced-motion guard
    cover_light = os.path.join(repo_dir, "docs", "assets", "cover-light.svg")
    cover_dark = os.path.join(repo_dir, "docs", "assets", "cover-dark.svg")
    if os.path.exists(cover_light):
        svg_l = open(cover_light, encoding="utf-8", errors="ignore").read()
        if 'opacity="0.14"' in svg_l:
            rep.fail(f"[{name}] docs/assets/cover-light.svg still uses legacy 0.14 wash (regenerate for 0.32)")
        elif 'opacity="0.32"' in svg_l:
            rep.ok(f"[{name}] docs/assets/cover-light.svg uses calibrated 0.32 light floor wash")
        if "@keyframes" in svg_l and "prefers-reduced-motion:no-preference" not in svg_l and "prefers-reduced-motion: no-preference" not in svg_l:
            rep.fail(f"[{name}] docs/assets/cover-light.svg has @keyframes outside prefers-reduced-motion guard")
    if os.path.exists(cover_dark):
        svg_d = open(cover_dark, encoding="utf-8", errors="ignore").read()
        if "@keyframes" in svg_d and "prefers-reduced-motion:no-preference" not in svg_d and "prefers-reduced-motion: no-preference" not in svg_d:
            rep.fail(f"[{name}] docs/assets/cover-dark.svg has @keyframes outside prefers-reduced-motion guard")

    # 3. Code & web-surface scan
    hits = []
    html_files = []
    for r, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "dist", "target", ".venv", "__pycache__")]
        for fn in files:
            if fn in ("verify-brand.py", "verify-themes.py"):
                continue
            fp = os.path.join(r, fn)
            rel = os.path.relpath(fp, repo_dir)
            if should_skip_file(rel):
                continue
            if fn.endswith((".css", ".html", ".js", ".ts")):
                txt = open(fp, encoding="utf-8", errors="ignore").read()
                if RX_OKLCH.search(txt):
                    hits.append(f"in oklch gradient in {rel}")
                if fn.endswith((".js", ".ts")) and RX_MODAL.search(txt):
                    hits.append(f"native modal call in {rel}")
                if RX_OLD_STROKE.search(txt):
                    hits.append(f"legacy 1.65 stroke in {rel}")
                if RX_CDN_FONTS.search(txt):
                    hits.append(f"external font CDN URL in {rel}")
                if fn.endswith(".html") and (rel == "index.html" or rel.replace("\\", "/") == "docs/index.html"):
                    html_files.append((rel, txt))
            if fn.endswith((".html", ".js", ".ts", ".json", ".toml", ".md", ".py")):
                txt = open(fp, encoding="utf-8", errors="ignore").read()
                if RX_PRIVATE.search(txt):
                    hits.append(f"private repo reference in {rel}")

    for rel, html in html_files:
        if 'name="color-scheme"' in html and 'content="light dark"' in html:
            hits.append(f"auto 'light dark' color-scheme in {rel} (must default to explicit dark)")
        elif 'name="color-scheme" content="dark"' in html:
            rep.ok(f"[{name}] {rel} sets explicit dark default (LX 263)")

    if hits:
        for h in hits:
            rep.fail(f"[{name}] {h}")
    else:
        rep.ok(f"[{name}] zero oklch gradients, native popups, CDN fonts, 1.65 strokes, or private leaks")


def verify_brand_kit(args, rep: Reporter):
    # 1. Validate tokens JSON + CHANGELOG parity
    tok_path = os.path.join(ROOT, "brand", "tokens", "rfs.tokens.json")
    try:
        tokens = json.load(open(tok_path, encoding="utf-8"))
        version = tokens["meta"]["version"]
        rep.ok(f"rfs.tokens.json valid (v{version})")
    except Exception as e:
        rep.fail(f"rfs.tokens.json invalid: {e}")
        version = None

    if version:
        cl_path = os.path.join(ROOT, "CHANGELOG.md")
        cl = open(cl_path, encoding="utf-8").read() if os.path.exists(cl_path) else ""
        if re.search(rf"^## {re.escape(version)} ", cl, re.M):
            rep.ok(f"CHANGELOG.md contains '## {version} ' release section")
        else:
            rep.fail(f"CHANGELOG.md is missing '## {version} ' section")

    # 1b. Validate W3C DTCG export + SKILL.md + docs/llms.txt
    dtcg_path = os.path.join(ROOT, "brand", "tokens", "rfs.dtcg.json")
    try:
        dtcg = json.load(open(dtcg_path, encoding="utf-8"))
        assert "$schema" in dtcg and "color" in dtcg and "$type" in dtcg["color"]
        rep.ok("rfs.dtcg.json valid W3C DTCG export")
    except Exception as e:
        rep.fail(f"rfs.dtcg.json invalid: {e}")

    skill_path = os.path.join(ROOT, "skills", "rfs-brand", "SKILL.md")
    if os.path.exists(skill_path):
        stxt = open(skill_path, encoding="utf-8").read()
        has_fm = stxt.startswith("---\n") and re.search(r"^name:\s*rfs-brand\s*$", stxt, re.M) and re.search(r"^description:\s*.+", stxt, re.M)
        refs = re.findall(r"references/[a-z0-9\-]+\.md", stxt)
        missing_refs = [r for r in sorted(set(refs)) if not os.path.exists(os.path.join(ROOT, "skills", "rfs-brand", r))]
        if not has_fm:
            rep.fail("skills/rfs-brand/SKILL.md missing valid YAML frontmatter (name/description)")
        elif missing_refs:
            rep.fail(f"skills/rfs-brand/SKILL.md references missing files: {missing_refs}")
        else:
            rep.ok(f"skills/rfs-brand/SKILL.md valid ({len(set(refs))} reference modules verified)")
    else:
        rep.fail("skills/rfs-brand/SKILL.md missing")

    llms_path = os.path.join(ROOT, "docs", "llms.txt")
    if os.path.exists(llms_path) and os.path.getsize(llms_path) > 200:
        rep.ok("docs/llms.txt present")
    else:
        rep.fail("docs/llms.txt missing or empty")

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
            rep.fail(f"icon library incomplete: {', '.join(missing[:6])}")
        else:
            rep.ok(f"icon library complete ({len(idata['icons'])} standalone SVGs + sprite symbols)")
    except Exception as e:
        rep.fail(f"icon library check failed: {e}")

    # 3. Verify byte-sync between brand/ & assets/ and docs/assets/
    sync_pairs = [
        ("brand/tokens/rfs.css", "docs/assets/rfs.css"),
        ("brand/tokens/rfs-components.css", "docs/assets/rfs-components.css"),
        ("brand/tokens/rfs.tokens.json", "docs/assets/rfs.tokens.json"),
        ("brand/tokens/rfs.dtcg.json", "docs/assets/rfs.dtcg.json"),
        ("brand/tokens/rfs-tailwind.css", "docs/assets/rfs-tailwind.css"),
        ("brand/tokens/rfs-tokens.ts", "docs/assets/rfs-tokens.ts"),
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
        ("brand/social/rfs-social-org-dark-1280x640.png", "docs/assets/rfs-social-org-dark-1280x640.png"),
        ("brand/social/rfs-social-org-light-1280x640.png", "docs/assets/rfs-social-org-light-1280x640.png"),
        ("brand/social/rfs-header-dark-1500x500.png", "docs/assets/rfs-header-dark-1500x500.png"),
        ("brand/social/rfs-header-light-1500x500.png", "docs/assets/rfs-header-light-1500x500.png"),
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
        rep.fail(f"asset drift detected: {'; '.join(drift)}")
    else:
        rep.ok(f"all {len(sync_pairs)} canonical brand <-> docs/assets pairs byte-synced")

    # 4. Scan code files for forbidden regressions
    scan_roots = [ROOT]
    if args.workspace:
        for sib in ("Real-Fruit-Snacks", "Real-Fruit-Snacks.github.io", "rfs.tools"):
            sp = os.path.join(args.workspace, sib)
            if os.path.isdir(sp):
                scan_roots.append(sp)

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
                    if RX_OKLCH.search(txt):
                        code_hits.append(f"in oklch gradient in {rel}")
                    if fn.endswith(".js") and RX_MODAL.search(txt):
                        code_hits.append(f"native modal call in {rel}")
                    if RX_OLD_STROKE.search(txt):
                        code_hits.append(f"legacy 1.65 stroke in {rel}")
                if fn.endswith((".html", ".js", ".json", ".toml", ".md", ".py")):
                    txt = open(fp, encoding="utf-8", errors="ignore").read()
                    if RX_PRIVATE.search(txt):
                        code_hits.append(f"private repo reference in {rel}")

    if code_hits:
        for h in code_hits:
            rep.fail(h)
    else:
        rep.ok(f"zero oklch gradients, native popups, 1.65 strokes, or private-repo leaks across {len(scan_roots)} repo(s)")

    # 5. Optional sibling active-tool catalog parity check
    if args.workspace:
        tools_json = os.path.join(args.workspace, "Real-Fruit-Snacks.github.io", "tools.json")
        board_py = os.path.join(args.workspace, "Real-Fruit-Snacks", "art", "make-board.py")
        covers_dir = os.path.join(args.workspace, "_repo-covers")
        if os.path.exists(tools_json) and os.path.exists(board_py):
            tj_repos = [t["repo"] for t in json.load(open(tools_json, encoding="utf-8"))["tools"]]
            board_src = open(board_py, encoding="utf-8").read()
            missing_board = [r for r in tj_repos if f'"{r}"' not in board_src]
            cover_root = covers_dir if os.path.isdir(covers_dir) else args.workspace
            cover_label = "_repo-covers" if os.path.isdir(covers_dir) else "sibling repos"
            missing_covers = [
                r for r in tj_repos
                if not os.path.exists(os.path.join(cover_root, r, "docs", "assets", "cover-dark.svg"))
            ]
            if missing_board:
                rep.fail(f"make-board.py missing tools: {missing_board}")
            if missing_covers:
                rep.fail(f"{cover_label} missing covers: {missing_covers}")
            if not missing_board and not missing_covers:
                rep.ok(f"{len(tj_repos)}-tool parity verified across tools.json, make-board.py, and {cover_label} ({len(tj_repos)} tools)")


def main():
    ap = argparse.ArgumentParser(description="Verify RFS Cyclorama Dawn brand kit, sibling parity, or any tool repo.")
    ap.add_argument("--workspace", help="Optional parent folder containing sibling staged repos")
    ap.add_argument("--repo", action="append", help="Audit one or more target RFS repository directories")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON output")
    args = ap.parse_args()

    rep = Reporter(as_json=args.json)
    if args.repo:
        for repo_path in args.repo:
            audit_repo(repo_path, rep)
    else:
        verify_brand_kit(args, rep)
    rep.finish()


if __name__ == "__main__":
    main()
