import logging

from fastapi import FastAPI
from app.controller.router import router

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="URL Shortener API",
    description="A URL shortener API with Swagger documentation",
    version="1.0.0",
)

# Include the router
app.include_router(router)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to the URL Shortener API"}
