from pydantic import BaseModel, HttpUrl


class ShortenURLRequest(BaseModel):
    url: HttpUrl


class ShortenURLResponse(BaseModel):
    shortened_url: str


class RedirectResponseModel(BaseModel):
    redirect_to: HttpUrl
