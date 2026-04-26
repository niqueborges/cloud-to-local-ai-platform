from app.modules.image_analysis.models_db import ImageAnalysis
from sqlalchemy.orm import Session
import uuid
import os
import io
import cv2
import numpy as np
from PIL import Image

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


def process_image(contents: bytes, db: Session):
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

    # gerar nome e caminho
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(OUTPUT_DIR, filename)

    # salvar imagem
    result_image = Image.fromarray(image_np)
    result_image.save(file_path)

    # salvar no banco
    analysis = ImageAnalysis(
        filename=filename,
        path=file_path,
        faces_detected=len(faces_data)
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {
    "filename": filename,
    "faces_detected": len(faces_data),
    "faces": faces_data,
    "url": f"http://127.0.0.1:8000/image/files/{filename}"
}