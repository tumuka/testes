#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tesla stok kontrolü – ScraperAPI ile
Her 10 dakikada bir Tesla API’sini POST ederek sonuç sayısını okur.
Stok varsa Telegram’a mesaj yollar.

• TOKEN         : Telegram bot token’ınız
• USER_ID       : Kendinize ait chat id
• SCRAPER_KEY   : https://dashboard.scraperapi.com altında API Key
"""

import time, json, requests

# ────────────────────────────────────────────  AYARLAR

TOKEN       = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"
USER_ID     = "6944382551"
SCRAPER_KEY = "b0794e1bca8dbc04ded56bae2611480a"

TESLA_POST_URL = "https://www.tesla.com/inventory/api/v1/inventory-results"

BODY = {
    "query": {
        "model": "my",
        "condition": "new",
        "arrangeby": "plh",
        "order": "asc",
        "market": "TR",
        "language": "tr",
        "super_region": "EMEA",
        "zip": "34000",
        "range": 2000,
        "outsideSearch": True      # diğer bayiler
    },
    "offset": 0,
    "count": 1000
}

HEADERS = {"Content-Type": "application/json"}

# ────────────────────────────────────────────  YARDIMCI

def send(msg: str) -> None:
    """Telegram mesajı gönder"""
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": msg},
        timeout=10,
    )

def fetch_inventory() -> dict | None:
    """ScraperAPI üzerinden Tesla POST isteğini yap ve JSON döndür"""
    base = "https://api.scraperapi.com"
    params = {
        "api_key": SCRAPER_KEY,
        "url": TESLA_POST_URL,
        "render": "false"          # yalnızca HTML renderını kapatır
    }

    for attempt in range(3):
        try:
            r = requests.post(
                base,
                params=params,     # ScraperAPI query
                json=BODY,         # Tesla body’si
                headers=HEADERS,
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            print(f"{attempt+1}/3 bağlantı hatası:", e, flush=True)
            time.sleep(3)
            continue

        if r.status_code == 200:
            return r.json()

        print(f"{attempt+1}/3 – ScraperAPI {r.status_code}, retry…", flush=True)
        time.sleep(3)

    print("↪ Üst üste 3 hata, döngüde atlandı.", flush=True)
    return None

def check_once() -> None:
    """Tek seferlik kontrol"""
    data = fetch_inventory()
    if not data:
        return

    total = data.get("total_matches_found", 0)
    print("Toplam sonuç:", total, flush=True)

    if total:
        send(
            "🚗 **Tesla stokta araç bulundu!**\n"
            "https://www.tesla.com/tr_TR/inventory/new/my?zip=34000"
        )
        print("STOK BULUNDU!  Telegram gönderildi", flush=True)
    else:
        print("Stok bulunamadı.", flush=True)

# ────────────────────────────────────────────  ANA DÖNGÜ

if __name__ == "__main__":
    print("Kod başladı", flush=True)
    while True:
        check_once()
        time.sleep(600)   # 10 dk
