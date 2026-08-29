#!/usr/bin/env python3
"""Regenerates stars.svg and the SIGNAL block in README.md from the GitHub API.

star-history.com was the obvious way to do this and it is not usable here: its
SVG endpoint hardcodes an xkcd hand-drawn font with no parameter to turn it off,
which reads as a different site's chart dropped into this one. So the chart is
drawn locally instead, in the same palette as hero.svg.

Run: GITHUB_TOKEN=... python3 scripts/update_stars.py
Called by scripts/refresh-cards.sh, which the refresh-cards workflow runs daily.
"""
import datetime as dt
import json
import os
import pathlib
import re
import urllib.error
import urllib.request

USER = "whoisaldo"
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOP_N = 4          # rows in the SIGNAL block
CHARTED = 2        # series on the chart; beyond this the lines sit on the axis

INK, VOLT, FUCH, CYAN = "#07070C", "#FCEE0A", "#FF2E88", "#00F0FF"
BRIGHT, DIM = "#EAFEFF", "#5B6470"
SERIES_COLOURS = [VOLT, FUCH, CYAN]

W, H = 820, 300
PAD_L, PAD_R, PAD_T, PAD_B = 54, 132, 42, 40


def api(path, accept="application/vnd.github+json"):
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={"Accept": accept, "User-Agent": f"{USER}-readme"},
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r), r.headers.get("Link", "")


def repos():
    out, page = [], 1
    while True:
        data, _ = api(f"users/{USER}/repos?per_page=100&page={page}&type=owner")
        if not data:
            break
        out += [r for r in data if not r["fork"]]
        page += 1
    return sorted(out, key=lambda r: -r["stargazers_count"])


def stargazers(full_name):
    """(datetime, cumulative) points. Needs the star+json media type for starred_at."""
    stamps, page = [], 1
    while True:
        data, link = api(
            f"repos/{full_name}/stargazers?per_page=100&page={page}",
            accept="application/vnd.github.star+json",
        )
        if not data:
            break
        stamps += [dt.datetime.strptime(s["starred_at"], "%Y-%m-%dT%H:%M:%SZ") for s in data]
        if 'rel="next"' not in link:
            break
        page += 1
    stamps.sort()
    return [(t, i + 1) for i, t in enumerate(stamps)]


# ----------------------------------------------------------------- the chart
def chart(series, now):
    """series: [(label, colour, [(datetime, cumulative), ...]), ...]"""
    pts = [p for _, _, s in series for p in s]
    if not pts:
        return None
    t0 = min(t for t, _ in pts)
    t1 = max(now, max(t for t, _ in pts))
    t1 += (t1 - t0) * 0.03
    span = max((t1 - t0).total_seconds(), 1)
    ymax = max(4, max(c for _, c in pts))
    # round the top of the axis up to something a human would label
    step = next(s for s in (5, 10, 20, 25, 50, 100, 200, 500) if ymax / s <= 5)
    ytop = -(-ymax // step) * step

    def px(t):
        return PAD_L + (W - PAD_L - PAD_R) * (t - t0).total_seconds() / span

    def py(c):
        return H - PAD_B - (H - PAD_T - PAD_B) * (c / ytop)

    o = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Cumulative stargazers over time">',
         '<defs>',
         f'<pattern id="g" width="26" height="26" patternUnits="userSpaceOnUse">'
         f'<path d="M26 0 H0 V26" fill="none" stroke="{CYAN}" stroke-width="0.5" opacity="0.05"/></pattern>',
         '<pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse">'
         '<rect width="3" height="1" fill="#000" opacity="0.16"/></pattern>',
         '<filter id="glow" x="-40%" y="-40%" width="180%" height="180%">'
         '<feGaussianBlur stdDeviation="3" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
         "<style><![CDATA["
         ".t{font-family:'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}"
         "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}"
         ".live{animation:pulse 2s ease-in-out infinite}"
         "]]></style>"]
    for i, (_, col, _) in enumerate(series):
        o.append(f'<linearGradient id="f{i}" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="{col}" stop-opacity="0.30"/>'
                 f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>')
    o += ['</defs>',
          f'<rect width="{W}" height="{H}" fill="{INK}"/>',
          f'<rect width="{W}" height="{H}" fill="url(#g)"/>']

    # y grid + labels
    for k in range(0, ytop + 1, step):
        y = py(k)
        o.append(f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{W-PAD_R}" y2="{y:.1f}" '
                 f'stroke="{DIM}" stroke-width="1" opacity="0.22"/>')
        o.append(f'<text class="t" x="{PAD_L-10}" y="{y+3.5:.1f}" text-anchor="end" '
                 f'font-size="10" fill="{DIM}">{k}</text>')

    # x labels, first of each month that fits
    month, seen = t0.replace(day=1), set()
    while month <= t1:
        if month >= t0 and month.strftime("%b") not in seen:
            x = px(month)
            if PAD_L <= x <= W - PAD_R:
                o.append(f'<line x1="{x:.1f}" y1="{PAD_T}" x2="{x:.1f}" y2="{H-PAD_B}" '
                         f'stroke="{DIM}" stroke-width="1" opacity="0.14"/>')
                o.append(f'<text class="t" x="{x:.1f}" y="{H-PAD_B+18}" text-anchor="middle" '
                         f'font-size="10" fill="{DIM}">{month.strftime("%b").upper()}</text>')
                seen.add(month.strftime("%b"))
        month = (month.replace(day=28) + dt.timedelta(days=8)).replace(day=1)

    # axes
    o.append(f'<line x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{H-PAD_B}" stroke="{DIM}" stroke-width="1.5" opacity="0.5"/>')
    o.append(f'<line x1="{PAD_L}" y1="{H-PAD_B}" x2="{W-PAD_R}" y2="{H-PAD_B}" stroke="{DIM}" stroke-width="1.5" opacity="0.5"/>')

    # series, drawn as step lines: a star is a discrete event, not a slope
    for i, (label, col, s) in enumerate(series):
        if not s:
            continue
        d = [f"M{px(s[0][0]):.1f},{H-PAD_B:.1f}"]
        prev = H - PAD_B
        for t, c in s:
            x, y = px(t), py(c)
            d.append(f"L{x:.1f},{prev:.1f}L{x:.1f},{y:.1f}")
            prev = y
        d.append(f"L{px(t1):.1f},{prev:.1f}")
        line = " ".join(d)
        o.append(f'<path d="{line} L{px(t1):.1f},{H-PAD_B:.1f} L{px(s[0][0]):.1f},{H-PAD_B:.1f} Z" fill="url(#f{i})"/>')
        o.append(f'<path d="{line}" fill="none" stroke="{col}" stroke-width="2" '
                 f'stroke-linejoin="round" filter="url(#glow)"/>')
        o.append(f'<circle class="live" cx="{px(t1):.1f}" cy="{prev:.1f}" r="4" fill="{col}" filter="url(#glow)"/>')

    # Burst callout. A repo that sits flat and then goes near-vertical looks
    # like a broken chart unless the jump is labelled. Magnitude only: the
    # window it landed in is deliberately not stated.
    window = dt.timedelta(days=4)
    for label, col, s_ in series:
        if len(s_) < 8:
            continue
        lo = 0
        best = (0, 0, 0)          # (gain, lo, hi)
        for hi in range(len(s_)):
            while s_[hi][0] - s_[lo][0] > window:
                lo += 1
            gain = s_[hi][1] - s_[lo][1]
            if gain > best[0]:
                best = (gain, lo, hi)
        gain, lo, hi = best
        if gain < max(12, 0.35 * s_[-1][1]):
            continue
        x = px(s_[hi][0])
        y_hi, y_lo = py(s_[hi][1]), py(s_[lo][1])
        o.append(f'<line x1="{x-16:.1f}" y1="{y_hi:.1f}" x2="{x-16:.1f}" y2="{y_lo:.1f}" '
                 f'stroke="{col}" stroke-width="1" opacity="0.6"/>')
        for yy in (y_hi, y_lo):
            o.append(f'<line x1="{x-20:.1f}" y1="{yy:.1f}" x2="{x-12:.1f}" y2="{yy:.1f}" '
                     f'stroke="{col}" stroke-width="1" opacity="0.6"/>')
        mid = (y_hi + y_lo) / 2
        o.append(f'<text class="t" x="{x-26:.1f}" y="{mid+4:.1f}" text-anchor="end" '
                 f'font-size="14" fill="{col}">+{gain}</text>')

    # legend, right gutter
    ly = PAD_T + 6
    o.append(f'<text class="t" x="{W-PAD_R+14}" y="{ly}" font-size="9" fill="{DIM}" letter-spacing="1.2">STARGAZERS</text>')
    for i, (label, col, s) in enumerate(series):
        y = ly + 22 + i * 34
        o.append(f'<rect x="{W-PAD_R+14}" y="{y-8}" width="10" height="3" fill="{col}"/>')
        o.append(f'<text class="t" x="{W-PAD_R+14}" y="{y+10}" font-size="15" fill="{col}">{s[-1][1] if s else 0}</text>')
        o.append(f'<text class="t" x="{W-PAD_R+14}" y="{y+22}" font-size="8" fill="{DIM}">{label[:18]}</text>')

    o.append(f'<text class="t" x="{PAD_L}" y="24" font-size="10" fill="{VOLT}" letter-spacing="2">'
             f'&gt; STARGAZERS // CUMULATIVE</text>')
    o.append(f'<text class="t" x="{W-PAD_R}" y="24" text-anchor="end" font-size="9" fill="{DIM}">'
             f'SYNCED {now:%Y-%m-%d}</text>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


# ----------------------------------------------------------------- the block
BLOCKS = "█"


def signal_block(rows, total, now):
    top = max(r["stars"] for r in rows) or 1
    name_w = max(len(r["name"]) for r in rows)
    lines = [f"SIGNAL // stargazers across {USER}   ·   synced {now:%Y-%m-%d}",
             "─" * 66]
    for r in rows:
        bar = BLOCKS * round(28 * r["stars"] / top) if r["stars"] else ""
        bar = bar or "▏"
        lines.append(f"{r['name']:<{name_w}}  {bar:<28} {r['stars']:>4}  {r['note']}")
    lines += ["─" * 66,
              f"{'TOTAL':<{name_w}}  {'':<28} {total:>4}"]
    return "\n".join(lines)


def main():
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None, microsecond=0)
    all_repos = repos()
    total = sum(r["stargazers_count"] for r in all_repos)

    rows = []
    for r in all_repos[:TOP_N]:
        note = r["language"] or "—"
        if r["name"].lower() == USER.lower():
            note = "you are here"
        rows.append({"name": r["name"], "stars": r["stargazers_count"], "note": note})

    series = []
    for i, r in enumerate(all_repos[:CHARTED]):
        if r["stargazers_count"] == 0:
            continue
        series.append((r["name"], SERIES_COLOURS[i % len(SERIES_COLOURS)],
                       stargazers(r["full_name"])))

    svg = chart(series, now)
    if svg:
        (ROOT / "stars.svg").write_text(svg)
        print(f"stars.svg: {len(svg)} bytes, {len(series)} series")

    readme = ROOT / "README.md"
    text = readme.read_text()
    block = signal_block(rows, total, now)
    new = re.sub(
        r"(<!-- STARS:START -->\n```\n).*?(\n```\n<!-- STARS:END -->)",
        lambda m: m.group(1) + block + m.group(2),
        text, flags=re.S,
    )
    if new != text:
        readme.write_text(new)
        print("README.md SIGNAL block updated")
    else:
        print("README.md unchanged")
    print(block)


if __name__ == "__main__":
    main()
