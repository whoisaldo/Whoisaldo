#!/usr/bin/env python3
"""Generate cards/stats.svg and cards/top-langs.svg for the profile README.

Replaces the github-readme-stats.vercel.app dependency (deployment paused as of
Aug 2026): pulls the same numbers straight from the GitHub API via `gh` and
renders them in the profile palette. Run through scripts/refresh-cards.sh,
locally or in the refresh-cards workflow (needs GH_TOKEN there).
"""
import html
import json
import subprocess
import sys

USER = "whoisaldo"

BG = "#0A0A0F"
CYAN = "#00F0FF"
PINK = "#FF2D78"
YELLOW = "#FFE600"
TEXT = "#EAFEFF"
DIM = "#5B6470"
MONO = "'JetBrains Mono','Fira Code',ui-monospace,Menlo,Consolas,monospace"

# Octicons (16x16), MIT licensed path data
ICONS = {
    "star": "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z",
    "commit": "M10.5 7.75a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0Zm1.43.75a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Z",
    "pr": "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z",
    "issue": "M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm0-9.5a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z",
    "repo": "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1V1.5h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25v3.25a.25.25 0 0 0 .4.2l1.45-1.087a.249.249 0 0 1 .3 0L8.6 15.7a.25.25 0 0 0 .4-.2v-3.25a.25.25 0 0 0-.25-.25h-3.5a.25.25 0 0 0-.25.25Z",
    "octocat": "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z",
}

GRAPHQL = """
query($login: String!) {
  user(login: $login) {
    name
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestReviewContributions
    }
    repositoriesContributedTo(contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def gh(*args):
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    ).stdout


def fetch():
    user = json.loads(
        gh("api", "graphql", "-f", f"query={GRAPHQL}", "-F", f"login={USER}")
    )["data"]["user"]

    contrib = user["contributionsCollection"]
    restricted = contrib["restrictedContributionsCount"]
    try:
        public_commits = int(
            gh("api", f"search/commits?q=author:{USER}+is:public",
               "--jq", ".total_count").strip()
        )
        commits = public_commits + restricted
    except (subprocess.CalledProcessError, ValueError):
        commits = contrib["totalCommitContributions"] + restricted

    langs = {}
    stars = 0
    for repo in user["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            color = edge["node"]["color"] or DIM
            size, _ = langs.get(name, (0, color))
            langs[name] = (size + edge["size"], color)

    return {
        "name": user["name"] or USER,
        "stars": stars,
        "commits": commits,
        "prs": user["pullRequests"]["totalCount"],
        "issues": user["issues"]["totalCount"],
        "reviews": contrib["totalPullRequestReviewContributions"],
        "followers": user["followers"]["totalCount"],
        "contributed": user["repositoriesContributedTo"]["totalCount"],
        "langs": langs,
    }


def rank_percentile(d):
    # Mirrors github-readme-stats' rank algorithm (all-commits medians)
    def exp_cdf(x):
        return 1 - 2 ** (-x)

    def log_norm_cdf(x):
        return x / (1 + x)

    parts = [
        (2, exp_cdf(d["commits"] / 1000)),
        (3, exp_cdf(d["prs"] / 50)),
        (1, exp_cdf(d["issues"] / 25)),
        (1, exp_cdf(d["reviews"] / 2)),
        (4, log_norm_cdf(d["stars"] / 50)),
        (1, log_norm_cdf(d["followers"] / 10)),
    ]
    total_weight = sum(w for w, _ in parts)
    return (1 - sum(w * v for w, v in parts) / total_weight) * 100


def stats_svg(d):
    rows = [
        ("star", "Total Stars Earned", d["stars"]),
        ("commit", "Total Commits", d["commits"]),
        ("pr", "Total PRs", d["prs"]),
        ("issue", "Total Issues", d["issues"]),
        ("repo", "Contributed to", d["contributed"]),
    ]
    body = []
    y = 66
    for icon, label, value in rows:
        body.append(
            f'<g transform="translate(25,{y - 12})">'
            f'<path fill="{PINK}" d="{ICONS[icon]}"/></g>'
            f'<text class="row" x="50" y="{y}">{html.escape(label)}:</text>'
            f'<text class="row val" x="248" y="{y}">{value}</text>'
        )
        y += 25

    prog = max(2.0, min(100.0, 100 - rank_percentile(d)))
    r = 40
    circ = 2 * 3.14159 * r
    dash = circ * prog / 100
    ring = (
        f'<g transform="translate(375,97)">'
        f'<circle r="{r}" fill="none" stroke="{DIM}" stroke-opacity="0.3" stroke-width="7"/>'
        f'<circle r="{r}" fill="none" stroke="{CYAN}" stroke-width="7" stroke-linecap="round" '
        f'stroke-dasharray="{dash:.1f} {circ:.1f}" transform="rotate(-90)"/>'
        f'<g transform="translate(-16,-16) scale(2)"><path fill="{TEXT}" d="{ICONS["octocat"]}"/></g>'
        f"</g>"
    )

    title = html.escape(f"{d['name']}' GitHub Stats")
    return f"""<svg width="450" height="195" viewBox="0 0 450 195" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}">
  <style>
    .title {{ font: 700 16px {MONO}; fill: {CYAN}; }}
    .row {{ font: 400 13.5px {MONO}; fill: {TEXT}; }}
    .val {{ font-weight: 700; }}
  </style>
  <rect width="450" height="195" rx="4.5" fill="{BG}"/>
  <text class="title" x="25" y="35">{title}</text>
  {"".join(body)}
  {ring}
</svg>
"""


def top_langs_svg(d):
    total = sum(size for size, _ in d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda kv: kv[1][0], reverse=True)[:8]

    bar_w = 270
    x = 0.0
    segments = []
    for name, (size, color) in top:
        w = bar_w * size / total
        segments.append(
            f'<rect x="{x:.2f}" width="{max(w, 2):.2f}" height="8" fill="{color}"/>'
        )
        x += w

    legend = []
    for i, (name, (size, color)) in enumerate(top):
        col, row = divmod(i, 4)
        lx, ly = 25 + col * 145, 78 + row * 21
        pct = 100 * size / total
        legend.append(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{color}"/>'
            f'<text class="lang" x="{lx + 18}" y="{ly}">{html.escape(name)} {pct:.2f}%</text>'
        )

    return f"""<svg width="320" height="165" viewBox="0 0 320 165" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Most Used Languages">
  <style>
    .title {{ font: 700 16px {MONO}; fill: {CYAN}; }}
    .lang {{ font: 400 11px {MONO}; fill: {TEXT}; }}
  </style>
  <rect width="320" height="165" rx="4.5" fill="{BG}"/>
  <text class="title" x="25" y="35">Most Used Languages</text>
  <clipPath id="bar"><rect width="{bar_w}" height="8" rx="4"/></clipPath>
  <g transform="translate(25,49)" clip-path="url(#bar)">
    <rect width="{bar_w}" height="8" fill="{DIM}" fill-opacity="0.3"/>
    {"".join(segments)}
  </g>
  {"".join(legend)}
</svg>
"""


def main():
    d = fetch()
    with open("cards/stats.svg", "w") as f:
        f.write(stats_svg(d))
    with open("cards/top-langs.svg", "w") as f:
        f.write(top_langs_svg(d))
    print(
        f"generated: stars={d['stars']} commits={d['commits']} prs={d['prs']} "
        f"issues={d['issues']} contributed={d['contributed']} "
        f"langs={len(d['langs'])} rank_pct={rank_percentile(d):.1f}"
    )


if __name__ == "__main__":
    sys.exit(main())
