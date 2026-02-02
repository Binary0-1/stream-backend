from fastapi import UploadFile
import openai
from app.core.config import settings

class TranscriptionService:
    async def transcribe(self, file: UploadFile) -> str:
        # Skeleton for transcription
        # In a real implementation, you'd use Whisper API
        return "Skeleton transcription for " + file.filename

transcription_service = TranscriptionService()
