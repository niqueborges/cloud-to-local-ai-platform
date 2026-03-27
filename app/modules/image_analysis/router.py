from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io
import cv2
import numpy as np

router = APIRouter(prefix="/image", tags=["Image Analysis"])

face_cascade = cv2.CascadeClassifier(
    "app/models/haarcascade_frontalface_default.xml"
)


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))
    image_np = np.array(image)

    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    return {
        "filename": file.filename,
        "faces_detected": len(faces),
        "faces": faces.tolist()
    }