from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends
from app.services.jwt_service import get_current_user

from app.services.rag_service import generate_answer
from app.services.retriever import load_vector_store, get_relevant_chunks
from app.services.vision_service import process_image

import app.api.upload as upload

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str
    messages: list = []


@router.post("/ask")
async def ask(request: QuestionRequest,
              current_user=Depends(get_current_user)):

    question = request.question
    messages = request.messages

    # -------- IMAGE --------
    if upload.current_file_type == "image":

        answer = process_image(
            upload.current_image_path,
            question,
            messages
        )

        return {"answer": answer}

    # -------- PDF --------
    elif upload.current_file_type == "pdf":

        vector_db = load_vector_store()

        chunks = get_relevant_chunks(
            question,
            vector_db
        )

        answer = generate_answer(
            chunks,
            question,
            messages
        )

        return {"answer": answer}

    return {
        "answer": "Please upload a PDF or Image first."
    }