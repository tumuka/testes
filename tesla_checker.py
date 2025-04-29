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

        # ↓ değişti
        "range": 2000,          # 2000 km yarıçap
        "outsideSearch": True   # zip dışındaki stokları da getir
    },
    "offset": 0,
    "count": 1000              # (opsiyonel) daha çok satır çek
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
        "&method=POST&body_type=raw"
        "&headers=Content-Type:%20application/json"
    )
    try:
        resp = requests.post(url, data=json.dumps(BODY), timeout=30)
        data = resp.json()
        print("Debug cevap:", json.dumps(data)[:400])

    except ValueError:
        print("Beklenmeyen cevap:", resp.status_code, resp.text[:120])
        return
    ...


    if data.get("results"):
        print("STOK BULUNDU!  Telegram gönderildi")
        send("🚗 Tesla stokta araç bulundu!\nhttps://www.tesla.com/tr_TR/inventory/new/my?zip=34000")
    else:
        print("Stok bulunamadı.")

if __name__ == "__main__":
    while True:
        check_once()
        time.sleep(600)         # 10 dk
