from pydantic import BaseModel, EmailStr, Field
from datetime import date
from uuid import UUID, uuid4


class UserBase(BaseModel):
    name: str
    email: EmailStr
    birth_date: date


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: UUID = Field(default_factory=uuid4)