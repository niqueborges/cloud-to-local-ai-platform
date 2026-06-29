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

import uuid

@pytest.fixture
def auth_headers():
    email = f"test_{uuid.uuid4()}@example.com"
    # Create user
    client.post("/users/", json={
        "name": "Test User",
        "email": email,
        "password": "testpassword",
        "birth_date": "2000-01-01"
    })
    # Login
    resp = client.post("/auth/token", data={
        "username": email,
        "password": "testpassword"
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_image_history(auth_headers):
    response = client.get("/image/history", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analyze_image_mock(auth_headers):
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    response = client.post(
        "/image/analyze", 
        files={"file": ("test.jpg", img_byte_arr, "image/jpeg")},
        headers=auth_headers
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
