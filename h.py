import streamlit as st

import pandas as pd

from sklearn.linear_model import LinearRegression

#Load dataset CSV

data = pd.read_csv(dataset_kepuasan.csv)

#Fitur dan target

X = data[[Kecepatan_Layanan', 'Kualitas_Produk, "Harga, Kemudahan Penggunaan

y=data['Target_Kepuasan]

#Latih model regresi linier dari data CSV

model LinearRegression()

model.fit(X, y)

# Judul aplikasi

st.title('Prediksi Tingkat Kepuasan Pelanggan")

st.write("Masukkan faktor-faktor berikut untuk memperkirakan tingkat kepuasan pelanggan:)
Input dari pengguna

kecepatan st.slider('Kecepatan Layanan', 1, 10, 5)

kualitas st.slider('Kualitas Produk', 1, 10, 7)

harga st. slider('Harga', 1, 10, 5)

kemudahan st.slider('Kemudahan Penggunaan', 1, 10, 6)

#Membuat DataFrame input

input_df = pd.DataFrame({

'Kecepatan_Layanan': [kecepatan],

'Kualitas_Produk': [kualitas],

'Harga': [harga],

'Kemudahan_Penggunaan': [kemudahan] })

# Tombol untuk melakukan prediksi

if st.button('Prediksi Tingkat Kepuasan'):

prediksi = model.predict(input_df)[0]

st. write (f'Prediksi Skor Tingkat Kepuasan: {prediksi:.2f}')

# Interpretasi hasil

if prediksi >= 8:

tingkat = 'Sangat Puas'

elif prediksi >= 6:

tingkat = 'Puas'

elif prediksi >= 4: tingkat = 'Cukup Puas' else: tingkat = 'Tidak Puas' st.write(f'Tingkat Kepuasan: (tingkat}')
