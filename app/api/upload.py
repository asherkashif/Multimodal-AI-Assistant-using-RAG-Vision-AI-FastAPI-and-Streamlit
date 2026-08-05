from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import split_text
from app.services.vector_store import create_vector_store
from app.services.retriever import load_vector_store, similarity_search, get_relevant_chunks    
from app.services.rag_service import generate_answer
from app.services.vision_service import process_image
from fastapi import Depends
from app.services.jwt_service import get_current_user
from app.database.models import User
import os
import shutil

router = APIRouter()

upload_directory = "uploads"
os.makedirs(upload_directory, exist_ok=True)

current_file_type = None
current_image_path = None

@router.post("/upload")
async def upload_file(file: UploadFile = File(...),
                      current_user: User = Depends(get_current_user)):
    global current_file_type, current_image_path

    file_path = os.path.join(upload_directory, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.lower().endswith(".pdf"):
        
        current_file_type = "pdf"
        current_image_path = None
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
    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):

        current_file_type = "image"
        current_image_path = file_path

        return {
            "filename": file.filename,
            "message": "Image uploaded successfully."
        }

    return {
        "filename": file.filename,
        "message": "Only PDF files are supported."
    }