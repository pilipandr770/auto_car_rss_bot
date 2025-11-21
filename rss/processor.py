from datetime import datetime
from typing import Any

from dateutil import parser as date_parser  # треба буде додати в requirements
from app.models import Article
from app.extensions import db


def parse_entry(source_url: str, entry: Any) -> Article:
    """
    Перетворює один RSS-entry в об'єкт Article (ще не збережений у БД).
    Тут ми нормалізуємо поля: title, link, published, image тощо.
    """
    title = getattr(entry, "title", "Без назви")
    link = getattr(entry, "link", "")
    guid = getattr(entry, "id", link)

    # Публікація
    published_at = None
    if getattr(entry, "published", None):
        try:
            published_at = date_parser.parse(entry.published)
        except Exception:
            published_at = None

    # Проста спроба витягнути картинку, далі доробимо
    image_url = None
    if hasattr(entry, "media_content"):
        media = entry.media_content
        if isinstance(media, list) and media:
            image_url = media[0].get("url")

    article = Article(
        source=source_url,
        rss_guid=guid,
        title=title,
        url=link,
        image_url=image_url,
        published_at=published_at,
    )
    return article


def save_entry_if_new(source_url: str, entry: Any) -> Article | None:
    """
    Перевіряє, чи вже існує стаття з таким rss_guid.
    Якщо ні — створює і зберігає новий Article.
    """
    guid = getattr(entry, "id", getattr(entry, "link", None))
    if not guid:
        return None

    existing = Article.query.filter_by(rss_guid=guid).first()
    if existing:
        return None

    article = parse_entry(source_url, entry)
    db.session.add(article)
    db.session.commit()
    return article