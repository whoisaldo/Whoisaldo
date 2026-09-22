#!/usr/bin/env python3
"""Writes hero.svg, the banner at the top of the README.

Composition, top to bottom: a full-width beam, the ALDO wordmark with its
chromatic glitch, a short beam under it, the tagline, a full-width beam.
The beams are the same construction as the section dividers (dashed rail,
volt ticks, a travelling comet), so the page reads as one system.

Run: python3 scripts/generate-hero.py
"""
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1000, 360
INK, CYAN, PINK, VOLT = "#07070C", "#00F0FF", "#FF2E88", "#FCEE0A"
BRIGHT, DIM, GREEN = "#EAFEFF", "#5B6470", "#39FF7A"
MONO = "'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def beam(x0, width, y, colour, seed, comet="p", comet_dur=3.4, spark_dur=2.1, spark_begin=1.1):
    """A dashed rail with volt ticks and two comets sliding along it."""
    rng = random.Random(seed)
    gid = colour[1:]
    segs, x = [], 0
    while x < width:
        seg = min(rng.choice([18, 26, 34, 40, 96, 118, 158, 214]), width - x)
        op = 0.55 if seg > 60 else rng.choice([0.22, 0.3])
        segs.append(f'<rect x="{x0 + x}" y="{y - 1}" width="{seg}" height="2" rx="1" opacity="{op}"/>')
        x += seg + 8
    ticks = []
    for i, x in enumerate(range(0, width + 1, 38)):
        h = 5 if i % 3 == 0 else 2.5
        ticks.append(f'<line x1="{x0 + x}" y1="{y - h / 2}" x2="{x0 + x}" y2="{y + h / 2}"/>')
    return "\n".join([
        f'<g clip-path="url(#clip{seed})">',
        f'<g fill="{colour}" filter="url(#g{gid})">' + "".join(segs) + "</g>",
        f'<g stroke="{VOLT}" stroke-width="1" opacity="0.34">' + "".join(ticks) + "</g>",
        f'<rect x="{x0}" y="{y - 2.5}" width="132" height="5" rx="2.5" fill="url(#{comet}{gid})" filter="url(#g{gid})">'
        f'<animateTransform attributeName="transform" type="translate" from="-140 0" to="{width} 0" '
        f'dur="{comet_dur}s" repeatCount="indefinite"/></rect>',
        f'<rect x="{x0}" y="{y - 1.5}" width="46" height="3" rx="1.5" fill="{VOLT}" opacity="0.5" filter="url(#g{gid})">'
        f'<animateTransform attributeName="transform" type="translate" from="-60 0" to="{width} 0" '
        f'dur="{spark_dur}s" begin="{spark_begin}s" repeatCount="indefinite"/></rect>',
        "</g>",
    ])


def beam_defs(colour):
    gid = colour[1:]
    return (
        f'<filter id="g{gid}" x="-10%" y="-200%" width="120%" height="500%"><feGaussianBlur stdDeviation="1.5"/></filter>'
        f'<linearGradient id="p{gid}" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{colour}" stop-opacity="0"/><stop offset="0.45" stop-color="{colour}" stop-opacity="1"/>'
        f'<stop offset="0.55" stop-color="{BRIGHT}" stop-opacity="1"/><stop offset="1" stop-color="{colour}" stop-opacity="0"/>'
        f'</linearGradient>'
    )


# the wordmark, four glyphs drawn as strokes so every layer can restyle them
WORD = (
    '<g id="word" fill="none" stroke="currentColor" stroke-width="18" stroke-linecap="square" stroke-linejoin="miter">'
    '<g transform="translate(225,72)"><path d="M8,140 L50,8 L92,140"/><path d="M28,94 L72,94"/></g>'
    '<g transform="translate(375,72)"><path d="M18,8 L18,140 L92,140"/></g>'
    '<g transform="translate(525,72)"><path d="M18,140 L18,8 L62,8 L92,38 L92,110 L62,140 Z"/></g>'
    '<g transform="translate(675,72)"><path d="M30,8 L70,8 L92,38 L92,110 L70,140 L30,140 L8,110 L8,38 Z"/></g>'
    "</g>"
)

STYLE = f"""
.hud{{font-family:{MONO}}}
.cy{{transform:translate(-4px,0);animation:jcy 6s steps(1,end) infinite}}
.mg{{transform:translate(4px,0);animation:jmg 6s steps(1,end) infinite}}
.core{{animation:flk 6s linear infinite}}
.s1{{opacity:0;animation:sl1 6s steps(1,end) infinite}}
.s2{{opacity:0;animation:sl2 6s steps(1,end) infinite}}
.s3{{opacity:0;animation:sl3 6s steps(1,end) infinite}}
.sweep{{animation:swp 9s linear infinite}}
.cur{{animation:blink 1.06s steps(1,end) infinite}}
.dot{{animation:blink 1.4s steps(1,end) infinite}}
@keyframes jcy{{0%,84%,100%{{transform:translate(-4px,0)}}85%{{transform:translate(-13px,1px)}}87%{{transform:translate(3px,-1px)}}89%{{transform:translate(-8px,2px)}}91%{{transform:translate(-4px,0)}}95%{{transform:translate(-14px,-2px)}}96.5%{{transform:translate(-4px,0)}}}}
@keyframes jmg{{0%,84%,100%{{transform:translate(4px,0)}}85%{{transform:translate(13px,-1px)}}87%{{transform:translate(-3px,1px)}}89%{{transform:translate(8px,-2px)}}91%{{transform:translate(4px,0)}}95%{{transform:translate(14px,2px)}}96.5%{{transform:translate(4px,0)}}}}
@keyframes flk{{0%,100%{{opacity:1}}85%{{opacity:.45}}86%{{opacity:1}}90%{{opacity:.7}}91%{{opacity:1}}95.5%{{opacity:.3}}96.5%{{opacity:1}}}}
@keyframes sl1{{0%,84.5%,100%{{opacity:0;transform:translate(0,0)}}85%{{opacity:1;transform:translate(26px,0)}}86.5%{{opacity:0;transform:translate(0,0)}}95%{{opacity:1;transform:translate(-18px,0)}}96%{{opacity:0;transform:translate(0,0)}}}}
@keyframes sl2{{0%,86.5%,100%{{opacity:0;transform:translate(0,0)}}87%{{opacity:1;transform:translate(-22px,0)}}88.5%{{opacity:0;transform:translate(0,0)}}95.5%{{opacity:1;transform:translate(14px,0)}}96.5%{{opacity:0;transform:translate(0,0)}}}}
@keyframes sl3{{0%,89%,100%{{opacity:0;transform:translate(0,0)}}89.5%{{opacity:1;transform:translate(17px,0)}}90.5%{{opacity:0;transform:translate(0,0)}}}}
@keyframes swp{{0%{{transform:translateY(-90px)}}100%{{transform:translateY(390px)}}}}
@keyframes blink{{0%,52%{{opacity:1}}53%,100%{{opacity:0}}}}
""".strip()


def main():
    o = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="ALDO. Software engineer. Systems, iOS and web. Boston.">',
        "<defs>",
        f"<style><![CDATA[\n{STYLE}\n]]></style>",
        f'<radialGradient id="vig" cx="50%" cy="42%" r="75%"><stop offset="48%" stop-color="{INK}" stop-opacity="0"/>'
        f'<stop offset="100%" stop-color="{INK}" stop-opacity="0.94"/></radialGradient>',
        f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">'
        f'<path d="M32 0 H0 V32" fill="none" stroke="{CYAN}" stroke-width="0.5" opacity="0.055"/></pattern>',
        '<pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#000000" opacity="0.24"/></pattern>',
        f'<linearGradient id="sweepg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{CYAN}" stop-opacity="0.13"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>',
        '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<filter id="soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="1.5"/></filter>',
        '<filter id="halo" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="15"/></filter>',
        beam_defs(CYAN), beam_defs(PINK),
        # the rail under the wordmark runs pink into volt
        f'<linearGradient id="rFF2E88" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PINK}" stop-opacity="0"/>'
        f'<stop offset="0.45" stop-color="{PINK}"/><stop offset="0.55" stop-color="{BRIGHT}"/><stop offset="1" stop-color="{VOLT}" stop-opacity="0"/></linearGradient>',
        WORD,
        '<clipPath id="b1"><rect x="0" y="98" width="1000" height="20"/></clipPath>',
        '<clipPath id="b2"><rect x="0" y="142" width="1000" height="17"/></clipPath>',
        '<clipPath id="b3"><rect x="0" y="182" width="1000" height="21"/></clipPath>',
        '<clipPath id="clip1"><rect x="0" y="0" width="1000" height="24"/></clipPath>',
        '<clipPath id="clip2"><rect x="0" y="336" width="1000" height="24"/></clipPath>',
        '<clipPath id="clip3"><rect x="228" y="231" width="544" height="24"/></clipPath>',
        "</defs>",
        f'<rect width="{W}" height="{H}" fill="{INK}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#vig)"/>',
        f'<rect class="sweep" x="0" y="0" width="{W}" height="90" fill="url(#sweepg)"/>',
        # framing beams
        beam(0, W, 12, CYAN, 1, comet_dur=4.6, spark_dur=2.9, spark_begin=1.3),
        beam(0, W, 348, PINK, 2, comet_dur=5.2, spark_dur=3.1, spark_begin=0.6),
        # wordmark
        f'<use href="#word" color="{CYAN}" filter="url(#halo)" opacity="0.33"/>',
        f'<use href="#word" class="cy" color="{CYAN}" filter="url(#soft)" opacity="0.9" style="mix-blend-mode:screen"/>',
        f'<use href="#word" class="mg" color="{PINK}" filter="url(#soft)" opacity="0.9" style="mix-blend-mode:screen"/>',
        f'<use href="#word" class="core" color="{BRIGHT}" filter="url(#glow)"/>',
        f'<g clip-path="url(#b1)" class="s1"><use href="#word" color="{VOLT}"/></g>',
        f'<g clip-path="url(#b2)" class="s2"><use href="#word" color="{CYAN}"/></g>',
        f'<g clip-path="url(#b3)" class="s3"><use href="#word" color="{PINK}"/></g>',
        # rail + tagline
        beam(228, 544, 243, PINK, 3, comet="r"),
        f'<text class="hud" x="500" y="280" text-anchor="middle" font-size="14.5" letter-spacing="3.4" fill="{VOLT}">'
        f'&gt; SOFTWARE ENGINEER<tspan fill="{DIM}">  ::  </tspan><tspan fill="{BRIGHT}">SYSTEMS</tspan>'
        f'<tspan fill="{DIM}"> // </tspan><tspan fill="{BRIGHT}">iOS</tspan><tspan fill="{DIM}"> // </tspan>'
        f'<tspan fill="{BRIGHT}">WEB</tspan><tspan class="cur" fill="{CYAN}"> _</tspan></text>',
        # corners + readouts
        f'<g fill="none" stroke="{CYAN}" stroke-width="1.5" opacity="0.8">'
        '<path d="M16,50 L16,24 L42,24"/><path d="M958,24 L984,24 L984,50"/>'
        '<path d="M16,310 L16,336 L42,336"/><path d="M958,336 L984,336 L984,310"/></g>',
        '<g class="hud" font-size="10.5" letter-spacing="1.6">'
        f'<text x="52" y="39" fill="{CYAN}" opacity="0.72">WHOISALDO.EXE</text>'
        f'<text x="948" y="39" text-anchor="end" fill="{CYAN}" opacity="0.72">SYS://ONLINE</text>'
        f'<circle class="dot" cx="958" cy="35.5" r="3" fill="{GREEN}"/>'
        f'<text x="52" y="327" fill="{PINK}" opacity="0.75">LOC: BOSTON.MA</text>'
        f'<text x="948" y="327" text-anchor="end" fill="{VOLT}" opacity="0.72">BUILD//2027</text></g>',
        f'<rect width="{W}" height="{H}" fill="url(#scan)" pointer-events="none"/>',
        "</svg>",
    ]
    svg = "\n".join(o) + "\n"
    (ROOT / "hero.svg").write_text(svg)
    print(f"hero.svg: {len(svg)} bytes")


if __name__ == "__main__":
    main()
