from app.services.ppt_service import build_ppt


def run(prompt: str):
    md = f"""# {prompt}

자동 생성된 PPT입니다.

- Hermes V2
- Ollama
- Telegram
"""

    ppt = build_ppt(md)

    return ppt