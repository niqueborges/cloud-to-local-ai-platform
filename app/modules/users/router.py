from app.modules.users import service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.modules.users.schemas import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])
@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return service.list_users(db)

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user.model_dump())

@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return service.get_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        service.delete_user(db, user_id)
        return {"message": "User deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{user_id}")
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    try:
        return service.update_user(db, user_id, user_update.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    