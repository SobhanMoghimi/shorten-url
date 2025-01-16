import os

from fastapi import APIRouter, HTTPException
from pydantic import HttpUrl
from starlette.responses import FileResponse

from app.models.models import (
    NewURLsTodayDTO,
    TotalAccessesTodayDTO,
    TopAccessedURLDTO,
    URLsTimeSinceLastAccessDTO,
    ShortenURLRequest,
    ShortenURLResponse,
    RedirectResponseModel, RegisteredURLsEachDayDTO
)
from app.dal.dal import (
    save_url_to_db,
    get_top_3_accessed_urls,
    get_urls_time_since_last_access,
    get_long_url,
    get_accesses_per_day_per_url, get_registered_urls_each_day, generate_charts
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

from fastapi import APIRouter, HTTPException



@router.get("/dashboard/accesses_per_day_per_url", tags=["Dashboard"])
def dashboard_accesses_per_day_per_url():
    if data := get_accesses_per_day_per_url():
        return data
    raise HTTPException(status_code=404, detail="No data found")



@router.get("/dashboard/registered_urls_each_day", response_model=list[RegisteredURLsEachDayDTO], tags=["Dashboard"])
def dashboard_registered_urls_each_day():
    if data := get_registered_urls_each_day():
        return data
    raise HTTPException(status_code=404, detail="No data found")


@router.post("/dashboard/generate_charts", tags=["Dashboard"])
def dashboard_generate_charts():
    try:
        generate_charts()
        return {"message": "Charts generated successfully and saved to the 'charts' folder."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating charts: {str(e)}") from e


@router.get("/dashboard/charts/{chart_name}", tags=["Dashboard"])
def get_chart(chart_name: str):
    chart_path = os.path.join("charts", chart_name)
    if os.path.exists(chart_path):
        return FileResponse(chart_path)
    raise HTTPException(status_code=404, detail="Chart not found")
