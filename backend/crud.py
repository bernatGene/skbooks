from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import get_session
from models import (
    Author,
    Book,
    BookCreate,
    BookRead,
    BookReadWithDetails,
    BookUpdate,
    Category,
)

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/books/", response_model=BookReadWithDetails)
async def create_book(book_in: BookCreate, session: SessionDep):
    """
    Create a new book, along with authors and categories if they don't exist.
    """
    book_data = book_in.model_dump(exclude={"authors", "categories"})
    db_book = Book.model_validate(book_data)

    if book_in.authors:
        for author_name in book_in.authors:
            statement = select(Author).where(Author.name == author_name)
            result = await session.exec(statement)
            author = result.first()
            if not author:
                author = Author(name=author_name)
            db_book.authors.append(author)

    if book_in.categories:
        for category_name in book_in.categories:
            statement = select(Category).where(Category.name == category_name)
            result = await session.exec(statement)
            category = result.first()
            if not category:
                category = Category(name=category_name)
            db_book.categories.append(category)

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book


@router.get("/books/", response_model=list[BookRead])
async def read_books(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retrieve a list of books.
    """
    statement = select(Book).offset(offset).limit(limit)
    result = await session.exec(statement)
    books = result.all()
    return books


@router.get("/books/{book_id}", response_model=BookReadWithDetails)
async def read_book(book_id: int, session: SessionDep):
    """
    Retrieve a single book by its ID.
    """
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/books/{book_id}", response_model=BookReadWithDetails)
async def update_book(
    book_id: int,
    book_in: BookUpdate,
    session: SessionDep,
):
    """
    Update a book's details.
    """
    db_book = await session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = book_in.model_dump(exclude_unset=True)

    # Handle non-relationship fields
    for key, value in book_data.items():
        if key not in ["authors", "categories"]:
            setattr(db_book, key, value)

    # Handle authors relationship
    if book_in.authors is not None:
        updated_authors = []
        for author_name in book_in.authors:
            statement = select(Author).where(Author.name == author_name)
            result = await session.exec(statement)
            author = result.first()
            if not author:
                author = Author(name=author_name)
            updated_authors.append(author)
        db_book.authors = updated_authors

    # Handle categories relationship
    if book_in.categories is not None:
        updated_categories = []
        for category_name in book_in.categories:
            statement = select(Category).where(Category.name == category_name)
            result = await session.exec(statement)
            category = result.first()
            if not category:
                category = Category(name=category_name)
            updated_categories.append(category)
        db_book.categories = updated_categories

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book


@router.delete("/books/{book_id}")
async def delete_book(book_id: int, session: SessionDep):
    """
    Delete a book.
    """
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await session.delete(book)
    await session.commit()
    return {"ok": True}
