import os, time, json, requests

# --- ENV değişkenleri ---
TOKEN   = os.environ["TG_TOKEN"]        # Telegram bot token
USER_ID = os.environ["TG_USER"]         # Telegram chat-id
KEY     = os.environ["SCRAPER_KEY"]     # ScraperAPI anahtarı
# ------------------------

TESLA_URL = "https://www.tesla.com/inventory/api/v1/inventory-results"

BODY = {
    "query": {
        "model": "my", "condition": "new",
        "arrangeby": "plh", "order": "asc",
        "market": "TR", "language": "tr",
        "super_region": "EMEA", "zip": "34000",
        "range": 2000, "outsideSearch": True
    },
    "offset": 0, "count": 1000
}

COMMON = {
    "api_key": KEY,
    "url": TESLA_URL,
    "method": "POST",
    "body_type": "raw",
    "headers": "Content-Type:application/json",

    # ─── İŞE YARAYAN HAVUZ ───
    "country_code": "us_residential",        # fr→nl→se→us_residential deneyebilirsiniz
    "device_type": "desktop",    # desktop / mobile
    # ──────────────────────────

    "render": "false",
    "max_timeout": "40000"       # 40 sn ScraperAPI tarafı
}

def tg(msg: str) -> None:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": msg},
        timeout=10,
    )

def fetch() -> dict | None:
    for i in range(3):
        try:
            r = requests.post(
                "https://api.scraperapi.com/",
                params=COMMON,
                data=json.dumps(BODY),
                timeout=40        # 40 sn bizim taraf
            )
            if r.status_code == 200:
                return r.json()
            print(f"{i+1}/3 → ScraperAPI {r.status_code}, retry…")
        except requests.Timeout:
            print(f"{i+1}/3 bağlantı hatası: Read timeout, retry…")
        time.sleep(3)
    print("↪ Üst üste 3 hata, döngüde atlandı.")
    return None

def loop() -> None:
    data = fetch()
    if not data:
        return
    total = data.get("total_matches_found", 0)
    print("Toplam sonuç:", total)
    if total:
        tg("🚗 Tesla stokta araç bulundu!\nhttps://www.tesla.com/tr_TR/inventory/new/my?zip=34000")

if __name__ == "__main__":
    # Anahtarı ve çıkış IP’sini bir kez göster
    print("Anahtar testi:", requests.get(
        f"https://api.scraperapi.com/?api_key={KEY}&url=https://httpbin.org/ip"
    ).status_code)
    print("Railway çıkış IP:\n", requests.get("https://httpbin.org/ip").text)

    while True:
        loop()
        time.sleep(600)       # 10 dk
