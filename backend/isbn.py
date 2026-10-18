import asyncio
import logging
import random
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
import httpx

from models import BookInfo
from settings import settings

logger = logging.getLogger(__name__)

_RETRY_STATUSES = {500, 502, 503, 504}
_MAX_ATTEMPTS = 3
_BACKOFF_BASE = 0.5
_BACKOFF_MAX = 5.0


async def _get_with_retry(
    client: httpx.AsyncClient, url: str
) -> httpx.Response:
    for attempt in range(_MAX_ATTEMPTS):
        try:
            response = await client.get(url)
        except httpx.RequestError as e:
            if attempt == _MAX_ATTEMPTS - 1:
                raise
            wait = min(_BACKOFF_BASE * 2**attempt, _BACKOFF_MAX)
            logger.warning(
                f"Request error for {url}, retrying in {wait:.2f}s: {e}"
            )
            await asyncio.sleep(wait + random.uniform(0, 0.25))
            continue

        if response.status_code < 500 or attempt == _MAX_ATTEMPTS - 1:
            response.raise_for_status()
            return response

        wait = min(_BACKOFF_BASE * 2**attempt, _BACKOFF_MAX)
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                wait = max(wait, float(retry_after))
            except ValueError:
                pass
        logger.warning(
            f"Got {response.status_code} for {url}, retrying in {wait:.2f}s"
        )
        await asyncio.sleep(wait + random.uniform(0, 0.25))

    raise RuntimeError("unreachable")


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
        logger.error("Google Books API key is missing.")
        return UNKNOWN_BOOK.model_copy(
            update={"identifier": isbn, "title": "API Key Missing"}
        )

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&projection=full&key={settings.GOOGLE_API_KEY}"

    async with httpx.AsyncClient() as client:
        try:
            logger.debug(f"Requesting URL: {url}")
            response = await _get_with_retry(client, url)
            data = response.json()
            logger.debug(f"Initial response data: {data}")

            if not (data.get("totalItems", 0) > 0 and data.get("items")):
                logger.warning(f"Book with ISBN {isbn} not found.")
                return UNKNOWN_BOOK.model_copy(
                    update={"identifier": isbn, "title": "Book Not Found"}
                )

            volume_id = data["items"][0]["id"]
            volume_info = data["items"][0].get("volumeInfo", {})
            logger.debug(f"Initial volume_info: {volume_info}")

            # 2. Fetch the specific volume by its ID for complete data
            volume_url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}?key={settings.GOOGLE_API_KEY}"
            logger.debug(f"Requesting volume URL: {volume_url}")
            volume_response = await _get_with_retry(client, volume_url)
            volume_data = volume_response.json()
            logger.debug(f"Detailed volume data: {volume_data}")

            volume_info |= volume_data.get("volumeInfo", {})
            logger.debug(f"Merged volume_info: {volume_info}")

            book_info = BookInfo(
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
                original_language=volume_info.get("language"),
            )
            logger.debug(f"Constructed BookInfo before scraping: {book_info}")

            # 3. Scrape the preview link for extra data
            if preview_link := volume_info.get("previewLink"):
                parsed_url = urlparse(preview_link)
                book_id = parse_qs(parsed_url.query).get("id", [None])[0]
                if book_id:
                    scrape_url = f"https://books.google.es/books?id={book_id}&hl=en"
                    logger.debug(f"Scraping URL: {scrape_url}")
                    scrape_response = await _get_with_retry(client, scrape_url)
                    soup = BeautifulSoup(scrape_response.content, "html.parser")
                    if table := soup.find("table", id="metadata_content_table"):
                        for row in table.find_all("tr", class_="metadata_row"):
                            label_tag = row.find("td", class_="metadata_label")
                            value_tag = row.find("td", class_="metadata_value")
                            if label_tag and value_tag:
                                label = label_tag.text.strip().lower()
                                value = value_tag.text.strip()
                                logger.debug(
                                    f"Scraped row: Label='{label}', Value='{value}'"
                                )
                                if "translated by" in label:
                                    book_info.is_translation = True
                                    book_info.translation_language = (
                                        book_info.original_language
                                    )
                                    book_info.translators = [
                                        t.strip() for t in value.split(",")
                                    ]
                                    logger.debug(
                                        f"Found translators: {book_info.translators}"
                                    )

            logger.info(f"Final BookInfo: {book_info}")
            return book_info

        except httpx.HTTPStatusError as e:
            logger.error(f"API request failed: {e.response.status_code}", exc_info=True)
            return UNKNOWN_BOOK.model_copy(
                update={"identifier": isbn, "title": "API Request Failed"}
            )
        except httpx.RequestError as e:
            logger.error(f"Error fetching book info: {e}", exc_info=True)
            return UNKNOWN_BOOK.model_copy(
                update={"identifier": isbn, "title": "Error Fetching Data"}
            )
