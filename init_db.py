from app import create_app
from app.extensions import db
from app.models import metadata
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Створюємо схему, якщо не існує
    schema = app.config.get('DB_SCHEMA', 'auto_car_bot')
    db.session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
    db.session.commit()

    # Встановлюємо схему для metadata
    metadata.schema = schema

    # Створюємо таблиці в схемі
    db.create_all()
    print(f"Database schema '{schema}' and tables created.")