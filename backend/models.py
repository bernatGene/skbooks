from sqlmodel import Field, SQLModel, Relationship

# --- Link Tables ---

class BookAuthorLink(SQLModel, table=True):
    book_id: int | None = Field(default=None, foreign_key="book.id", primary_key=True)
    author_id: int | None = Field(default=None, foreign_key="author.id", primary_key=True)

class BookCategoryLink(SQLModel, table=True):
    book_id: int | None = Field(default=None, foreign_key="book.id", primary_key=True)
    category_id: int | None = Field(default=None, foreign_key="category.id", primary_key=True)

# --- Main Models ---

class AuthorBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(back_populates="authors", link_model=BookAuthorLink)

class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list["Book"] = Relationship(back_populates="categories", link_model=BookCategoryLink)

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
    physical_location: str | None = Field(default=None, index=True)

class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    authors: list[Author] = Relationship(back_populates="books", link_model=BookAuthorLink)
    categories: list[Category] = Relationship(back_populates="books", link_model=BookCategoryLink)

# --- Public Models (for API) ---

class AuthorRead(AuthorBase):
    id: int

class CategoryRead(CategoryBase):
    id: int

class BookRead(BookBase):
    id: int

class BookReadWithDetails(BookRead):
    authors: list[AuthorRead] = []
    categories: list[CategoryRead] = []

class BookCreate(BookBase):
    authors: list[str] = []
    categories: list[str] = []

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
    physical_location: str | None = None
    authors: list[str] | None = None
    categories: list[str] | None = None
