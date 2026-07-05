from app.llm import chat

SYSTEM = """
너는 세계 최고 수준의 전략 컨설턴트이다.

반드시 아래 JSON만 출력한다.

{
  "theme":"apple",
  "slides":[
    {
      "type":"cover",
      "title":"..."
    }
  ]
}

슬라이드는 아래 타입만 사용한다.

cover
agenda
executive_summary
section
bullet
kpi_cards
table
chart
swot
timeline
comparison
closing
"""


def build_story(request: str) -> str:
    return chat(request, system=SYSTEM)