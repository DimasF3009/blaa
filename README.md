```
from flask import Flask, request, jsonify
import json
import os
import requests # Digunakan untuk mengirim HTTP requests (untuk replikasi)

app = Flask(__name__)
DATA_FILE = 'data.json' # Nama file tempat data akan disimpan

# --- KONFIGURASI SERVER INI ---
# ######################################################################
# ### BACALAH DENGAN SAKSAMA DAN UBAH SESUAI DENGAN LAPTOP KAMU ##########
# ######################################################################

# Ganti dengan IP address dari LAPTOP KALI LINUX (SECONDARY SERVER)
# Contoh: '192.168.1.101' atau '172.29.80.96' jika itu IP Kali kamu
REPLICATION_TARGET_IP = 'GANTI_DENGAN_IP_LAPTOP_KALI_LINUX_DI_SINI'

# Setel IS_PRIMARY:
# - True jika ini adalah LAPTOP UBUNTU (PRIMARY SERVER)
# - False jika ini adalah LAPTOP KALI LINUX (SECONDARY SERVER)
IS_PRIMARY = True # <--- UBAH INI JIKA KAMU DI LAPTOP KALI LINUX MENJADI False

# ######################################################################
# ### AKHIR KONFIGURASI ################################################
# ######################################################################


# Fungsi untuk membaca data dari file JSON
def read_data():
    # Jika file data belum ada, buat dengan data default
    if not os.path.exists(DATA_FILE):
        default_data = {"message": "Server initialized, no specific data yet."}
        with open(DATA_FILE, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
    try:
        # Baca data dari file
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Tangani jika file data korup atau kosong
        print(f"Warning: {DATA_FILE} is corrupted or empty. Resetting to default.")
        default_data = {"message": "Data file corrupted/empty, reset to default."}
        with open(DATA_FILE, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data

# Fungsi untuk menulis data ke file JSON
def write_data(new_data):
    with open(DATA_FILE, 'w') as f:
        json.dump(new_data, f, indent=4)

# Endpoint utama: Menampilkan data saat ini
@app.route('/')
def index():
    data = read_data()
    # Menambahkan informasi peran server (Primary/Secondary) dan hostname
    server_role = "Primary" if IS_PRIMARY else "Secondary"
    data["served_by"] = f"Server {server_role} ({os.uname().nodename})"
    return jsonify(data)

# Endpoint untuk menerima data dari server lain (digunakan untuk replikasi)
@app.route('/replicate', methods=['POST'])
def replicate_data():
    if request.is_json:
        new_data = request.get_json()
        write_data(new_data) # Tulis data yang diterima ke file lokal
        print(f"Data replicated: {new_data}")
        return jsonify({"status": "success", "message": "Data replicated successfully"}), 200
    return jsonify({"status": "error", "message": "Request must be JSON"}), 400

# Endpoint untuk memperbarui data dari pengguna (Hanya di server Primary yang akan memicu replikasi)
@app.route('/update', methods=['POST'])
def update_data():
    # Hanya server Primary yang boleh menerima update langsung dari client
    if not IS_PRIMARY:
        return jsonify({"status": "error", "message": "This is a secondary server, cannot update directly."}), 403

    if request.is_json:
        new_data_from_client = request.get_json()
        write_data(new_data_from_client) # Tulis data yang diterima ke file lokal
        print(f"Data updated by client: {new_data_from_client}")

        # --- BAGIAN LOGIKA REPLIKASI KE SERVER CADANGAN ---
        try:
            # Kirim data terbaru ke endpoint /replicate di server cadangan
            # Pastikan REPLICATION_TARGET_IP sudah benar diatur di atas
            response = requests.post(f"http://{REPLICATION_TARGET_IP}:5000/replicate", json=new_data_from_client)
            if response.status_code == 200:
                print("Replication to secondary successful.")
            else:
                print(f"Replication to secondary failed: {response.text}")
        except requests.exceptions.ConnectionError as e:
            print(f"Could not connect to secondary server for replication: {e}")
        # --- AKHIR LOGIKA REPLIKASI ---

        return jsonify({"status": "success", "message": "Data updated by client and (attempted) replicated"}), 200
    return jsonify({"status": "error", "message": "Request must be JSON"}), 400

# Main entry point: Menjalankan aplikasi Flask
if __name__ == '__main__':
    # Jalankan aplikasi di semua interface (0.0.0.0) agar bisa diakses dari jaringan
    # Debug=True hanya untuk pengembangan, jangan gunakan di produksi
    app.run(host='0.0.0.0', port=5000, debug=False)
```
