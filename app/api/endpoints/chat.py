from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import llm_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await llm_service.get_response(request.message)
    return {"response": response}
