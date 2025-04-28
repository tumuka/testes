import asyncio
from playwright.async_api import async_playwright
import requests
import os

# Telegram Bilgilerin
TELEGRAM_BOT_TOKEN = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"
TELEGRAM_USER_ID = "6944382551"

# Tesla URL
TESLA_INVENTORY_URL = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34000&range=0"

async def check_tesla_inventory():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(TESLA_INVENTORY_URL)
        await page.wait_for_timeout(5000)  # 5 saniye bekle, sayfa tam yüklensin

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
    asyncio.run(check_tesla_inventory())
