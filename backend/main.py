from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from crud import router as books_router
from database import engine
from isbn import get_book_info_by_isbn
from models import BookInfo


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    yield
    # On shutdown
    await engine.dispose()


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.
    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            assert route.methods
            method = list(route.methods)[0]
            route.operation_id = f"{route.name}_{method}"


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(books_router, prefix="/api")


@app.get("/api/isbn/{isbn}", response_model=BookInfo)
async def get_book_by_isbn(isbn: str):
    """gets book info by isbn"""
    return await get_book_info_by_isbn(isbn)


@app.get("/")
async def root():
    return {"message": "Welcome to skbooks backend!"}


use_route_names_as_operation_ids(app)
