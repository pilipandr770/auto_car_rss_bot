from flask_sqlalchemy import SQLAlchemy

# Єдине місце, де створюємо об'єкти розширень
# Щоб уникнути циклічних імпортів
db = SQLAlchemy()