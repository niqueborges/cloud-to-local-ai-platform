from fastapi import FastAPI
from app.modules.users.router import router as users_router
from app.modules.image_analysis.router import router as image_router

from app.database import engine, Base
from app.modules.users.models import UserDB
from app.modules.image_analysis import models_db  # importante importar

app = FastAPI()

# cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# routers
app.include_router(users_router)
app.include_router(image_router)


@app.get("/")
def read_root():
    return {"message": "API is running"}
