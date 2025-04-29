# -*- coding: utf-8 -*-
"""
Tesla envanterini ScraperAPI ile sorgular, stok varsa Telegram’a haber verir.
• Anahtar doğrulama          : check_key()
• Railway çıkış IP testi     : print_my_ip()
• Country-rotation (DE/NL/FR): SCRAPER_PARAMS["country_code"]
"""

import time, json, requests, sys

# ──────────────── KULLANICI AYARLARI ────────────────
SCRAPER_KEY   = "b0794e1bca8dbc04ded56bae2611480a"
TELEGRAM_TOKEN = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"
TELEGRAM_USER  = "6944382551"        # tek kişi ise user id, grup ise grup id

TESLA_URL = "https://www.tesla.com/inventory/api/v1/inventory-results"

# POST gövdesi (dilerseniz filtreleri burada değiştirin)
BODY = {
    "query": {
        "model": "my", "condition": "new",
        "arrangeby": "plh", "order": "asc",
        "market": "TR", "language": "tr",
        "super_region": "EMEA", "zip": "34000",
        "range": 2000,           # km yarıçap
        "outsideSearch": True
    },
    "offset": 0,
    "count": 1000
}

# ScraperAPI query-string parametreleri  ----------------
SCRAPER_PARAMS = {
    "api_key": SCRAPER_KEY,
    "url": TESLA_URL,
    "method": "POST",
    "body_type": "raw",
    "headers": "Content-Type:application/json",
    "country_code": "de",       # tr/de/nl/fr …  (engelleme yaşarsanız değiştirin)
    "render": "false",
}
# ------------------------------------------------------

HEADERS = {"Content-Type": "application/json"}

# ───────────────── YARDIMCI FONKSİYONLAR ──────────────
def telegram_send(text: str) -> None:
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_USER, "text": text},
            timeout=10,
        )
    except Exception as e:
        print("Telegram gönderimi hatası:", e, file=sys.stderr)

def build_scraper_url() -> str:
    return "https://api.scraperapi.com/?" + "&".join(
        f"{k}={requests.utils.quote(str(v))}" for k, v in SCRAPER_PARAMS.items()
    )

def check_key() -> None:
    test = f"https://api.scraperapi.com/?api_key={SCRAPER_KEY}&url=https://httpbin.org/ip"
    r = requests.get(test, timeout=10)
    print("Anahtar testi:", r.status_code, r.text.strip())
    if r.status_code != 200:
        print("❌ ScraperAPI anahtarında sorun var!")
        sys.exit(1)

def print_my_ip() -> None:
    print("Railway çıkış IP:")
    try:
        print(requests.get("https://httpbin.org/ip", timeout=10).text.strip())
    except Exception as e:
        print("IP testinde hata:", e)

# ───────────────── ANA İŞLEV ──────────────────────────
def fetch_inventory() -> dict | None:
    url = build_scraper_url()
    for attempt in range(3):              # max 3 deneme
        try:
            r = requests.post(
                url, headers=HEADERS,
                data=json.dumps(BODY),
                timeout=15 if attempt else 10   # ilk deneme 10 sn, sonra 15
            )
            if r.status_code == 200:
                return r.json()
            print(f"{attempt+1}/3 – ScraperAPI {r.status_code}, retry…")
        except requests.exceptions.ReadTimeout:
            print(f"{attempt+1}/3 bağlantı hatası: Read timeout, retry…")
        time.sleep(3)
    print("↪ Üst üste 3 hata, döngüde atlandı.")
    return None

def check_once() -> None:
    print("Kod başladı")
    data = fetch_inventory()
    if not data:
        return
    # debug – ilk 300 karakteri göster
    # print("Debug ham cevap:", json.dumps(data)[:300])

    total = data.get("total_matches_found", 0)
    print("Toplam sonuç:", total)
    if total:
        msg = "🚗 Tesla stokta araç bulundu!\nhttps://www.tesla.com/tr_TR/inventory/new/my?zip=34000"
        telegram_send(msg)
        print("STOK BULUNDU! Telegram gönderildi")
    else:
        print("Stok bulunamadı.")

# ───────────────────────── MAIN LOOP ──────────────────
if __name__ == "__main__":
    check_key()       # ilk açılışta anahtarı doğrula
    print_my_ip()     # Railway’deki çıkış IP’sini yazdır
    while True:
        check_once()
        time.sleep(600)   # 10 dk
