from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from app.db.session import Base

class Signed_Url(Base):
    __tablename__ = "signed_urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    expires_at = Column(DateTime(timezone=True), index=True, nullable=False)
