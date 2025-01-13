from fastapi import APIRouter, HTTPException, Depends
from pydantic import HttpUrl

from app.models.models import ShortenURLRequest, ShortenURLResponse, RedirectResponseModel
from app.logic.logic import create_short_url, get_long_url

router = APIRouter()


@router.post("/shorten", response_model=ShortenURLResponse, tags=["URL Operations"])
def shorten_url(request: ShortenURLRequest):
    """
    Shorten a long URL into a 6-character short URL.
    """
    try:
        return create_short_url(str(request.url))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{short_url}", response_model=RedirectResponseModel, tags=["URL Operations"])
def redirect_to_url(short_url: str):
    """
    Redirect to the original URL using the short URL.
    """
    if long_url := get_long_url(short_url):
        return RedirectResponseModel(redirect_to=HttpUrl(long_url))
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
