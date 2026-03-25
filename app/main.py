from fastapi import FastAPI
from app.modules.users.router import router as users_router
from app.database import engine, Base
from app.modules.users.models_db import UserDB

# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users_router)


@app.get("/")
def read_root():
    return {"message": "API is running"}
