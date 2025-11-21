import os
from dotenv import load_dotenv

# Завантажуємо .env на рівні модуля,
# щоб усі змінні були доступні одразу
load_dotenv()


class BaseConfig:
    """Базова конфігурація Flask-додатку."""

    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change_me")

    # Налаштування БД
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///auto_car_rss_bot.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Схема БД (для PostgreSQL)
    DB_SCHEMA = os.getenv("DB_SCHEMA", "auto_car_bot")

    # Налаштування мови та часової зони
    APP_LANGUAGE = os.getenv("APP_LANGUAGE", "uk")
    APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Europe/Berlin")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
    TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID", "")

    # RSS
    RSS_FEEDS = os.getenv("RSS_FEEDS", "")
    RSS_POLL_INTERVAL_SECONDS = int(os.getenv("RSS_POLL_INTERVAL_SECONDS", "3600"))

    # Логування
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    APP_MODE = os.getenv("APP_MODE", "ALL")


class DevelopmentConfig(BaseConfig):
    """Конфіг для розробки."""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Конфіг для продакшена."""
    DEBUG = False


def get_config(name: str | None):
    """
    Вибір класу конфігурації по імені.
    Якщо name None або невідоме — повертаємо DevelopmentConfig.
    """
    mapping = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
    }
    if not name:
        name = os.getenv("FLASK_ENV", "development")
    return mapping.get(name, DevelopmentConfig)