import time, requests

# ▶ Telegram bilgilerin
TOKEN   = "8117324210:AAGUyfXfnUSmZDKhuvz4VrR0jxYFsnjZ69E"      # Bot tokenını buraya yaz
USER_ID = "6944382551"             # Kendi chat-id’in

# ▶ İzlenecek sayfa
TESLA_URL = (
    "https://www.tesla.com/tr_TR/inventory/new/my"
    "?arrangeby=plh&zip=34000&range=0"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

def send(msg: str) -> None:
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": USER_ID, "text": msg},
        timeout=10,
    )
    print("Telegram OK" if r.ok else f"Telegram HATA {r.status_code}: {r.text[:120]}")

def check_once() -> None:
    for attempt in range(3):                       # en fazla 3 deneme
        try:
            resp = requests.get(
                TESLA_URL,
                headers=HEADERS,
                timeout=60        # 60 sn
            )
            html = resp.text.lower()
            break                 # başarılıysa döngüden çık
        except requests.exceptions.RequestException as e:
            print(f"Deneme {attempt+1}/3 hata:", e)
            time.sleep(5)         # 5 sn bekleyip tekrar dene
    else:
        print("➡ Tesla sayfasına ulaşılamadı, döngü kapanıyor.")
        return

    if ("no inventory available" in html or
        "mevcut araç bulunamadı" in html):
        print("Stok bulunamadı.")
    else:
        print("STOK BULUNDU!  Telegram gönderildi")
        send(f"🚗 Tesla stokta araç bulundu!\n{TESLA_URL}")


    if "no inventory available" in html or "mevcut araç bulunamadı" in html:
        print("Stok bulunamadı.")
    else:
        print("STOK BULUNDU!  → Telegram gönderildi")
        send(f"🚗 Tesla stokta araç bulundu!\n{TESLA_URL}")

if __name__ == "__main__":
    while True:
        try:
            check_once()
        except Exception as e:
            print("Hata:", e)
        time.sleep(300)          # 5 dk’da bir kontrol
