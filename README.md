# Stream-M Backend

This is a FastAPI-based backend with LLM and Speech-to-Text capabilities.

## Requirements
- Python 3.10+
- Docker
- PostgreSQL

## Setup
1. Clone the repo
2. Create a `.env` file from `.env.example`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `uvicorn app.main:app --reload`

## Features
- FastAPI Backend
- LLM Integration (OpenAI/LangChain)
- Transcription Service (Whisper/OpenAI)
- PostgreSQL Database
- Dockerized
- CI/CD with GitHub Actions
- 95%+ Test Coverage target
