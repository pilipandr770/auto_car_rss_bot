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

    # Встановлюємо схему для metadata
    metadata.schema = schema

    # Створюємо таблиці в схемі
    db.create_all()
    print(f"Database schema '{schema}' and tables initialized.")