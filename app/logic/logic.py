from app.dal.dal import save_url_to_db, fetch_long_url
import uuid

from app.models.models import ShortenURLResponse


def create_short_url(long_url: str) -> ShortenURLResponse:
    """
    Generate a short URL and save it to the database.
    """
    short_url = save_url_to_db(long_url)
    return ShortenURLResponse(shortened_url=short_url)


def get_long_url(short_url: str) -> str:
    """
    Retrieve the original long URL for a given short URL.
    """
    return fetch_long_url(short_url)
