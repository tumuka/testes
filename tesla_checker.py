import time, requests, json

print("Kod başladı", flush=True)

# Telegram
TOKEN   = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"
USER_ID = "6944382551"

# ScraperAPI anahtarı
SCRAPER_KEY = "b0794e1bca8dbc04ded56bae2611480a"

# Tesla API body
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
        "outsideSearch": True
    },
    "offset": 0,
    "count": 1000
}

HEADERS = {"Content-Type": "application/json"}


def send(msg: str) -> None:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": msg},
        timeout=10
    )


def fetch_inventory() -> dict | None:
    url = (
        "https://api.scraperapi.com"
        f"?api_key={SCRAPER_KEY}"
        "&url=https://www.tesla.com/inventory/api/v1/inventory-results"
        "&method=POST&body_type=raw"
        "&headers=Content-Type:application/json"
    )

    for attempt in range(3):
        r = requests.post(url, headers=HEADERS, data=json.dumps(BODY), timeout=30)
        if r.status_code == 200:
            return r.json()
        print(f"{attempt+1}/3 – ScraperAPI {r.status_code}, retry…")
        time.sleep(3)

    print("↪ Üst üste 3 hata, döngüde atlandı.")
    return None


def check_once() -> None:
    data = fetch_inventory()
    if not data:
        return

    total = data.get("total_matches_found", 0)
    print("Toplam sonuç:", total)

    if total:
        send(
            "🚗 Tesla stokta araç bulundu!\n"
            "https://www.tesla.com/tr_TR/inventory/new/my?zip=34000"
        )
        print("STOK BULUNDU! Telegram gönderildi")
    else:
        print("Stok bulunamadı.")


if __name__ == "__main__":
    while True:
        check_once()
        time.sleep(600)      # 10 dk
