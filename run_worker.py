import os
import time
import logging
from datetime import datetime

from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.models import Article
from rss.fetcher import fetch_all_feeds
from rss.processor import save_entry_if_new
from services.content_generator import generate_article_from_summary
from bot.telegram_bot import send_photo_with_caption, send_text_to_channel
from utils.logging_config import setup_logging

load_dotenv()
logger = logging.getLogger(__name__)


def publish_one_article() -> None:
    """
    Публікує одну неопубліковану статтю в Telegram.
    """
    app = create_app()
    with app.app_context():
        article = Article.query.filter_by(posted_to_telegram=False).first()
        if not article:
            logger.info("Немає неопублікованих статей для публікації")
            return

        logger.info("Публікую статтю: %s", article.title)
        try:
            if article.generated_content:
                if article.image_url:
                    send_photo_with_caption(
                        photo_url=article.image_url,
                        caption=article.generated_content,
                    )
                else:
                    send_text_to_channel(text=article.generated_content)

                article.posted_to_telegram = True
                article.posted_at = datetime.utcnow()
                db.session.commit()
                logger.info("Опубліковано в Telegram: %s", article.title)
            else:
                logger.warning("Стаття %s не має згенерованого контенту", article.id)
        except Exception as exc:
            logger.exception("Помилка публікації статті %s: %s", article.id, exc)


def process_new_articles() -> None:
    """
    Обробляє RSS: завантажує, зберігає нові статті та генерує контент.
    Публікація відбувається окремо.
    """
    app = create_app()
    with app.app_context():
        feeds = fetch_all_feeds()
        logger.info("Завантажено %d RSS-стрічок", len(feeds))

        new_articles: list[Article] = []

        # Зберігаємо нові статті
        for source_url, feed in feeds:
            for entry in feed.entries:
                article = save_entry_if_new(source_url, entry)
                if article:
                    logger.info("Нова стаття: %s", article.title)
                    new_articles.append(article)

        # Генеруємо контент для нових статей
        for article in new_articles:
            logger.info("Починаю обробку статті: %s", article.title)
            try:
                # Примітивне самарі на зараз: беремо опис з RSS, доробимо пізніше
                summary = getattr(getattr(article, "summary", None), "strip", lambda: "")()
                if not summary:
                    summary = article.title
                logger.info("Summary для статті: %s", summary[:100])

                logger.info("Генерую контент через OpenAI для статті: %s", article.title)
                generated = generate_article_from_summary(
                    summary=summary,
                    original_title=article.title,
                    source=article.source,
                )
                if generated:
                    logger.info("Згенеровано контент довжиною %d символів", len(generated))
                    article.generated_content = generated
                    db.session.commit()
                    logger.info("Збережено згенерований контент для статті: %s", article.title)
                else:
                    logger.warning("Не вдалося згенерувати контент для статті: %s", article.title)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Помилка обробки статті %s: %s", article.id, exc)


def main():
    """
    Основний цикл воркера:
    - RSS перевіряється раз на день.
    - Публікація: кожні 3 години по одній статті.
    - При запуску: відразу публікує одну, якщо є.
    """
    setup_logging()
    rss_interval = 86400  # 1 день
    publish_interval = 10800  # 3 години

    app = create_app()
    with app.app_context():
        total_articles = Article.query.count()
        unpublished = Article.query.filter_by(posted_to_telegram=False).count()
        logger.info("Кількість статей в БД: %d, неопублікованих: %d", total_articles, unpublished)

    last_rss = 0
    last_publish = time.time()  # щоб відразу опублікувати

    logger.info("Старт воркера. RSS інтервал: %s сек, Публікація: %s сек", rss_interval, publish_interval)

    # При запуску відразу перевіряємо RSS та генеруємо контент
    process_new_articles()
    last_rss = time.time()

    # Потім публікуємо одну статтю
    publish_one_article()
    last_publish = time.time()

    while True:
        now = time.time()

        # Перевірка RSS раз на день
        if now - last_rss >= rss_interval:
            try:
                process_new_articles()
                last_rss = now
            except Exception as exc:
                logger.exception("Помилка обробки RSS: %s", exc)

        # Публікація кожні 3 години
        if now - last_publish >= publish_interval:
            try:
                publish_one_article()
                last_publish = now
            except Exception as exc:
                logger.exception("Помилка публікації: %s", exc)

        time.sleep(60)  # Перевірка кожну хвилину


if __name__ == "__main__":
    main()