#!/usr/bin/env python3
"""Render README banner options (1280x400 SVG) from a project palette. Python 3 standard library only.

  banner.py --palette palette.json --name "Acme" --tagline "One line pitch" [--logo logo.svg]
            [--line "npx acme init"] [--caption "what the line is"] [--chips "⌥⇧T,MIT"] [--ghost]
            [--layout icon|typing|centered|prompt|all] [--out docs/assets]

palette.json: {"bg", "fg", "accent", "muted"} required; "accent2", "border", "font_mono", "font_sans" optional.
The typing layout is animated with CSS (GitHub plays it inside <img>); static renderers such as rsvg-convert
show its final frame, which is the PNG fallback.
"""
import argparse
import base64
import html
import json
import mimetypes
import pathlib
import sys
import textwrap

W, H = 1280, 400
CW = 0.6  # monospace advance in em; textLength pins every mono string to it, whatever font the viewer has
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


def width(s, size, spacing=0.0):
    return len(s) * size * (CW + spacing) - size * spacing if s else 0


def fit(s, size, room, spacing=0.0):
    """Largest font size up to `size` that keeps mono `s` within `room`."""
    return min(size, room / max(width(s, 1, spacing), 0.01))


class Banner:
    def __init__(self, p, a):
        self.p, self.a, self.parts, self.css = p, a, [], []
        self.mono = html.escape((f"'{p['font_mono']}', " if p.get("font_mono") else "") + MONO)
        self.sans = html.escape((f"'{p['font_sans']}', " if p.get("font_sans") else "") + SANS)

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size, fill, weight=400, spacing=0.0, anchor="start", sans=False, extra=""):
        common = f'x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}'
        if sans:
            self.add(f'<text {common} font-family="{self.sans}">{html.escape(s)}</text>')
        else:
            self.add(f'<text {common} font-family="{self.mono}" textLength="{width(s, size, spacing):.1f}" '
                     f'lengthAdjust="spacing">{html.escape(s.replace(" ", "\u00a0"))}</text>')  # renderers collapse plain spaces

    def logo(self, x, y, size):
        path = pathlib.Path(self.a.logo)
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        data = base64.b64encode(path.read_bytes()).decode()
        self.add(f'<image href="data:{mime};base64,{data}" x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" '
                 'preserveAspectRatio="xMidYMid meet"/>')

    def chips(self, x, y, size, align="start", fill_first=False, draw=True):
        """Pills from --chips, top edge at y; returns their total width (draw=False only measures)."""
        items = [c.strip() for c in (self.a.chips or "").split(",") if c.strip()]
        h, gap = size * 1.8, size * 0.6
        widths = [width(c, size) + size * 1.4 for c in items]
        total = sum(widths) + gap * max(len(items) - 1, 0)
        cx = x - total if align == "end" else x
        for i, (c, w) in enumerate(zip(items, widths) if draw else []):
            filled = fill_first and i == 0
            self.add(f'<rect x="{cx:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" '
                     f'fill="{self.p["accent"] if filled else self.p["bg"]}" stroke="{self.p["accent"] if filled else self.p["border"]}" stroke-width="1.5"/>')
            self.text(cx + w / 2, y + h * 0.66, c, size, self.p["bg"] if filled else self.p["fg"], 600, anchor="middle")
            cx += w + gap
        return total

    def svg(self, command):
        p = self.p
        label = html.escape(f"{self.a.name}: {self.a.tagline}")
        style = f"<style>{''.join(self.css)}</style>" if self.css else ""
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
<!-- {html.escape(command).replace('--', '- -')} -->
<title>{label}</title>
<defs>
<radialGradient id="tl" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="700"><stop offset="0" stop-color="{p['accent']}" stop-opacity="0.22"/><stop offset="1" stop-color="{p['accent']}" stop-opacity="0"/></radialGradient>
<radialGradient id="br" gradientUnits="userSpaceOnUse" cx="{W}" cy="{H}" r="600"><stop offset="0" stop-color="{p['accent2']}" stop-opacity="0.16"/><stop offset="1" stop-color="{p['accent2']}" stop-opacity="0"/></radialGradient>
<filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="34"/></filter>
</defs>
{style}
<rect width="{W}" height="{H}" fill="{p['bg']}"/><rect width="{W}" height="{H}" fill="url(#tl)"/><rect width="{W}" height="{H}" fill="url(#br)"/>
{chr(10).join(self.parts)}
</svg>
"""


def icon(b):
    """A: app icon (or monogram) beside the wordmark, tagline and chips."""
    p, a = b.p, b.a
    tile, gap = 230, 64
    name = a.name.upper()
    room = W - 160 - tile - gap
    ns, ts = fit(name, 84, room, 0.08), fit(a.tagline, 28, room)
    tw = max(width(name, ns, 0.08), width(a.tagline, ts), b.chips(0, 0, 22, draw=False))
    x0, y0 = (W - tile - gap - tw) / 2, (H - tile) / 2
    b.add(f'<rect x="{x0 + 20:.1f}" y="{y0 + 20:.1f}" width="{tile - 40}" height="{tile - 40}" rx="40" fill="{p["accent2"]}" opacity="0.45" filter="url(#blur)"/>')
    b.add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{tile}" height="{tile}" rx="{tile * 0.225:.1f}" fill="{p["bg"]}" stroke="{p["border"]}" stroke-width="2"/>')
    if a.logo:
        b.logo(x0 + tile * 0.14, y0 + tile * 0.14, tile * 0.72)
    else:
        b.text(x0 + tile / 2, y0 + tile * 0.7, name[0], tile * 0.55, p["accent"], 800, anchor="middle")
    tx = x0 + tile + gap
    top = 88 if a.chips else 118
    b.text(tx, top + ns * 0.8, name, ns, p["fg"], 800, 0.08)
    b.text(tx, top + ns * 0.8 + 60, a.tagline, ts, p["muted"])
    b.chips(tx, top + ns * 0.8 + 92, 22)


def typing(b):
    """B: a line types itself under a small header (animated); --ghost shows the pending text dimmed."""
    p, a = b.p, b.a
    if a.logo:
        b.logo(80, 72, 40)
    b.text(80 + (52 if a.logo else 0), 102, a.name.upper(), 26, p["accent"], 700, 0.2)
    b.chips(W - 80, 72, 20, align="end")
    line = a.line or a.tagline
    size = 44 if len(line) <= int((W - 160) / (44 * CW)) else 36
    lines = textwrap.wrap(line, int((W - 160) / (size * CW)), max_lines=2, placeholder=" …")
    if " ".join(lines) != " ".join(line.split()):
        print(f"warning: --line is cut to two lines: {' / '.join(lines)}", file=sys.stderr)
    cw, lh, top = size * CW, size * 1.45, 200
    seq = []  # one entry per keystroke: (line, column, char); a wrapped space is a keystroke too
    for li, text in enumerate(lines):
        seq += [(li, c, ch) for c, ch in enumerate(text)]
        if li < len(lines) - 1:
            seq.append((li, len(text), " "))
    start, dt = 0.8, 0.065
    dur = start + len(seq) * dt + 3.2
    pct = lambda t: f"{t / dur * 100:.2f}%"
    final = (len(lines) - 1, len(lines[-1]))
    where = lambda li, c: (80 + c * cw, top + li * lh)
    fx, fy = where(*final)
    # Block caret behind the text, drawn at its final spot; the animation offsets it from there.
    hops = [(0, (seq[0][0], seq[0][1]) if seq else final)]
    hops += [(start + k * dt, (seq[k + 1][0], seq[k + 1][1]) if k + 1 < len(seq) else final) for k in range(len(seq))]
    frames = "".join(f"{pct(t)}{{transform:translate({where(*pos)[0] - fx:.1f}px,{where(*pos)[1] - fy:.1f}px)}}" for t, pos in hops)
    b.css.append(f"@keyframes caret{{{frames}}}@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}"
                 f".caret{{animation:caret {dur:.2f}s step-end infinite}}.blink{{animation:blink 1.06s linear infinite}}"
                 f".ch{{animation-duration:{dur:.2f}s;animation-iteration-count:infinite;animation-timing-function:step-end}}")
    b.add(f'<g class="blink"><rect class="caret" x="{fx:.1f}" y="{fy - size * 0.9:.1f}" width="{cw:.1f}" height="{size * 1.15:.1f}" fill="{p["accent"]}" opacity="0.85"/></g>')
    hidden = f"fill:{p['muted']};fill-opacity:.5" if a.ghost else "opacity:0"
    shown = f"fill:{p['fg']};fill-opacity:1" if a.ghost else "opacity:1"
    for k, (li, c, ch) in enumerate(seq):
        if ch == " ":
            continue
        b.css.append(f"@keyframes k{k}{{0%{{{hidden}}}{pct(start + k * dt)}{{{shown}}}}}.c{k}{{animation-name:k{k}}}")
        x, y = where(li, c)
        b.text(x, y, ch, size, p["fg"], extra=f'class="ch c{k}"')
    y = top + (len(lines) - 1) * lh
    if a.caption:
        b.text(80, y + 54, a.caption, 19, p["muted"], sans=True)
    b.text(W - 80, H - 48, a.tagline, fit(a.tagline, 22, W - 160), p["muted"], anchor="end")


def centered(b):
    """C: glowing logo, spaced wordmark and tagline, centered."""
    p, a = b.p, b.a
    spaced = " ".join(a.name.upper())
    ns = fit(spaced, 54, W - 160, 0.1)
    base = 300 if a.logo else 215
    if a.logo:
        b.add(f'<circle cx="{W / 2}" cy="128" r="60" fill="{p["accent2"]}" opacity="0.5" filter="url(#blur)"/>')
        b.logo(W / 2 - 75, 53, 150)
    b.text(W / 2, base, spaced, ns, p["fg"], 700, 0.1, anchor="middle")
    b.text(W / 2, base + 52, a.tagline, fit(a.tagline, 24, W - 160), p["muted"], anchor="middle")


def prompt(b):
    """D: lowercase wordmark like a shell prompt, ending in a blinking cursor bar."""
    p, a = b.p, b.a
    full = a.name.lower()
    first = full.split(" ", 1)[0]
    size = fit(full + "  ", 130, W - 200)
    total = width(full, size) + size * 0.58
    x0, base = (W - total) / 2, 225
    b.text(x0, base, first, size, p["accent"], 800)
    rest = full[len(first):]
    if rest.strip():  # placed after its leading spaces: renderers drop leading whitespace
        b.text(x0 + width(full[:len(full) - len(rest.lstrip())], size), base, rest.lstrip(), size, p["fg"], 800)
    b.css.append("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1.06s linear infinite}")
    h = size * 0.16
    b.add(f'<rect class="blink" x="{x0 + width(full, size) + size * 0.08:.1f}" y="{base - h:.1f}" width="{size * 0.5:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{p["accent2"]}"/>')
    cw = b.chips(x0, base + 50, 22, fill_first=True)
    b.text(x0 + cw + (18 if cw else 0), base + 50 + 22 * 1.8 * 0.66, a.tagline, fit(a.tagline, 26, W - 160 - cw), p["muted"])


LAYOUTS = {"icon": icon, "typing": typing, "centered": centered, "prompt": prompt}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--palette", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--tagline", required=True)
    ap.add_argument("--logo")
    ap.add_argument("--line", help="text the typing layout types (a command, a quote, a code line)")
    ap.add_argument("--caption", help="small line under the typed text")
    ap.add_argument("--chips", help="comma-separated pills: a shortcut, a version, a license")
    ap.add_argument("--ghost", action="store_true", help="typing layout: show pending text dimmed instead of hidden")
    ap.add_argument("--layout", default="all", choices=[*LAYOUTS, "all"])
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    p = json.loads(pathlib.Path(a.palette).read_text())
    missing = [k for k in ("bg", "fg", "accent", "muted") if not p.get(k)]
    if missing:
        sys.exit(f"palette is missing {', '.join(missing)}")
    p.setdefault("accent2", p["accent"])
    p.setdefault("border", p["muted"])
    if a.logo and not pathlib.Path(a.logo).is_file():
        sys.exit(f"logo not found: {a.logo}")
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    command = "banner.py " + " ".join(sys.argv[1:])
    for name in LAYOUTS if a.layout == "all" else [a.layout]:
        b = Banner(p, a)
        LAYOUTS[name](b)
        path = out / f"banner-{name}.svg"
        path.write_text(b.svg(command))
        print(path)



if __name__ == "__main__":
    main()
