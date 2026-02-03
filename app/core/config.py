from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stream-M Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    DATABASE_URL: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    DEEPGRAM_API_KEY: Optional[str] = "your-deepgram-api-key"
    BUCKET_NAME: Optional[str] = "stream/uploads"
    AWS_SECRET_ACCESS_KEY:Optional[str]=""
    AWS_REGION:Optional[str]=""
    AWS_ACCESS_KEY_ID:Optional[str]=""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
