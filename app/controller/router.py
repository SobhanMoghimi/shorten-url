from fastapi import APIRouter, HTTPException, Depends
from app.models.models import ShortenURLRequest, ShortenURLResponse, RedirectResponseModel
from app.logic.logic import create_short_url, get_long_url

router = APIRouter()


@router.post("/shorten", response_model=ShortenURLResponse, tags=["URL Operations"])
def shorten_url(request: ShortenURLRequest):
    """
    Shorten a long URL into a 6-character short URL.
    """
    try:
        short_url = create_short_url(str(request.url))
        return {"shortened_url": f"http://localhost:8000/{short_url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{short_url}", response_model=RedirectResponseModel, tags=["URL Operations"])
def redirect_to_url(short_url: str):
    """
    Redirect to the original URL using the short URL.
    """
    long_url = get_long_url(short_url)
    if not long_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {"redirect_to": long_url}
