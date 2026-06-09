# Daily Grace for Meme

A simple Catholic comfort site that shows a fresh prayer, thought, blessing, family image, and link to the USCCB Daily Mass Readings each morning.

Live site: https://dustincole-data.github.io/daily-grace-for-mom/

## Files

- `index.html` — the static website
- `styles.css` — warm, comforting Catholic-inspired design
- `app.js` — loads the generated daily content and current image
- `scripts/update_daily.py` — writes `data/today.json` and chooses the day’s image
- `scripts/publish_daily.sh` — cron entrypoint: generate, commit, push, then email the day’s material
- `scripts/send_daily_email.py` — sends Melanie the day’s prayer, thought, image, and site link through Gmail
- `assets/photos/` — rotating family images
- `data/today.json` — current day’s prayer content
- `logs/update.log` — cron output, not committed

## Manual update

```bash
cd /home/hermes/mom-daily-prayers
PRAYER_SITE_TZ=America/New_York /usr/bin/python3 scripts/update_daily.py
```

## Manual publish + email

```bash
/home/hermes/mom-daily-prayers/scripts/publish_daily.sh
```

## Email dry-run

```bash
cd /home/hermes/mom-daily-prayers
/usr/bin/python3 scripts/send_daily_email.py --dry-run
```

## Local preview

```bash
cd /home/hermes/mom-daily-prayers
/usr/bin/python3 -m http.server 8088
```

Then open: http://localhost:8088

## Cron schedule

Installed in the user crontab with Eastern time:

```cron
CRON_TZ=America/New_York
0 6 * * * /home/hermes/mom-daily-prayers/scripts/publish_daily.sh >> /home/hermes/mom-daily-prayers/logs/update.log 2>&1
```

The generator is intentionally network-free for reliability. The site links to USCCB for the official daily readings rather than copying them.
