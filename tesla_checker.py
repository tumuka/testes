import time, requests, json
print("Kod başladı")
# Telegram
TOKEN   = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"          # Bot token
USER_ID = "6944382551"

# ScrapingAnt ücretsiz API anahtarın
ANT_KEY = "1cf224181d6449fc9a268944f5bc7f7d"

# Tesla API body
BODY = {
    "query": {
        "model": "my", "condition": "new", "arrangeby": "plh", "order": "asc",
        "market": "TR", "language": "tr", "super_region": "EMEA", "zip": "34000",
        "range": 2000, "outsideSearch": True
    },
    "offset": 0, "count": 1000
}

HEADERS = {"Content-Type": "application/json"}

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": msg}, timeout=10
    )

def fetch_inventory():
    url = (
        "https://api.scrapingant.com/v2/general"
        f"?x-api-key={ANT_KEY}"
        "&url=https://www.tesla.com/inventory/api/v1/inventory-results"
        "&method=POST&body_type=raw"
        "&headers=Content-Type:%20application/json"
    )
    for attempt in range(3):
        r = requests.post(url, headers=HEADERS, data=json.dumps(BODY), timeout=30)
        if r.status_code == 200:
            return r.json()
        print(f"{attempt+1}/3 – ScrapingAnt {r.status_code}, retry…")
        time.sleep(3)
    print("↪ Üst üste 3 hata, döngüde atlandı.")
    return None

def check_once():
    data = fetch_inventory()
    if not data:
        return

    total = data.get("total_matches_found", 0)
    print("Toplam sonuç:", total)
    if total:
        send("🚗 Tesla stokta araç bulundu!\nhttps://www.tesla.com/tr_TR/inventory/new/my?zip=34000")
        print("STOK BULUNDU! Telegram gönderildi")
    else:
        print("Stok bulunamadı.")

if __name__ == "__main__":
    print("Kod başladı")
    while True:
        check_once()
        time.sleep(600)   # 10 dk
