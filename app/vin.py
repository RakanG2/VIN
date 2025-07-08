from fastapi import APIRouter, HTTPException
from playwright.async_api import async_playwright
import os, tempfile, base64
from PIL import Image
import pytesseract

router = APIRouter()

async def solve_captcha(page):
    img = await page.wait_for_selector(".code img")
    src = await img.get_attribute("src")
    if src.startswith("data:image"):
        _, encoded = src.split(",", 1)
        data = base64.b64decode(encoded)
    else:
        resp = await page.request.get(src)
        data = await resp.body()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
        f.write(data)
        path = f.name
    text = pytesseract.image_to_string(Image.open(path), config="--psm 7 -c tessedit_char_whitelist=0123456789")
    return text.strip()

@router.get("/vin/{vin}")
async def fetch_vehicle(vin: str):
    LOGIN_URL = "https://xgss.xcmg.com/#/login"
    TARGET_URL = f"https://xgss.xcmg.com/#/struct/car/{vin}"
    username = os.getenv("XCMG_USERNAME")
    password = os.getenv("XCMG_PASSWORD")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(LOGIN_URL)
        await page.fill("input[placeholder='Логин']", username)
        await page.fill("input[placeholder='Пароль']", password)
        code = await solve_captcha(page)
        await page.fill("input[placeholder='Проверочный код']", code)
        await page.click("button:has-text('Логин')")
        await page.wait_for_url(TARGET_URL, timeout=10000)
        await page.goto(TARGET_URL)
        try:
            await page.wait_for_selector(".ivu-tree", timeout=5000)
        except:
            await browser.close()
            raise HTTPException(status_code=404, detail="VIN не найден")
        html = await page.content()
        await browser.close()
        return {"vin": vin, "html": html}
