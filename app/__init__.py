from flask import Flask
from .config import get_config
from .extensions import db
from .routes import main_bp
from .models import metadata
from sqlalchemy import text


def create_app(config_name: str | None = None) -> Flask:
    """
    Фабрика створення Flask-додатку.
    Через config_name можна підключати різні конфіги (development/production).
    """
    app = Flask(__name__)

    # Завантажуємо конфігурацію з класів у config.py
    app.config.from_object(get_config(config_name))

    # Ініціалізація розширень (база даних, інше)
    db.init_app(app)

    # Реєструємо Blueprint з маршрутами
    app.register_blueprint(main_bp)

    # Можна додати healthcheck route тут або в routes.py
    return app


# Створюємо екземпляр додатку для Gunicorn
app = create_app()

# Ініціалізація бази даних при старті додатку
with app.app_context():
    # Створюємо схему, якщо не існує
    schema = app.config.get('DB_SCHEMA', 'auto_car_bot')
    db.session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
    db.session.commit()

    # Створюємо таблицю articles в схемі
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {schema}.articles (
        id SERIAL PRIMARY KEY,
        source VARCHAR(255) NOT NULL,
        rss_guid VARCHAR(512) UNIQUE,
        title VARCHAR(512) NOT NULL,
        url VARCHAR(1024) NOT NULL,
        image_url VARCHAR(1024),
        summary TEXT,
        generated_content TEXT,
        language VARCHAR(8) DEFAULT 'uk',
        published_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        posted_to_telegram BOOLEAN DEFAULT FALSE,
        posted_at TIMESTAMP
    )
    """
    db.session.execute(text(create_table_sql))
    db.session.commit()

    print(f"Database schema '{schema}' and articles table created.")