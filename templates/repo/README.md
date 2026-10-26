<!--
  RFS REPO README — TEMPLATE
  Section order is fixed. Sections may be deleted if empty; never reordered, never renamed.
  Voice: Plain · Specific · Dry · Honest. No emoji. No "blazing", "powerful", "modern", "seamless".
  Every adjective should be replaceable with a fact. If it can't be, delete it.
  Delete every HTML comment before committing.
  No RFS lockup or logo above the title: the org mark lives on the cover (BRAND.md §7).
-->

# repo-name

<!--
  ONE sentence, ≤ 60 characters, no period. What it does and for whom.
  This exact text is also the GitHub repo description — keep them identical.
  Good: "Keeps a forwarded VPN port and qBittorrent in sync"
  Bad:  "A powerful, modern tool for seamlessly synchronising your VPN configuration!"
-->
What it does, for whom

<!--
  Cover: generated, never hand-drawn. docs/assets/cover.toml → tools/make-cover.py (BRAND.md §7).
  Alt text says what the panel shows, in one sentence.
-->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/cover-dark.svg">
  <img alt="repo-name: what the panel shows" src="docs/assets/cover-light.svg" width="100%">
</picture>

<!--
  Install comes BEFORE the explanation. One canonical line per platform you actually support.
  Use the language fence that matches the shell: powershell / sh.
-->
```powershell
irm rfs.sh/repo-name | iex
```

<!--
  Two or three sentences. Why it exists, what it replaced, what it assumes about the reader's setup.
  First person singular is correct for a single maintainer. No history lesson.
-->
Why this exists and what it assumes about your setup.

## What's in it

<!--
  One row per command / module / entry point. "Does" column is one line, present tense, no period.
  If this table passes ~12 rows, the tool is probably two tools.
-->

| Command | Does |
|---|---|
| `Verb-Noun` | One line |
| `Verb-Noun` | One line |

## Tested on

<!--
  Real OS + runtime versions you have actually run it on. Not "should work on".
  The last bullet names what is NOT tested — this is required, not optional.
-->

- OS version · runtime version
- OS version · runtime version
- *Not* tested: platform — probably works, no promises

## Known issues

<!--
  Above the fold means above Configuration, not at the bottom.
  State the limitation plainly; link the issue number if one exists. Empty? Delete the section, don't write "none".
-->

- The first limitation, plainly, with the issue number if there is one (#12)

## Configuration

<!-- Include only if there is something to configure. Prefer a sensible default over a setting. -->

## License

MIT
