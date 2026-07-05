from openai import OpenAI
from app.config import settings
from app.memory.history import add, get
from app.utils.logger import info, error

client = OpenAI(
    base_url=settings.OLLAMA_BASE_URL,
    api_key="ollama",
)


def chat(prompt: str, system: str = "You are Hermes V2.") -> str:
    try:
        history = get()

        messages = [
            {
                "role": "system",
                "content": system,
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        info(f"LLM Request ({len(messages)} messages)")

        response = client.chat.completions.create(
            model=settings.OLLAMA_MODEL,
            messages=messages,
            temperature=0.2,
        )

        answer = response.choices[0].message.content or ""

        add("user", prompt)
        add("assistant", answer)

        info("LLM Response OK")

        return answer

    except Exception as e:
        error(f"LLM Error: {e}")
        raise