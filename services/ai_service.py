import os
from google import genai

MODEL_NAME = "gemini-3-flash-preview"
GEMINI_API_KEY =

def generate_text(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        return "GEMINI_API_KEY недостасува. Провери .env фајл."

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return (response.text or "").strip() or "Нема резултат од AI."
    except Exception as e:
        return f"AI грешка: {e}"
