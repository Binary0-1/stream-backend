from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import boto3
from app.api import deps
from app.models.file_upload import FileUpload, FileStatus
from app.schemas.file_upload import FileUploadCreate, PresignedPostResponse, FileUploadComplete
from app.schemas import user as user_schema
from app.core.config import settings

router = APIRouter()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

BUCKET_NAME = "stream-m-uploads"

def process_file_task(file_id: int):
    """
    Placeholder for background processing (e.g., transcription)
    """
    print(f"Processing file {file_id} in background...")
    # This is where you would call transcription_service or push to a real queue

@router.post("/presigned-url", response_model=PresignedPostResponse)
def create_presigned_url(
    *,
    db: Session = Depends(deps.get_db),
    file_in: FileUploadCreate,
    current_user: user_schema.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Generate a presigned POST URL to upload a file directly to S3.
    """
    file_key = f"uploads/{current_user.id}/{file_in.filename}"
    
    try:
        presigned_post = s3_client.generate_presigned_post(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Fields={"Content-Type": file_in.content_type},
            Conditions=[
                ["content-length-range", 0, 10485760],
                {"Content-Type": file_in.content_type}
            ],
            ExpiresIn=3600
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate presigned URL: {str(e)}")

    db_file = FileUpload(
        user_id=current_user.id,
        key=file_key,
        bucket=BUCKET_NAME,
        content_type=file_in.content_type,
        status=FileStatus.pending
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return {
        "url": presigned_post["url"],
        "fields": presigned_post["fields"],
        "file_id": db_file.id
    }

@router.post("/confirm", response_model=Any)
def confirm_upload(
    *,
    db: Session = Depends(deps.get_db),
    confirm_in: FileUploadComplete,
    background_tasks: BackgroundTasks,
    current_user: user_schema.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Confirm that the file has been uploaded to S3 and trigger background processing.
    """
    db_file = db.query(FileUpload).filter(
        FileUpload.id == confirm_in.file_id,
        FileUpload.user_id == current_user.id
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File record not found")

    # Update status (you might want to verify with S3 head_object here)
    db_file.status = FileStatus.success
    db.add(db_file)
    db.commit()

    # Trigger background task
    background_tasks.add_task(process_file_task, db_file.id)

    return {"msg": "Upload confirmed and processing started", "file_id": db_file.id}
 