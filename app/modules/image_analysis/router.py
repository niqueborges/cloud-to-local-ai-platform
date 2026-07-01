import logging
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os

logger = logging.getLogger(__name__)

from app.dependencies import get_db
from app.modules.image_analysis.service import receive_image, get_presigned_url
from app.modules.image_analysis.models import ImageAnalysis
from app.modules.auth.dependencies import get_current_user
from app.worker import process_image_task
from fastapi import status

router = APIRouter(prefix="/image", tags=["Image Analysis"])


@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def analyze_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    contents = await file.read()

    try:
        analysis = await run_in_threadpool(receive_image, contents, db, current_user.id)
        
        process_image_task.delay(analysis.id)
        
        return {
            "message": "Image queued for processing",
            "id": analysis.id,
            "status": analysis.status,
            "filename": analysis.filename,
            "url": get_presigned_url(analysis.filename)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Erro ao processar imagem")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/files/{filename}")
def get_image(filename: str):
    try:
        url = get_presigned_url(filename)
        return RedirectResponse(url)
    except Exception as e:
        logger.exception("Erro ao gerar URL da imagem")
        raise HTTPException(status_code=500, detail="Error retrieving image")


@router.get("/history")
def get_history(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    records = db.query(ImageAnalysis).filter(ImageAnalysis.user_id == current_user.id).order_by(ImageAnalysis.created_at.desc()).all()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "status": r.status,
            "faces_detected": r.faces_detected,
            "created_at": r.created_at,
            "url": get_presigned_url(r.filename)
        }
        for r in records
    ]

