from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import get_session
from models import (
    Author,
    Book,
    Bookcase,
    BookcaseCreate,
    BookcaseRead,
    BookcaseReadWithCounts,
    BookcaseReadWithShelves,
    BookcaseUpdate,
    BookCreate,
    BookRead,
    BookReadWithDetails,
    BookUpdate,
    Category,
    Shelf,
    ShelfCreate,
    ShelfRead,
    ShelfReadWithBookCount,
    ShelfReadWithBooks,
    ShelfUpdate,
)

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/bookcases/", response_model=list[BookcaseReadWithCounts])
async def read_bookcases_with_counts(session: SessionDep):
    """
    Retrieve all bookcases with a count of shelves and books per shelf.
    """
    book_count_subquery = (
        select(Shelf.id.label("shelf_id"), func.count(Book.id).label("book_count"))
        .join(Book, Shelf.id == Book.shelf_id, isouter=True)
        .group_by(Shelf.id)
        .subquery()
    )

    statement = (
        select(Bookcase, Shelf, book_count_subquery.c.book_count)
        .join(Shelf, Bookcase.id == Shelf.bookcase_id)
        .join(
            book_count_subquery,
            Shelf.id == book_count_subquery.c.shelf_id,
            isouter=True,
        )
        .order_by(Bookcase.id, Shelf.number)
    )

    result = await session.exec(statement)

    bookcases_map = {}
    for bookcase, shelf, book_count in result:
        if bookcase.id not in bookcases_map:
            bookcases_map[bookcase.id] = BookcaseReadWithCounts(
                id=bookcase.id, name=bookcase.name, shelves=[]
            )

        bookcases_map[bookcase.id].shelves.append(
            ShelfReadWithBookCount(
                id=shelf.id,
                number=shelf.number,
                bookcase_id=shelf.bookcase_id,
                book_count=book_count or 0,
            )
        )

    return list(bookcases_map.values())


@router.post("/bookcases/", response_model=BookcaseRead)
async def create_bookcase(bookcase_in: BookcaseCreate, session: SessionDep):
    """
    Create a new bookcase.
    """
    db_bookcase = Bookcase.model_validate(bookcase_in)
    session.add(db_bookcase)
    await session.commit()
    await session.refresh(db_bookcase)
    return db_bookcase


@router.get("/bookcases/{bookcase_id}", response_model=BookcaseReadWithShelves)
async def read_bookcase(bookcase_id: int, session: SessionDep):
    """
    Retrieve a single bookcase by its ID with its shelves.
    """
    bookcase = await session.get(Bookcase, bookcase_id)
    if not bookcase:
        raise HTTPException(status_code=404, detail="Bookcase not found")
    return bookcase


@router.patch("/bookcases/{bookcase_id}", response_model=BookcaseRead)
async def update_bookcase(
    bookcase_id: int,
    bookcase_in: BookcaseUpdate,
    session: SessionDep,
):
    """
    Update a bookcase's details.
    """
    db_bookcase = await session.get(Bookcase, bookcase_id)
    if not db_bookcase:
        raise HTTPException(status_code=404, detail="Bookcase not found")

    bookcase_data = bookcase_in.model_dump(exclude_unset=True)
    for key, value in bookcase_data.items():
        setattr(db_bookcase, key, value)

    session.add(db_bookcase)
    await session.commit()
    await session.refresh(db_bookcase)
    return db_bookcase


@router.delete("/bookcases/{bookcase_id}")
async def delete_bookcase(bookcase_id: int, session: SessionDep):
    """
    Delete a bookcase.
    """
    # Note: This will fail if the bookcase has shelves due to FK constraints.
    bookcase = await session.get(Bookcase, bookcase_id)
    if not bookcase:
        raise HTTPException(status_code=404, detail="Bookcase not found")
    await session.delete(bookcase)
    await session.commit()
    return {"ok": True}


# Shelf CRUD


@router.post("/shelves/", response_model=ShelfRead)
async def create_shelf(shelf_in: ShelfCreate, session: SessionDep):
    """
    Create a new shelf.
    """
    if shelf_in.bookcase_id:
        bookcase = await session.get(Bookcase, shelf_in.bookcase_id)
        if not bookcase:
            raise HTTPException(
                status_code=404, detail="Bookcase not found for this shelf"
            )

    db_shelf = Shelf.model_validate(shelf_in)
    session.add(db_shelf)
    await session.commit()
    await session.refresh(db_shelf)
    return db_shelf


@router.get("/shelves/", response_model=list[ShelfRead])
async def read_shelves(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retrieve a list of shelves.
    """
    statement = select(Shelf).offset(offset).limit(limit)
    result = await session.exec(statement)
    shelves = result.all()
    return shelves


@router.get("/shelves/{shelf_id}", response_model=ShelfReadWithBooks)
async def read_shelf(shelf_id: int, session: SessionDep):
    """
    Retrieve a single shelf by its ID with its books.
    """
    shelf = await session.get(Shelf, shelf_id)
    if not shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")
    return shelf


@router.patch("/shelves/{shelf_id}", response_model=ShelfRead)
async def update_shelf(
    shelf_id: int,
    shelf_in: ShelfUpdate,
    session: SessionDep,
):
    """
    Update a shelf's details.
    """
    db_shelf = await session.get(Shelf, shelf_id)
    if not db_shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")

    shelf_data = shelf_in.model_dump(exclude_unset=True)

    if "bookcase_id" in shelf_data and shelf_data["bookcase_id"] is not None:
        bookcase = await session.get(Bookcase, shelf_data["bookcase_id"])
        if not bookcase:
            raise HTTPException(status_code=404, detail="Bookcase not found")

    for key, value in shelf_data.items():
        setattr(db_shelf, key, value)

    session.add(db_shelf)
    await session.commit()
    await session.refresh(db_shelf)
    return db_shelf


@router.delete("/shelves/{shelf_id}")
async def delete_shelf(shelf_id: int, session: SessionDep):
    """
    Delete a shelf.
    """
    # Note: This will fail if there are books on the shelf due to FK constraints.
    shelf = await session.get(Shelf, shelf_id)
    if not shelf:
        raise HTTPException(status_code=404, detail="Shelf not found")
    await session.delete(shelf)
    await session.commit()
    return {"ok": True}


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
