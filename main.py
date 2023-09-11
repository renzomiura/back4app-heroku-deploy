import random
import re
import string
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from starlette.responses import RedirectResponse

app = FastAPI(
    title="back4app-url-shortener",
    description="simple (in-memory) url shortener service",
    version="1.0.0",
)
url_regex = r"^(http|https)://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$"
urls = {}


def generate_alias():
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def generate_unique_alias():
    alias = generate_alias()
    while alias in urls:
        alias = generate_alias()

    return alias


@app.get("/")
async def root():
    return {
        "title": app.title,
        "description": app.description,
        "version": app.version,
    }


class ShortenRequest(BaseModel):
    long_url: str
    alias: Optional[str] = None


@app.post("/shorten")
async def shorten(request: Request, data: ShortenRequest):
    if not re.match(url_regex, data.long_url):
        raise HTTPException(status_code=400, detail="Invalid URL.")

    if data.alias and data.alias in urls:
        raise HTTPException(status_code=400, detail="This URL alias is already taken.")

    alias = data.alias if data.alias else generate_unique_alias()
    urls[alias] = data.long_url

    return {
        "long_url": data.long_url,
        "shortened_url": f"{request.base_url}{alias}",
    }


@app.get("/{alias}")
async def shortened_url(alias: str):
    if alias not in urls:
        raise HTTPException(status_code=404, detail="Shortened URL not found.")

    return RedirectResponse(urls[alias], status_code=303)
