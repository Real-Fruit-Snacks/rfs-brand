# Per-repo settings checklist (Settings → General)

Run through this once per repo; it's what makes sixteen repos look like one org.

- [ ] **Description** — identical to the README's first line. ≤ 60 chars, sentence case, no period, no emoji.
- [ ] **Website** — leave blank unless the repo has docs that aren't the README.
- [ ] **Topics** (max 6) — at least one language tag and one domain tag:
      languages: `powershell` · `python` · `go` · `shell`
      domains:   `self-hosted` · `windows` · `networking` · `certificates` · `automation`
- [ ] **Social preview** — `python3 make-social.py <repo> "<description>"` → upload the 1280×640 PNG.
- [ ] **Releases** — tag `vX.Y.Z`, release title = the tag, no codename. Notes: what changed, what broke, nothing else.
- [ ] **Archived repos** — README body replaced with one line: `Superseded by [repo](link).` Then archive. Never delete.
- [ ] **Default branch** — `main`.
