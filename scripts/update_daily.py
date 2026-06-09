#!/usr/bin/env python3
"""Generate the daily Catholic prayer/thought content for Meme's comfort site.

No network is required. The site links to the USCCB daily readings rather than
copying full readings, keeping the page reliable and respectful of source rights.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PHOTO_DIR = ROOT / "assets" / "photos"
TZ = ZoneInfo(os.environ.get("PRAYER_SITE_TZ", "America/New_York"))
SITE_URL = "https://dustincole-data.github.io/daily-grace-for-mom/"

DAILY_IMAGES = [
    {"file": "meme-01.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-02.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-03.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-04.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-05.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-06.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-07.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-08.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-09.jpeg", "alt": "A loving family photo for Meme"},
    {"file": "meme-10.jpeg", "alt": "A loving family photo for Meme"},
]

PRAYERS = [
    {
        "title": "Morning Offering",
        "text": "O Jesus, through the Immaculate Heart of Mary, I offer You my prayers, works, joys, and sufferings of this day for all the intentions of Your Sacred Heart, in union with the Holy Sacrifice of the Mass throughout the world. Amen.",
        "source": "Traditional Catholic morning prayer; see USCCB Morning Offering",
        "link": "https://www.usccb.org/prayers/morning-offering",
    },
    {
        "title": "Hail Mary",
        "text": "Hail Mary, full of grace, the Lord is with thee. Blessed art thou among women, and blessed is the fruit of thy womb, Jesus. Holy Mary, Mother of God, pray for us sinners, now and at the hour of our death. Amen.",
        "source": "Traditional Catholic prayer",
        "link": "https://www.usccb.org/prayers/hail-mary",
    },
    {
        "title": "Prayer for Healing and Trust",
        "text": "Lord Jesus, place Your gentle hand upon me today. Bring peace to my body, courage to my heart, and trust to my spirit. Help me receive each kindness as a sign of Your nearness. Amen.",
        "source": "Original prayer inspired by Catholic devotion to Christ the Healer",
        "link": "https://bible.usccb.org/",
    },
    {
        "title": "Memorare",
        "text": "Remember, O most gracious Virgin Mary, that never was it known that anyone who fled to thy protection, implored thy help, or sought thy intercession was left unaided. Inspired by this confidence, I fly unto thee, O Virgin of virgins, my Mother. Amen.",
        "source": "Traditional Marian prayer",
        "link": "https://www.usccb.org/prayers/memorare",
    },
    {
        "title": "Sacred Heart Prayer",
        "text": "Sacred Heart of Jesus, I place all my trust in You. Keep me close to Your mercy today, and let Your love be stronger than my worries. Amen.",
        "source": "Short devotion to the Sacred Heart of Jesus",
        "link": "https://www.usccb.org/prayers/act-consecration-sacred-heart-jesus",
    },
    {
        "title": "Glory Be",
        "text": "Glory be to the Father, and to the Son, and to the Holy Spirit, as it was in the beginning, is now, and ever shall be, world without end. Amen.",
        "source": "Traditional doxology",
        "link": "https://www.usccb.org/prayers/glory-be",
    },
    {
        "title": "Our Father",
        "text": "Our Father, who art in heaven, hallowed be thy name; thy kingdom come; thy will be done on earth as it is in heaven. Give us this day our daily bread, and forgive us our trespasses, as we forgive those who trespass against us. Amen.",
        "source": "The Lord's Prayer",
        "link": "https://www.usccb.org/prayers/our-father",
    },
]

THOUGHTS = [
    {
        "headline": "You are held today.",
        "body": "A hospital room can feel small, but God’s mercy is not small. Let this morning be enough for this morning: one breath, one prayer, one quiet sign of love at a time.",
        "verse": "The Lord is near to the brokenhearted. — Psalm 34:19",
    },
    {
        "headline": "Peace can arrive gently.",
        "body": "You do not need to force strength. Catholic hope is not pretending things are easy; it is trusting that Christ stays close even here, especially here.",
        "verse": "Do not let your hearts be troubled or afraid. — John 14:27",
    },
    {
        "headline": "Mary is praying with you.",
        "body": "When words are hard, let the Blessed Mother carry the prayer. A simple Hail Mary can be a soft place for the heart to rest.",
        "verse": "Blessed are you who believed. — Luke 1:45",
    },
    {
        "headline": "Small graces count.",
        "body": "A good nurse, a warm blanket, a phone call, a moment without pain — each can become a little candle. Notice one mercy today and let it be enough.",
        "verse": "His mercies are renewed each morning. — Lamentations 3:23",
    },
    {
        "headline": "Jesus knows the body’s suffering.",
        "body": "Christ did not love us from far away. He entered weakness, pain, and fear. He is not embarrassed by your needs; He meets you in them.",
        "verse": "Come to me, all you who labor and are burdened, and I will give you rest. — Matthew 11:28",
    },
    {
        "headline": "Today has a holy purpose.",
        "body": "Even a day of waiting can be offered to God. Your prayers, patience, and courage can become a quiet gift for the people you love.",
        "verse": "Offer your bodies as a living sacrifice, holy and pleasing to God. — Romans 12:1",
    },
    {
        "headline": "You are loved beyond measure.",
        "body": "Before any test result, before any update, before anything you can do or cannot do: you are God’s beloved daughter. Nothing in this room can take that away.",
        "verse": "I have called you by name: you are mine. — Isaiah 43:1",
    },
]

BLESSINGS = [
    "May the Lord bless you and keep you in His peace today.",
    "May Our Lady wrap you in her mantle and bring comfort to your heart.",
    "May Christ the Divine Physician bring healing, patience, and hope.",
    "May the Holy Spirit give you quiet courage for each hour.",
    "May your room feel lighter today, filled with grace and love.",
]

LITURGICAL_HINTS = [
    "Light a small candle in your heart and offer this day to Jesus.",
    "If you have the energy, pray one decade of the Rosary slowly.",
    "Ask St. Joseph, patron of families, to guard everyone who loves you.",
    "Make today’s waiting a prayer: ‘Jesus, I trust in You.’",
    "Let gratitude be small today: name one person, one comfort, one grace.",
]


def pick(items: list[dict | str], day_index: int, salt: int = 0):
    return items[(day_index + salt) % len(items)]


def main() -> None:
    now = datetime.now(TZ)
    day_index = int(now.strftime("%j")) + now.year * 17
    prayer = pick(PRAYERS, day_index)
    thought = pick(THOUGHTS, day_index, 2)
    payload = {
        "generated_at": now.isoformat(),
        "display_date": now.strftime("%A, %B %-d, %Y") if os.name != "nt" else now.strftime("%A, %B %#d, %Y"),
        "site_title": "Daily Grace for Meme",
        "site_url": SITE_URL,
        "dedication": "For Meme",
        "daily_image": {
            **pick(DAILY_IMAGES, day_index, 6),
            "url": f"assets/photos/{pick(DAILY_IMAGES, day_index, 6)['file']}",
        },
        "prayer": prayer,
        "thought": thought,
        "blessing": pick(BLESSINGS, day_index, 4),
        "practice": pick(LITURGICAL_HINTS, day_index, 1),
        "daily_readings": {
            "label": "USCCB Daily Mass Readings",
            "url": "https://bible.usccb.org/",
            "note": "Read or listen to today’s Catholic Mass readings from the United States Conference of Catholic Bishops.",
        },
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "today.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    history = DATA_DIR / f"{now.strftime('%Y-%m-%d')}.json"
    history.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {DATA_DIR / 'today.json'} for {payload['display_date']}")


if __name__ == "__main__":
    main()
