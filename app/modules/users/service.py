from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modules.users.models import UserDB

def list_users(db: Session):
    return db.query(UserDB).all()

def create_user(db: Session, data):
    user = UserDB(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: str):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()

def update_user(db: Session, user_id: str, data: dict):
    user = get_user(db, user_id)

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user