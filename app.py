from flask import Flask, request
import time
import threading

app = Flask(__name__)
STOCK_FILE = 'stock.txt'
lock = threading.Lock()  # Tambahkan lock global

@app.route('/buy', methods=['POST'])
def buy():
    item = request.form.get('item', 'banana')
    qty = int(request.form.get('qty', '1'))

    try:
        with lock:  # Lindungi blok critical section
            with open(STOCK_FILE, 'r') as f:
                stock_data = f.read().strip()

            if not stock_data.isdigit():
                return "Stock file corrupted or unreadable", 500

            stock = int(stock_data)

            if stock < qty:
                return f"Insufficient stock! Available: {stock}", 400

            stock -= qty

            with open(STOCK_FILE, 'w') as f:
                f.write(str(stock))

        return f"Successfully bought {qty} {item}(s). Remaining: {stock}"
    
    except Exception as e:
        return f"Internal error: {e}", 500

if __name__ == '__main__':
    # Inisialisasi stok ke angka besar agar cukup untuk semua thread
    with open(STOCK_FILE, 'w') as f:
        f.write('10')
    app.run(debug=True, threaded=True)
