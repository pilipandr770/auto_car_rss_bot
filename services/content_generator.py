import os
from typing import Optional
import logging

from .openai_client import get_openai_client

logger = logging.getLogger(__name__)


def build_prompt_from_summary(summary: str, original_title: str, source: str) -> str:
    """
    Формує текст промпта для моделі на основі самарі RSS-новини.
    Тут ми описуємо стиль, довжину, цільову аудиторію (україномовні автомобілісти).
    """
    return f"""
Ти — українськомовний автор корисних статей для Telegram-каналу про автомобілі.

На основі нижчого самарі з новини напиши цікаву, структуровану і корисну статтю для власників авто в Україні.
Стаття повинна:
- бути українською,
- містити практичні поради,
- не дублювати дослівно текст оригіналу,
- закінчуватись коротким висновком.

**Важливо:** Якщо новость стосується політики, економіки (не авто), спорту, культури або будь-яких тем, не пов'язаних з автомобілями, автомобільною індустрією, порадами водіям, новинами про авто в Україні чи Європі — НЕ ПИШИ СТАТТЮ. Просто поверни порожній відповідь.

В кінці статті додай призив до дії: "Якщо вас цікавить покупка авто з Європи, зв'яжіться з нашим бот-менеджером @eu_auto_bot".

Заголовок оригіналу: "{original_title}"
Джерело: {source}

Самарі новини:
---
{summary}
---

Напиши тільки текст статті без пояснень. Якщо тема не релевантна — порожній відповідь.
    """.strip()


def generate_article_from_summary(
    summary: str,
    original_title: str,
    source: str,
    model: Optional[str] = None,
) -> str:
    """
    Викликає OpenAI-модель для генерації статті по самарі.
    (Пізніше можна буде замінити на Assistants API з OPENAI_ASSISTANT_ID.)
    """
    try:
        client = get_openai_client()
        model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        prompt = build_prompt_from_summary(summary, original_title, source)

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.choices[0].message.content
        return text
    except Exception as e:
        logger.error(f"Помилка генерації контенту через OpenAI: {e}")
        return ""  # Повертаємо порожній рядок, щоб уникнути None