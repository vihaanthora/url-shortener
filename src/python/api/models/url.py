from pydantic import BaseModel, HttpUrl

class URL(BaseModel):
    original: HttpUrl
    custom: str | None = None
