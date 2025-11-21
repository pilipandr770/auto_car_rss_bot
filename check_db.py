from app import create_app
from app.models import Article
from app.extensions import db

app = create_app()

with app.app_context():
    articles = Article.query.order_by(Article.created_at.desc()).limit(10).all()
    for a in articles:
        print(f"ID: {a.id}, Title: {a.title}")
        print(f"Generated Content: {a.generated_content[:100] if a.generated_content else 'None'}...")
        print(f"Posted: {a.posted_to_telegram}")
        print("---")