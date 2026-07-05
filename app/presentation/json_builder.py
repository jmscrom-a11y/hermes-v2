import json
from app.presentation.schema import Presentation


def build(json_text: str) -> Presentation:
    data = json.loads(json_text)
    return Presentation.model_validate(data)