from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import chat, transcribe, login, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix=settings.API_V1_STR, tags=["login"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["chat"])
app.include_router(transcribe.router, prefix=settings.API_V1_STR, tags=["transcribe"])

@app.get("/")
async def root():
    return {"message": "Welcome to Stream-M Backend"}
