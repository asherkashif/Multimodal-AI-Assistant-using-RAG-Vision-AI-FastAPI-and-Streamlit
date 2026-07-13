from fastapi import APIRouter, UploadFile, File
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
    return {"filename": file.filename, "message": "File uploaded successfully"}