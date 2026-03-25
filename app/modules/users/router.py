from fastapi import APIRouter
from typing import List
from app.modules.users.models import UserCreate, UserResponse
from uuid import uuid4

router = APIRouter(prefix="/users", tags=["Users"])

fake_db: List[UserResponse] = []


@router.get("/", response_model=List[UserResponse])
def list_users():
    return fake_db


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = UserResponse(id=uuid4(), **user.dict())
    fake_db.append(new_user)
    return new_user