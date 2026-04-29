from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.dependencies import get_db
from app.modules.image_analysis.service import process_image, OUTPUT_DIR
from app.modules.image_analysis.models import ImageAnalysis

router = APIRouter(prefix="/image", tags=["Image Analysis"])


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    try:
        result = process_image(contents, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/files/{filename}")
def get_image(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(ImageAnalysis).order_by(ImageAnalysis.created_at.desc()).all()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "faces_detected": r.faces_detected,
            "created_at": r.created_at
        }
        for r in records
    ]

