import httpx

from models import BookInfo
from settings import settings

UNKNOWN_BOOK = BookInfo(
    title="Unknown Title",
    authors=["Unknown Author"],
    publisher="Unknown Publisher",
    published_date="Unknown Date",
    thumbnail="/no-image-placeholder.svg",
    identifier="",
)


async def get_book_info_by_isbn(isbn: str) -> BookInfo:
    """Queries the Google Books API for a book by its ISBN."""
    if not settings.GOOGLE_API_KEY:
        print("Google Books API key is missing.")
        return UNKNOWN_BOOK.model_copy(
            update={"identifier": isbn, "title": "API Key Missing"}
        )

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={settings.GOOGLE_API_KEY}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("totalItems", 0) > 0 and data.get("items"):
                volume_info = data["items"][0].get("volumeInfo", {})
                return BookInfo(
                    title=volume_info.get("title", UNKNOWN_BOOK.title),
                    authors=volume_info.get("authors", UNKNOWN_BOOK.authors),
                    publisher=volume_info.get("publisher", UNKNOWN_BOOK.publisher),
                    published_date=volume_info.get(
                        "publishedDate", UNKNOWN_BOOK.published_date
                    ),
                    thumbnail=volume_info.get("imageLinks", {}).get(
                        "thumbnail", UNKNOWN_BOOK.thumbnail
                    ),
                    identifier=isbn,
                )
            return UNKNOWN_BOOK.model_copy(
                update={"identifier": isbn, "title": "Book Not Found"}
            )
        except httpx.HTTPStatusError as e:
            print(f"API request failed: {e.response.status_code}")
            return UNKNOWN_BOOK.model_copy(
                update={"identifier": isbn, "title": "API Request Failed"}
            )
        except httpx.RequestError as e:
            print(f"Error fetching book info: {e}")
            return UNKNOWN_BOOK.model_copy(
                update={"identifier": isbn, "title": "Error Fetching Data"}
            )

