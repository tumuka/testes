import asyncio
from playwright.async_api import async_playwright
import requests

# ❶ Telegram
TELEGRAM_BOT_TOKEN = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"
TELEGRAM_USER_ID   = "6944382551"

# ❷ Browserless
BROWSERLESS_WS_ENDPOINT = "wss://playwright.browserless.io?token=SDHJ6gIu79Ys4q06e3e4de0e2ffce5502462e479ae"

# ❸ Tesla URL
TESLA_INVENTORY_URL = (
    "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34000&range=0"
)

async def check_tesla_inventory() -> None:
    async with async_playwright() as p:
        # Browserless’a bağlan
        browser = await p.connect(BROWSERLESS_WS_ENDPOINT)
        page = await browser.new_page()
        await page.goto(TESLA_INVENTORY_URL, timeout=45_000)
        await page.wait_for_timeout(5_000)

        html = await page.content()

        if (
            "No Inventory Available" in html
            or "Mevcut araç bulunamadı" in html
        ):
            print("Stok bulunamadı.")
        else:
            print("STOK BULUNDU!")
            send_telegram_message(
                f"🚗 Tesla stokta araç bulundu!\n{TESLA_INVENTORY_URL}"
            )

        await browser.close()

def send_telegram_message(text: str) -> None:
    resp = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_USER_ID, "text": text},
        timeout=10,
    )
    print(
        "Telegram OK" if resp.ok else f"Telegram HATA: {resp.status_code} {resp.text}"
    )

if __name__ == "__main__":
    async def main() -> None:
        while True:
            try:
                await check_tesla_inventory()
            except Exception as e:
                print("Hata →", e)
            await asyncio.sleep(300)   # 5 dk

    asyncio.run(main())
