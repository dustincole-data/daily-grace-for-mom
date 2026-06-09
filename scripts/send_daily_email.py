#!/usr/bin/env python3
"""Send the Daily Grace for Meme email with the day's prayer and image.

Default mode is --send because this script is called by the approved cron job.
Use --dry-run for validation without sending.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import os
import sys
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "today.json"
SENT_MARKER_DIR = ROOT / "logs" / "email-sent"
DEFAULT_TO = "Melaniecole2323@gmail.com"
DEFAULT_SITE_URL = "https://dustincole-data.github.io/daily-grace-for-mom/"
TOKEN_PATH = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))) / "google_token.json"


def get_gmail_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    if not TOKEN_PATH.exists():
        raise RuntimeError(f"Google token not found at {TOKEN_PATH}")

    token_data = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    scopes = token_data.get("scopes") or ["https://www.googleapis.com/auth/gmail.send"]
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        payload = json.loads(creds.to_json())
        payload.setdefault("type", "authorized_user")
        TOKEN_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if not creds.valid:
        raise RuntimeError("Google credentials are invalid; re-run Google Workspace auth.")
    return build("gmail", "v1", credentials=creds)


def image_part(image_path: Path, cid: str) -> MIMEBase:
    data = image_path.read_bytes()
    subtype = (mimetypes.guess_type(str(image_path))[0] or "image/jpeg").split("/")[-1]
    try:
        part: MIMEBase = MIMEImage(data, _subtype=subtype)
    except TypeError:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(data)
        encoders.encode_base64(part)
    part.add_header("Content-ID", f"<{cid}>")
    part.add_header("Content-Disposition", "attachment", filename=image_path.name)
    return part


def build_message(data: dict, to_addr: str) -> tuple[MIMEMultipart, str, Path]:
    site_url = data.get("site_url") or DEFAULT_SITE_URL
    date = data.get("display_date", "today")
    subject = f"Daily Grace for Meme — {date}"
    prayer = data["prayer"]
    thought = data["thought"]
    daily_image = data.get("daily_image") or {}
    image_url = daily_image.get("url", "")
    image_path = ROOT / image_url
    if not image_path.exists():
        raise FileNotFoundError(f"Daily image is missing: {image_path}")

    cid = "daily-grace-image"
    plain = f"""Daily Grace for Meme — {date}

Today's prayer: {prayer['title']}
{prayer['text']}

Gentle thought: {thought['headline']}
{thought['body']}

{thought['verse']}

Today's blessing: {data['blessing']}
Small practice: {data['practice']}

Open the site: {site_url}
Daily readings: {data['daily_readings']['url']}
"""

    html_body = f"""
    <div style="margin:0;padding:0;background:#fbf7ef;color:#201b18;font-family:Arial,Helvetica,sans-serif;">
      <div style="max-width:680px;margin:0 auto;padding:28px 18px;">
        <div style="background:#fffdf8;border:1px solid #eadcc5;border-radius:28px;padding:28px;box-shadow:0 12px 36px rgba(79,55,26,.08);">
          <p style="margin:0 0 10px;color:#a97922;font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:12px;">Catholic morning prayer</p>
          <h1 style="margin:0;color:#201b18;font-family:Georgia,serif;font-size:42px;line-height:1;">Daily Grace for Meme</h1>
          <p style="margin:12px 0 22px;color:#766f66;font-size:16px;">{html.escape(date)}</p>
          <img src="cid:{cid}" alt="{html.escape(daily_image.get('alt', 'A loving family photo for Meme'))}" style="width:100%;max-height:430px;object-fit:cover;border-radius:22px;border:1px solid #eadcc5;display:block;" />
          <h2 style="font-family:Georgia,serif;font-size:30px;margin:26px 0 8px;color:#201b18;">{html.escape(prayer['title'])}</h2>
          <p style="font-family:Georgia,serif;font-size:22px;line-height:1.45;color:#51453b;margin:0 0 16px;">{html.escape(prayer['text'])}</p>
          <h2 style="font-family:Georgia,serif;font-size:30px;margin:26px 0 8px;color:#201b18;">{html.escape(thought['headline'])}</h2>
          <p style="font-size:17px;line-height:1.65;color:#5f554b;margin:0 0 14px;">{html.escape(thought['body'])}</p>
          <blockquote style="border-left:4px solid #f4dfad;margin:18px 0;padding-left:16px;color:#597ba6;font-weight:700;line-height:1.5;">{html.escape(thought['verse'])}</blockquote>
          <div style="background:#eef2f8;border-radius:20px;padding:20px;margin-top:24px;">
            <p style="margin:0 0 8px;font-weight:700;color:#455b79;">Today’s blessing</p>
            <p style="margin:0;color:#3b4554;font-size:17px;line-height:1.55;">{html.escape(data['blessing'])}</p>
            <p style="margin:16px 0 8px;font-weight:700;color:#455b79;">Small practice</p>
            <p style="margin:0;color:#3b4554;font-size:17px;line-height:1.55;">{html.escape(data['practice'])}</p>
          </div>
          <p style="margin:24px 0 0;"><a href="{html.escape(site_url)}" style="display:inline-block;background:#6d7f9e;color:white;text-decoration:none;padding:13px 18px;border-radius:999px;font-weight:700;">Open today’s page</a></p>
          <p style="margin:16px 0 0;color:#766f66;font-size:14px;">Daily Mass readings: <a href="{html.escape(data['daily_readings']['url'])}" style="color:#6f5523;">USCCB</a></p>
        </div>
      </div>
    </div>
    """

    msg = MIMEMultipart("related")
    msg["To"] = to_addr
    msg["Subject"] = subject
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(plain, "plain", "utf-8"))
    alt.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt)
    msg.attach(image_part(image_path, cid))
    return msg, subject, image_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", default=os.environ.get("DAILY_GRACE_EMAIL_TO", DEFAULT_TO))
    parser.add_argument("--dry-run", action="store_true", help="Build and summarize the email without sending it")
    parser.add_argument("--force", action="store_true", help="Send even if today's local sent marker exists")
    args = parser.parse_args()

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    date_key = (data.get("generated_at") or datetime.now().isoformat())[:10]
    marker = SENT_MARKER_DIR / f"{date_key}.sent"
    msg, subject, image_path = build_message(data, args.to)

    if args.dry_run:
        print(json.dumps({
            "status": "dry-run",
            "to": args.to,
            "subject": subject,
            "image": str(image_path),
            "site_url": data.get("site_url") or DEFAULT_SITE_URL,
            "bytes": len(msg.as_bytes()),
        }, indent=2))
        return 0

    if marker.exists() and not args.force:
        print(f"Email already sent for {date_key}; marker {marker}")
        return 0

    service = get_gmail_service()
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    result = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    SENT_MARKER_DIR.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({"message_id": result.get("id"), "to": args.to, "subject": subject}, indent=2), encoding="utf-8")
    print(json.dumps({"status": "sent", "id": result.get("id"), "to": args.to, "subject": subject}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
