from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class FileStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class FileUpload(Base):
    __tablename__ = "file_uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    key = Column(String, nullable=False)
    bucket = Column(String, nullable=True)
    content_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    status = Column(Enum(FileStatus, name="file_status_enum"), nullable=False, default=FileStatus.pending)
    result_key = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
