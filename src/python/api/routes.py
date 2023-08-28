from fastapi import APIRouter
from routers import qr, url

router = APIRouter()

router.include_router(url.router, prefix="/url", tags=["url"])
# router.include_router(qr_code.router, prefix="/qr_code", tags=["qr_code"])
