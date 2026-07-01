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

import boto3

MINIO_URL = os.getenv("MINIO_URL", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET_NAME = os.getenv("BUCKET_NAME", "cloud-to-local-bucket")

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"
)

def get_presigned_url(filename: str):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": filename},
        ExpiresIn=3600
    )

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

def upload_raw_image(contents: bytes) -> str:
    filename = f"{uuid.uuid4()}.jpg"
    buffer = io.BytesIO(contents)
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=buffer,
        ContentType="image/jpeg"
    )
    return filename

def receive_image(contents: bytes, db: Session, user_id: str):
    filename = upload_raw_image(contents)
    
    analysis = ImageAnalysis(
        filename=filename,
        path=filename,
        faces_detected=None,
        status="PENDING",
        user_id=user_id
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return analysis

def perform_background_processing(analysis_id: int, db: Session):
    analysis = db.query(ImageAnalysis).filter(ImageAnalysis.id == analysis_id).first()
    if not analysis:
        return
        
    analysis.status = "PROCESSING"
    db.commit()
    
    try:
        # Download raw image from MinIO
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=analysis.filename)
        contents = response['Body'].read()
        
        image_np = load_image(contents)
        faces = detect_faces(image_np)
        faces_data = format_faces(faces)
        image_np = draw_faces(image_np, faces)
        
        # Upload processed image back (overwrite)
        buffer = io.BytesIO()
        Image.fromarray(image_np).save(buffer, format="JPEG")
        buffer.seek(0)
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=analysis.filename,
            Body=buffer,
            ContentType="image/jpeg"
        )
        
        # Update DB
        analysis.faces_detected = len(faces_data)
        analysis.status = "COMPLETED"
        db.commit()
        
    except Exception as e:
        analysis.status = "FAILED"
        db.commit()
        raise e