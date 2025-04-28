import asyncio
from playwright.async_api import async_playwright
import requests

# Telegram Bilgilerin
TELEGRAM_BOT_TOKEN = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"
TELEGRAM_USER_ID = "6944382551"

# Browserless Playwright WebSocket URL'in
BROWSERLESS_WS_ENDPOINT = "wss://playwright.browserless.io?token=SDHJ6gIu79Ys4q06e3e4de0e2ffce5502462e479ae"

# Tesla URL
TESLA_INVENTORY_URL = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34000&range=0"

async def check_tesla_inventory():
    async with async_playwright() as p:
        browser = await p.connect(BROWSERLESS_WS_ENDPOINT)
        page = await browser.new_page()
        await page.goto(TESLA_INVENTORY_URL)
        await page.wait_for_timeout(5000)

        content = await page.content()

        if "No Inventory Available" in content or "Mevcut araç bulunamadı" in content:
            print("Stok bulunamadı.")
