import re

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from utils.mongo_client import client

router = APIRouter()


# endpoint to redirect users to the main url
@router.get("/{shortened}")
def redirect(shortened: str):
    db = client.url_shortener
    mappings = db.mappings
    regex_pattern = f"^{shortened}$|^_{shortened}$"
    row = mappings.find_one({"shortened": {"$regex": re.compile(regex_pattern)}})
    if row is not None:
        original_url = row["original"]
        if not original_url.startswith(("http://", "https://")):
            original_url = f"http://{original_url}"
        return RedirectResponse(url=original_url, status_code=302)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
