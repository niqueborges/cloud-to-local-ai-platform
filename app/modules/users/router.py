from fastapi import APIRouter
from typing import List
from app.modules.users.models import User

router = APIRouter(prefix="/users", tags=["Users"])

fake_db: List[User] = []


@router.get("/")
def list_users():
    return fake_db


@router.post("/")
def create_user(user: User):
    fake_db.append(user)
    return user