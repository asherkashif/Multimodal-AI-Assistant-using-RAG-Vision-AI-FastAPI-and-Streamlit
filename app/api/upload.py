from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import split_text
from app.services.vector_store import create_vector_store
from app.services.retriever import load_vector_store, similarity_search, get_relevant_chunks    
from app.services.rag_service import generate_answer
import os
import shutil

router = APIRouter()

upload_directory = "uploads"
os.makedirs(upload_directory, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(upload_directory, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        # Extract text
        extracted_text = extract_text_from_pdf(file_path)

        # Split text into chunks
        chunks = split_text(extracted_text)

        # Create FAISS vector store
        create_vector_store(chunks)

        return {
            "filename": file.filename,
            "chunks": len(chunks),
            "message": "Vector store created successfully."
        }

    return {
        "filename": file.filename,
        "message": "Only PDF files are supported."
    }