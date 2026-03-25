from pydantic import BaseModel, EmailStr
from datetime import date
from uuid import UUID, uuid4


class User(BaseModel):
    id: UUID = uuid4()
    name: str
    email: EmailStr
    birth_date: date