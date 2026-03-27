from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io

router = APIRouter(prefix="/image", tags=["Image Analysis"])


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))

    width, height = image.size
    format = image.format

    return {
        "filename": file.filename,
        "format": format,
        "width": width,
        "height": height
    }