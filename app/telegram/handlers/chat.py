"""일반 메시지 → RAG 답변 핸들러."""

from telegram import Update
from telegram.ext import ContextTypes

from app.llm.agent import ask_llm
from app.rag.pipeline import RAGPipeline


def answer_question(question: str, pipeline: RAGPipeline, llm=ask_llm) -> str:
    """RAG 파이프라인으로 답변하거나 pipeline 없으면 LLM에 직접 요청."""
    if pipeline is None:
        return llm(question)

    try:
        documents = pipeline.retrieve(question)
    except Exception:
        documents = []

    if not documents:
        return llm(question)

    prompt = pipeline.prompt_builder.build(question, documents)
    answer = llm(prompt)
    return pipeline._format_answer(answer, documents)


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE, pipeline: RAGPipeline
) -> None:
    if not update.message or not update.message.text:
        return

    answer = answer_question(update.message.text, pipeline)
    await update.message.reply_text(answer)
