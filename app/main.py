from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

from app.auth import router as auth_router
from app.orders import router as orders_router
from app.stock import router as stock_router
from app.vin import router as vin_router

app = FastAPI(title="XCMG Middleware API")

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(orders_router, prefix="/api/orders", tags=["orders"])
app.include_router(stock_router, prefix="/api/stock", tags=["stock"])
app.include_router(vin_router, prefix="/api", tags=["vin"])

@app.get("/")
async def root():
    return {"message": "XCMG Middleware is running"}
