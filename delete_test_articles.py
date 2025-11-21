from app import create_app
from app.models import Article
from app.extensions import db

app = create_app()

with app.app_context():
    # Видаляємо тестові статті
    test_articles = Article.query.filter(Article.rss_guid.in_(["test1", "test2"])).all()
    for article in test_articles:
        db.session.delete(article)
    db.session.commit()
    print(f"Видалено {len(test_articles)} тестових статей")