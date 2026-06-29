import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Fallback para caso o env var não exista (focado no docker-compose local)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+pg8000://postgres:password@localhost:5432/cloud_to_local_db")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()