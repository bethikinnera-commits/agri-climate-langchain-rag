from rag_pipeline import query_kb
from weather_api import get_3day_climate
import re


def extract_city(question):
    question = re.sub(r"[^\w\s]", "", question.lower())

    words = question.split()

    stopwords = [
        "what", "is", "climate", "for", "3", "days",
        "in", "weather", "can", "i", "do", "tomorrow",
        "spray", "pesticides"
    ]

    filtered = [w for w in words if w not in stopwords]

    return filtered[-1].capitalize() if filtered else None


def route_question(question):

    # 1️⃣ KB FIRST
    kb_answer = query_kb(question)

    if kb_answer:
        return kb_answer

    # 2️⃣ WEATHER FALLBACK
    city = extract_city(question)

    if not city:
        return "City not detected"

    return get_3day_climate(city)