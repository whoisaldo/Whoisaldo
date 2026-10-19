#!/usr/bin/env python3
"""Regenerates panel.svg, the live panel at the bottom of the README.

Two sections. GitHub: contributions over the last year as one LED bar per
week, next to public commits, active days and the current streak. The day
counts are read off the public profile, so the total matches the one it shows.
Stargazers: total stars across the owner's repos and the Sideband Studio org,
with a meter per repo.

Fonts are embedded as data URIs because an SVG loaded through <img> cannot
fetch anything. All are OFL; the licenses sit next to them in assets/fonts.

Run: GITHUB_TOKEN=... python3 scripts/panel.py
The refresh workflow runs it daily. On failure it exits non-zero and leaves
the previous panel.svg in place.
"""
import base64
import datetime as dt
import json
import math
import os
import pathlib
import re
import urllib.parse
import urllib.request
from xml.sax.saxutils import escape

USER = "whoisaldo"
OWN = ["whoisaldo", "sidebandstudio"]   # repos counted for stars
STAR_ROWS = 2

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"

INK, LINE, BONE, DIM, MUTED, VOLT = "#050506", "#24242a", "#eceae4", "#5c5c58", "#9a9a94", "#fcee0a"
W = 880
SEGMENTS = 40
BAR, BAR_PITCH, LEVELS = 11, 15, 12   # weekly bars: width, pitch, segments
MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": f"{USER}-readme"},
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def calendar():
    """(date, count) for each day on the public contribution graph."""
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions",
                                 headers={"User-Agent": f"{USER}-readme"})
    with urllib.request.urlopen(req, timeout=30) as r:
        page = r.read().decode()
    dates = {i: d for d, i in re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*id="([^"]+)"', page)}
    days = {}
    for i, n in re.findall(r'for="([^"]+)"[^>]*>(No|[\d,]+) contributions? on', page):
        days[dates[i]] = 0 if n == "No" else int(n.replace(",", ""))
    if len(days) < 365 or len(days) != len(dates):
        raise SystemExit("contribution graph: markup changed, keeping the old panel")
    return sorted(days.items())


def own_repos():
    out = []
    for owner in OWN:
        page = 1
        while True:
            data = api(f"users/{owner}/repos?per_page=100&page={page}&type=owner")
            if not data:
                break
            out += [(r["full_name"], r["stargazers_count"]) for r in data
                    if not r["fork"] and not r["private"]]
            page += 1
    return sorted(out, key=lambda kv: (-kv[1], kv[0].lower()))


def search_count(kind, q):
    return api(f"search/{kind}?q={urllib.parse.quote(q)}&per_page=1")["total_count"]


def font(name, file):
    data = base64.b64encode((FONTS / file).read_bytes()).decode()
    return f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{data}) format('woff2');}}"


def label(o, y, text, live=False):
    if live:
        o.append(f'<circle class="live" cx="43" cy="{y - 4}" r="3" fill="{VOLT}"/>')
    else:
        o.append(f'<circle cx="43" cy="{y - 4}" r="3" fill="{VOLT}"/>')
    o.append(f'<text class="m k" x="56" y="{y}" font-size="11" fill="{VOLT}">{text}</text>')


def section_height(rows, sub):
    return max(124 if sub else 104, 38 * rows)


def headline(o, top, total, caption, sub, height):
    """The big number on the left of a section, and the rule after it."""
    o.append(f'<text class="d" x="38" y="{top + 72}" font-size="78" fill="{BONE}">{total}</text>')
    o.append(f'<text class="m k" x="40" y="{top + 100}" font-size="10" fill="{MUTED}">{caption}</text>')
    if sub:
        o.append(f'<text class="m k" x="40" y="{top + 118}" font-size="10" fill="{DIM}">{sub}</text>')
    o.append(f'<rect x="262" y="{top + 6}" width="1" height="{height - 6}" fill="{LINE}"/>')


def meters(o, x0, x1, top, rows, start):
    """One LED meter per row, scaled to the first."""
    seg_w = (x1 - x0) / SEGMENTS
    peak = rows[0][1] if rows else 1
    for i, (name, n) in enumerate(rows):
        y = top + 20 + i * 38
        lit = max(1, round(SEGMENTS * n / peak))
        o.append(f'<text class="m" x="{x0}" y="{y}" font-size="12.5" fill="{BONE}">{escape(name)}</text>')
        o.append(f'<text class="d" x="{x1}" y="{y + 1}" font-size="17" fill="{VOLT}" text-anchor="end">{n}</text>')
        for k in range(SEGMENTS):
            sx = x0 + k * seg_w
            if k < lit:
                # Lit is the resting state, so a viewer that skips SMIL still
                # shows the full bar; the animation only adds the fill-in.
                delay = start + i * 0.15 + k * 0.025
                dur = delay + 0.25
                o.append(f'<rect x="{sx:.1f}" y="{y + 9}" width="{seg_w - 3:.1f}" height="7" fill="{VOLT}">'
                         f'<animate attributeName="opacity" values="0.12;0.12;1" '
                         f'keyTimes="0;{delay / dur:.3f};1" dur="{dur:.3f}s" fill="freeze"/></rect>')
            else:
                o.append(f'<rect x="{sx:.1f}" y="{y + 9}" width="{seg_w - 3:.1f}" height="7" fill="{BONE}" opacity="0.07"/>')


def section(o, top, total, caption, sub, rows, start):
    """A big number on the left, one LED meter per row on the right."""
    headline(o, top, total, caption, sub, section_height(len(rows), sub))
    meters(o, 292, W - 40, top, rows, start)


def weekly(o, base, days, start):
    """One LED bar per week, square-root scaled so quiet weeks still show."""
    weeks = {}
    for d, n in days:
        day = dt.date.fromisoformat(d)
        sunday = day - dt.timedelta(days=(day.weekday() + 1) % 7)
        weeks[sunday] = weeks.get(sunday, 0) + n
    weeks = sorted(weeks.items())
    peak = max(n for _, n in weeks) or 1
    x0 = (W - len(weeks) * BAR_PITCH + (BAR_PITCH - BAR)) / 2
    # Each bar is a dashed stroke from the bottom up: 5px segment, 2px gap.
    # Strokes stay crisp when GitHub scales the image; pattern fills do not.
    end = lambda k: base - 7 * k + 2   # top edge of segment k
    bar = lambda x, k, paint: (f'<line x1="{x}" y1="{base}" x2="{x}" y2="{end(k)}" stroke-width="{BAR}" '
                               f'stroke-dasharray="5 2" {paint}')

    for i, (sunday, n) in enumerate(weeks):
        x = x0 + i * BAR_PITCH + BAR / 2
        lit = math.ceil(LEVELS * math.sqrt(n / peak)) if n else 0
        o.append(bar(x, LEVELS, f'stroke="{BONE}" stroke-opacity="0.07"/>'))
        if lit:
            # Rises one segment at a time, then rests full. Like the meters,
            # it starts dim rather than empty.
            delay, step = start + i * 0.02, 0.04
            dur = delay + lit * step
            times = ";".join(["0"] + [f"{(delay + j * step) / dur:.3f}" for j in range(lit)])
            ends = ";".join([str(base)] + [str(end(j)) for j in range(1, lit + 1)])
            o.append(bar(x, lit, f'stroke="{VOLT}" stroke-opacity="0.12"/>'))
            o.append(bar(x, lit, f'stroke="{VOLT}">') +
                     f'<animate attributeName="y2" values="{ends}" keyTimes="{times}" '
                     f'dur="{dur:.3f}s" calcMode="discrete" fill="freeze"/></line>')
        last = sunday + dt.timedelta(days=6)
        if last.day <= 7:   # the 1st of a month falls in this week
            o.append(f'<text class="m k" x="{x - BAR / 2}" y="{base + 18}" font-size="9" fill="{DIM}">'
                     f'{MONTHS[last.month - 1]}</text>')


def streaks(days):
    counts = [n for _, n in days]
    longest = run = 0
    for n in counts:
        run = run + 1 if n else 0
        longest = max(longest, run)
    # Today may not have anything yet; a streak through yesterday still counts.
    current = 0
    for n in reversed(counts if counts[-1] else counts[:-1]):
        if not n:
            break
        current += 1
    return current, longest


def panel(days, commits, repos, today):
    stars = [r for r in repos if r[1]]
    current, longest = streaks(days)

    gh_top = 66
    base = gh_top + 124 + 30 + LEVELS * 7
    star_label = base + 18 + 54
    star_top = star_label + 20
    H = star_top + section_height(STAR_ROWS, None) + 32
    cut = 14
    o = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="{sum(n for _, n in days)} contributions in the last year; {sum(n for _, n in stars)} '
         f'stargazers">',
         "<defs><style><![CDATA[",
         font("Chakra Petch", "chakra-petch-latin-700-normal.woff2"),
         font("JBM", "jetbrains-mono-latin-wght-normal.woff2"),
         ".d{font-family:'Chakra Petch',sans-serif;font-weight:700}"
         ".m{font-family:'JBM',ui-monospace,monospace;font-weight:500}"
         ".k{letter-spacing:.16em}"
         "@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:.2}}"
         ".live{animation:blink 1.6s steps(1,end) infinite}"
         "]]></style></defs>",
         f'<path d="M{cut} 0H{W}V{H - cut}L{W - cut} {H}H0V{cut}Z" fill="{INK}"/>']

    label(o, 37, f"GITHUB · @{USER.upper()}", live=True)
    o.append(f'<text class="m k" x="{W - 40}" y="37" font-size="10" fill="{DIM}" text-anchor="end">'
             f'SYNCED {today:%Y-%m-%d}</text>')
    o.append(f'<rect x="40" y="52" width="{W - 80}" height="1" fill="{LINE}"/>')
    headline(o, gh_top, f"{sum(n for _, n in days):,}", "CONTRIBUTIONS, LAST YEAR", None, 124)
    cells = [(f"{commits:,}", "COMMITS", "PUBLIC, ALL TIME"),
             (str(sum(1 for _, n in days if n)), "ACTIVE DAYS", "LAST YEAR"),
             (str(current), "DAY STREAK", f"LONGEST {longest}")]
    for j, (value, caption, sub) in enumerate(cells):
        x = 292 + j * 183
        o.append(f'<text class="d" x="{x - 2}" y="{gh_top + 72}" font-size="40" fill="{BONE}">{value}</text>')
        o.append(f'<text class="m k" x="{x}" y="{gh_top + 100}" font-size="10" fill="{MUTED}">{caption}</text>')
        o.append(f'<text class="m k" x="{x}" y="{gh_top + 118}" font-size="10" fill="{DIM}">{sub}</text>')
    weekly(o, base, days, 0.3)

    o.append(f'<rect x="40" y="{star_label - 26}" width="{W - 80}" height="1" fill="{LINE}"/>')
    label(o, star_label, "STARGAZERS")
    section(o, star_top, sum(n for _, n in stars), f"STARS ACROSS {len(stars)} REPOS",
            None, stars[:STAR_ROWS], 0.9)
    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    today = dt.date.today()
    days = calendar()
    commits = search_count("commits", f"author:{USER} is:public")
    repos = own_repos()
    svg = panel(days, commits, repos, today)
    (ROOT / "panel.svg").write_text(svg)
    print(f"panel.svg: {sum(n for _, n in days)} contributions, {commits} commits, "
          f"{sum(n for _, n in repos)} stars in {sum(1 for _, n in repos if n)} repos")


if __name__ == "__main__":
    main()
