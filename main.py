import feedparser
import json
import requests
import os
import time
from datetime import datetime, timezone, timedelta

WEBHOOK_URL = "dummy"
FEED_URL = "https://www.apple.com/jp/newsroom/rss-feed.rss"
DELTA_MINUTES = 30


def notify_discord(entry):
    title = entry.title
    url = entry.link
    description = entry.summary
    image_url = None
    for link in entry.links:
        if link.get("rel") == "enclosure" and link.get("type", "").startswith("image/"):
            image_url = link["href"]
            break

    embed = {
        "title": title,
        "url": url,
        "description": description,
        "color": 16777215,
        "image": {"url": image_url} if image_url else {},
        "footer": {"text": "Apple Newsroom Japan"}
    }

    # print(embed)
    # print()

    payload = {
        "content": "🆕 Apple Newsroomに新しい記事が投稿されました！",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=payload)


def main():
    feed = feedparser.parse(FEED_URL)
    now = datetime.now(timezone.utc)
    for entry in feed.entries:
        updated_dt = datetime.fromtimestamp(time.mktime(entry.updated_parsed), tz=timezone.utc)
        delta = now - updated_dt
        if delta <= timedelta(minutes=DELTA_MINUTES):
            notify_discord(entry)


if __name__ == "__main__":
    main()
