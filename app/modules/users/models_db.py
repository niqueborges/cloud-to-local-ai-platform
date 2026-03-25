from sqlalchemy import Column, String, Date
from app.database import Base
import uuid


class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)