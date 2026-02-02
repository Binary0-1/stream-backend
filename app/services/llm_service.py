import openai
from app.core.config import settings

class LLMService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY

    async def get_response(self, message: str) -> str:
        # Skeleton for LLM response
        # In a real implementation, you'd use langchain or openai client
        return f"Skeleton response to: {message}"

llm_service = LLMService()
