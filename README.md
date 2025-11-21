# Auto Car RSS Bot

Бот для автоматичного збору новин з RSS-стрічок автомобільних сайтів, генерації контенту через OpenAI та публікації в Telegram-канал.

## Встановлення

1. Клонуйте репозиторій або створіть структуру файлів.
2. Встановіть залежності: `pip install -r requirements.txt`
3. Ініціалізуйте базу даних: `python init_db.py`
4. Налаштуйте `.env` файл з вашими ключами (див. приклад нижче).

## Налаштування .env

Створіть файл `.env` у корені проекту з наступними змінними:

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///auto_car_rss_bot.db
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_channel_username
RSS_FEEDS=https://example.com/rss1.xml,https://example.com/rss2.xml
RSS_POLL_INTERVAL_SECONDS=3600
LOG_LEVEL=INFO
```

## Запуск

### Окремі компоненти:
- Веб-сервер: `python run_web.py`
- Воркер: `python run_worker.py`

### Запуск всього одною командою:
`python run_all.py`

Це запустить веб-сервер на http://127.0.0.1:5000 та воркер для обробки RSS у фоновому режимі.

## API

- `GET /` - Healthcheck
- `GET /api/articles` - Список останніх 20 статей

## Розгортання на Render

1. Підключіть репозиторій до Render.
2. Створіть **Web Service**:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --config gunicorn.conf.py app:create_app`
3. Додайте **PostgreSQL Database** (якщо не використовуєте існуючу):
   - Виберіть існуючу або створіть нову.
4. Встановіть **Environment Variables** у сервісі:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your_secret_key`
   - `DATABASE_URL=postgresql://...` (з вашої БД)
   - `DB_SCHEMA=auto_car_bot`
   - `OPENAI_API_KEY=...`
   - `TELEGRAM_BOT_TOKEN=...`
   - `TELEGRAM_CHANNEL_ID=...`
   - Інші з `.env.example`
5. Розгорніть — Render виконає build та запустить додаток.
6. Перевірте логи та API.

Якщо використовуєте існуючу БД, переконайтеся, що схема `auto_car_bot` створена (локально вже зроблено). (логування)