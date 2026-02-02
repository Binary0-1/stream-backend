from fastapi import APIRouter, UploadFile, File
from app.services.transcription_service import transcription_service

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    text = await transcription_service.transcribe(file)
    return {"text": text}
