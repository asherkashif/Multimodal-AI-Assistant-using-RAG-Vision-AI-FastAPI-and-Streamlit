from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import generate_answer
from app.services.rag_service import generate_answer
from app.services.retriever import load_vector_store, get_relevant_chunks

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask(request: QuestionRequest):

    vector_db = load_vector_store()

    chunks = get_relevant_chunks(
        request.question,
        vector_db
    )

    answer = generate_answer(
        chunks,
        request.question
    )

    return {
        "answer": answer
    }