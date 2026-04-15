from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from fastapi import HTTPException
import os

from app.modules.image_analysis.service import process_image, OUTPUT_DIR

router = APIRouter(prefix="/image", tags=["Image Analysis"])


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()
    return process_image(contents)


@router.get("/files/{filename}")
def get_image(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)