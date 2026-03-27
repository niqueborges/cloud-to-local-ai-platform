from pydantic import BaseModel, EmailStr, Field
from datetime import date
from uuid import UUID, uuid4
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    birth_date: date


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: UUID = Field(default_factory=uuid4)

model_config = {
    "from_attributes": True
}


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
