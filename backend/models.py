from sqlmodel import Field, Relationship, SQLModel

# --- Link Tables ---


class BookAuthorLink(SQLModel, table=True):
    book_id: int | None = Field(default=None, foreign_key="book.id", primary_key=True)
    author_id: int | None = Field(
        default=None, foreign_key="author.id", primary_key=True
    )


class BookCategoryLink(SQLModel, table=True):
    book_id: int | None = Field(default=None, foreign_key="book.id", primary_key=True)
    category_id: int | None = Field(
        default=None, foreign_key="category.id", primary_key=True
    )


# --- Main Models ---


class AuthorBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(
        back_populates="authors", link_model=BookAuthorLink
    )


class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(
        back_populates="categories", link_model=BookCategoryLink
    )


class BookcaseBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Bookcase(BookcaseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    shelves: list["Shelf"] = Relationship(back_populates="bookcase")


class ShelfBase(SQLModel):
    # A shelf is identified by its position in the bookcase
    # and the bookcase it belongs to.
    number: int
    bookcase_id: int | None = Field(default=None, foreign_key="bookcase.id")


class Shelf(ShelfBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bookcase: "Bookcase" = Relationship(back_populates="shelves")
    books: list["Book"] = Relationship(back_populates="shelf")


class BookBase(SQLModel):
    title: str
    subtitle: str | None = None
    isbn_13: str = Field(unique=True, index=True)
    isbn_10: str | None = Field(unique=True, index=True, default=None)
    publisher: str | None = None
    published_date: str | None = None
    page_count: int | None = None
    language: str | None = None
    description: str | None = None
    image_link: str | None = None
    # A book can be in a shelf, or not.
    shelf_id: int | None = Field(default=None, foreign_key="shelf.id")


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    authors: list[Author] = Relationship(
        back_populates="books", link_model=BookAuthorLink
    )
    categories: list[Category] = Relationship(
        back_populates="books", link_model=BookCategoryLink
    )
    shelf: Shelf | None = Relationship(back_populates="books")


# --- Public Models (for API) ---


class AuthorRead(AuthorBase):
    id: int


class CategoryRead(CategoryBase):
    id: int


class BookcaseRead(BookcaseBase):
    id: int


class ShelfRead(ShelfBase):
    id: int


class BookRead(BookBase):
    id: int


class BookcaseReadWithShelves(BookcaseRead):
    shelves: list[ShelfRead] = []


class ShelfReadWithBooks(ShelfRead):
    books: list[BookRead] = []


class BookReadWithDetails(BookRead):
    authors: list[AuthorRead] = []
    categories: list[CategoryRead] = []
    shelf: ShelfRead | None = None


# --- Create Models ---


class BookcaseCreate(BookcaseBase):
    pass


class ShelfCreate(ShelfBase):
    pass


class BookCreate(BookBase):
    authors: list[str] = []
    categories: list[str] = []


# --- Update Models ---


class BookcaseUpdate(SQLModel):
    name: str | None = None


class ShelfUpdate(SQLModel):
    number: int | None = None
    bookcase_id: int | None = None


class BookUpdate(SQLModel):
    title: str | None = None
    subtitle: str | None = None
    isbn_13: str | None = None
    isbn_10: str | None = None
    publisher: str | None = None
    published_date: str | None = None
    page_count: int | None = None
    language: str | None = None
    description: str | None = None
    image_link: str | None = None
    shelf_id: int | None = None
    authors: list[str] | None = None
    categories: list[str] | None = None


# --- Google Books API ---


class BookInfo(SQLModel):
    title: str
    authors: list[str]
    publisher: str | None = None
    published_date: str | None = None
    thumbnail: str | None = None
    identifier: str
