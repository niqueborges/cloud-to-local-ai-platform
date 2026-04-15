import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from fastapi import HTTPException
from PIL import Image
import io
import cv2
import numpy as np
import os

router = APIRouter(prefix="/image", tags=["Image Analysis"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

cascade_path = os.path.join(
    BASE_DIR,
    "models",
    "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(cascade_path)

OUTPUT_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "storage", "images")
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.get("/files/{filename}")
def get_image(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_np = np.array(image)

    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    h_img, w_img = gray.shape

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(50, 50),
        maxSize=(w_img // 2, h_img // 2)
    )

    faces_data = []

    for (x, y, w, h) in faces:
        faces_data.append({
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        })

        cv2.rectangle(
            image_np,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # salvar imagem
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(OUTPUT_DIR, filename)

    result_image = Image.fromarray(image_np)
    result_image.save(file_path)

    return {
        "filename": filename,
        "faces_detected": len(faces_data),
        "faces": faces_data,
        "path": file_path
    }