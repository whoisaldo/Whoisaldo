#!/usr/bin/env python3
"""Regenerates stars.svg and the SIGNAL block in README.md from the GitHub API.

stars.svg is a live meter, not a time series, and that is deliberate. It was a
cumulative-stargazers-over-time chart first. Plotted against a date axis, a repo
that picks up most of its stars in a short window renders as a near-vertical
wall, and the honest reading of that shape competes with a much worse one:
that the stars were bought. They were not. Removing the time axis removes the
question, and for a profile README the interesting number was never the slope
anyway. It is how many.

So: no dates, no x-axis, no growth rate. Counts, ranked, with a bar each.
Do not reintroduce a time axis here.

star-history.com is unusable for the same reason plus a second one: it is a time
series by construction, and its SVG endpoint hardcodes an xkcd hand-drawn font
with no parameter to turn it off.

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
TOP_N = 4          # rows in both the SIGNAL block and the meter panel

INK, VOLT, FUCH, CYAN = "#07070C", "#FCEE0A", "#FF2E88", "#00F0FF"
BRIGHT, DIM = "#EAFEFF", "#5B6470"
SERIES_COLOURS = [VOLT, FUCH, CYAN]
GREEN = "#39FF7A"

W, H = 820, 248
SEGMENTS = 42      # LED cells in a full bar


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


# ----------------------------------------------------------------- the panel
def panel(rows, total, now):
    """A ranked meter. Deliberately has no time axis — see the module docstring."""
    top = max((r["stars"] for r in rows), default=0) or 1
    o = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Stargazer counts by repository">',
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
         "@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:.15}}"
         ".live{animation:blink 1.5s steps(1,end) infinite}"
         "]]></style>",
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#g)"/>']

    # header
    o.append(f'<text class="t" x="40" y="34" font-size="11" fill="{VOLT}" letter-spacing="2.4">'
             f'&gt; STARGAZERS // LIVE</text>')
    o.append(f'<circle class="live" cx="232" cy="30" r="3.5" fill="{GREEN}"/>')
    o.append(f'<text class="t" x="{W-40}" y="34" text-anchor="end" font-size="9" fill="{DIM}" '
             f'letter-spacing="1.2">SYNCED {now:%Y-%m-%d}</text>')
    o.append(f'<line x1="40" y1="48" x2="{W-40}" y2="48" stroke="{DIM}" stroke-width="1" opacity="0.3"/>')

    # total, left
    o.append(f'<text class="t" x="40" y="82" font-size="9.5" fill="{DIM}" letter-spacing="2">TOTAL</text>')
    o.append(f'<text class="t" x="40" y="152" font-size="64" fill="{VOLT}" filter="url(#glow)">{total}</text>')
    o.append(f'<text class="t" x="40" y="176" font-size="9.5" fill="{BRIGHT}" letter-spacing="2">STARGAZERS</text>')
    o.append(f'<text class="t" x="40" y="194" font-size="9" fill="{DIM}" letter-spacing="1.2">'
             f'ACROSS {len(rows)} TRACKED REPOS</text>')
    o.append(f'<line x1="252" y1="62" x2="252" y2="{H-30}" stroke="{DIM}" stroke-width="1" opacity="0.3"/>')

    # meters, right
    x0, bar_w = 280, W - 40 - 280
    seg_w = bar_w / SEGMENTS
    for i, r in enumerate(rows):
        col = SERIES_COLOURS[i] if i < len(SERIES_COLOURS) else DIM
        y = 84 + i * 40
        lit = max(1, round(SEGMENTS * r["stars"] / top)) if r["stars"] else 0
        o.append(f'<text class="t" x="{x0}" y="{y}" font-size="11.5" fill="{BRIGHT}">{r["name"]}</text>')
        note_x = x0 + len(r["name"]) * 6.92 + 12
        o.append(f'<text class="t" x="{note_x:.1f}" y="{y}" font-size="8.5" fill="{DIM}" '
                 f'letter-spacing="1">{r["note"].upper()}</text>')
        o.append(f'<text class="t" x="{W-40}" y="{y}" text-anchor="end" font-size="15" fill="{col}">'
                 f'{r["stars"]}</text>')
        for k in range(SEGMENTS):
            sx = x0 + k * seg_w
            if k < lit:
                o.append(f'<rect x="{sx:.1f}" y="{y+8}" width="{seg_w-2:.1f}" height="8" fill="{col}">'
                         f'<animate attributeName="opacity" values="1;0.72;1" dur="2.4s" '
                         f'begin="{k*0.045:.2f}s" repeatCount="indefinite"/></rect>')
            else:
                o.append(f'<rect x="{sx:.1f}" y="{y+8}" width="{seg_w-2:.1f}" height="8" '
                         f'fill="{DIM}" opacity="0.16"/>')

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

    svg = panel(rows, total, now)
    (ROOT / "stars.svg").write_text(svg)
    print(f"stars.svg: {len(svg)} bytes, {len(rows)} meters")

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
