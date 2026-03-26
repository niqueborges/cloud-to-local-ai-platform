from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.users.models import UserCreate, UserResponse
from app.modules.users.models_db import UserDB
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserDB(
        name=user.name,
        email=user.email,
        birth_date=user.birth_date
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user