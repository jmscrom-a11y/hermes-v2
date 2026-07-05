from app.presentation.pipeline import create_presentation


def run(prompt: str):
    return create_presentation(prompt)