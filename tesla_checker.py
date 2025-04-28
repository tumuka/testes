import time, requests, json

# Telegram
TOKEN   = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"          # Bot token
USER_ID = "6944382551"

# ScrapingAnt ücretsiz API anahtarın
ANT_KEY = "1cf224181d6449fc9a268944f5bc7f7d"

# Tesla API body (değişmedi)
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
        "range": 0
    },
    "offset": 0,
    "count": 20
}

HEADERS = {"Content-Type": "application/json"}

def send(msg: str):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": msg},
        timeout=10,
    )

def check_once():
    url = (
        "https://api.scrapingant.com/v2/general"
        f"?x-api-key={ANT_KEY}"
        "&url=https://www.tesla.com/inventory/api/v1/inventory-results"
    )

    try:
        resp = requests.post(url, headers=HEADERS, data=json.dumps(BODY), timeout=30)
        data = resp.json()
    except Exception as e:
        print("Hata:", e)
        return

    if data.get("results"):
        print("STOK BULUNDU!  Telegram gönderildi")
        send("🚗 Tesla stokta araç bulundu!\nhttps://www.tesla.com/tr_TR/inventory/new/my?zip=34000")
    else:
        print("Stok bulunamadı.")

if __name__ == "__main__":
    while True:
        check_once()
        time.sleep(300)         # 5 dk
