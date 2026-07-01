from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ImageAnalysisResponse(BaseModel):
    id: int
    filename: str
    path: str
    status: str
    faces_detected: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True