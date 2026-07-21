"""일반 메시지 → RAG 답변 핸들러."""

from telegram import Update
from telegram.ext import ContextTypes

from app.llm.agent import ask_llm
from app.rag.pipeline import RAGPipeline


def _is_document_question(text: str) -> bool:
    """문서 내용 질문인지 판별."""
    doc_keywords = [
        "pdf", "pdf는", "pdf가", "pdf를",
        "문서", "문서야", "문서야?", "문서야?",
        "파일", "파일은", "파일이", "파일을",
        "요약", "요약해", "요약해줘", "요약해주세요",
        "에대한", "에 대한", "에관한", "에 관한",
        "에따라", "에 따라",
        "무엇이야", "무엇인가요", "어떤", "어떤거",
        "어떤거야", "어떤건데",
        "내용", "내용은", "내용이", "내용을",
        "what", "document", "file", "summarize", "summary",
    ]
    lower = text.lower().strip()
    return any(k in lower for k in doc_keywords)


def answer_question(question: str, pipeline: RAGPipeline, llm=ask_llm) -> str:
    """RAG 파이프라인으로 답변하거나 pipeline 없으면 LLM에 직접 요청."""
    print(f"PIPELINE={pipeline!r}, TYPE={type(pipeline)}")
    if pipeline is None:
        print("[answer_question] pipeline is None → fallback to LLM")
        return llm(question)

    try:
        documents = pipeline.retrieve(question)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise

    print(f"[answer_question] retrieve returned {len(documents)} documents")
    if not documents:
        print("[answer_question] no documents → fallback to LLM")
        return llm(question)

    prompt = pipeline.prompt_builder.build(question, documents)
    answer = llm(prompt)
    return pipeline._format_answer(answer, documents)


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE, pipeline: RAGPipeline
) -> None:
    if not update.message or not update.message.text:
        return

    question = update.message.text

    # 라우팅: 문서 질문 → RAG, 나머지 → LLM
    if _is_document_question(question):
        print(f"[handle_message] document question → RAG: {question}")
        answer = answer_question(question, pipeline)
    else:
        print(f"[handle_message] general → direct LLM: {question}")
        answer = ask_llm(question)
    await update.message.reply_text(answer)
