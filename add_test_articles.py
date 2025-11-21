from app import create_app
from app.models import Article
from app.extensions import db
from datetime import datetime

app = create_app()

with app.app_context():
    # Додамо кілька тестових статей
    articles = [
        Article(
            source="test.com",
            rss_guid="test1",
            title="Тестова стаття 1",
            url="https://test.com/1",
            summary="Це тестова стаття для перевірки.",
            generated_content="Згенерований контент для тестової статті 1.",
            posted_to_telegram=False
        ),
        Article(
            source="test.com",
            rss_guid="test2",
            title="Тестова стаття 2",
            url="https://test.com/2",
            summary="Ще одна тестова стаття.",
            generated_content="Згенерований контент для тестової статті 2.",
            posted_to_telegram=False
        )
    ]
    db.session.add_all(articles)
    db.session.commit()
    print("Додано тестові статті")