from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_stock():
    # TODO: реализовать получение остатков на складе
    return []

@router.get("/search")
async def search_stock(query: str):
    # TODO: реализовать поиск запчастей
    return []
