#!/bin/bash

# Menampilkan opsi pencarian
echo "Pilih opsi pencarian:"
echo "1. Menampilkan user yang aktif login"
echo "2. Mencari error di file log"
echo "3. Mencari pola teks tertentu di file"

# Membaca input pilihan pengguna
read -p "Masukkan pilihan (1/2/3): " pilihan

# Melakukan aksi berdasarkan pilihan
case $pilihan in
    1)
        # Menampilkan user yang aktif login
        echo "User yang aktif login:"
        who
        ;;
    2)
        # Mencari entri error dalam file log
        read -p "Masukkan lokasi file log (misalnya: /var/log/syslog): " logfile
        if [ -f "$logfile" ]; then
            echo "Entri error di $logfile:"
            grep -i "error" "$logfile" | awk '{print $1, $2, $3, $5, $6}'
        else
            echo "File log tidak ditemukan: $logfile"
        fi
        ;;
    3)
        # Mencari pola teks tertentu di file
        read -p "Masukkan nama file: " filename
        if [ -f "$filename" ]; then
            read -p "Masukkan pola teks yang dicari: " pattern
            echo "Hasil pencarian untuk pola '$pattern' di $filename:"
            grep "$pattern" "$filename"
        else
            echo "File tidak ditemukan: $filename"
        fi
        ;;
    *)
        # Pilihan tidak valid
        echo "Pilihan tidak valid."
        ;;
esac
