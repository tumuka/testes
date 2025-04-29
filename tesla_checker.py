import time, json, requests, os

TOKEN   = os.environ["8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"]
USER_ID = os.environ["6944382551"]
KEY     = os.environ["b0794e1bca8dbc04ded56bae2611480a"]

TESLA_URL  = "https://www.tesla.com/inventory/api/v1/inventory-results"
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

BASE = "https://api.scraperapi.com/"
COMMON = {
    "api_key": KEY,
    "url": TESLA_URL,
    "method": "POST",
    "body_type": "raw",
    "headers": "Content-Type:application/json",
    "country_code": "de",      # ⚠  de → fr → nl deneyebilirsiniz
    "device_type": "mobile",   # LTE/IPV4 havuzu
    "render": "false",
    "max_timeout": "25000"     # 25 000 ms = 25 s
}

def tg(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": msg}, timeout=10
    )

def fetch():
    for i in range(3):
        try:
            r = requests.post(
                BASE, params=COMMON, data=json.dumps(BODY), timeout=25
            )
            if r.status_code == 200:
                return r.json()
            print(f"{i+1}/3 → ScraperAPI {r.status_code}, retry…")
        except requests.Timeout:
            print(f"{i+1}/3 bağlantı hatası: Read timeout, retry…")
        time.sleep(3)
    print("↪ Üst üste 3 hata, döngüde atlandı.")
    return None

def loop():
    data = fetch()
    if not data:
        return
    total = data.get("total_matches_found", 0)
    print("Toplam sonuç:", total)
    if total:
        tg("🚗 Tesla stokta araç bulundu! https://www.tesla.com/tr_TR/inventory/new/my?zip=34000")

if __name__ == "__main__":
    # tek seferlik anahtar testi
    print("Anahtar testi:", requests.get(
        f"{BASE}?api_key={KEY}&url=https://httpbin.org/ip"
    ).status_code)
    print("Railway çıkış IP:\n", requests.get("https://httpbin.org/ip").text)
    while True:
        print("Kod başladı")
        loop()
        time.sleep(600)
