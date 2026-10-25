---
name: showcase-readme
description: Showcase README for an open-source project, with a brand banner, logo options, real screenshots or demo GIF, badges and translations. Use when creating or redesigning a README to look polished (hero banner, animated header, demo), adding a README in another language, or making banner/logo options for a repo.
license: MIT
---

Build a README that sells the project in one scroll: animated hero, one-line pitch, proof it runs, then reference. Works for any stack; every visual comes from the project's own brand and its real output. For a plain internal or config README, use `crafting-effective-readmes` instead when it is available.

## Steps

1. **Learn the project.** Read the manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Package.swift`…), the current README, docs, CI and release config. Done when you can state, from repo evidence: what it is, who it is for, the platform, every install path that really exists (registry, Homebrew, releases, source), and the 3–6 features worth a bullet. Every claim in the README must trace to code or config; verify numbers, paths, flags and names before writing them.

2. **Find the palette.** Search brand docs (`brand/`, `Brand/`, `design/`, `docs/brand*`), design tokens, `tailwind.config.*`, CSS `:root` variables, theme files, color constants in UI code, and fills in existing logo SVGs. Done when you hold `bg`, `fg`, `accent`, `muted` (plus `accent2`, `border` if present) **from this project**. When nothing is found or sources conflict, first ask the user whether they have a color preference (hex codes, another project's brand to reuse, or a mood) and stop until they answer. Only when they have none, or ask for options, propose 3–4 palettes built from their answer and the project's mood, each shown as a rendered swatch. The palette always comes from the project or the user; there is no default palette. Save it as `docs/assets/palette.json`.

3. **Settle the logo.** Use the existing logo when there is one. Otherwise draw 3–4 SVG logo options in the palette, built from the project's concept (a letterform, a symbol of what it does), render each to PNG, open them for the user and let them pick. Save the choice as `docs/assets/logo.svg`.

4. **Ask once** (one questionnaire): which languages (English `README.md` is primary; each translation is `README.<lang>.md`), what the typing banner should type (a command, a code line, a quote from the product), and 1–3 chips (shortcut, version, license).

5. **Banner options.** Run `scripts/banner.py` from this skill (Python 3, no dependencies) with `--layout all`: `icon`, `typing` (animated), `centered`, `prompt`. Render each to PNG (`rsvg-convert -w 1280 x.svg -o x.png`, or a browser screenshot), look at every one yourself, fix overflow or clipping, then open them for the user and ask which is the header and whether it animates. Keep the runner-up as `banner-alt.*`: users change their minds. Copy the chosen SVGs into `docs/assets/`; each SVG carries the command that made it in a comment. One banner per language.

6. **Proof it runs.** Capture the real product, never a mockup: see [references/visuals.md](references/visuals.md) for the capture route per platform, sizes and the regeneration script. Ask before capturing the user's screen. Use temporary data, never the user's.

7. **Write the README** from [assets/README.template.md](assets/README.template.md), following the section order and patterns in [references/anatomy.md](references/anatomy.md). Write each translation with the same structure, its own anchors, and the register of the project's UI copy.

8. **Verify.** Done when: every local `src`/`href` path exists; every image has alt text; you viewed every image and every animated frame you captured (re-render under a new file name when re-checking, since viewers cache by path); GIFs stay under ~1 MB each and `docs/assets` under ~5 MB; every factual claim has been checked against the code; contributor docs (`AGENTS.md`, `CONTRIBUTING.md`) mention the translations and how to regenerate the assets.

## Output

Report the files created, the choices the user made (palette, logo, banner, languages), what you verified, and what you could not check (rendering on GitHub, platforms you did not run).
