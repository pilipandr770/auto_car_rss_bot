from flask import Blueprint, jsonify

from .models import Article

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """
    Простий healthcheck + коротка інформація про сервіс.
    Цей маршрут можна використовувати для моніторингу (наприклад Render/uptime-бот).
    """
    return jsonify(
        {
            "status": "ok",
            "message": "Auto Car RSS Bot: Flask API працює",
        }
    )


@main_bp.route("/health")
def health():
    """
    Альтернативний healthcheck endpoint.
    """
    return jsonify({"status": "healthy"})


@main_bp.route("/api/articles")
def list_articles():
    """
    Повертає останні 20 статей із БД у JSON.
    Потім можна використовувати як внутрішню адмінку/моніторинг.
    """
    articles = (
        Article.query.order_by(Article.created_at.desc())
        .limit(20)
        .all()
    )
    data = [
        {
            "id": a.id,
            "title": a.title,
            "source": a.source,
            "url": a.url,
            "generated_content": a.generated_content,
            "posted_to_telegram": a.posted_to_telegram,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in articles
    ]
    return jsonify(data)