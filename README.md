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
## Database Migrations

We use **Alembic** for handling database migrations.

### Creating a new migration
When you add or modify a SQLAlchemy model, run the following command to generate a migration script automatically:
```bash
alembic revision --autogenerate -m "description of changes"
```

### Applying migrations
To apply the migrations to your local or production database:
```bash
alembic upgrade head
```

### Important Note
Ensure any new model is imported in `app/models/__init__.py` so that Alembic can detect it for autogeneration.
