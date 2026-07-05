from app.presentation.story import build_story
from app.presentation.json_builder import build
from app.services.ppt_service import build_ppt


def create_presentation(request: str):
    json_text = build_story(request)

    presentation = build(json_text)

    markdown = ""

    for slide in presentation.slides:
        markdown += f"# {slide.title}\n\n"

        for bullet in slide.bullets:
            markdown += f"- {bullet}\n"

        markdown += "\n"

    return build_ppt(markdown)