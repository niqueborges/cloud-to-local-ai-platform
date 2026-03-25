from fastapi import FastAPI
from app.modules.users.router import router as users_router

app = FastAPI()

app.include_router(users_router)


@app.get("/")
def read_root():
    return {"message": "API is running"}