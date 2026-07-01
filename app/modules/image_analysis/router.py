import logging
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

logger = logging.getLogger(__name__)

from app.dependencies import get_db
from app.modules.image_analysis.service import process_image, OUTPUT_DIR
from app.modules.image_analysis.models import ImageAnalysis
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/image", tags=["Image Analysis"])


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    contents = await file.read()

    try:
        result = await run_in_threadpool(process_image, contents, db, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Erro ao processar imagem")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/files/{filename}")
def get_image(filename: str):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(OUTPUT_DIR, safe_filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@router.get("/history")
def get_history(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    records = db.query(ImageAnalysis).filter(ImageAnalysis.user_id == current_user.id).order_by(ImageAnalysis.created_at.desc()).all()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "faces_detected": r.faces_detected,
            "created_at": r.created_at
        }
        for r in records
    ]

