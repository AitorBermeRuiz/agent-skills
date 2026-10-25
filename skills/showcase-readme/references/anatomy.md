# README anatomy

The order, top to bottom. Each section earns its place by answering the next question a visitor has. Patterns come from READMEs that do this well (gentle-ai, rtk, codegraph).

| # | Section | Question it answers | Pattern |
|---|---------|--------------------|---------|
| 1 | Hero (centered `<div align="center">`) | What is this? | Banner `<img width="100%">`, one bold line, one sentence with the core action (`<kbd>` for keys) |
| 2 | Badges | Is it alive and can I trust it? | 3–6 `shields.io` badges, `style=for-the-badge`, `labelColor` = palette `bg`, `color` = `accent`/`accent2`/`muted`. Only badges backed by something real (release, CI workflow, platform, license) |
| 3 | Nav line | Where do I go? | `Install • How it works • … ` links to anchors, bold |
| 4 | Language switch | Can I read it in mine? | `<strong>English</strong> • <a href="README.es.md">Español</a>`; current language bold, not linked |
| 5 | Pitch | Why should I care? | 1–3 sentences: the pain, then what the project does about it. No feature list here |
| 6 | Demo | Does it really work? | One GIF or video of a real run, `width` ≈ 720, caption in `<sub>` stating it is real |
| 7 | Features | What do I get? | 4–7 bullets, **bold lead phrase** + one sentence. Then screenshots side by side in a 2-column `<table>` with `<sub>` captions |
| 8 | Install | How do I get it? | Fastest path first as a code block; alternatives and migration notes in `<details>`; a `> [!TIP]` for an optional extra |
| 9 | How it works / Quick start | How do I use it? | Concepts table (term → one-line definition) or numbered steps; for CLIs, a command block with comments |
| 10 | Reference | What are all the options? | Shortcuts, commands, config, formats as tables and code blocks. A screenshot beside a list: `<img align="right" width="380">` then `<br clear="right"/>` |
| 11 | Data / privacy | Where does my data go? | Table of what is stored where; say plainly if there is no network or telemetry, and how to remove everything |
| 12 | Build from source / Contributing | How do I hack on it? | Exact commands; links to `AGENTS.md`, `CONTRIBUTING.md`, roadmap; release process in `<details>` |
| 13 | License | Can I use it? | One line plus exceptions |
| 14 | Footer | — | Centered small logo, `<sub>` tagline, `back to top ↑` linking to `<a id="top"></a>` at the very top |

## Rules

- Primary file is `README.md` in English; translations are `README.<lang>.md` (`README.es.md`, `README.zh.md`). Same sections, same images, translated alt text. Anchors follow the translated headings (GitHub lowercases, keeps accents, turns spaces into `-`).
- Images that differ per language get a `-<lang>` suffix (`banner-en.svg`, `banner-es.svg`); shared ones have none.
- Keep the existing README's correct reference content (formats, flags, secrets); restyle it, never drop it.
- A star-history chart or a "works with" logo row only when the project has the stars or integrations to show.
- Collapsed `<details>` for anything most readers skip: alternative installs, release process, troubleshooting.
- Write for the reader who lands from a link and decides in ten seconds: hero, pitch and demo must stand alone.
