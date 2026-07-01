from sqlalchemy.orm import Session

from app.modules.users.models import UserDB


def list_users(db: Session):
    return db.query(UserDB).all()

def create_user(db: Session, data):
    from app.modules.auth.service import get_password_hash
    password = data.pop("password", None)
    if not password:
        raise ValueError("Password is required")
        
    user = UserDB(**data, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_user(db: Session, user_id: str):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise ValueError("User not found")
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