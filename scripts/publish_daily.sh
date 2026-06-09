#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/hermes/mom-daily-prayers"
cd "$ROOT"

# Keep local checkout current before writing a daily update.
git pull --ff-only origin main

PRAYER_SITE_TZ=America/New_York /usr/bin/python3 scripts/update_daily.py

git add data/*.json
if git diff --cached --quiet; then
  echo "No daily prayer changes to commit."
  exit 0
fi

git commit -m "Update daily prayer $(TZ=America/New_York date +%F)"
git push origin main
