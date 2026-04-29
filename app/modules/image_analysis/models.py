from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class ImageAnalysis(Base):
    __tablename__ = "image_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    faces_detected = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)