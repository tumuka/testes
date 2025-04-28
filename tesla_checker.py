import time, requests, json

TOKEN   = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"      # Telegram
USER_ID = "6944382551"

URL = "https://www.tesla.com/inventory/api/v1/inventory-results"
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

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Content-Type": "application/json"
}

def send(txt: str):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": txt},
        timeout=10,
    )

def check_once():
    for i in range(3):
        try:
            r = requests.post(URL, headers=HEADERS, data=json.dumps(BODY), timeout=20)
            r.raise_for_status()
            data = r.json()
            break
        except Exception as e:
            print(f"Deneme {i+1}/3 hata:", e)
            time.sleep(3)
    else:
        print("➡ Tesla API erişilemedi, sonraki döngü.")
        return

    if data.get("results"):
        print("STOK BULUNDU!  Telegram gönderildi")
        send("🚗 Tesla stokta araç bulundu!\nhttps://www.tesla.com/tr_TR/inventory/new/my?zip=34000")
    else:
        print("Stok bulunamadı.")

if __name__ == "__main__":
    while True:
        try:
            check_once()
        except Exception as e:
            print("Genel Hata:", e)
        time.sleep(300)        # 5 dk

