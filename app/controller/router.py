from fastapi import APIRouter, HTTPException
from pydantic import HttpUrl

from app.models.models import (
    NewURLsTodayDTO,
    TotalAccessesTodayDTO,
    TopAccessedURLDTO,
    URLsTimeSinceLastAccessDTO,
    ShortenURLRequest,
    ShortenURLResponse,
    RedirectResponseModel
)
from app.dal.dal import (
    save_url_to_db,
    get_top_3_accessed_urls,
    get_urls_time_since_last_access,
    get_long_url,
    get_total_accesses_today,
    get_new_urls_today
)

router = APIRouter()


@router.post("/shorten", response_model=ShortenURLResponse, tags=["URL Operations"])
def shorten_url(request: ShortenURLRequest):
    try:
        return ShortenURLResponse(shortened_url=save_url_to_db(str(request.url)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{short_url}", response_model=RedirectResponseModel, tags=["URL Operations"])
def redirect_to_url(short_url: str):
    if long_url := get_long_url(short_url):
        return RedirectResponseModel(redirect_to=HttpUrl(long_url))
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")


@router.get("/dashboard/new_urls_today", response_model=NewURLsTodayDTO, tags=["Dashboard"])
def dashboard_new_urls_today():
    if data := get_new_urls_today():
        return data
    raise HTTPException(status_code=404, detail="No data found")


@router.get("/dashboard/total_accesses_today", response_model=TotalAccessesTodayDTO, tags=["Dashboard"])
def dashboard_total_accesses_today():
    if data := get_total_accesses_today():
        return data
    raise HTTPException(status_code=404, detail="No data found")


@router.get("/dashboard/top_3_accessed_urls", response_model=list[TopAccessedURLDTO], tags=["Dashboard"])
def dashboard_top_3_accessed_urls():
    if data := get_top_3_accessed_urls():
        return data
    raise HTTPException(status_code=404, detail="No data found")


@router.get("/dashboard/urls_time_since_last_access", response_model=list[URLsTimeSinceLastAccessDTO],
            tags=["Dashboard"])
def dashboard_urls_time_since_last_access():
    if data := get_urls_time_since_last_access():
        return data
    raise HTTPException(status_code=404, detail="No data found")
