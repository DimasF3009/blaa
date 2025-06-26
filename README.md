```                                              app.py                                                             from flask import Flask, request, jsonify
import json
import os
import requests # Penting untuk mengirim request HTTP

app = Flask(__name__)
DATA_FILE = 'data.json'

# --- KONFIGURASI SERVER INI ---
# Ganti dengan IP dari Laptop 2 (Secondary Server)
REPLICATION_TARGET_IP = '172.29.80.96' # <-- GANTI DENGAN IP AKTUAL LAPTOP 2

# Setel IS_PRIMARY ke True jika ini Laptop 1 (Primary), False jika Laptop 2 (Secondary)
IS_PRIMARY = True # <-- GANTI: Setel True di Laptop 1, Setel False di Laptop 2
# --- AKHIR KONFIGURASI ---

# Fungsi untuk membaca data
def read_data():
    if not os.path.exists(DATA_FILE):
        # Jika file belum ada, buat dengan data default
        default_data = {"message": "No data yet or server just initialized."}
        with open(DATA_FILE, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Jika file korup, kembalikan default dan reset file
```
