import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import cv2
import numpy as np

router = APIRouter(prefix="/image", tags=["Image Analysis"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

cascade_path = os.path.join(
    BASE_DIR,
    "models",
    "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(cascade_path)


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_np = np.array(image)

    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=7,  
    minSize=(50, 50)  
)

    # desenhar retângulos
    for (x, y, w, h) in faces:
        cv2.rectangle(
            image_np,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # converter de volta para imagem
    result_image = Image.fromarray(image_np)

    img_bytes = io.BytesIO()
    result_image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/jpeg")