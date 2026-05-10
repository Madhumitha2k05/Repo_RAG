from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_pipeline import ask_question

router = APIRouter()

class Query(BaseModel):
    question: str

@router.post("/ask")
def ask(query: Query):
    answer = ask_question(query.question)
    return {"response": answer}