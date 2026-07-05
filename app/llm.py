from openai import OpenAI
from app.config import settings

client = OpenAI(
    base_url=settings.OLLAMA_BASE_URL,
    api_key="ollama",
)


def chat(prompt: str, system: str = "You are Hermes V2.") -> str:
    response = client.chat.completions.create(
        model=settings.OLLAMA_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content or ""