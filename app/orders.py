from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_orders():
    # TODO: реализовать сбор списка заказов
    return []

@router.get("/{order_id}")
async def get_order_details(order_id: str):
    # TODO: реализовать получение деталей заказа
    return {}
