from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
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
        extracted_text = extract_text_from_pdf(file_path)
        return {
            "filename": file.filename,
            "text": extracted_text[:3000]  # Return only the first 3000 characters of the extracted text
        }
    
    return {
        "filename": file.filename,
        "message": "File uploaded successfully"
    }