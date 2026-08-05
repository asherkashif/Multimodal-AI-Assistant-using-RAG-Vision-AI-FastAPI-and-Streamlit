from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi import Depends
from app.services.jwt_service import get_current_user
from app.database.models import User
from app.services.pdf_report import generate_chat_report
import os

router = APIRouter()

class ReportRequest(BaseModel):
    messages: list

@router.post("/generate-report")
async def generate_report(request: ReportRequest,
                          current_user: User = Depends(get_current_user)):

    pdf_path = generate_chat_report(request.messages)

    print("PDF Path:", pdf_path)
    print("Exists:", os.path.exists(pdf_path))

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="PDF was not created.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="conversation_report.pdf"
    )