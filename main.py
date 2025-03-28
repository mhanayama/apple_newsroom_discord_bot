#!/usr/bin/python

import feedparser
import json
import requests
import os
import time
import logging
from datetime import datetime, timezone, timedelta

WEBHOOK_URL = "dummy"
FEED_URL = "https://www.apple.com/jp/newsroom/rss-feed.rss"
DELTA_MINUTES = 10


def notify_discord(entry):
    title = entry.title
    url = entry.link
    description = entry.summary
    image_url = None
    for link in entry.links:
        if link.get("rel") == "enclosure" and link.get("type", "").startswith("image/"):
            image_url = link["href"]
            break

    logging.info(f"Sending title: {title}")

    embed = {
        "title": title,
        "url": url,
        "description": description,
        "color": 16777215,
        "image": {"url": image_url} if image_url else {},
        "footer": {"text": "Apple Newsroom Japan - Powered by Masato Hanayama"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    payload = {
        "content": "🍎 Apple Newsroomに新しい記事が投稿されました！",
        "embeds": [embed]
    }
    try:
        res = requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        logging.error(f"Error sending notification: {e}")
    finally:
        logging.info(f"Status Code: {res.status_code}")
        time.sleep(2)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Apple Newsroom Notifier...")
    feed = feedparser.parse(FEED_URL)
    now = datetime.now(timezone.utc)
    for entry in feed.entries:
        updated_dt = datetime.fromtimestamp(time.mktime(entry.updated_parsed), tz=timezone.utc)
        delta = now - updated_dt
        if delta <= timedelta(minutes=DELTA_MINUTES):
            notify_discord(entry)
        # break
    logging.info("All done!")


if __name__ == "__main__":
    main()
