# Daily Grace for Mom

A simple Catholic comfort site that shows a fresh prayer, thought, blessing, and link to the USCCB Daily Mass Readings each morning.

## Files

- `index.html` — the static website
- `styles.css` — warm, comforting Catholic-inspired design
- `app.js` — loads the generated daily content
- `scripts/update_daily.py` — writes `data/today.json`
- `data/today.json` — current day’s prayer content
- `logs/update.log` — cron output

## Manual update

```bash
cd /home/hermes/mom-daily-prayers
/usr/bin/python3 scripts/update_daily.py
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
0 6 * * * cd /home/hermes/mom-daily-prayers && /usr/bin/python3 scripts/update_daily.py >> /home/hermes/mom-daily-prayers/logs/update.log 2>&1
```

The generator is intentionally network-free for reliability. The site links to USCCB for the official daily readings rather than copying them.
