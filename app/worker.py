import os
from celery import Celery
from app.database import SessionLocal
from app.modules.image_analysis.service import perform_background_processing

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="process_image_task")
def process_image_task(analysis_id: int):
    db = SessionLocal()
    try:
        perform_background_processing(analysis_id, db)
    finally:
        db.close()
