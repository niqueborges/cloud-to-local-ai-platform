from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class ImageAnalysis(Base):
    __tablename__ = "image_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    status = Column(String, default="PENDING")
    faces_detected = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)