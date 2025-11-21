from app import create_app
from utils.logging_config import setup_logging


def main():
    """
    Точка входу для запуску Flask-додатку.
    Використовується при локальній розробці.
    """
    setup_logging()
    app = create_app()
    # Для dev-деплою можна явно вказати host/port
    app.run(host="0.0.0.0", port=5000, use_reloader=False)


if __name__ == "__main__":
    main()