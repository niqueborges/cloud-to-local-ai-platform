from pydantic import BaseModel
from datetime import datetime


class ImageAnalysisResponse(BaseModel):
    id: int
    filename: str
    path: str
    faces_detected: int
    created_at: datetime

    class Config:
        from_attributes = True