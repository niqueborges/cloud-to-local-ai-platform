import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
import pytest
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_image_history():
    response = client.get("/image/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analyze_image_mock():
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    response = client.post(
        "/image/analyze", 
        files={"file": ("test.jpg", img_byte_arr, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert "faces_detected" in data
    assert data["faces_detected"] == 0 
    assert "faces" in data
    assert "url" in data

def test_get_image_not_found():
    response = client.get("/image/files/notfound.jpg")
    assert response.status_code == 404
