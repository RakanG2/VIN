from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

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

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"/><title>XCMG VIN Lookup</title></head>
<body>
<h1>Введите VIN-код машины</h1>
<input type="text" id="vinInput" placeholder="Например: LXGCPA339LA025257"/>
<button onclick="lookup()">Найти</button>
<div id="result"></div>
<script>
async function lookup() {
  const vin = document.getElementById('vinInput').value.trim();
  if (!vin) return alert('Введите VIN-код');
  document.getElementById('result').innerHTML = 'Загружается...';
  const resp = await fetch(`/api/vin/${vin}`);
  if (!resp.ok) {
    const err = await resp.json();
    document.getElementById('result').innerHTML = '<p style="color:red;">' + err.detail + '</p>';
    return;
  }
  const data = await resp.json();
  document.getElementById('result').innerHTML = data.html;
}
</script>
</body>
</html>
"""
