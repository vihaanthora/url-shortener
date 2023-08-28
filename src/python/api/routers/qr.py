from fastapi import APIRouter

router = APIRouter()

@router.get("/generate")
def generate_qr(url: str):
    return {"qr": "todo"}