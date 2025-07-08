from fastapi import APIRouter, HTTPException
from playwright.async_api import async_playwright
import os

router = APIRouter()

@router.get("/vin/{vin}")
async def fetch_vehicle(vin: str):
    """
    Логинимся на xgss.xcmg.com, переходим на страницу структуры по VIN
    и возвращаем весь HTML. Если VIN не найден — 404.
    """
    LOGIN_URL = "https://xgss.xcmg.com/#/login"
    TARGET_URL = f"https://xgss.xcmg.com/#/struct/car/{vin}"

    username = os.getenv("XCMG_USERNAME")
    password = os.getenv("XCMG_PASSWORD")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context()
        page = await ctx.new_page()

        # 1) Открываем страницу логина
        await page.goto(LOGIN_URL)
        await page.fill("input[name='username']", username)
        await page.fill("input[name='password']", password)
        await page.click("button[type='submit']")

        # 2) Переходим на страницу VIN
        await page.goto(TARGET_URL)

        # 3) Ждём либо дерева запчастей, либо появление текста ошибки
        #    допустим, у нашей структуры есть CSS-класс .ivu-tree
        try:
            await page.wait_for_selector(".ivu-tree", timeout=5000)
        except:
            await browser.close()
            raise HTTPException(status_code=404, detail="VIN не найден")

        html = await page.content()
        await browser.close()
        return {"vin": vin, "html": html}
