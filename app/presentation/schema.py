from pydantic import BaseModel
from typing import List, Optional


class Slide(BaseModel):
    type: str
    title: str = ""
    subtitle: str = ""
    bullets: List[str] = []
    notes: str = ""
    chart: Optional[dict] = None
    table: Optional[dict] = None
    image: Optional[str] = None


class Presentation(BaseModel):
    theme: str = "apple"
    slides: List[Slide]