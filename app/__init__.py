from flask import Flask
from .config import get_config
from .extensions import db
from .routes import main_bp


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