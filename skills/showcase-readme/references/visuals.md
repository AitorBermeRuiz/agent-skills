# Visuals: banners, captures, demo

## Banners (`scripts/banner.py`)

- `--palette docs/assets/palette.json --name … --tagline … [--logo docs/assets/logo.svg] [--line …] [--caption …] [--chips "a,b"] [--ghost] [--layout …] [--out docs/assets]`.
- `typing` animates with CSS inside the SVG; GitHub plays it in `<img>`. `--ghost` shows the pending text dimmed (typing-tutor style); without it the text appears as typed (terminal style). Static renderers (`rsvg-convert`, npm, PyPI) show the final frame, so the PNG export doubles as the fallback.
- Mono text is pinned to 0.6 em per character with `textLength`, so layout holds whatever monospace font the viewer has. To force a brand font, set `font_mono`/`font_sans` in the palette (used when installed) or outline the text in a vector editor.
- Preview animation in a real browser: open the SVG through an HTML page with `<img>`, wait, screenshot. Headless Chrome `--screenshot` freezes CSS animations at t=0, so it only proves the first frame.
- Light/dark: when the project wants both, render a light-palette variant and use `<picture><source media="(prefers-color-scheme: light)" srcset="…">`.

## Real captures, by platform

Render from the real product with throwaway data, at 2× scale, framed on a background in the palette with padding and a soft shadow.

| Project | Screenshots | Demo GIF |
|---------|-------------|----------|
| Web app / site | Playwright: `page.screenshot()` per state, seeded fixture data | Playwright `recordVideo` → `ffmpeg` → GIF, or frame screenshots → GIF |
| CLI / TUI | `vhs` (charmbracelet) `Screenshot` | `vhs demo.tape` writes the GIF directly; or `asciinema rec` + `agg` |
| Native macOS / iOS (SwiftUI) | `ImageRenderer` on the real views with a temporary store | Render frames while driving the real model in real time, write the GIF with ImageIO |
| Desktop (Electron, Tauri, Qt, GTK) | Playwright/Electron `capturePage`, or a window capture (`screencapture -l<id>` on macOS) | Screen recording of the window → `ffmpeg` → GIF |
| Library / SDK / API | No screenshot: a short code block and its real output | Optional: a terminal run recorded with `vhs` |
| Mobile (Android) | `adb exec-out screencap -p` | `adb shell screenrecord` → `ffmpeg` |

Rules:

- Commit the capture as a script (`scripts/readme-assets.*`) so anyone can regenerate the images when the UI changes; document it next to the build commands.
- Drive the demo with real input at a human pace so the numbers on screen are real; include a mistake and its fix when the product handles errors.
- Ask the user before any capture of their screen, and close what you opened.
- Size: 720 px wide demos at 10–15 fps; trim the middle of long runs instead of speeding them up. `gifski` or `ffmpeg` palette generation keeps GIFs small; keep each under ~1 MB.
- Alt text describes what the image shows, not its filename.
