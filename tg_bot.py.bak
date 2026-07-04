import os, json, requests, pptx
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from duckduckgo_search import DDGS
URL = "http://localhost:11434/v1/chat/completions"
def make_ppt(t, c):
    p = pptx.Presentation()
    s = p.slides.add_slide(p.slide_layouts[1])
    s.shapes.title.text = str(t)
    if isinstance(c, list): c = chr(10).join(c)
    s.placeholders[1].text = str(c)
    p.save("report.pptx")
def search_web(q):
    try:
        res = DDGS().news(q, max_results=5)
        if not res: res = DDGS().text(q, max_results=5)
