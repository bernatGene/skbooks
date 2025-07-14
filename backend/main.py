from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.database import init_db
from backend.crud import router as books_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    await init_db()
    yield
    # On shutdown
    # (any cleanup)

app = FastAPI(lifespan=lifespan)

app.include_router(books_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to skbooks backend!"}