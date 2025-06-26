```
import os
from flask import Flask, request, jsonify
import requests
import json
import threading
import time

app = Flask(__name__)

# Default values - akan ditimpa di main block
REPLICATION_TARGET_IP = None
REPLICATION_TARGET_PORT = 5000
IS_PRIMARY = None

DATA_FILE = 'data.json'
data = {}
data_lock = threading.Lock()

# Fungsi untuk memuat data dari file
def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {} # Jika file rusak/kosong, mulai dari kosong
    else:
        data = {}

# Fungsi untuk menyimpan data ke file
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Muat data saat aplikasi dimulai
load_data()

# Endpoint untuk mendapatkan data
@app.route('/data', methods=['GET'])
def get_data():
    with data_lock:
        # os.uname().nodename bekerja di Linux/WSL, di Windows native akan error
        # Kita gunakan platform.node() untuk kompatibilitas lintas OS
        import platform
        hostname = platform.node()
        return jsonify({"status": "success", "data": data, "served_by": hostname})

# Endpoint untuk menambahkan/mengupdate data (hanya di Primary)
@app.route('/data', methods=['POST'])
def update_data():
    if not IS_PRIMARY:
        return jsonify({"status": "error", "message": "This is a secondary server, cannot update directly."}), 403

    new_data = request.json
    if not new_data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    with data_lock:
        data.update(new_data)
        save_data() # Simpan ke file

        # Jika ini primary, replikasi ke secondary di background
        threading.Thread(target=replicate_data, args=(new_data,)).start()
        return jsonify({"status": "success", "message": "Data updated", "data": data, "served_by": platform.node()})

# Endpoint untuk menerima replikasi (hanya untuk secondary)
@app.route('/replicate', methods=['POST'])
def receive_replication():
    if IS_PRIMARY: # Primary tidak seharusnya menerima replikasi
        return jsonify({"status": "error", "message": "Primary server cannot receive replication"}), 403

    replicated_data = request.json
    if not replicated_data:
        return jsonify({"status": "error", "message": "No replication data provided"}), 400

    with data_lock:
        data.update(replicated_data)
        save_data()
        print(f"[{platform.node()}] Data replicated successfully: {replicated_data}")
    return jsonify({"status": "success", "message": "Data replicated"}), 200

# Fungsi untuk mereplikasi data ke target
def replicate_data(data_to_replicate):
    if not REPLICATION_TARGET_IP:
        print("REPLICATION_TARGET_IP not configured. Skipping replication.")
        return

    try:
        print(f"[{platform.node()}] Attempting to replicate data to {REPLICATION_TARGET_IP}:{REPLICATION_TARGET_PORT}")
        response = requests.post(
            f'http://{REPLICATION_TARGET_IP}:{REPLICATION_TARGET_PORT}/replicate',
            json=data_to_replicate,
            timeout=5 # Timeout untuk mencegah hang
        )
        response.raise_for_status() # Akan memunculkan HTTPError untuk status kode 4xx/5xx
        print(f"[{platform.node()}] Replication successful to {REPLICATION_TARGET_IP}")
    except requests.exceptions.ConnectionError as e:
        print(f"[{platform.node()}] Replication failed: Connection error to {REPLICATION_TARGET_IP}. Is the secondary server running and accessible? Error: {e}")
    except requests.exceptions.Timeout:
        print(f"[{platform.node()}] Replication failed: Timeout connecting to {REPLICATION_TARGET_IP}")
    except requests.exceptions.RequestException as e:
        print(f"[{platform.node()}] Replication failed: An unexpected error occurred: {e}")

if __name__ == '__main__':
    # --- PENTING: SET KONFIGURASI DI SINI BERDASARKAN LAPTOP KAMU ---
    import platform
    current_hostname = platform.node()

    # Untuk Laptop 1 (Ubuntu):
    # GANTI 'your_ubuntu_hostname' dengan output perintah 'hostname' di terminal Ubuntu
    if current_hostname == 'your_ubuntu_hostname': # <-- GANTI INI!
        IS_PRIMARY = True
        REPLICATION_TARGET_IP = '192.168.1.101' # <-- IP WINDOWS KAMU
        print(f"[{current_hostname}] Running as PRIMARY server. Target for replication: {REPLICATION_TARGET_IP}")
    # Untuk Laptop 2 (Windows):
    # GANTI 'your_windows_hostname' dengan output perintah 'hostname' di Command Prompt Windows
    elif current_hostname == 'your_windows_hostname': # <-- GANTI INI!
        IS_PRIMARY = False
        REPLICATION_TARGET_IP = '192.168.1.100' # <-- IP UBUNTU KAMU
        print(f"[{current_hostname}] Running as SECONDARY server. Target for replication: {REPLICATION_TARGET_IP}")
    else:
        print(f"WARNING: Hostname '{current_hostname}' not recognized. Please set IS_PRIMARY and REPLICATION_TARGET_IP manually.")
        exit("Exiting: Server role not defined based on hostname.")

    app.run(host='0.0.0.0', port=5000, debug=False)
```
