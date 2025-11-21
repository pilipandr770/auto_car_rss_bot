import os
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def send_text_to_channel(text: str, channel_id: Optional[str] = None) -> None:
    """
    Надсилає текстове повідомлення в канал.
    Якщо channel_id не переданий — беремо TELEGRAM_CHANNEL_ID з .env.
    """
    if channel_id is None:
        channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

    if not channel_id:
        raise RuntimeError("TELEGRAM_CHANNEL_ID не налаштовано в .env")

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не налаштовано в .env")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": channel_id,
        "text": text,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=data)
    result = response.json()

    if not result.get("ok"):
        logger.error(f"Помилка надсилання повідомлення в Telegram: {result.get('description', 'Невідома помилка')}")
        raise Exception(f"Telegram API error: {result}")


def send_photo_with_caption(
    photo_url: str,
    caption: str,
    channel_id: Optional[str] = None,
) -> None:
    """
    Надсилає фото з підписом (caption) у канал.
    """
    if channel_id is None:
        channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

    if not channel_id:
        raise RuntimeError("TELEGRAM_CHANNEL_ID не налаштовано в .env")

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не налаштовано в .env")

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    data = {
        "chat_id": channel_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=data)
    result = response.json()

    if not result.get("ok"):
        logger.error(f"Помилка надсилання фото в Telegram: {result.get('description', 'Невідома помилка')}")
        raise Exception(f"Telegram API error: {result}")