from fastapi import FastAPI
from app.modules.users.router import router as users_router
from app.database import engine, Base
from app.modules.users.models_db import UserDB
from app.modules.image_analysis.router import router as image_router

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

app.include_router(users_router)

app.include_router(image_router)


@app.get("/")
def read_root():
    return {"message": "API is running"}
