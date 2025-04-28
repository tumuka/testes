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
        else:
            print("STOK BULUNDU!")
            send_telegram_message("🚗 Tesla stokta araç bulundu! Hemen bak: " + TESLA_INVENTORY_URL)

        await browser.close()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_USER_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Telegram mesajı gönderilemedi:", response.text)
    else:
        print("Telegram mesajı gönderildi.")

if __name__ == "__main__":
    async def main():
        while True:
            await check_tesla_inventory()
            await asyncio.sleep(300)  # 5 dakika bekle (300 saniye)

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
