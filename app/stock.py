from fastapi import APIRouter
router = APIRouter()
@router.get("/")
async def get_stock():
    return []
@router.get("/search")
async def search_stock(query: str):
    return []