from pydantic import BaseModel, HttpUrl


class ShortenURLRequest(BaseModel):
    url: HttpUrl


class ShortenURLResponse(BaseModel):
    shortened_url: str


class RedirectResponseModel(BaseModel):
    redirect_to: HttpUrl

class NewURLsTodayDTO(BaseModel):
    total_new_urls: int


class TotalAccessesTodayDTO(BaseModel):
    total_accesses: int


class TopAccessedURLDTO(BaseModel):
    shortened_url: str
    accessed_count: int


class URLsTimeSinceLastAccessDTO(BaseModel):
    shortened_url: str
    accessed_count: int
    time_since_last_access: str
