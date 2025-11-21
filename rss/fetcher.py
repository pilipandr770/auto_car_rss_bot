import os
from typing import List

import feedparser


def get_rss_feed_urls() -> List[str]:
    """
    Зчитує список RSS-URL із змінної оточення RSS_FEEDS.
    Очікується формат: url1,url2,url3
    """
    raw = os.getenv("RSS_FEEDS", "")
    urls = [u.strip() for u in raw.split(",") if u.strip()]
    return urls


def fetch_feed(url: str):
    """
    Завантажує одну RSS-стрічку та повертає результат feedparser.
    """
    return feedparser.parse(url)


def fetch_all_feeds():
    """
    Ітерується по всіх RSS-URL та повертає список кортежів:
    [(url, feed_result), ...]
    """
    urls = get_rss_feed_urls()
    results = []
    for url in urls:
        feed = fetch_feed(url)
        results.append((url, feed))
    return results