#!/usr/bin/env bash
# Refresh the stat cards in cards/ and stars.svg so the README serves them
# from the repo instead of depending on third-party card services at view time.
# Both are generated from the GitHub API (the public github-readme-stats
# instance is paused). A failed refresh keeps the previous copy —
# the profile never shows an error card.
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p cards

status=0

if python3 scripts/generate-cards.py; then
  echo "ok: cards/stats.svg + cards/top-langs.svg (generated from GitHub API)"
else
  echo "warn: card generation failed; keeping previous copies" >&2
  status=1
fi

if python3 scripts/update_stars.py; then
  echo "ok: stars.svg"
else
  echo "warn: star refresh failed; keeping previous copy" >&2
  status=1
fi

exit $status
