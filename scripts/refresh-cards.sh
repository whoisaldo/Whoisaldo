#!/usr/bin/env bash
# Refresh the stat cards in cards/ so the README serves them from the repo
# instead of depending on third-party card services at view time.
# stats.svg + top-langs.svg are generated from the GitHub API (the public
# github-readme-stats instance is paused); streak.svg is fetched from the
# maintained demolab instance. A failed refresh keeps the previous copy —
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

fetch() {
  local url="$1" out="$2" tmp code=000
  tmp="$(mktemp)"
  for attempt in $(seq 1 10); do
    code="$(curl -sS -o "$tmp" -w '%{http_code}' "$url" 2>/dev/null || echo 000)"
    if [ "$code" = 200 ] && grep -q '<svg' "$tmp" \
      && ! grep -qiE 'something went wrong|maximum retries|rate limit' "$tmp"; then
      mv "$tmp" "$out"
      echo "ok: $out (attempt $attempt)"
      return 0
    fi
    sleep 8
  done
  rm -f "$tmp"
  echo "warn: could not refresh $out (last HTTP $code); keeping previous copy" >&2
  return 1
}

if python3 scripts/update_stars.py; then
  echo "ok: stars.svg + README SIGNAL block"
else
  echo "warn: star refresh failed; keeping previous copy" >&2
  status=1
fi

fetch 'https://streak-stats.demolab.com/?user=whoisaldo&hide_border=true&background=07070C&stroke=00F0FF&ring=FF2E88&fire=FCEE0A&currStreakLabel=00F0FF&sideLabels=EAFEFF&currStreakNum=EAFEFF&sideNums=EAFEFF&dates=5B6470' cards/streak.svg || status=1

exit $status
