from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import enum

class FileStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class FileUploadBase(BaseModel):
    key: str
    bucket: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    status: FileStatus = FileStatus.pending

class FileUploadCreate(BaseModel):
    filename: str
    content_type: str

class PresignedPostResponse(BaseModel):
    url: str
    fields: Dict[str, str]
    file_id: int

class FileUploadComplete(BaseModel):
    file_id: int

class FileUpload(FileUploadBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
