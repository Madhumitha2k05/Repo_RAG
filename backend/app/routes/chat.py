from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_pipeline import ask_question

router = APIRouter()

# ============================================
# REQUEST MODEL
# ============================================

class ChatRequest(BaseModel):
    query: str

# ============================================
# GENERAL CHATBOT
# ============================================

@router.post("/chat")
def general_chat(data: ChatRequest):

    answer = ask_question(
        data.query,
        use_repo=False
    )

    return {
        "answer": answer
    }

# ============================================
# REPOSITORY CHATBOT
# ============================================

@router.post("/ask")
def repo_chat(data: ChatRequest):

    answer = ask_question(
        data.query,
        use_repo=True
    )

    return {
        "answer": answer
    }