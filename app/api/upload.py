from pydoc import text

from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import split_text
from app.services.vector_store import create_vector_store
import os
import shutil


router = APIRouter()
upload_directory = "uploads"
os.makedirs(upload_directory, exist_ok=True)

chunks = split_text(text)
create_vector_store(chunks)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    if file.filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
        return {
            "filename": file.filename,
            "text": extracted_text[:3000]  # Return only the first 3000 characters of the extracted text
        }
    
    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "message": "File uploaded successfully"
    }