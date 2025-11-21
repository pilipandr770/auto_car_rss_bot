from datetime import datetime
from sqlalchemy import MetaData
from .extensions import db

metadata = MetaData()

class Article(db.Model):
    """
    Стаття/новина, яку ми витягнули з RSS та/або вже опублікували в Telegram.
    """
    __tablename__ = "articles"
    __table_args__ = {"schema": "auto_car_bot"}
    metadata = metadata

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=False)        # назва або домен джерела
    rss_guid = db.Column(db.String(512), unique=True)         # унікальний ідентифікатор з RSS (guid/link)
    title = db.Column(db.String(512), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    image_url = db.Column(db.String(1024))
    summary = db.Column(db.Text)                              # коротке самарі
    generated_content = db.Column(db.Text)                    # згенерована стаття для Telegram
    language = db.Column(db.String(8), default="uk")

    published_at = db.Column(db.DateTime)                     # час публікації на сайті
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    posted_to_telegram = db.Column(db.Boolean, default=False)
    posted_at = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<Article id={self.id} source={self.source} title={self.title[:30]!r}>"