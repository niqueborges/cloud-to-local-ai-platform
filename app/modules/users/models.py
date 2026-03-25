from pydantic import BaseModel, EmailStr, Field
from datetime import date
from uuid import UUID, uuid4


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: EmailStr
    birth_date: date