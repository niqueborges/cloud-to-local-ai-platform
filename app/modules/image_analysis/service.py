from app.modules.image_analysis.models import ImageAnalysis
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
if face_cascade.empty():
    raise RuntimeError("Failed to load Haar cascade file")

OUTPUT_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "storage", "images")
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_image(contents: bytes):
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        return np.array(image)
    except Exception:
        raise ValueError("Invalid image file")
    
def detect_faces(image_np):
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    height, width = gray.shape
    max_size = (width // 2, height // 2)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(50, 50),
        maxSize=max_size
    )

    return faces

def format_faces(faces):
    return [
        {
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        }
        for (x, y, w, h) in faces
    ]

def draw_faces(image_np, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(
            image_np,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )
    return image_np

def save_image(image_np):
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(OUTPUT_DIR, filename)

    Image.fromarray(image_np).save(file_path)

    return filename, file_path

def save_analysis(db: Session, filename: str, path: str, faces_count: int):
    analysis = ImageAnalysis(
        filename=filename,
        path=path,
        faces_detected=faces_count
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis

def process_image(contents: bytes, db: Session):
    image_np = load_image(contents)

    faces = detect_faces(image_np)

    faces_data = format_faces(faces)

    image_np = draw_faces(image_np, faces)

    filename, file_path = save_image(image_np)

    analysis = save_analysis(db, filename, file_path, len(faces_data))

    return {
        "id": analysis.id,
        "filename": filename,
        "faces_detected": len(faces_data),
        "faces": faces_data,
       "url": f"/image/files/{filename}"
    }